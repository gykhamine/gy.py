import customtkinter
import threading
import socket
import queue
import os
import struct # Pour empaqueter/désemballer les tailles de fichiers
from tkinter import filedialog # Pour ouvrir la boîte de dialogue de sélection de fichier

# Constantes pour notre protocole de fichier
# Nous utilisons un code simple pour indiquer le type de message
MSG_TYPE_TEXT = 1
MSG_TYPE_FILE = 2
# La taille de l'entête pour le type de message et la taille du nom de fichier/fichier
# '!' pour network byte order, 'B' pour byte (type), 'H' pour unsigned short (taille_nom_fichier), 'L' pour unsigned long (taille_fichier)
# Soit 1 + 2 + 4 = 7 octets pour l'entête du fichier
FILE_HEADER_FORMAT = "!BHL" # Type, Longueur du nom, Longueur du fichier
FILE_HEADER_SIZE = struct.calcsize(FILE_HEADER_FORMAT)


class NetApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Application Réseau (Serveur, Client & Fichiers)")
        self.geometry("1000x700")

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Cadre Serveur ---
        self.server_frame = customtkinter.CTkFrame(self)
        self.server_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.server_frame.grid_columnconfigure(1, weight=1)
        self.server_frame.grid_rowconfigure(6, weight=1)

        self.server_label = customtkinter.CTkLabel(self.server_frame, text="--- Serveur ---", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.server_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.server_ip_label = customtkinter.CTkLabel(self.server_frame, text="IP Serveur:")
        self.server_ip_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.server_ip_entry = customtkinter.CTkEntry(self.server_frame)
        self.server_ip_entry.insert(0, "127.0.0.1")
        self.server_ip_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.server_port_label = customtkinter.CTkLabel(self.server_frame, text="Port Serveur:")
        self.server_port_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.server_port_entry = customtkinter.CTkEntry(self.server_frame)
        self.server_port_entry.insert(0, "12345")
        self.server_port_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.server_protocol_label = customtkinter.CTkLabel(self.server_frame, text="Protocole:")
        self.server_protocol_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.server_protocol_optionmenu = customtkinter.CTkOptionMenu(self.server_frame, values=["TCP", "UDP"])
        self.server_protocol_optionmenu.set("TCP")
        self.server_protocol_optionmenu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.start_server_button = customtkinter.CTkButton(self.server_frame, text="Démarrer Serveur", command=self.start_server)
        self.start_server_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.stop_server_button = customtkinter.CTkButton(self.server_frame, text="Arrêter Serveur", command=self.stop_server, state="disabled")
        self.stop_server_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.server_log_text = customtkinter.CTkTextbox(self.server_frame, height=200)
        self.server_log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # --- Cadre Client ---
        self.client_frame = customtkinter.CTkFrame(self)
        self.client_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.client_frame.grid_columnconfigure(1, weight=1)
        self.client_frame.grid_rowconfigure(9, weight=1) # Log client

        self.client_label = customtkinter.CTkLabel(self.client_frame, text="--- Client ---", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.client_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.target_ip_label = customtkinter.CTkLabel(self.client_frame, text="IP Cible:")
        self.target_ip_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.target_ip_entry = customtkinter.CTkEntry(self.client_frame)
        self.target_ip_entry.insert(0, "127.0.0.1")
        self.target_ip_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.target_port_label = customtkinter.CTkLabel(self.client_frame, text="Port Cible:")
        self.target_port_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.target_port_entry = customtkinter.CTkEntry(self.client_frame)
        self.target_port_entry.insert(0, "12345")
        self.target_port_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.client_protocol_label = customtkinter.CTkLabel(self.client_frame, text="Protocole:")
        self.client_protocol_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.client_protocol_optionmenu = customtkinter.CTkOptionMenu(self.client_frame, values=["TCP", "UDP"], command=self.on_client_protocol_change)
        self.client_protocol_optionmenu.set("TCP")
        self.client_protocol_optionmenu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.message_to_send_label = customtkinter.CTkLabel(self.client_frame, text="Message Texte:")
        self.message_to_send_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.message_to_send_entry = customtkinter.CTkEntry(self.client_frame)
        self.message_to_send_entry.insert(0, "Hello from client!")
        self.message_to_send_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.send_text_button = customtkinter.CTkButton(self.client_frame, text="Envoyer Texte", command=self.send_text_message_client)
        self.send_text_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.file_path_label = customtkinter.CTkLabel(self.client_frame, text="Fichier à envoyer:")
        self.file_path_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.file_path_entry = customtkinter.CTkEntry(self.client_frame)
        self.file_path_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        self.browse_file_button = customtkinter.CTkButton(self.client_frame, text="Parcourir...", command=self.browse_file)
        self.browse_file_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.send_file_button = customtkinter.CTkButton(self.client_frame, text="Envoyer Fichier", command=self.send_file_message_client)
        self.send_file_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")


        self.client_log_text = customtkinter.CTkTextbox(self.client_frame, height=200)
        self.client_log_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # --- Variables d'état ---
        self.server_thread = None
        self.server_running = threading.Event()
        self.server_message_queue = queue.Queue()

        self.client_thread = None
        self.client_socket_tcp = None
        self.client_message_queue = queue.Queue()
        self.client_socket_lock = threading.Lock() # Pour protéger l'accès au socket client TCP

        self.after(100, self.check_server_message_queue)
        self.after(100, self.check_client_message_queue)

        self.on_client_protocol_change(self.client_protocol_optionmenu.get())

    def on_client_protocol_change(self, choice):
        if choice == "TCP":
            # Le bouton "Connecter/Envoyer" n'est plus pertinent car il y a des boutons spécifiques pour texte et fichier
            # Mais si on veut une connexion TCP persistante, on peut réactiver un bouton "Connecter" séparé.
            # Pour l'instant, l'envoi de texte ou fichier TCP gérera la connexion.
            if self.client_socket_tcp:
                self.log_client_message("Une connexion TCP existante peut être utilisée pour envoyer texte/fichier.")
            else:
                self.log_client_message("Pas de connexion TCP active. L'envoi de texte/fichier tentera de se connecter.")
        elif choice == "UDP":
            if self.client_socket_tcp:
                self.client_socket_lock.acquire()
                try:
                    self.client_socket_tcp.close()
                    self.client_socket_tcp = None
                    self.log_client_message("La connexion TCP du client a été fermée car le protocole a changé pour UDP.")
                finally:
                    self.client_socket_lock.release()

    def log_server_message(self, message):
        self.server_log_text.insert("end", message + "\n")
        self.server_log_text.see("end")

    def log_client_message(self, message):
        self.client_log_text.insert("end", message + "\n")
        self.client_log_text.see("end")

    def check_server_message_queue(self):
        try:
            while True:
                message = self.server_message_queue.get_nowait()
                self.log_server_message(message)
        except queue.Empty:
            pass
        self.after(100, self.check_server_message_queue)

    def check_client_message_queue(self):
        try:
            while True:
                message = self.client_message_queue.get_nowait()
                self.log_client_message(message)
        except queue.Empty:
            pass
        self.after(100, self.check_client_message_queue)

    # --- Logique Serveur ---

    def start_server(self):
        ip = self.server_ip_entry.get()
        port = int(self.server_port_entry.get())
        server_type = self.server_protocol_optionmenu.get()

        self.server_running.set()
        if server_type == "TCP":
            self.server_thread = threading.Thread(target=self.run_tcp_server, args=(ip, port), name="TCP_Server_Thread")
        elif server_type == "UDP":
            self.server_thread = threading.Thread(target=self.run_udp_server, args=(ip, port), name="UDP_Server_Thread")
        
        self.server_thread.daemon = True
        self.server_thread.start()

        self.start_server_button.configure(state="disabled")
        self.stop_server_button.configure(state="normal")
        self.server_message_queue.put(f"Tentative de démarrage du serveur {server_type} sur {ip}:{port}...")

    def stop_server(self):
        self.server_running.clear()
        self.server_message_queue.put("Signal d'arrêt envoyé au serveur...")

        if self.server_thread and self.server_thread.is_alive():
            if self.server_thread.name == "TCP_Server_Thread":
                 try:
                     dummy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                     dummy_sock.connect((self.server_ip_entry.get(), int(self.server_port_entry.get())))
                     dummy_sock.close()
                 except socket.error:
                     pass
            
            self.server_thread.join(timeout=2)
            if self.server_thread.is_alive():
                self.server_message_queue.put("Le thread du serveur ne s'est pas terminé gracieusement.")
            else:
                self.server_message_queue.put("Serveur arrêté.")
        else:
            self.server_message_queue.put("Le serveur n'est pas en cours d'exécution ou est déjà arrêté.")

        self.start_server_button.configure(state="normal")
        self.stop_server_button.configure(state="disabled")

    def run_tcp_server(self, ip, port):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((ip, port))
            sock.listen(5)
            self.server_message_queue.put(f"Serveur TCP écoutant sur {ip}:{port}")
            sock.settimeout(1.0)

            while self.server_running.is_set():
                try:
                    conn, addr = sock.accept()
                    self.server_message_queue.put(f"Connexion TCP acceptée de {addr}")
                    client_handler_thread = threading.Thread(target=self.handle_tcp_client, args=(conn, addr))
                    client_handler_thread.daemon = True
                    client_handler_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    self.server_message_queue.put(f"Erreur Serveur TCP: {e}")
                    break

        except Exception as e:
            self.server_message_queue.put(f"Échec du démarrage du Serveur TCP: {e}")
        finally:
            if sock:
                sock.close()
                self.server_message_queue.put("Socket du serveur TCP fermé.")
            self.server_running.clear()

    def handle_tcp_client(self, conn, addr):
        try:
            with conn:
                while self.server_running.is_set():
                    # Lire le type de message (1 octet)
                    msg_type_byte = conn.recv(1)
                    if not msg_type_byte: # Client déconnecté
                        self.server_message_queue.put(f"Client TCP {addr} déconnecté.")
                        break

                    msg_type = struct.unpack("!B", msg_type_byte)[0]

                    if msg_type == MSG_TYPE_TEXT:
                        # Lire la taille du message texte (2 octets)
                        len_bytes = conn.recv(2)
                        if not len_bytes: break
                        msg_len = struct.unpack("!H", len_bytes)[0]
                        
                        # Lire le message texte
                        data = b''
                        while len(data) < msg_len:
                            packet = conn.recv(min(msg_len - len(data), 4096))
                            if not packet: break
                            data += packet
                        if len(data) != msg_len:
                            self.server_message_queue.put(f"Erreur: Données de texte incomplètes de {addr}")
                            break
                        
                        message_received = data.decode('utf-8')
                        self.server_message_queue.put(f"[TCP] Reçu texte de {addr}: '{message_received}'")
                        response = f"Serveur TCP a reçu texte: '{message_received}'".encode('utf-8')
                        conn.sendall(response)

                    elif msg_type == MSG_TYPE_FILE:
                        # Lire le reste de l'entête du fichier (longueur_nom, longueur_fichier)
                        file_header_rest = conn.recv(FILE_HEADER_SIZE - 1) # Déjà lu 1 octet de type
                        if not file_header_rest or len(file_header_rest) != (FILE_HEADER_SIZE - 1):
                            self.server_message_queue.put(f"Erreur: Entête de fichier incomplet de {addr}")
                            break
                        
                        file_name_len, file_size = struct.unpack("!HL", file_header_rest)

                        # Lire le nom du fichier
                        file_name_bytes = b''
                        while len(file_name_bytes) < file_name_len:
                            packet = conn.recv(min(file_name_len - len(file_name_bytes), 4096))
                            if not packet: break
                            file_name_bytes += packet
                        if len(file_name_bytes) != file_name_len:
                            self.server_message_queue.put(f"Erreur: Nom de fichier incomplet de {addr}")
                            break
                        file_name = file_name_bytes.decode('utf-8')

                        self.server_message_queue.put(f"[TCP] Reçu fichier '{file_name}' ({file_size} octets) de {addr}...")
                        
                        # Recevoir le contenu du fichier
                        received_bytes = 0
                        output_filepath = os.path.join("received_files", os.path.basename(file_name))
                        os.makedirs(os.path.dirname(output_filepath), exist_ok=True) # Créer le dossier si nécessaire

                        try:
                            with open(output_filepath, 'wb') as f:
                                while received_bytes < file_size:
                                    chunk_size = min(file_size - received_bytes, 4096)
                                    chunk = conn.recv(chunk_size)
                                    if not chunk: # Connexion interrompue
                                        self.server_message_queue.put(f"Erreur: Connexion interrompue lors de la réception de '{file_name}' de {addr}")
                                        break
                                    f.write(chunk)
                                    received_bytes += len(chunk)
                            
                            if received_bytes == file_size:
                                self.server_message_queue.put(f"[TCP] Fichier '{file_name}' reçu et enregistré dans '{output_filepath}'.")
                                conn.sendall(b"Fichier recu avec succes.")
                            else:
                                self.server_message_queue.put(f"Erreur: Fichier '{file_name}' incomplet de {addr}. Reçu {received_bytes}/{file_size} octets.")
                                conn.sendall(b"Erreur: Fichier incomplet.")
                        except Exception as file_e:
                            self.server_message_queue.put(f"Erreur lors de l'enregistrement du fichier '{file_name}': {file_e}")
                            conn.sendall(b"Erreur serveur lors de la reception du fichier.")

                    else:
                        self.server_message_queue.put(f"Type de message inconnu ({msg_type}) de {addr}")
                        # Lire le reste du paquet pour ne pas bloquer
                        conn.recv(4096) # Tente de vider le buffer

        except Exception as e:
            self.server_message_queue.put(f"Erreur de gestion client TCP {addr}: {e}")
        finally:
            self.server_message_queue.put(f"Gestionnaire client TCP pour {addr} terminé.")

    def run_udp_server(self, ip, port):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((ip, port))
            self.server_message_queue.put(f"Serveur UDP écoutant sur {ip}:{port}")
            sock.settimeout(1.0)

            # UDP est sans connexion, donc nous recevons des datagrammes et non des flux
            # Le transfert de fichiers UDP est plus complexe (fiabilité, ordre),
            # Nous ferons un exemple simple qui reçoit tout le fichier en un seul datagramme ou en perd des morceaux.
            # Pour de gros fichiers en UDP, un protocole de type "fiable UDP" est nécessaire.
            # Ici, nous supposons que le datagramme complet (entête + données) tiendra dans un seul recvfrom.
            
            while self.server_running.is_set():
                try:
                    data, addr = sock.recvfrom(65535) # Max UDP packet size
                    
                    if len(data) < 1: # Pas assez de données pour le type de message
                        self.server_message_queue.put(f"UDP: Données vides ou trop courtes de {addr}.")
                        continue

                    msg_type = struct.unpack("!B", data[0:1])[0]
                    payload = data[1:] # Le reste du datagramme

                    if msg_type == MSG_TYPE_TEXT:
                        # Pour UDP texte, le message est juste après le type (pas de longueur explicite pour l'instant)
                        # Pour un UDP plus robuste, vous devriez inclure la longueur du message
                        message_received = payload.decode('utf-8')
                        self.server_message_queue.put(f"[UDP] Reçu texte de {addr}: '{message_received}'")
                        response = f"Serveur UDP a reçu texte: '{message_received}'".encode('utf-8')
                        sock.sendto(response, addr)

                    elif msg_type == MSG_TYPE_FILE:
                        if len(payload) < (FILE_HEADER_SIZE -1): # Pas assez pour l'entête
                            self.server_message_queue.put(f"UDP: Entête de fichier incomplet de {addr}.")
                            continue
                        
                        file_header_rest = payload[0:(FILE_HEADER_SIZE - 1)]
                        file_name_len, file_size = struct.unpack("!HL", file_header_rest)
                        
                        file_name_start_index = (FILE_HEADER_SIZE - 1)
                        file_content_start_index = file_name_start_index + file_name_len

                        if len(payload) < file_content_start_index:
                             self.server_message_queue.put(f"UDP: Nom de fichier incomplet ou absent de {addr}.")
                             continue

                        file_name_bytes = payload[file_name_start_index:file_content_start_index]
                        file_name = file_name_bytes.decode('utf-8')
                        
                        file_content = payload[file_content_start_index:]

                        if len(file_content) != file_size:
                            self.server_message_queue.put(f"ATTENTION: Fichier UDP '{file_name}' de {addr} reçu incomplet! Attendu {file_size}, reçu {len(file_content)} octets.")
                            # UDP ne garantit pas la livraison complète ou l'ordre, donc c'est une alerte
                        
                        self.server_message_queue.put(f"[UDP] Reçu fichier '{file_name}' ({len(file_content)}/{file_size} octets) de {addr}...")
                        
                        output_filepath = os.path.join("received_files", os.path.basename(file_name))
                        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

                        try:
                            with open(output_filepath, 'wb') as f:
                                f.write(file_content)
                            self.server_message_queue.put(f"[UDP] Fichier '{file_name}' reçu et enregistré dans '{output_filepath}'.")
                            sock.sendto(b"Fichier recu avec succes (UDP).", addr)
                        except Exception as file_e:
                            self.server_message_queue.put(f"Erreur lors de l'enregistrement du fichier '{file_name}' (UDP): {file_e}")
                            sock.sendto(b"Erreur serveur UDP.", addr)

                    else:
                        self.server_message_queue.put(f"Type de message UDP inconnu ({msg_type}) de {addr}")

                except socket.timeout:
                    continue
                except Exception as e:
                    self.server_message_queue.put(f"Erreur Serveur UDP: {e}")
                    break

        except Exception as e:
            self.server_message_queue.put(f"Échec du démarrage du Serveur UDP: {e}")
        finally:
            if sock:
                sock.close()
                self.server_message_queue.put("Socket du serveur UDP fermé.")
            self.server_running.clear()

    # --- Logique Client ---

    def browse_file(self):
        """Ouvre une boîte de dialogue pour sélectionner un fichier à envoyer."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_entry.delete(0, customtkinter.END)
            self.file_path_entry.insert(0, file_path)
            self.log_client_message(f"Fichier sélectionné: {file_path}")

    def send_text_message_client(self):
        """Envoie le message texte saisi par le client."""
        target_ip = self.target_ip_entry.get()
        target_port = int(self.target_port_entry.get())
        client_type = self.client_protocol_optionmenu.get()
        message = self.message_to_send_entry.get()

        if client_type == "TCP":
            thread_args = (target_ip, target_port, message.encode('utf-8'), MSG_TYPE_TEXT)
            self.client_thread = threading.Thread(target=self._send_tcp_data_with_header, args=thread_args, name="TCP_Client_Send_Text_Thread")
        elif client_type == "UDP":
            thread_args = (target_ip, target_port, message.encode('utf-8'), MSG_TYPE_TEXT)
            self.client_thread = threading.Thread(target=self._send_udp_data_with_header, args=thread_args, name="UDP_Client_Send_Text_Thread")
        
        self.client_thread.daemon = True
        self.client_thread.start()

    def send_file_message_client(self):
        """Envoie le fichier sélectionné par le client."""
        file_path = self.file_path_entry.get()
        if not os.path.exists(file_path):
            self.log_client_message("Erreur: Le fichier spécifié n'existe pas.")
            return

        target_ip = self.target_ip_entry.get()
        target_port = int(self.target_port_entry.get())
        client_type = self.client_protocol_optionmenu.get()

        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            file_name = os.path.basename(file_path)
            
            # Créer l'entête du fichier
            # type (1B), longueur_nom (2B), taille_fichier (4B)
            # max file_name_len: 65535, max file_size: 4GB
            file_name_bytes = file_name.encode('utf-8')
            if len(file_name_bytes) > 65535:
                self.log_client_message("Erreur: Nom de fichier trop long.")
                return
            if len(file_content) > 0xFFFFFFFF: # Plus de 4GB
                 self.log_client_message("Erreur: Fichier trop grand pour le protocole actuel (>4GB).")
                 return

            file_header = struct.pack(FILE_HEADER_FORMAT, MSG_TYPE_FILE, len(file_name_bytes), len(file_content))
            
            # Assembler le paquet complet pour l'envoi
            data_to_send = file_header + file_name_bytes + file_content

            if client_type == "TCP":
                thread_args = (target_ip, target_port, data_to_send, MSG_TYPE_FILE, file_name)
                self.client_thread = threading.Thread(target=self._send_tcp_data_with_header, args=thread_args, name="TCP_Client_Send_File_Thread")
            elif client_type == "UDP":
                thread_args = (target_ip, target_port, data_to_send, MSG_TYPE_FILE, file_name)
                self.client_thread = threading.Thread(target=self._send_udp_data_with_header, args=thread_args, name="UDP_Client_Send_File_Thread")
            
            self.client_thread.daemon = True
            self.client_thread.start()

        except Exception as e:
            self.log_client_message(f"Erreur lors de la préparation du fichier: {e}")


    def _send_tcp_data_with_header(self, ip, port, data_to_send, msg_type, file_name=None):
        """Logique d'envoi de données via TCP (texte ou fichier) avec gestion de connexion."""
        with self.client_socket_lock: # Assurer qu'un seul thread accède au socket client TCP
            if self.client_socket_tcp is None:
                try:
                    self.client_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket_tcp.settimeout(10.0) # Timeout pour la connexion
                    self.client_message_queue.put(f"Client TCP: Tentative de connexion à {ip}:{port}...")
                    self.client_socket_tcp.connect((ip, port))
                    self.client_message_queue.put(f"Client TCP: Connecté à {ip}:{port}")
                except socket.timeout:
                    self.client_message_queue.put(f"Client TCP: Échec de la connexion (timeout) à {ip}:{port}")
                    self.client_socket_tcp = None
                    return
                except Exception as e:
                    self.client_message_queue.put(f"Client TCP: Erreur de connexion: {e}")
                    self.client_socket_tcp = None
                    return
            
            try:
                if msg_type == MSG_TYPE_TEXT:
                    # Pour le texte, nous préfixons avec un octet de type + 2 octets pour la longueur du message texte
                    text_len = len(data_to_send)
                    if text_len > 65535: # Max unsigned short
                        self.client_message_queue.put("Erreur: Message texte trop long pour le protocole (>65535 octets).")
                        return
                    header = struct.pack("!BH", MSG_TYPE_TEXT, text_len)
                    self.client_socket_tcp.sendall(header + data_to_send)
                    self.client_message_queue.put(f"Client TCP: Envoyé texte: '{data_to_send.decode()}'")
                elif msg_type == MSG_TYPE_FILE:
                    self.client_socket_tcp.sendall(data_to_send) # data_to_send contient déjà l'entête du fichier
                    self.client_message_queue.put(f"Client TCP: Envoi du fichier '{file_name}' ({len(data_to_send)} octets, incluant l'entête).")
                
                # Attendre une réponse du serveur
                response_data = self.client_socket_tcp.recv(1024)
                if response_data:
                    response_message = response_data.decode('utf-8')
                    self.client_message_queue.put(f"Client TCP: Reçu du serveur: '{response_message}'")
                else:
                    self.client_message_queue.put("Client TCP: Serveur a fermé la connexion.")
                    self.client_socket_tcp.close()
                    self.client_socket_tcp = None

            except Exception as e:
                self.client_message_queue.put(f"Client TCP: Erreur d'envoi ou de réception: {e}")
                if self.client_socket_tcp:
                    self.client_socket_tcp.close()
                    self.client_socket_tcp = None


    def _send_udp_data_with_header(self, ip, port, data_to_send, msg_type, file_name=None):
        """Logique d'envoi de données via UDP (texte ou fichier)."""
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5.0) # Timeout pour la réponse
            
            if msg_type == MSG_TYPE_TEXT:
                # Pour UDP texte, nous préfixons avec un octet de type
                header = struct.pack("!B", MSG_TYPE_TEXT)
                packet = header + data_to_send
                self.client_message_queue.put(f"Client UDP: Envoi texte à {ip}:{port}: '{data_to_send.decode()}'")
            elif msg_type == MSG_TYPE_FILE:
                packet = data_to_send # data_to_send contient déjà l'entête du fichier
                self.client_message_queue.put(f"Client UDP: Envoi fichier '{file_name}' à {ip}:{port} ({len(packet)} octets, incluant l'entête).")
            
            if len(packet) > 65507: # Taille max d'un datagramme UDP (65535 - 28 octets d'entêtes IP/UDP)
                self.client_message_queue.put(f"ATTENTION UDP: Le paquet est trop grand ({len(packet)} octets) et pourrait être fragmenté ou perdu.")
                self.client_message_queue.put("Les fichiers volumineux ne sont pas fiables avec UDP simple.")
                
            sock.sendto(packet, (ip, port))

            # Attendre une réponse du serveur UDP
            response_data, addr_resp = sock.recvfrom(1024)
            response_message = response_data.decode('utf-8')
            self.client_message_queue.put(f"Client UDP: Reçu de {addr_resp}: '{response_message}'")

        except socket.timeout:
            self.client_message_queue.put(f"Client UDP: Pas de réponse du serveur à {ip}:{port} (timeout).")
        except Exception as e:
            self.client_message_queue.put(f"Client UDP: Erreur lors de l'envoi/réception: {e}")
        finally:
            if sock:
                sock.close()


if __name__ == "__main__":
    # Assurez-vous que le dossier de réception existe
    if not os.path.exists("received_files"):
        os.makedirs("received_files")
    
    app = NetApp()
    app.mainloop()