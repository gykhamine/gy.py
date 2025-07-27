import socket
import threading
import pyaudio
import numpy as np
import tkinter as tk
from tkinter import messagebox

# --- Paramètres VoIP ---
FORMAT = pyaudio.paFloat32  # Format audio (peut être ajusté : paInt16, paFloat32, etc.)
CHANNELS = 1                # Nombre de canaux (mono)
RATE = 44100                # Fréquence d'échantillonnage (Hz)
CHUNK_SIZE = 1024           # Taille du bloc audio à traiter

# --- Variables globales ---
calling = False
receiving = False
p_audio = None
stream_in = None
stream_out = None
peer_ip = ""
peer_port = 12345 # Port par défaut

# --- Fonction d'envoi audio ---
def send_audio(client_socket):
    global calling, p_audio, stream_in
    try:
        # Initialiser PyAudio si ce n'est pas déjà fait
        if p_audio is None:
            p_audio = pyaudio.PyAudio()

        stream_in = p_audio.open(format=FORMAT,
                                 channels=CHANNELS,
                                 rate=RATE,
                                 input=True,
                                 frames_per_buffer=CHUNK_SIZE)
        print("Enregistrement et envoi audio...")
        while calling:
            data = stream_in.read(CHUNK_SIZE, exception_on_overflow=False)
            client_socket.sendall(data)
    except Exception as e:
        print(f"Erreur lors de l'envoi audio: {e}")
        stop_call()
    finally:
        if stream_in:
            stream_in.stop_stream()
            stream_in.close()
            stream_in = None
        # Ne fermez pas p_audio ici car il pourrait être utilisé par le stream_out
        # La fermeture se fera dans stop_call()

# --- Fonction de réception audio ---
def receive_audio(conn, addr):
    global receiving, p_audio, stream_out
    try:
        # Initialiser PyAudio si ce n'est pas déjà fait
        if p_audio is None:
            p_audio = pyaudio.PyAudio()

        stream_out = p_audio.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer=CHUNK_SIZE)
        print(f"Réception audio de {addr}...")
        while receiving:
            data = conn.recv(CHUNK_SIZE * p_audio.get_sample_size(FORMAT))
            if not data:
                break
            stream_out.write(data)
    except Exception as e:
        print(f"Erreur lors de la réception audio: {e}")
        stop_call()
    finally:
        if stream_out:
            stream_out.stop_stream()
            stream_out.close()
            stream_out = None
        if conn:
            conn.close()
        # Ne fermez pas p_audio ici

# --- Fonction de démarrage d'appel (client) ---
def start_call_client():
    global calling, peer_ip, peer_port, p_audio
    peer_ip = entry_peer_ip.get()
    try:
        peer_port = int(entry_peer_port.get())
    except ValueError:
        messagebox.showerror("Erreur", "Le port doit être un nombre entier.")
        return

    if not peer_ip:
        messagebox.showerror("Erreur", "Veuillez entrer l'adresse IP du pair.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"Tentative de connexion à {peer_ip}:{peer_port}...")
        client_socket.connect((peer_ip, peer_port))
        messagebox.showinfo("Connexion établie", f"Connecté à {peer_ip}:{peer_port}")
        calling = True
        receiving = True

        # Initialiser PyAudio une fois au début
        if p_audio is None:
            p_audio = pyaudio.PyAudio()

        threading.Thread(target=send_audio, args=(client_socket,)).start()
        threading.Thread(target=receive_audio, args=(client_socket, ("client", 0))).start() # (client, 0) pour simuler addr
        btn_call.config(state=tk.DISABLED)
        btn_listen.config(state=tk.DISABLED)
        btn_stop.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Erreur de connexion", f"Impossible de se connecter au pair: {e}")
        calling = False
        receiving = False
        client_socket.close()
        if p_audio and not stream_in and not stream_out: # Fermer PyAudio si aucune connexion n'a été établie
            p_audio.terminate()
            p_audio = None

# --- Fonction de démarrage d'écoute (serveur) ---
def start_listen_server():
    global receiving, peer_port, p_audio
    try:
        peer_port = int(entry_listen_port.get())
    except ValueError:
        messagebox.showerror("Erreur", "Le port doit être un nombre entier.")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('', peer_port))
        server_socket.listen(1)
        print(f"En attente de connexion sur le port {peer_port}...")
        messagebox.showinfo("En attente", f"En attente d'appels sur le port {peer_port}...")
        btn_call.config(state=tk.DISABLED)
        btn_listen.config(state=tk.DISABLED)
        btn_stop.config(state=tk.NORMAL)

        # Initialiser PyAudio une fois au début
        if p_audio is None:
            p_audio = pyaudio.PyAudio()

        def accept_connection():
            global calling, receiving
            try:
                conn, addr = server_socket.accept()
                print(f"Connexion acceptée de {addr}")
                messagebox.showinfo("Connexion acceptée", f"Connexion entrante de {addr[0]}")
                calling = True
                receiving = True
                threading.Thread(target=send_audio, args=(conn,)).start()
                threading.Thread(target=receive_audio, args=(conn, addr)).start()
            except Exception as e:
                messagebox.showerror("Erreur serveur", f"Erreur lors de l'acceptation de la connexion: {e}")
                stop_call()
            finally:
                server_socket.close()

        threading.Thread(target=accept_connection).start()
    except Exception as e:
        messagebox.showerror("Erreur serveur", f"Impossible de démarrer le serveur: {e}")
        server_socket.close()
        if p_audio and not stream_in and not stream_out: # Fermer PyAudio si aucune connexion n'a été établie
            p_audio.terminate()
            p_audio = None

# --- Fonction d'arrêt de l'appel ---
def stop_call():
    global calling, receiving, stream_in, stream_out, p_audio
    print("Arrêt de l'appel...")
    calling = False
    receiving = False

    if stream_in:
        stream_in.stop_stream()
        stream_in.close()
        stream_in = None
    if stream_out:
        stream_out.stop_stream()
        stream_out.close()
        stream_out = None
    if p_audio: # Terminer PyAudio seulement quand tous les streams sont fermés
        p_audio.terminate()
        p_audio = None

    messagebox.showinfo("Appel terminé", "L'appel a été arrêté.")
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
entry_peer_ip.insert(0, "127.0.0.1") # Exemple IP locale

tk.Label(frame_client, text="Port:").pack(side=tk.LEFT, padx=5, pady=5)
entry_peer_port = tk.Entry(frame_client, width=8)
entry_peer_port.pack(side=tk.LEFT, padx=5, pady=5)
entry_peer_port.insert(0, str(peer_port))

btn_call = tk.Button(frame_client, text="Appeler", command=start_call_client)
btn_call.pack(side=tk.RIGHT, padx=5, pady=5)

# Cadre pour l'écoute serveur
frame_server = tk.LabelFrame(root, text="Attendre un appel")
frame_server.pack(padx=10, pady=10, fill="x")

tk.Label(frame_server, text="Port d'écoute:").pack(side=tk.LEFT, padx=5, pady=5)
entry_listen_port = tk.Entry(frame_server, width=8)
entry_listen_port.pack(side=tk.LEFT, padx=5, pady=5)
entry_listen_port.insert(0, str(peer_port))

btn_listen = tk.Button(frame_server, text="Écouter", command=start_listen_server)
btn_listen.pack(side=tk.RIGHT, padx=5, pady=5)

# Bouton d'arrêt
btn_stop = tk.Button(root, text="Arrêter l'appel", command=stop_call, state=tk.DISABLED)
btn_stop.pack(pady=10)

# Gérer la fermeture de la fenêtre
def on_closing():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter? L'appel sera arrêté."):
        stop_call()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()