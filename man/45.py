import socket
import threading
import cv2
import numpy as np
import customtkinter as ctk # Pour l'interface graphique moderne
import tkinter as tk        # Pour PhotoImage (utilisé pour l'affichage sans PIL)
from tkinter import messagebox
import time
import io # Nécessaire pour gérer les données binaires en mémoire pour PhotoImage

# --- Paramètres Audio (PyAudio) ---
import pyaudio
FORMAT = pyaudio.paInt16    # Format des échantillons audio (16-bit entiers)
CHANNELS = 1                # Nombre de canaux (Mono)
RATE = 44100                # Fréquence d'échantillonnage (44.1 kHz, qualité CD)
CHUNK_SIZE = 1024           # Taille des échantillons audio à traiter à la fois

# --- Paramètres Vidéo (OpenCV) ---
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 20                    # Images par seconde
JPEG_QUALITY_NETWORK = 50   # Qualité JPEG pour l'envoi réseau (0-100), plus faible = plus petite taille

# --- Paramètres Réseau ---
BUFFER_SIZE = 65536         # Taille du buffer de réception pour la vidéo (doit être assez grand pour une image compressée)
AUDIO_PORT = 12345          # Port par défaut pour l'audio
VIDEO_PORT = 12346          # Port par défaut pour la vidéo

# --- Variables Globales d'État ---
audio_sending = False       # Indicateur pour contrôler le thread d'envoi audio
audio_receiving = False     # Indicateur pour contrôler le thread de réception audio
video_sending = False       # Indicateur pour contrôler le thread d'envoi vidéo
video_receiving = False     # Indicateur pour contrôler le thread de réception vidéo

# Variables PyAudio
p_audio = None              # Instance de PyAudio
stream_in = None            # Flux d'entrée audio (micro)
stream_out = None           # Flux de sortie audio (haut-parleur)
selected_input_device_index = -1 # Index du périphérique d'entrée audio par défaut
selected_output_device_index = -1 # Index du périphérique de sortie audio par défaut

# Variables OpenCV
cap = None # Objet de capture vidéo OpenCV (webcam)

# Références aux widgets CustomTkinter pour les mises à jour dynamiques
label_local_video = None    # Label pour afficher la vidéo locale
label_remote_video = None   # Label pour afficher la vidéo du pair
audio_status_label = None   # Label pour afficher le statut de l'audio

# --- Fonctions Audio (PyAudio) ---

def find_and_display_audio_devices():
    """
    Détecte et affiche les périphériques audio disponibles via PyAudio.
    Initialise p_audio si ce n'est pas déjà fait.
    """
    global p_audio, selected_input_device_index, selected_output_device_index

    if p_audio is None:
        try:
            p_audio = pyaudio.PyAudio()
        except Exception as e:
            messagebox.showerror("Erreur PyAudio", f"Impossible d'initialiser PyAudio. "
                                 f"Assurez-vous que PortAudio est installé et configuré: {e}")
            print(f"Erreur PyAudio: {e}")
            return -1, -1

    info = p_audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    available_devices_str = []
    
    selected_input_device_info = p_audio.get_default_input_device_info()
    selected_input_device_index = selected_input_device_info.get('index') if selected_input_device_info else -1
    
    selected_output_device_info = p_audio.get_default_output_device_info()
    selected_output_device_index = selected_output_device_info.get('index') if selected_output_device_info else -1

    available_devices_str.append("--- Périphériques audio disponibles ---")
    for i in range(0, numdevices):
        dev_info = p_audio.get_device_info_by_host_api_device_index(0, i)
        device_name = dev_info.get('name')
        max_input_channels = dev_info.get('maxInputChannels')
        max_output_channels = dev_info.get('maxOutputChannels')

        device_line = f"  Index {i}: {device_name}"
        if max_input_channels > 0:
            device_line += f" (Entrée: {max_input_channels} ch)"
        if max_output_channels > 0:
            device_line += f" (Sortie: {max_output_channels} ch)"
        
        available_devices_str.append(device_line)
    
    print("\n".join(available_devices_str))
    print(f"Indice d'entrée par défaut suggéré: {selected_input_device_index}")
    print(f"Indice de sortie par défaut suggéré: {selected_output_device_index}")
    
    messagebox.showinfo("Périphériques Audio Détectés", "\n".join(available_devices_str) + 
                        f"\n\nIndice d'entrée suggéré: {selected_input_device_index}" +
                        f"\nIndice de sortie suggéré: {selected_output_device_index}")

    return selected_input_device_index, selected_output_device_index

def send_audio_stream(client_socket_audio):
    """
    Capture l'audio du microphone et l'envoie via le socket.
    """
    global audio_sending, p_audio, stream_in, selected_input_device_index
    if p_audio is None:
        print("PyAudio non initialisé pour l'envoi audio.")
        return

    try:
        stream_in = p_audio.open(format=FORMAT,
                                 channels=CHANNELS,
                                 rate=RATE,
                                 input=True,
                                 frames_per_buffer=CHUNK_SIZE,
                                 input_device_index=selected_input_device_index)
        print("Envoi audio démarré...")
        while audio_sending:
            data = stream_in.read(CHUNK_SIZE, exception_on_overflow=False)
            client_socket_audio.sendall(data)
            time.sleep(0.001)
    except Exception as e:
        print(f"Erreur lors de l'envoi audio: {e}")
        messagebox.showerror("Erreur Audio", f"Erreur lors de l'envoi audio: {e}")
    finally:
        if stream_in:
            stream_in.stop_stream()
            stream_in.close()
            stream_in = None
        stop_audio_call()

def receive_audio_stream(conn_audio, addr):
    """
    Reçoit le flux audio via le socket et le joue sur les haut-parleurs.
    """
    global audio_receiving, p_audio, stream_out, selected_output_device_index
    if p_audio is None:
        print("PyAudio non initialisé pour la réception audio.")
        return

    try:
        stream_out = p_audio.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer=CHUNK_SIZE,
                                  output_device_index=selected_output_device_index)
        print(f"Réception audio de {addr} démarrée...")
        while audio_receiving:
            data = conn_audio.recv(CHUNK_SIZE * p_audio.get_sample_size(FORMAT))
            if not data:
                print("Pair audio déconnecté ou fin de flux.")
                break
            stream_out.write(data)
            time.sleep(0.001)
    except Exception as e:
        print(f"Erreur lors de la réception audio: {e}")
        messagebox.showerror("Erreur Audio", f"Erreur lors de la réception audio: {e}")
    finally:
        if stream_out:
            stream_out.stop_stream()
            stream_out.close()
            stream_out = None
        if conn_audio:
            conn_audio.close()
        stop_audio_call()

# --- Fonctions Vidéo (OpenCV et Tkinter pour l'affichage) ---

def convert_opencv_to_ppm(frame):
    """
    Convertit une image OpenCV (NumPy array BGR) en données PPM P6 (brutes)
    pour une utilisation directe avec tk.PhotoImage.
    """
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    header = f"P6\n{frame_rgb.shape[1]} {frame_rgb.shape[0]}\n255\n".encode('ascii')
    return header + frame_rgb.tobytes()

def send_video_stream(video_socket):
    """
    Capture le flux vidéo de la webcam, le prévisualise localement (via PPM),
    le compresse en JPEG et l'envoie via le socket.
    """
    global video_sending, cap, label_local_video

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Erreur Webcam", "Impossible d'accéder à la webcam. Assurez-vous qu'elle n'est pas déjà utilisée.")
        print("Erreur: Impossible d'ouvrir la webcam.")
        video_sending = False
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    print("Démarrage de l'envoi vidéo...")
    while video_sending:
        ret, frame = cap.read()
        if not ret:
            print("Erreur lors de la lecture de la frame.")
            break

        # --- Affichage local (via PPM pour CustomTkinter sans PIL) ---
        try:
            ppm_data = convert_opencv_to_ppm(frame)
            imgtk = tk.PhotoImage(data=ppm_data, format='ppm', width=FRAME_WIDTH, height=FRAME_HEIGHT)

            if label_local_video:
                label_local_video.configure(image=imgtk)
                label_local_video.image = imgtk
        except Exception as e:
            print(f"Erreur d'affichage local vidéo (PPM): {e}")

        # --- Envoi via socket (utilise JPEG pour la compression réseau) ---
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY_NETWORK]
        _, encoded_image = cv2.imencode('.jpg', frame, encode_param)
        data = encoded_image.tobytes()

        try:
            video_socket.sendall(len(data).to_bytes(4, 'big') + data)
        except (BrokenPipeError, ConnectionResetError):
            print("Connexion vidéo rompue côté envoi.")
            break
        except Exception as e:
            print(f"Erreur lors de l'envoi de la frame vidéo: {e}")
            break
        
        time.sleep(1 / FPS)

    print("Arrêt de l'envoi vidéo.")
    if cap:
        cap.release()
        cap = None
    stop_video_call()


def receive_video_stream(video_conn, addr):
    """
    Reçoit le flux vidéo, le décompresse (JPEG) et l'affiche (via PPM).
    """
    global video_receiving, label_remote_video

    print(f"Démarrage de la réception vidéo de {addr}...")
    while video_receiving:
        try:
            size_data = video_conn.recv(4)
            if not size_data:
                print("Pair vidéo déconnecté.")
                break
            
            frame_size = int.from_bytes(size_data, 'big')
            
            data = b''
            while len(data) < frame_size:
                packet = video_conn.recv(min(frame_size - len(data), BUFFER_SIZE))
                if not packet:
                    print("Données vidéo incomplètes ou pair déconnecté.")
                    break
                data += packet
            
            if len(data) < frame_size:
                continue

            np_data = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

            if frame is None:
                print("Erreur de décodage de l'image.")
                continue

            # --- Affichage distant (via PPM pour CustomTkinter sans PIL) ---
            try:
                ppm_data = convert_opencv_to_ppm(frame)
                imgtk = tk.PhotoImage(data=ppm_data, format='ppm', width=FRAME_WIDTH, height=FRAME_HEIGHT)
                
                if label_remote_video:
                    label_remote_video.configure(image=imgtk)
                    label_remote_video.image = imgtk
            except Exception as e:
                print(f"Erreur d'affichage distant vidéo (PPM): {e}")

        except (BrokenPipeError, ConnectionResetError):
            print("Connexion vidéo rompue côté réception.")
            break
        except Exception as e:
            print(f"Erreur lors de la réception de la frame vidéo: {e}")
            break

    print("Arrêt de la réception vidéo.")
    stop_video_call()

# --- Fonctions de Contrôle des Appels (Audio + Vidéo) ---

def start_call():
    """
    Démarre un appel P2P complet (audio et vidéo) en mode client.
    Tente de se connecter au pair spécifié.
    """
    global audio_sending, audio_receiving, video_sending, video_receiving
    global p_audio, selected_input_device_index, selected_output_device_index

    peer_ip = entry_peer_ip.get()
    try:
        audio_port = int(entry_audio_port.get())
        video_port = int(entry_video_port.get())
    except ValueError:
        messagebox.showerror("Erreur", "Les ports doivent être des nombres entiers.")
        return

    if not peer_ip:
        messagebox.showerror("Erreur", "Veuillez entrer l'adresse IP du pair.")
        return

    # 1. Initialiser PyAudio et détecter les périphériques audio
    _input_idx, _output_idx = find_and_display_audio_devices()
    if _input_idx == -1 or _output_idx == -1:
        messagebox.showerror("Erreur", "Impossible de trouver un périphérique audio valide. Vérifiez votre configuration PyAudio.")
        if p_audio: p_audio.terminate(); p_audio = None
        return
    selected_input_device_index = _input_idx
    selected_output_device_index = _output_idx

    # 2. Tenter de se connecter pour l'AUDIO
    client_socket_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"Tentative de connexion audio à {peer_ip}:{audio_port}...")
        client_socket_audio.connect((peer_ip, audio_port))
        print("Connexion audio établie.")
        audio_sending = True
        audio_receiving = True
        threading.Thread(target=send_audio_stream, args=(client_socket_audio,)).start()
        threading.Thread(target=receive_audio_stream, args=(client_socket_audio, (peer_ip, audio_port))).start()
    except Exception as e:
        messagebox.showerror("Erreur Connexion Audio", f"Impossible de se connecter pour l'audio: {e}")
        print(f"Erreur connexion audio client: {e}")
        client_socket_audio.close()
        stop_call()
        return

    # 3. Tenter de se connecter pour la VIDEO
    client_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"Tentative de connexion vidéo à {peer_ip}:{video_port}...")
        client_socket_video.connect((peer_ip, video_port))
        print("Connexion vidéo établie.")
        video_sending = True
        video_receiving = True
        threading.Thread(target=send_video_stream, args=(client_socket_video,)).start()
        threading.Thread(target=receive_video_stream, args=(client_socket_video, (peer_ip, video_port))).start()
    except Exception as e:
        messagebox.showerror("Erreur Connexion Vidéo", f"Impossible de se connecter pour la vidéo: {e}")
        print(f"Erreur connexion vidéo client: {e}")
        client_socket_video.close()
        video_sending = False
        video_receiving = False
    
    messagebox.showinfo("Appel Démarré", f"Appel vers {peer_ip} démarré. (Vérifiez les erreurs individuelles si besoin)")
    btn_call.configure(state="disabled")
    btn_listen.configure(state="disabled")
    btn_stop.configure(state="normal")
    audio_status_label.configure(text="Statut Audio: En appel...")


def start_listen():
    """
    Démarre l'écoute pour un appel P2P complet (audio et vidéo) en mode serveur.
    """
    global audio_sending, audio_receiving, video_sending, video_receiving
    global p_audio, selected_input_device_index, selected_output_device_index

    listen_ip = entry_listen_ip.get() # <--- RÉCUPÉRER L'IP D'ÉCOUTE ICI
    if not listen_ip:
        listen_ip = '0.0.0.0' # Par défaut, écouter sur toutes les interfaces

    try:
        audio_port = int(entry_audio_port_listen.get())
        video_port = int(entry_video_port_listen.get())
    except ValueError:
        messagebox.showerror("Erreur", "Les ports doivent être des nombres entiers.")
        return

    # 1. Initialiser PyAudio et détecter les périphériques audio
    _input_idx, _output_idx = find_and_display_audio_devices()
    if _input_idx == -1 or _output_idx == -1:
        messagebox.showerror("Erreur", "Impossible de trouver un périphérique audio valide. Vérifiez votre configuration PyAudio.")
        if p_audio: p_audio.terminate(); p_audio = None
        return
    selected_input_device_index = _input_idx
    selected_output_device_index = _output_idx

    # 2. Démarrer le serveur AUDIO
    server_socket_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_audio.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket_audio.bind((listen_ip, audio_port)) # <--- UTILISER listen_ip ICI
        server_socket_audio.listen(1)
        print(f"Serveur audio en attente sur {listen_ip}:{audio_port}...") # Afficher l'IP d'écoute
        
        def accept_audio_connection():
            global audio_sending, audio_receiving
            try:
                conn_audio, addr_audio = server_socket_audio.accept()
                print(f"Connexion audio acceptée de {addr_audio}")
                audio_sending = True
                audio_receiving = True
                threading.Thread(target=send_audio_stream, args=(conn_audio,)).start()
                threading.Thread(target=receive_audio_stream, args=(conn_audio, addr_audio)).start()
            except Exception as e:
                messagebox.showerror("Erreur Serveur Audio", f"Erreur lors de l'acceptation audio: {e}")
                print(f"Erreur accept_audio_connection: {e}")
                stop_audio_call()
            finally:
                server_socket_audio.close()
        
        threading.Thread(target=accept_audio_connection).start()
    except OSError as e:
        if e.errno == 98:
             messagebox.showerror("Erreur Port Audio", f"Le port audio {audio_port} sur {listen_ip} est déjà utilisé. Veuillez en choisir un autre.")
        else:
            messagebox.showerror("Erreur Serveur Audio", f"Impossible de démarrer le serveur audio sur {listen_ip}:{audio_port}: {e}")
        print(f"Erreur serveur audio: {e}")
        server_socket_audio.close()
        stop_call()
        return

    # 3. Démarrer le serveur VIDEO
    server_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_video.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket_video.bind((listen_ip, video_port)) # <--- UTILISER listen_ip ICI
        server_socket_video.listen(1)
        print(f"Serveur vidéo en attente sur {listen_ip}:{video_port}...") # Afficher l'IP d'écoute

        def accept_video_connection():
            global video_sending, video_receiving
            try:
                conn_video, addr_video = server_socket_video.accept()
                print(f"Connexion vidéo acceptée de {addr_video}")
                video_sending = True
                video_receiving = True
                threading.Thread(target=send_video_stream, args=(conn_video,)).start()
                threading.Thread(target=receive_video_stream, args=(conn_video, addr_video)).start()
            except Exception as e:
                messagebox.showerror("Erreur Serveur Vidéo", f"Erreur lors de l'acceptation vidéo: {e}")
                print(f"Erreur accept_video_connection: {e}")
                stop_video_call()
            finally:
                server_socket_video.close()
        
        threading.Thread(target=accept_video_connection).start()
    except OSError as e:
        if e.errno == 98:
             messagebox.showerror("Erreur Port Vidéo", f"Le port vidéo {video_port} sur {listen_ip} est déjà utilisé. Veuillez en choisir un autre.")
        else:
            messagebox.showerror("Erreur Serveur Vidéo", f"Impossible de démarrer le serveur vidéo sur {listen_ip}:{video_port}: {e}")
        print(f"Erreur serveur vidéo: {e}")
        server_socket_video.close()
        stop_call()
        return

    messagebox.showinfo("En attente d'Appel", f"En attente d'appels sur {listen_ip}: {audio_port} (audio) et {video_port} (vidéo)...")
    btn_call.configure(state="disabled")
    btn_listen.configure(state="disabled")
    btn_stop.configure(state="normal")
    audio_status_label.configure(text="Statut Audio: En attente...")


def stop_call():
    """
    Arrête tous les flux (audio et vidéo) et nettoie toutes les ressources.
    """
    global audio_sending, audio_receiving, video_sending, video_receiving
    global p_audio, stream_in, stream_out, cap

    print("Demande d'arrêt de l'appel complet...")
    audio_sending = False
    audio_receiving = False
    video_sending = False
    video_receiving = False

    if stream_in:
        try: stream_in.stop_stream(); stream_in.close()
        except Exception as e: print(f"Erreur lors de l'arrêt du flux d'entrée audio: {e}")
        stream_in = None
    if stream_out:
        try: stream_out.stop_stream(); stream_out.close()
        except Exception as e: print(f"Erreur lors de l'arrêt du flux de sortie audio: {e}")
        stream_out = None
    if p_audio:
        try: p_audio.terminate()
        except Exception as e: print(f"Erreur lors de la terminaison de PyAudio: {e}")
        p_audio = None

    if cap:
        try: cap.release()
        except Exception as e: print(f"Erreur lors de la libération de la webcam: {e}")
        cap = None
    
    black_img = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
    black_ppm_data = convert_opencv_to_ppm(black_img)
    black_photo_image = tk.PhotoImage(data=black_ppm_data, format='ppm', width=FRAME_WIDTH, height=FRAME_HEIGHT)

    if label_local_video:
        label_local_video.configure(image=black_photo_image)
        label_local_video.image = black_photo_image
    if label_remote_video:
        label_remote_video.configure(image=black_photo_image)
        label_remote_video.image = black_photo_image

    messagebox.showinfo("Appel Terminé", "L'appel vidéo et audio a été arrêté.")
    
    btn_call.configure(state="normal")
    btn_listen.configure(state="normal")
    btn_stop.configure(state="disabled")
    audio_status_label.configure(text="Statut Audio: Inactif")


def stop_audio_call():
    global audio_sending, audio_receiving
    audio_sending = False
    audio_receiving = False

def stop_video_call():
    global video_sending, video_receiving
    video_sending = False
    video_receiving = False


# --- Configuration de CustomTkinter ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- Interface Graphique CustomTkinter ---
root = ctk.CTk()
root.title("Appel Vidéo P2P (CustomTkinter - Sans PIL)")
root.geometry(f"{FRAME_WIDTH * 2 + 60}x{FRAME_HEIGHT + 380}") # Ajusté la taille pour le nouveau champ
root.resizable(False, False)

# --- Cadres pour les vidéos ---
frame_local_video = ctk.CTkFrame(root, width=FRAME_WIDTH + 20, height=FRAME_HEIGHT + 20)
frame_local_video.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame_local_video.grid_propagate(False)

label_local_title = ctk.CTkLabel(frame_local_video, text="Ma Vidéo", font=ctk.CTkFont(size=16, weight="bold"))
label_local_title.pack(pady=5)
label_local_video = ctk.CTkLabel(frame_local_video, text="", width=FRAME_WIDTH, height=FRAME_HEIGHT, bg_color="black")
label_local_video.pack(pady=5)

frame_remote_video = ctk.CTkFrame(root, width=FRAME_WIDTH + 20, height=FRAME_HEIGHT + 20)
frame_remote_video.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
frame_remote_video.grid_propagate(False)

label_remote_title = ctk.CTkLabel(frame_remote_video, text="Vidéo du Pair", font=ctk.CTkFont(size=16, weight="bold"))
label_remote_title.pack(pady=5)
label_remote_video = ctk.CTkLabel(frame_remote_video, text="", width=FRAME_WIDTH, height=FRAME_HEIGHT, bg_color="black")
label_remote_video.pack(pady=5)

# --- Cadre pour les contrôles ---
frame_controls = ctk.CTkFrame(root)
frame_controls.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
frame_controls.grid_columnconfigure(1, weight=1)
frame_controls.grid_columnconfigure(3, weight=1)
frame_controls.grid_columnconfigure(5, weight=1)


# Labels et entrées pour l'appel (mode client)
ctk.CTkLabel(frame_controls, text="IP du pair:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_peer_ip = ctk.CTkEntry(frame_controls)
entry_peer_ip.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
entry_peer_ip.insert(0, "127.0.0.1")

ctk.CTkLabel(frame_controls, text="Port Audio:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_audio_port = ctk.CTkEntry(frame_controls, width=80)
entry_audio_port.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
entry_audio_port.insert(0, str(AUDIO_PORT))

ctk.CTkLabel(frame_controls, text="Port Vidéo:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=4, padx=5, pady=5, sticky="w")
entry_video_port = ctk.CTkEntry(frame_controls, width=80)
entry_video_port.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
entry_video_port.insert(0, str(VIDEO_PORT))

btn_call = ctk.CTkButton(frame_controls, text="Appeler", command=start_call)
btn_call.grid(row=0, column=6, padx=10, pady=5)


# Labels et entrées pour l'écoute (mode serveur)
ctk.CTkLabel(frame_controls, text="IP d'écoute:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w") # NOUVEAU
entry_listen_ip = ctk.CTkEntry(frame_controls) # NOUVEAU
entry_listen_ip.grid(row=1, column=1, padx=5, pady=5, sticky="ew") # NOUVEAU
entry_listen_ip.insert(0, "0.0.0.0") # Par défaut, écouter sur toutes les interfaces

ctk.CTkLabel(frame_controls, text="Audio:", font=ctk.CTkFont(weight="normal")).grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_audio_port_listen = ctk.CTkEntry(frame_controls, width=80)
entry_audio_port_listen.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
entry_audio_port_listen.insert(0, str(AUDIO_PORT))

ctk.CTkLabel(frame_controls, text="Vidéo:", font=ctk.CTkFont(weight="normal")).grid(row=1, column=4, padx=5, pady=5, sticky="w")
entry_video_port_listen = ctk.CTkEntry(frame_controls, width=80)
entry_video_port_listen.grid(row=1, column=5, padx=5, pady=5, sticky="ew")
entry_video_port_listen.insert(0, str(VIDEO_PORT))

btn_listen = ctk.CTkButton(frame_controls, text="Écouter", command=start_listen)
btn_listen.grid(row=1, column=6, padx=10, pady=5)

# Bouton d'arrêt général de l'appel
btn_stop = ctk.CTkButton(frame_controls, text="Arrêter l'Appel", command=stop_call, state="disabled", fg_color="red", hover_color="darkred")
btn_stop.grid(row=2, column=0, columnspan=7, pady=10)

audio_status_label = ctk.CTkLabel(root, text="Statut Audio: Inactif", font=ctk.CTkFont(size=14))
audio_status_label.grid(row=2, column=0, columnspan=2, pady=5)


def on_closing_ctk():
    if messagebox.askokcancel("Quitter l'application", "Voulez-vous vraiment quitter? L'appel sera arrêté et les ressources libérées."):
        stop_call()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing_ctk)

# --- Initialisation des images noires au démarrage ---
black_img = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
black_ppm_data = convert_opencv_to_ppm(black_img)
black_photo_image = tk.PhotoImage(data=black_ppm_data, format='ppm', width=FRAME_WIDTH, height=FRAME_HEIGHT)

if label_local_video:
    label_local_video.configure(image=black_photo_image)
    label_local_video.image = black_photo_image
if label_remote_video:
    label_remote_video.configure(image=black_photo_image)
    label_remote_video.image = black_photo_image

root.mainloop()