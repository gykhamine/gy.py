import socket
import threading
import pyaudio
import numpy as np
import tkinter as tk
from tkinter import messagebox
import time # Pour des pauses courtes si nécessaire

# --- Paramètres VoIP ---
# FORMAT peut être pyaudio.paInt16 pour 16-bit entier ou pyaudio.paFloat32 pour 32-bit flottant.
# paInt16 est plus courant pour la VoIP simple.
FORMAT = pyaudio.paInt16
CHANNELS = 1                # Nombre de canaux (mono)
RATE = 44100                # Fréquence d'échantillonnage (Hz). 48000 Hz est aussi très courant.
CHUNK_SIZE = 1024           # Taille du bloc audio à traiter (devrait être une puissance de 2, ex: 512, 1024, 2048)
                            # Une taille plus petite réduit la latence mais augmente la charge CPU et réseau.

# --- Variables globales ---
calling = False             # Indicateur si un appel est en cours (pour l'envoi)
receiving = False           # Indicateur si on reçoit de l'audio (pour la lecture)
p_audio = None              # Instance de PyAudio
stream_in = None            # Flux audio d'entrée (microphone)
stream_out = None           # Flux audio de sortie (haut-parleur)
peer_ip = ""                # Adresse IP du pair
peer_port = 12345           # Port par défaut pour la communication

# Indices des périphériques audio sélectionnés par défaut
# Ces valeurs seront déterminées par find_and_display_audio_devices()
selected_input_device_index = -1
selected_output_device_index = -1

# --- Fonction utilitaire pour trouver les indices des périphériques et les afficher ---
def find_and_display_audio_devices():
    """
    Initialise PyAudio (si nécessaire), liste les périphériques audio disponibles,
    tente de sélectionner les périphériques d'entrée et de sortie par défaut,
    et affiche ces informations dans la console et une boîte de dialogue.
    """
    global p_audio, selected_input_device_index, selected_output_device_index

    # Initialiser PyAudio si ce n'est pas déjà fait
    if p_audio is None:
        try:
            p_audio = pyaudio.PyAudio()
        except Exception as e:
            messagebox.showerror("Erreur PyAudio", f"Impossible d'initialiser PyAudio. "
                                 f"Assurez-vous que PortAudio est installé et configuré: {e}")
            print(f"Erreur PyAudio: {e}")
            return -1, -1 # Retourne des indices invalides

    info = p_audio.get_host_api_info_by_index(0) # Généralement 0 pour l'API hôte par défaut (ALSA/PulseAudio/PipeWire)
    numdevices = info.get('deviceCount')
    
    available_devices_str = []
    input_devices_map = {}  # Pour stocker les périphériques d'entrée valides
    output_devices_map = {} # Pour stocker les périphériques de sortie valides

    print("\n--- Périphériques audio disponibles (via PyAudio) ---")
    available_devices_str.append("--- Périphériques audio disponibles ---")
    
    # Parcourir tous les périphériques détectés
    for i in range(0, numdevices):
        dev_info = p_audio.get_device_info_by_host_api_device_index(0, i)
        device_name = dev_info.get('name')
        max_input_channels = dev_info.get('maxInputChannels')
        max_output_channels = dev_info.get('maxOutputChannels')

        device_line = f"  Index {i}: {device_name}"
        
        is_input = False
        is_output = False

        if max_input_channels > 0:
            device_line += f" (Entrée: {max_input_channels} ch)"
            input_devices_map[device_name] = i
            is_input = True
            # Tente de trouver le périphérique d'entrée par "défaut" ou contenant "pipewire"/"pulse"
            if selected_input_device_index == -1 and ("default" in device_name.lower() or "pipewire" in device_name.lower() or "pulse" in device_name.lower()):
                selected_input_device_index = i
        
        if max_output_channels > 0:
            device_line += f" (Sortie: {max_output_channels} ch)"
            output_devices_map[device_name] = i
            is_output = True
            # Tente de trouver le périphérique de sortie par "défaut" ou contenant "pipewire"/"pulse"
            if selected_output_device_index == -1 and ("default" in device_name.lower() or "pipewire" in device_name.lower() or "pulse" in device_name.lower()):
                selected_output_device_index = i
        
        # N'afficher que les périphériques qui ont une capacité d'entrée ou de sortie
        if is_input or is_output:
            print(device_line)
            available_devices_str.append(device_line)
    
    print("-" * 60)
    
    # Si aucun périphérique par défaut n'a été trouvé par nom, prendre le premier valide
    if selected_input_device_index == -1 and input_devices_map:
        selected_input_device_index = next(iter(input_devices_map.values()))
        print(f"Aucun périphérique d'entrée 'par défaut' trouvé, utilisant le premier trouvé: index {selected_input_device_index}")
    
    if selected_output_device_index == -1 and output_devices_map:
        selected_output_device_index = next(iter(output_devices_map.values()))
        print(f"Aucun périphérique de sortie 'par défaut' trouvé, utilisant le premier trouvé: index {selected_output_device_index}")

    print(f"Indice d'entrée sélectionné pour l'utilisation : {selected_input_device_index}")
    print(f"Indice de sortie sélectionné pour l'utilisation : {selected_output_device_index}")
    
    # Afficher les périphériques dans une boîte de dialogue pour l'utilisateur
    messagebox.showinfo("Périphériques Audio Détectés", "\n".join(available_devices_str) + 
                        f"\n\nIndice d'entrée suggéré: {selected_input_device_index}" +
                        f"\nIndice de sortie suggéré: {selected_output_device_index}\n"
                        f"Si l'audio ne fonctionne pas, essayez de changer ces indices manuellement dans le code.")

    return selected_input_device_index, selected_output_device_index

# --- Fonction d'envoi audio (client côté VoIP) ---
def send_audio(client_socket):
    """
    Enregistre l'audio depuis le microphone et l'envoie via le socket.
    Exécuté dans un thread séparé.
    """
    global calling, p_audio, stream_in, selected_input_device_index

    if p_audio is None:
        print("Erreur: PyAudio n'est pas initialisé pour l'envoi.")
        stop_call()
        return

    try:
        stream_in = p_audio.open(format=FORMAT,
                                 channels=CHANNELS,
                                 rate=RATE,
                                 input=True,
                                 frames_per_buffer=CHUNK_SIZE,
                                 input_device_index=selected_input_device_index # Utilise l'indice détecté
                                 )
        print("Enregistrement et envoi audio démarrés...")
        while calling:
            try:
                # Lire un bloc audio. exception_on_overflow=False pour éviter de planter
                # si le buffer du micro déborde.
                data = stream_in.read(CHUNK_SIZE, exception_on_overflow=False)
                client_socket.sendall(data)
            except IOError as e:
                # Gérer les erreurs de flux audio spécifiques (underflow/overflow)
                print(f"Erreur d'E/S audio lors de l'envoi: {e}")
                if e.errno == pyaudio.paInputOverflowed:
                    print("AVERTISSEMENT: Le buffer du microphone a débordé. L'audio pourrait être haché.")
                elif e.errno == pyaudio.paOutputUnderflowed:
                    print("AVERTISSEMENT: Le buffer de sortie a sous-débordé. L'audio pourrait être haché.")
                else:
                    print(f"Erreur inattendue de PyAudio lors de l'envoi. Arrêt de l'appel: {e}")
                    stop_call()
                    break # Sortir de la boucle d'envoi
            except Exception as e:
                print(f"Erreur générale lors de l'envoi audio: {e}")
                stop_call()
                break # Sortir de la boucle d'envoi
            time.sleep(0.001) # Petite pause pour libérer le CPU
    except Exception as e:
        print(f"Impossible d'ouvrir le flux d'entrée audio (microphone): {e}")
        messagebox.showerror("Erreur Audio Entrée", f"Impossible d'ouvrir le microphone: {e}\n"
                                                 "Vérifiez la sélection du périphérique, les permissions ou si le micro est déjà utilisé.")
        stop_call() # S'assurer que tout est nettoyé
    finally:
        if stream_in:
            try:
                stream_in.stop_stream()
                stream_in.close()
            except Exception as e:
                print(f"Erreur lors de l'arrêt/fermeture du stream d'entrée: {e}")
            stream_in = None

# --- Fonction de réception audio (serveur côté VoIP) ---
def receive_audio(conn, addr):
    """
    Reçoit l'audio via le socket et le joue sur les haut-parleurs.
    Exécuté dans un thread séparé.
    """
    global receiving, p_audio, stream_out, selected_output_device_index

    if p_audio is None:
        print("Erreur: PyAudio n'est pas initialisé pour la réception.")
        stop_call()
        return

    try:
        stream_out = p_audio.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer=CHUNK_SIZE,
                                  output_device_index=selected_output_device_index # Utilise l'indice détecté
                                  )
        print(f"Réception audio de {addr} démarrée...")
        while receiving:
            try:
                # Calculer la taille attendue des données en octets pour un CHUNK_SIZE donné
                expected_data_size = CHUNK_SIZE * p_audio.get_sample_size(FORMAT)
                data = conn.recv(expected_data_size)
                if not data:
                    print("Pair déconnecté ou fin de transmission détectée.")
                    break # Sortir de la boucle de réception
                
                # S'assurer que les données reçues ont la bonne taille
                if len(data) == expected_data_size:
                    stream_out.write(data)
                else:
                    print(f"AVERTISSEMENT: Taille de données reçue inattendue: {len(data)} octets "
                          f"au lieu de {expected_data_size}. Possible perte de paquets ou désynchronisation.")
                    # Peut-être jouer un silence ou une trame partielle si désiré, ici on l'ignore.
            except IOError as e:
                print(f"Erreur d'E/S audio lors de la réception: {e}")
                if e.errno == pyaudio.paOutputUnderflowed:
                    print("AVERTISSEMENT: Le buffer du haut-parleur a sous-débordé. L'audio pourrait être haché.")
                else:
                    print(f"Erreur inattendue de PyAudio lors de la réception. Arrêt de l'appel: {e}")
                    stop_call()
                    break # Sortir de la boucle de réception
            except Exception as e:
                print(f"Erreur générale lors de la réception audio: {e}")
                stop_call()
                break # Sortir de la boucle de réception
            time.sleep(0.001) # Petite pause
            
    except Exception as e:
        print(f"Impossible d'ouvrir le flux de sortie audio (haut-parleurs): {e}")
        messagebox.showerror("Erreur Audio Sortie", f"Impossible d'ouvrir les haut-parleurs: {e}\n"
                                                  "Vérifiez la sélection du périphérique, les permissions ou si le périphérique est déjà utilisé.")
        stop_call()
    finally:
        if stream_out:
            try:
                stream_out.stop_stream()
                stream_out.close()
            except Exception as e:
                print(f"Erreur lors de l'arrêt/fermeture du stream de sortie: {e}")
            stream_out = None
        if conn:
            conn.close() # Fermer la connexion du socket client/serveur

# --- Fonction de démarrage d'appel (client) ---
def start_call_client():
    """
    Tente de se connecter à un pair en tant que client et démarre les threads audio.
    """
    global calling, peer_ip, peer_port, p_audio, selected_input_device_index, selected_output_device_index

    peer_ip = entry_peer_ip.get()
    try:
        peer_port = int(entry_peer_port.get())
    except ValueError:
        messagebox.showerror("Erreur", "Le port doit être un nombre entier valide.")
        return

    if not peer_ip:
        messagebox.showerror("Erreur", "Veuillez entrer l'adresse IP du pair.")
        return

    # Initialiser PyAudio et trouver les périphériques au début de l'appel/écoute
    # Cela affichera la boîte de dialogue avec les infos sur les périphériques.
    _input_idx, _output_idx = find_and_display_audio_devices() 
    if _input_idx == -1 or _output_idx == -1:
        messagebox.showerror("Erreur", "Impossible de trouver un périphérique audio d'entrée ou de sortie valide. "
                                     "Vérifiez la console pour les diagnostics PyAudio.")
        # Nettoyer PyAudio si initialisé mais non utilisable
        if p_audio: 
            try: p_audio.terminate() 
            except: pass
            p_audio = None
        return

    selected_input_device_index = _input_idx
    selected_output_device_index = _output_idx

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"Tentative de connexion à {peer_ip}:{peer_port}...")
        client_socket.connect((peer_ip, peer_port))
        messagebox.showinfo("Connexion établie", f"Connecté à {peer_ip}:{peer_port}")
        
        calling = True
        receiving = True
        
        # Démarrer les threads d'envoi et de réception audio
        threading.Thread(target=send_audio, args=(client_socket,)).start()
        # Pour receive_audio, le deuxième argument est juste pour l'information de logging (adresse du pair)
        threading.Thread(target=receive_audio, args=(client_socket, (peer_ip, peer_port))).start() 
        
        # Mettre à jour l'état des boutons de l'interface
        btn_call.config(state=tk.DISABLED)
        btn_listen.config(state=tk.DISABLED)
        btn_stop.config(state=tk.NORMAL)
    except ConnectionRefusedError:
        messagebox.showerror("Erreur de connexion", "Connexion refusée. Assurez-vous que le pair écoute sur le port spécifié.")
        client_socket.close()
        stop_call() # Nettoyer proprement
    except Exception as e:
        messagebox.showerror("Erreur de connexion", f"Impossible de se connecter au pair: {e}")
        print(f"Erreur de connexion client: {e}")
        client_socket.close()
        stop_call() # Nettoyer proprement

# --- Fonction de démarrage d'écoute (serveur) ---
def start_listen_server():
    """
    Démarre un serveur qui écoute les connexions entrantes et démarre les threads audio.
    """
    global receiving, peer_port, p_audio, selected_input_device_index, selected_output_device_index
    try:
        peer_port = int(entry_listen_port.get())
    except ValueError:
        messagebox.showerror("Erreur", "Le port doit être un nombre entier valide.")
        return

    # Initialiser PyAudio et trouver les périphériques au début de l'appel/écoute
    _input_idx, _output_idx = find_and_display_audio_devices()
    if _input_idx == -1 or _output_idx == -1:
        messagebox.showerror("Erreur", "Impossible de trouver un périphérique audio d'entrée ou de sortie valide. "
                                     "Vérifiez la console pour les diagnostics PyAudio.")
        if p_audio: 
            try: p_audio.terminate() 
            except: pass
            p_audio = None
        return

    selected_input_device_index = _input_idx
    selected_output_device_index = _output_idx

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permet de réutiliser l'adresse rapidement

    try:
        server_socket.bind(('', peer_port)) # Lie le socket à toutes les interfaces réseau disponibles
        server_socket.listen(1) # N'accepte qu'une seule connexion en attente
        print(f"En attente de connexion sur le port {peer_port}...")
        messagebox.showinfo("En attente", f"En attente d'appels sur le port {peer_port}...")
        
        # Mettre à jour l'état des boutons
        btn_call.config(state=tk.DISABLED)
        btn_listen.config(state=tk.DISABLED)
        btn_stop.config(state=tk.NORMAL)

        def accept_connection_and_start_voip():
            """
            Fonction interne pour accepter une connexion et lancer les threads VoIP.
            Exécutée dans un thread pour ne pas bloquer l'interface.
            """
            global calling, receiving
            try:
                conn, addr = server_socket.accept() # Bloque jusqu'à ce qu'une connexion soit acceptée
                print(f"Connexion acceptée de {addr}")
                messagebox.showinfo("Connexion acceptée", f"Connexion entrante de {addr[0]}")
                
                calling = True
                receiving = True
                
                # Démarrer les threads d'envoi et de réception audio
                threading.Thread(target=send_audio, args=(conn,)).start()
                threading.Thread(target=receive_audio, args=(conn, addr)).start()
            except Exception as e:
                messagebox.showerror("Erreur Serveur", f"Erreur lors de l'acceptation de la connexion: {e}")
                print(f"Erreur accept_connection_and_start_voip: {e}")
                stop_call() # Nettoyer proprement
            finally:
                server_socket.close() # Fermer le socket serveur une fois la connexion établie

        # Lancer un thread pour accepter la connexion
        threading.Thread(target=accept_connection_and_start_voip).start()
    except OSError as e:
        if e.errno == 98: # Erreur "Address already in use"
             messagebox.showerror("Erreur de port", f"Le port {peer_port} est déjà utilisé. Veuillez en choisir un autre.")
        else:
            messagebox.showerror("Erreur Serveur", f"Impossible de démarrer le serveur: {e}")
        print(f"Erreur de démarrage du serveur: {e}")
        server_socket.close()
        stop_call() # Nettoyer proprement
    except Exception as e:
        messagebox.showerror("Erreur Serveur", f"Impossible de démarrer le serveur: {e}")
        print(f"Erreur de démarrage du serveur: {e}")
        server_socket.close()
        stop_call() # Nettoyer proprement

# --- Fonction d'arrêt de l'appel ---
def stop_call():
    """
    Arrête tous les flux audio, ferme PyAudio et réinitialise l'interface.
    """
    global calling, receiving, stream_in, stream_out, p_audio
    print("Demande d'arrêt de l'appel...")
    
    # Signaler aux threads de s'arrêter
    calling = False
    receiving = False

    # Arrêter et fermer proprement les flux audio si ils sont actifs
    if stream_in:
        try:
            if stream_in.is_active():
                stream_in.stop_stream()
            stream_in.close()
            print("Stream d'entrée arrêté et fermé.")
        except Exception as e:
            print(f"Erreur lors de l'arrêt/fermeture du stream d'entrée: {e}")
        stream_in = None
        
    if stream_out:
        try:
            if stream_out.is_active():
                stream_out.stop_stream()
            stream_out.close()
            print("Stream de sortie arrêté et fermé.")
        except Exception as e:
            print(f"Erreur lors de l'arrêt/fermeture du stream de sortie: {e}")
        stream_out = None
    
    # Terminer l'instance PyAudio seulement quand tous les flux sont fermés
    if p_audio: 
        try:
            p_audio.terminate()
            print("PyAudio terminé.")
        except Exception as e:
            print(f"Erreur lors de la terminaison de PyAudio: {e}")
        p_audio = None

    messagebox.showinfo("Appel terminé", "L'appel a été arrêté.")
    
    # Réactiver les boutons d'appel/écoute et désactiver le bouton d'arrêt
    btn_call.config(state=tk.NORMAL)
    btn_listen.config(state=tk.NORMAL)
    btn_stop.config(state=tk.DISABLED)

# --- Interface graphique Tkinter ---
root = tk.Tk()
root.title("VoIP P2P Simple (PyAudio)")

# Cadre pour l'appel client
frame_client = tk.LabelFrame(root, text="Appeler un pair")
frame_client.pack(padx=10, pady=10, fill="x")

tk.Label(frame_client, text="IP du pair:").pack(side=tk.LEFT, padx=5, pady=5)
entry_peer_ip = tk.Entry(frame_client)
entry_peer_ip.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill="x")
entry_peer_ip.insert(0, "127.0.0.1") # Exemple d'IP locale pour le test

tk.Label(frame_client, text="Port:").pack(side=tk.LEFT, padx=5, pady=5)
entry_peer_port = tk.Entry(frame_client, width=8)
entry_peer_port.pack(side=tk.LEFT, padx=5, pady=5)
entry_peer_port.insert(0, str(peer_port)) # Port par défaut

btn_call = tk.Button(frame_client, text="Appeler", command=start_call_client)
btn_call.pack(side=tk.RIGHT, padx=5, pady=5)

# Cadre pour l'écoute serveur
frame_server = tk.LabelFrame(root, text="Attendre un appel")
frame_server.pack(padx=10, pady=10, fill="x")

tk.Label(frame_server, text="Port d'écoute:").pack(side=tk.LEFT, padx=5, pady=5)
entry_listen_port = tk.Entry(frame_server, width=8)
entry_listen_port.pack(side=tk.LEFT, padx=5, pady=5)
entry_listen_port.insert(0, str(peer_port)) # Port par défaut

btn_listen = tk.Button(frame_server, text="Écouter", command=start_listen_server)
btn_listen.pack(side=tk.RIGHT, padx=5, pady=5)

# Bouton d'arrêt général
btn_stop = tk.Button(root, text="Arrêter l'appel", command=stop_call, state=tk.DISABLED)
btn_stop.pack(pady=10)

# Gérer la fermeture de la fenêtre Tkinter pour un arrêt propre
def on_closing():
    if messagebox.askokcancel("Quitter l'application", "Voulez-vous vraiment quitter? L'appel sera arrêté."):
        stop_call() # S'assurer que les ressources audio/réseau sont libérées
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing) # Attache la fonction on_closing à l'événement de fermeture de la fenêtre

# Lancer la boucle principale de Tkinter
root.mainloop()