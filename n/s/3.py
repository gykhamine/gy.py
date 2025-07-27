import customtkinter
import threading
import socket
import queue
import os
import struct
from tkinter import filedialog
from datetime import datetime # Pour l'estampille temporelle

# Constants for our file transfer protocol
MSG_TYPE_TEXT = 1
MSG_TYPE_FILE = 2
FILE_HEADER_FORMAT = "!BHL"
FILE_HEADER_SIZE = struct.calcsize(FILE_HEADER_FORMAT)
TCP_CHUNK_SIZE = 4096

class NetApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Network Application (Server, Client & Files)")
        self.geometry("1000x800") # Increased height for chat area

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1) # Main grid row for frames

        # --- Server Frame ---
        self.server_frame = customtkinter.CTkFrame(self)
        self.server_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.server_frame.grid_columnconfigure(1, weight=1)
        self.server_frame.grid_rowconfigure(6, weight=1) # Log text area

        self.server_label = customtkinter.CTkLabel(self.server_frame, text="--- Server ---", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.server_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.server_ip_label = customtkinter.CTkLabel(self.server_frame, text="Server IP:")
        self.server_ip_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.server_ip_entry = customtkinter.CTkEntry(self.server_frame)
        self.server_ip_entry.insert(0, "127.0.0.1")
        self.server_ip_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.server_port_label = customtkinter.CTkLabel(self.server_frame, text="Server Port:")
        self.server_port_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.server_port_entry = customtkinter.CTkEntry(self.server_frame)
        self.server_port_entry.insert(0, "12345")
        self.server_port_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.server_protocol_label = customtkinter.CTkLabel(self.server_frame, text="Protocol:")
        self.server_protocol_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.server_protocol_optionmenu = customtkinter.CTkOptionMenu(self.server_frame, values=["TCP", "UDP"])
        self.server_protocol_optionmenu.set("TCP")
        self.server_protocol_optionmenu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.start_server_button = customtkinter.CTkButton(self.server_frame, text="Start Server", command=self.start_server)
        self.start_server_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.stop_server_button = customtkinter.CTkButton(self.server_frame, text="Stop Server", command=self.stop_server, state="disabled")
        self.stop_server_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Server Log (for system messages, not chat)
        self.server_log_text = customtkinter.CTkTextbox(self.server_frame, height=150)
        self.server_log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # --- Client Frame ---
        self.client_frame = customtkinter.CTkFrame(self)
        self.client_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.client_frame.grid_columnconfigure(1, weight=1)
        self.client_frame.grid_rowconfigure(9, weight=1) # Chat display area

        self.client_label = customtkinter.CTkLabel(self.client_frame, text="--- Client ---", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.client_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.target_ip_label = customtkinter.CTkLabel(self.client_frame, text="Target IP:")
        self.target_ip_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.target_ip_entry = customtkinter.CTkEntry(self.client_frame)
        self.target_ip_entry.insert(0, "127.0.0.1")
        self.target_ip_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.target_port_label = customtkinter.CTkLabel(self.client_frame, text="Target Port:")
        self.target_port_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.target_port_entry = customtkinter.CTkEntry(self.client_frame)
        self.target_port_entry.insert(0, "12345")
        self.target_port_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.client_protocol_label = customtkinter.CTkLabel(self.client_frame, text="Protocol:")
        self.client_protocol_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.client_protocol_optionmenu = customtkinter.CTkOptionMenu(self.client_frame, values=["TCP", "UDP"], command=self.on_client_protocol_change)
        self.client_protocol_optionmenu.set("TCP")
        self.client_protocol_optionmenu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # --- Chat Display Area ---
        self.chat_display_frame = customtkinter.CTkScrollableFrame(self.client_frame, label_text="Conversation")
        self.chat_display_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.chat_display_frame.grid_columnconfigure(0, weight=1) # Allows messages to expand

        # --- Message Input Area ---
        self.message_input_frame = customtkinter.CTkFrame(self.client_frame)
        self.message_input_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.message_input_frame.grid_columnconfigure(0, weight=1)

        self.message_to_send_entry = customtkinter.CTkEntry(self.message_input_frame, placeholder_text="Type your message here...")
        self.message_to_send_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.send_text_button = customtkinter.CTkButton(self.message_input_frame, text="Send Text", command=self.send_text_message_client)
        self.send_text_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # --- File Transfer Controls ---
        self.file_transfer_frame = customtkinter.CTkFrame(self.client_frame)
        self.file_transfer_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.file_transfer_frame.grid_columnconfigure(1, weight=1)

        self.file_path_label = customtkinter.CTkLabel(self.file_transfer_frame, text="File to Send:")
        self.file_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.file_path_entry = customtkinter.CTkEntry(self.file_transfer_frame)
        self.file_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.browse_file_button = customtkinter.CTkButton(self.file_transfer_frame, text="Browse...", command=self.browse_file)
        self.browse_file_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.send_file_button = customtkinter.CTkButton(self.file_transfer_frame, text="Send File", command=self.send_file_message_client)
        self.send_file_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Client Log (for system messages, not chat)
        self.client_log_text = customtkinter.CTkTextbox(self.client_frame, height=100)
        self.client_log_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


        # --- State Variables ---
        # Server
        self.server_thread = None
        self.server_running = threading.Event()
        self.server_message_queue = queue.Queue() # For server system logs

        # Client
        self.client_socket_tcp = None # Persistent TCP client socket
        self.client_message_queue = queue.Queue() # For client system logs
        self.client_socket_lock = threading.Lock() # Protects access to client_socket_tcp

        # Chat Message Queue (for messages to display in the chat bubble area)
        self.chat_message_queue = queue.Queue()

        # Start periodic checks for message queues (GUI updates from other threads)
        self.after(100, self.check_server_message_queue)
        self.after(100, self.check_client_message_queue)
        self.after(100, self.check_chat_message_queue) # New for chat bubbles

        self.on_client_protocol_change(self.client_protocol_optionmenu.get())

    def on_client_protocol_change(self, choice):
        """Adjusts client behavior based on selected protocol."""
        if choice == "TCP":
            if self.client_socket_tcp:
                self.log_client_message("Existing TCP connection can be used to send text/file.")
            else:
                self.log_client_message("No active TCP connection. Sending text/file will attempt to connect.")
        elif choice == "UDP":
            with self.client_socket_lock:
                if self.client_socket_tcp:
                    try:
                        self.client_socket_tcp.close()
                        self.client_socket_tcp = None
                        self.log_client_message("Client TCP connection closed as protocol changed to UDP.")
                    except Exception as e:
                        self.log_client_message(f"Error closing TCP socket: {e}")

    def log_server_message(self, message):
        """Displays a message in the server log area."""
        self.server_log_text.insert("end", message + "\n")
        self.server_log_text.see("end")

    def log_client_message(self, message):
        """Displays a message in the client log area."""
        self.client_log_text.insert("end", message + "\n")
        self.client_log_text.see("end")

    def display_chat_message(self, sender, message_content, is_self=False, is_file=False):
        """
        Displays a message in the chat area as a styled 'bubble'.
        :param sender: Name of the sender (e.g., "Moi", "Serveur").
        :param message_content: The actual message text or file info.
        :param is_self: True if the message was sent by this client (align right, different color).
        :param is_file: True if the message is about a file transfer.
        """
        timestamp = datetime.now().strftime("%H:%M")
        
        # Create a frame for the bubble
        bubble_frame = customtkinter.CTkFrame(self.chat_display_frame, corner_radius=10)
        
        # Determine colors and alignment
        if is_self:
            bubble_frame.configure(fg_color=("#D9FDD3", "#226B52")) # Light green for sent
            # Align bubble frame to the right by setting column weight
            bubble_frame.grid(row=len(self.chat_display_frame.winfo_children()), column=1, pady=2, padx=5, sticky="e")
            self.chat_display_frame.grid_columnconfigure(0, weight=1) # Push to right
            self.chat_display_frame.grid_columnconfigure(1, weight=0)
        else:
            bubble_frame.configure(fg_color=("#F0F0F0", "#333333")) # Light gray for received
            # Align bubble frame to the left
            bubble_frame.grid(row=len(self.chat_display_frame.winfo_children()), column=0, pady=2, padx=5, sticky="w")
            self.chat_display_frame.grid_columnconfigure(0, weight=0)
            self.chat_display_frame.grid_columnconfigure(1, weight=1) # Push to left

        # Add sender info and timestamp
        sender_info_label = customtkinter.CTkLabel(bubble_frame, 
                                                 text=f"{sender} - {timestamp}", 
                                                 font=customtkinter.CTkFont(size=10),
                                                 text_color="gray")
        sender_info_label.pack(anchor="nw", padx=8, pady=(5, 0))

        # Add message content label
        if is_file:
            message_label = customtkinter.CTkLabel(bubble_frame, 
                                                   text=f"Fichier: {message_content}", 
                                                   font=customtkinter.CTkFont(size=12, weight="bold"),
                                                   wraplength=300) # Wrap text
        else:
            message_label = customtkinter.CTkLabel(bubble_frame, 
                                                   text=message_content, 
                                                   font=customtkinter.CTkFont(size=12),
                                                   wraplength=300) # Wrap text

        message_label.pack(anchor="nw", padx=8, pady=(0, 5))
        
        # Auto-scroll to the bottom
        self.chat_display_frame.update_idletasks()
        self.chat_display_frame._parent_canvas.yview_moveto(1.0)


    def check_server_message_queue(self):
        """Periodically checks the server system log message queue."""
        try:
            while True:
                message = self.server_message_queue.get_nowait()
                self.log_server_message(message)
        except queue.Empty:
            pass
        self.after(100, self.check_server_message_queue)

    def check_client_message_queue(self):
        """Periodically checks the client system log message queue."""
        try:
            while True:
                message = self.client_message_queue.get_nowait()
                self.log_client_message(message)
        except queue.Empty:
            pass
        self.after(100, self.check_client_message_queue)

    def check_chat_message_queue(self):
        """Periodically checks the chat message queue for displaying in bubbles."""
        try:
            while True:
                sender, message_content, is_self, is_file = self.chat_message_queue.get_nowait()
                self.display_chat_message(sender, message_content, is_self, is_file)
        except queue.Empty:
            pass
        self.after(100, self.check_chat_message_queue)

    # --- Server Logic ---

    def start_server(self):
        """Starts the server listener in a separate thread."""
        ip = self.server_ip_entry.get()
        port = int(self.server_port_entry.get())
        server_type = self.server_protocol_optionmenu.get()

        self.server_running.set()
        if server_type == "TCP":
            self.server_thread = threading.Thread(target=self.run_tcp_server, args=(ip, port), name="TCP_Server_Listener_Thread")
        elif server_type == "UDP":
            self.server_thread = threading.Thread(target=self.run_udp_server, args=(ip, port), name="UDP_Server_Listener_Thread")
        
        self.server_thread.daemon = True
        self.server_thread.start()

        self.start_server_button.configure(state="disabled")
        self.stop_server_button.configure(state="normal")
        self.server_message_queue.put(f"Attempting to start {server_type} server on {ip}:{port}...")

    def stop_server(self):
        """Signals the server thread to stop."""
        self.server_running.clear()
        self.server_message_queue.put("Stop signal sent to server...")

        if self.server_thread and self.server_thread.is_alive():
            if self.server_thread.name == "TCP_Server_Listener_Thread":
                 try:
                     dummy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                     dummy_sock.connect((self.server_ip_entry.get(), int(self.server_port_entry.get())))
                     dummy_sock.close()
                 except socket.error:
                     pass
            
            self.server_thread.join(timeout=2)
            if self.server_thread.is_alive():
                self.server_message_queue.put("Server thread did not terminate gracefully.")
            else:
                self.server_message_queue.put("Server stopped.")
        else:
            self.server_message_queue.put("Server is not running or already stopped.")

        self.start_server_button.configure(state="normal")
        self.stop_server_button.configure(state="disabled")

    def run_tcp_server(self, ip, port):
        """TCP server listener logic."""
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((ip, port))
            sock.listen(5)
            self.server_message_queue.put(f"TCP Server listening on {ip}:{port}")
            sock.settimeout(1.0)

            while self.server_running.is_set():
                try:
                    conn, addr = sock.accept()
                    self.server_message_queue.put(f"TCP connection accepted from {addr}")
                    client_handler_thread = threading.Thread(target=self.handle_tcp_client, args=(conn, addr))
                    client_handler_thread.daemon = True
                    client_handler_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    self.server_message_queue.put(f"TCP Server Listener Error: {e}")
                    break

        except Exception as e:
            self.server_message_queue.put(f"Failed to start TCP Server: {e}")
        finally:
            if sock:
                sock.close()
                self.server_message_queue.put("TCP Server socket closed.")
            self.server_running.clear()

    def handle_tcp_client(self, conn, addr):
        """Handles a single TCP client connection."""
        try:
            with conn:
                while self.server_running.is_set():
                    msg_type_byte = conn.recv(1)
                    if not msg_type_byte:
                        self.server_message_queue.put(f"TCP Client {addr} disconnected.")
                        break

                    msg_type = struct.unpack("!B", msg_type_byte)[0]

                    if msg_type == MSG_TYPE_TEXT:
                        len_bytes = self.receive_all(conn, 2)
                        if not len_bytes: break
                        msg_len = struct.unpack("!H", len_bytes)[0]
                        
                        data = self.receive_all(conn, msg_len)
                        if not data or len(data) != msg_len:
                            self.server_message_queue.put(f"Error: Incomplete text data from {addr}")
                            break
                        
                        message_received = data.decode('utf-8')
                        self.server_message_queue.put(f"[TCP] Received text from {addr}: '{message_received}'")
                        # For the server, we might want to display this as a received message too
                        self.chat_message_queue.put(("Client " + str(addr), message_received, False, False)) # Sender, Content, is_self, is_file
                        response = f"Serveur TCP a reçu texte: '{message_received}'".encode('utf-8')
                        conn.sendall(response)

                    elif msg_type == MSG_TYPE_FILE:
                        file_header_rest = self.receive_all(conn, FILE_HEADER_SIZE - 1)
                        if not file_header_rest or len(file_header_rest) != (FILE_HEADER_SIZE - 1):
                            self.server_message_queue.put(f"Error: Incomplete file header from {addr}")
                            break
                        
                        file_name_len, file_size = struct.unpack("!HL", file_header_rest)

                        file_name_bytes = self.receive_all(conn, file_name_len)
                        if not file_name_bytes or len(file_name_bytes) != file_name_len:
                            self.server_message_queue.put(f"Error: Incomplete filename from {addr}")
                            break
                        file_name = file_name_bytes.decode('utf-8')

                        self.server_message_queue.put(f"[TCP] Receiving file '{file_name}' ({file_size} bytes) from {addr}...")
                        self.chat_message_queue.put(("Client " + str(addr), file_name, False, True))

                        received_bytes = 0
                        output_filepath = os.path.join("received_files", os.path.basename(file_name))
                        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

                        try:
                            with open(output_filepath, 'wb') as f:
                                while received_bytes < file_size:
                                    chunk_size = min(file_size - received_bytes, TCP_CHUNK_SIZE)
                                    chunk = conn.recv(chunk_size)
                                    if not chunk:
                                        self.server_message_queue.put(f"Error: Connection interrupted while receiving '{file_name}' from {addr}")
                                        break
                                    f.write(chunk)
                                    received_bytes += len(chunk)
                            
                            if received_bytes == file_size:
                                self.server_message_queue.put(f"[TCP] File '{file_name}' received and saved to '{output_filepath}'.")
                                conn.sendall(b"File received successfully.")
                            else:
                                self.server_message_queue.put(f"Error: Incomplete file '{file_name}' from {addr}. Received {received_bytes}/{file_size} bytes.")
                                conn.sendall(b"Error: Incomplete file received.")
                        except Exception as file_e:
                            self.server_message_queue.put(f"Error saving file '{file_name}': {file_e}")
                            conn.sendall(b"Server error during file reception.")
                        break

                    else:
                        self.server_message_queue.put(f"Unknown message type ({msg_type}) from {addr}")
                        conn.recv(4096)
                        break

        except Exception as e:
            self.server_message_queue.put(f"Error handling TCP client {addr}: {e}")
        finally:
            self.server_message_queue.put(f"TCP client handler for {addr} terminated.")

    def receive_all(self, sock, n_bytes):
        """Helper to ensure all n_bytes are received from a TCP socket."""
        data = b''
        while len(data) < n_bytes:
            packet = sock.recv(n_bytes - len(data))
            if not packet:
                return None
            data += packet
        return data

    def run_udp_server(self, ip, port):
        """UDP server listener logic."""
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((ip, port))
            self.server_message_queue.put(f"UDP Server listening on {ip}:{port}")
            sock.settimeout(1.0)

            while self.server_running.is_set():
                try:
                    data, addr = sock.recvfrom(65535)
                    
                    if len(data) < 1:
                        self.server_message_queue.put(f"UDP: Empty or too short data from {addr}.")
                        continue

                    msg_type = struct.unpack("!B", data[0:1])[0]
                    payload = data[1:]

                    if msg_type == MSG_TYPE_TEXT:
                        message_received = payload.decode('utf-8')
                        self.server_message_queue.put(f"[UDP] Received text from {addr}: '{message_received}'")
                        self.chat_message_queue.put(("Client " + str(addr), message_received, False, False))
                        response = f"Serveur UDP a reçu texte: '{message_received}'".encode('utf-8')
                        sock.sendto(response, addr)

                    elif msg_type == MSG_TYPE_FILE:
                        if len(payload) < (FILE_HEADER_SIZE -1):
                            self.server_message_queue.put(f"UDP: Incomplete file header from {addr}.")
                            continue
                        
                        file_header_rest = payload[0:(FILE_HEADER_SIZE - 1)]
                        file_name_len, file_size = struct.unpack("!HL", file_header_rest)
                        
                        file_name_start_index = (FILE_HEADER_SIZE - 1)
                        file_content_start_index = file_name_start_index + file_name_len

                        if len(payload) < file_content_start_index:
                             self.server_message_queue.put(f"UDP: Incomplete or missing filename from {addr}.")
                             continue

                        file_name_bytes = payload[file_name_start_index:file_content_start_index]
                        file_name = file_name_bytes.decode('utf-8')
                        
                        file_content = payload[file_content_start_index:]

                        if len(file_content) != file_size:
                            self.server_message_queue.put(f"WARNING: UDP file '{file_name}' from {addr} received incomplete! Expected {file_size}, got {len(file_content)} bytes.")
                        
                        self.server_message_queue.put(f"[UDP] Received file '{file_name}' ({len(file_content)}/{file_size} bytes) from {addr}...")
                        self.chat_message_queue.put(("Client " + str(addr), file_name, False, True))
                        
                        output_filepath = os.path.join("received_files", os.path.basename(file_name))
                        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

                        try:
                            with open(output_filepath, 'wb') as f:
                                f.write(file_content)
                            self.server_message_queue.put(f"[UDP] File '{file_name}' received and saved to '{output_filepath}'.")
                            sock.sendto(b"File received successfully (UDP).", addr)
                        except Exception as file_e:
                            self.server_message_queue.put(f"Error saving file '{file_name}' (UDP): {file_e}")
                            sock.sendto(b"UDP server error.", addr)

                    else:
                        self.server_message_queue.put(f"Unknown UDP message type ({msg_type}) from {addr}")

                except socket.timeout:
                    continue
                except Exception as e:
                    self.server_message_queue.put(f"UDP Server Error: {e}")
                    break

        except Exception as e:
            self.server_message_queue.put(f"Failed to start UDP Server: {e}")
        finally:
            if sock:
                sock.close()
                self.server_message_queue.put("UDP Server socket closed.")
            self.server_running.clear()

    # --- Client Logic ---

    def browse_file(self):
        """Opens a file dialog for selecting a file to send."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_entry.delete(0, customtkinter.END)
            self.file_path_entry.insert(0, file_path)
            self.log_client_message(f"File selected: {file_path}")

    def send_text_message_client(self):
        """Initiates sending a text message from the client."""
        message = self.message_to_send_entry.get()
        if not message.strip():
            self.log_client_message("Cannot send empty message.")
            return

        target_ip = self.target_ip_entry.get()
        target_port = int(self.target_port_entry.get())
        client_type = self.client_protocol_optionmenu.get()

        # Display the message locally first
        self.chat_message_queue.put(("Moi", message, True, False)) # Sender, Content, is_self, is_file
        self.message_to_send_entry.delete(0, customtkinter.END) # Clear input field

        if client_type == "TCP":
            thread_args = (target_ip, target_port, message.encode('utf-8'), MSG_TYPE_TEXT)
            threading.Thread(target=self._send_tcp_data_with_header, args=thread_args, daemon=True, name="TCP_Client_Send_Text_Thread").start()
        elif client_type == "UDP":
            thread_args = (target_ip, target_port, message.encode('utf-8'), MSG_TYPE_TEXT)
            threading.Thread(target=self._send_udp_data_with_header, args=thread_args, daemon=True, name="UDP_Client_Send_Text_Thread").start()

    def send_file_message_client(self):
        """Initiates sending a file from the client."""
        file_path = self.file_path_entry.get()
        if not os.path.exists(file_path):
            self.log_client_message("Error: The specified file does not exist.")
            return

        target_ip = self.target_ip_entry.get()
        target_port = int(self.target_port_entry.get())
        client_type = self.client_protocol_optionmenu.get()

        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            file_name = os.path.basename(file_path)
            
            self.chat_message_queue.put(("Moi", file_name, True, True)) # Display file info locally
            
            file_name_bytes = file_name.encode('utf-8')
            if len(file_name_bytes) > 65535:
                self.log_client_message("Error: Filename too long.")
                return
            if len(file_content) > 0xFFFFFFFF:
                 self.client_message_queue.put("Error: File too large for current protocol (>4GB).")
                 return

            file_header = struct.pack(FILE_HEADER_FORMAT, MSG_TYPE_FILE, len(file_name_bytes), len(file_content))
            data_to_send = file_header + file_name_bytes + file_content

            if client_type == "TCP":
                thread_args = (target_ip, target_port, data_to_send, MSG_TYPE_FILE, file_name)
                threading.Thread(target=self._send_tcp_data_with_header, args=thread_args, daemon=True, name="TCP_Client_Send_File_Thread").start()
            elif client_type == "UDP":
                thread_args = (target_ip, target_port, data_to_send, MSG_TYPE_FILE, file_name)
                threading.Thread(target=self._send_udp_data_with_header, args=thread_args, daemon=True, name="UDP_Client_Send_File_Thread").start()

        except Exception as e:
            self.log_client_message(f"Error preparing file: {e}")


    def _send_tcp_data_with_header(self, ip, port, data_to_send, msg_type, file_name=None):
        """Handles sending data via TCP (text or file) including connection management."""
        with self.client_socket_lock:
            if self.client_socket_tcp is None:
                try:
                    self.client_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket_tcp.settimeout(10.0)
                    self.client_message_queue.put(f"Client TCP: Attempting to connect to {ip}:{port}...")
                    self.client_socket_tcp.connect((ip, port))
                    self.client_message_queue.put(f"Client TCP: Connected to {ip}:{port}")
                except socket.timeout:
                    self.client_message_queue.put(f"Client TCP: Connection failed (timeout) to {ip}:{port}")
                    self.client_socket_tcp = None
                    return
                except Exception as e:
                    self.client_message_queue.put(f"Client TCP: Connection error: {e}")
                    self.client_socket_tcp = None
                    return
            
            try:
                if msg_type == MSG_TYPE_TEXT:
                    text_len = len(data_to_send)
                    if text_len > 65535:
                        self.client_message_queue.put("Error: Text message too long for protocol (>65535 bytes).")
                        return
                    header = struct.pack("!BH", MSG_TYPE_TEXT, text_len)
                    self.client_socket_tcp.sendall(header + data_to_send)
                    # self.client_message_queue.put(f"Client TCP: Sent text: '{data_to_send.decode()}'") # Now displayed in chat bubble
                elif msg_type == MSG_TYPE_FILE:
                    self.client_socket_tcp.sendall(data_to_send)
                    # self.client_message_queue.put(f"Client TCP: Sending file '{file_name}' ({len(data_to_send)} bytes, including header).") # Now displayed in chat bubble
                
                response_data = self.client_socket_tcp.recv(1024)
                if response_data:
                    response_message = response_data.decode('utf-8')
                    self.client_message_queue.put(f"Client TCP: Received response: '{response_message}'")
                else:
                    self.client_message_queue.put("Client TCP: Server closed the connection.")
                    self.client_socket_tcp.close()
                    self.client_socket_tcp = None

            except Exception as e:
                self.client_message_queue.put(f"Client TCP: Send/Receive Error: {e}")
                if self.client_socket_tcp:
                    self.client_socket_tcp.close()
                    self.client_socket_tcp = None


    def _send_udp_data_with_header(self, ip, port, data_to_send, msg_type, file_name=None):
        """Handles sending data via UDP (text or file)."""
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5.0)
            
            if msg_type == MSG_TYPE_TEXT:
                header = struct.pack("!B", MSG_TYPE_TEXT)
                packet = header + data_to_send
                # self.client_message_queue.put(f"Client UDP: Sending text to {ip}:{port}: '{data_to_send.decode()}'") # Now displayed in chat bubble
            elif msg_type == MSG_TYPE_FILE:
                packet = data_to_send
                # self.client_message_queue.put(f"Client UDP: Sending file '{file_name}' to {ip}:{port} ({len(packet)} octets, incluant l'entête).") # Now displayed in chat bubble
            
            if len(packet) > 65507:
                self.client_message_queue.put(f"WARNING UDP: Packet is too large ({len(packet)} bytes) and might be fragmented or lost.")
                self.client_message_queue.put("Large files are not reliable with simple UDP.")
                
            sock.sendto(packet, (ip, port))

            response_data, addr_resp = sock.recvfrom(1024)
            response_message = response_data.decode('utf-8')
            self.client_message_queue.put(f"Client UDP: Received from {addr_resp}: '{response_message}'")

        except socket.timeout:
            self.client_message_queue.put(f"Client UDP: No response from server at {ip}:{port} (timeout).")
        except Exception as e:
            self.client_message_queue.put(f"Client UDP: Send/Receive Error: {e}")
        finally:
            if sock:
                sock.close()


if __name__ == "__main__":
    if not os.path.exists("received_files"):
        os.makedirs("received_files")
    
    app = NetApp()
    app.mainloop()