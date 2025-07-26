import customtkinter as ctk
import threading
import time
import psutil
import os
import sys
import subprocess
from datetime import datetime

# Make sure CTkMessagebox is available. Install it with: pip install CTkMessagebox
try:
    from CTkMessagebox import CTkMessagebox
except ImportError:
    print("CTkMessagebox not found. Please install it: pip install CTkMessagebox")
    print("Falling back to standard tkinter messagebox for alerts (less pretty).")
    from tkinter import messagebox as CTkMessagebox # Fallback for CTkMessagebox

# --- ptrace related imports (add these) ---
try:
    PtraceDebugger = None # Set to None to disable ptrace features
except ImportError:
    PtraceDebugger = None
    print("python-ptrace not found. Syscall tracing via ptrace will be disabled.")


class ProcessMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Moniteur de Processus Avancé")
        self.geometry("1400x900") 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.monitoring_active = False
        self.process_refresh_thread = None
        self.selected_pid = None
        self.selected_process_obj = None
        self.syscall_thread = None 
        self.debugger = None 

        # Store previous network counters for speed calculation
        self.last_net_io_counters = psutil.net_io_counters()
        self.last_net_time = time.time()
        
        # Store structured network data instead of raw lines
        self.structured_network_data = {
            'global_stats': {},
            'interfaces': [],
            'connections': []
        }

        # --- Control Frame ---
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.status_label = ctk.CTkLabel(self.control_frame, text="Statut: Arrêté", text_color="red", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.toggle_button = ctk.CTkButton(self.control_frame,
                                           text="Démarrer le Moniteur",
                                           command=self.toggle_monitoring,
                                           font=ctk.CTkFont(size=14, weight="bold"),
                                           height=40)
        self.toggle_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.refresh_button = ctk.CTkButton(self.control_frame,
                                            text="Rafraîchir Maintenant",
                                            command=self.update_process_list_display,
                                            font=ctk.CTkFont(size=14),
                                            height=40)
        self.refresh_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        # --- Selected Process Info & Actions Frame ---
        self.selected_process_actions_frame = ctk.CTkFrame(self)
        self.selected_process_actions_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.selected_process_actions_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.selected_pid_label = ctk.CTkLabel(self.selected_process_actions_frame, text="PID sélectionné: Aucun", font=ctk.CTkFont(size=14, weight="bold"))
        self.selected_pid_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.selected_name_label = ctk.CTkLabel(self.selected_process_actions_frame, text="Nom: N/A", font=ctk.CTkFont(size=14, weight="bold"))
        self.selected_name_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.kill_button = ctk.CTkButton(self.selected_process_actions_frame,
                                         text="Tuer Processus",
                                         command=self.kill_selected_process,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         fg_color="red",
                                         hover_color="#CC0000",
                                         height=40,
                                         state="disabled")
        self.kill_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        
        self.trace_syscalls_button = ctk.CTkButton(self.selected_process_actions_frame,
                                                    text="Tracer Appels Système (Désactivé)", 
                                                    command=self.start_syscall_tracing, 
                                                    font=ctk.CTkFont(size=14, weight="bold"),
                                                    fg_color="gray", 
                                                    hover_color="gray",
                                                    height=40,
                                                    state="disabled") 
        self.trace_syscalls_button.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        self.disassemble_exe_button = ctk.CTkButton(self.selected_process_actions_frame,
                                            text="Désassembler l'Exécutable",
                                            command=self.disassemble_executable,
                                            font=ctk.CTkFont(size=14),
                                            fg_color="purple",
                                            hover_color="#800080",
                                            height=40,
                                            state="disabled")
        self.disassemble_exe_button.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

        # --- Main Content Area: Tabbed Views ---
        self.main_content_frame = ctk.CTkFrame(self)
        self.main_content_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(0, weight=1)

        self.tab_view = ctk.CTkTabview(self.main_content_frame)
        self.tab_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.tab_view.add("Liste des Processus")
        self.tab_view.add("Détails du Processus")
        self.tab_view.add("Appels Système (Désactivé)") 
        self.tab_view.add("Désassemblage Executable")
        self.tab_view.add("Activité Réseau") 

        # --- Tab 1: Process List Display ---
        self.process_list_textbox = ctk.CTkTextbox(self.tab_view.tab("Liste des Processus"), wrap="none", font=ctk.CTkFont(family="Consolas", size=12))
        self.process_list_textbox.pack(fill="both", expand=True)
        self.process_list_textbox.bind("<Button-1>", self.on_process_list_click)

        # --- Tab 2: Detailed Process Information ---
        self.details_textbox = ctk.CTkTextbox(self.tab_view.tab("Détails du Processus"), wrap="word", font=ctk.CTkFont(family="Consolas", size=12))
        self.details_textbox.pack(fill="both", expand=True)
        self.details_textbox.insert(ctk.END, "Sélectionnez un processus dans la liste pour voir les détails ici.")

        # --- Tab 3: System Call Trace Output (Now disabled) ---
        self.syscall_output_textbox = ctk.CTkTextbox(self.tab_view.tab("Appels Système (Désactivé)"), wrap="none", font=ctk.CTkFont(family="Consolas", size=12))
        self.syscall_output_textbox.pack(fill="both", expand=True)
        self.syscall_output_textbox.insert(ctk.END, "Le traçage des appels système est désactivé car il nécessite des outils externes (strace) ou des bibliothèques complexes (python-ptrace) qui ne sont pas inclus dans cette version.\n")
        
        self.stop_syscall_button = ctk.CTkButton(self.tab_view.tab("Appels Système (Désactivé)"),
                                                 text="Arrêter le Traçage",
                                                 command=self.stop_syscall_tracing,
                                                 fg_color="gray",
                                                 hover_color="gray",
                                                 state="disabled")
        self.stop_syscall_button.pack(pady=5)

        # --- Tab 4: Disassembly Output ---
        self.disassembly_textbox = ctk.CTkTextbox(self.tab_view.tab("Désassemblage Executable"), wrap="none", font=ctk.CTkFont(family="Consolas", size=12))
        self.disassembly_textbox.pack(fill="both", expand=True)
        self.disassembly_textbox.insert(ctk.END, "Le désassemblage de l'exécutable du processus sélectionné apparaîtra ici.\n")
        self.disassembly_textbox.insert(ctk.END, "Assurez-vous que 'objdump' est installé sur votre système (e.g., sudo apt install binutils).\n")
        self.disassembly_textbox.configure(state="disabled")

        # --- Tab 5: Network Activity Output (with advanced Filters) ---
        self.network_activity_tab_frame = ctk.CTkFrame(self.tab_view.tab("Activité Réseau"))
        self.network_activity_tab_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.network_activity_tab_frame.grid_columnconfigure(0, weight=1)
        self.network_activity_tab_frame.grid_columnconfigure(1, weight=1)
        self.network_activity_tab_frame.grid_rowconfigure(5, weight=1) # Row for textbox

        # Filter Checkboxes
        self.filter_global_var = ctk.BooleanVar(value=True)
        self.filter_interfaces_var = ctk.BooleanVar(value=True)
        self.filter_connections_var = ctk.BooleanVar(value=True)

        self.filter_global_cb = ctk.CTkCheckBox(self.network_activity_tab_frame, text="Statistiques Globales", variable=self.filter_global_var, command=self.apply_network_filter)
        self.filter_global_cb.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        self.filter_interfaces_cb = ctk.CTkCheckBox(self.network_activity_tab_frame, text="Statistiques par Interface", variable=self.filter_interfaces_var, command=self.apply_network_filter)
        self.filter_interfaces_cb.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        self.filter_connections_cb = ctk.CTkCheckBox(self.network_activity_tab_frame, text="Connexions de Processus", variable=self.filter_connections_var, command=self.apply_network_filter)
        self.filter_connections_cb.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        # Specific Filter Inputs
        self.ip_filter_label = ctk.CTkLabel(self.network_activity_tab_frame, text="IP/Adresse:")
        self.ip_filter_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.filter_ip_entry = ctk.CTkEntry(self.network_activity_tab_frame, placeholder_text="192.168.1.1", font=ctk.CTkFont(size=12))
        self.filter_ip_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        self.filter_ip_entry.bind("<Return>", self.apply_network_filter)

        self.port_filter_label = ctk.CTkLabel(self.network_activity_tab_frame, text="Port:")
        self.port_filter_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.filter_port_entry = ctk.CTkEntry(self.network_activity_tab_frame, placeholder_text="80, 443, 22", font=ctk.CTkFont(size=12))
        self.filter_port_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        self.filter_port_entry.bind("<Return>", self.apply_network_filter)

        self.protocol_filter_label = ctk.CTkLabel(self.network_activity_tab_frame, text="Protocole:")
        self.protocol_filter_label.grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.filter_protocol_entry = ctk.CTkEntry(self.network_activity_tab_frame, placeholder_text="tcp, udp", font=ctk.CTkFont(size=12))
        self.filter_protocol_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=2)
        self.filter_protocol_entry.bind("<Return>", self.apply_network_filter)

        self.general_keyword_label = ctk.CTkLabel(self.network_activity_tab_frame, text="Mot-clé Général:")
        self.general_keyword_label.grid(row=5, column=0, sticky="w", padx=5, pady=2) # Moved to 5 to make space for textbox
        self.filter_keyword_entry = ctk.CTkEntry(self.network_activity_tab_frame, placeholder_text="any text", font=ctk.CTkFont(size=12))
        self.filter_keyword_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=2)
        self.filter_keyword_entry.bind("<Return>", self.apply_network_filter)

        self.apply_filter_button = ctk.CTkButton(self.network_activity_tab_frame, text="Appliquer Filtres", command=self.apply_network_filter, font=ctk.CTkFont(size=12, weight="bold"))
        self.apply_filter_button.grid(row=6, column=0, columnspan=2, pady=5) # Below all filter options

        # Network Activity Textbox
        self.network_activity_textbox = ctk.CTkTextbox(self.network_activity_tab_frame, wrap="word", font=ctk.CTkFont(family="Consolas", size=12))
        self.network_activity_textbox.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5) # New row for textbox
        self.network_activity_textbox.insert(ctk.END, "Statistiques réseau et connexions apparaîtront ici.")
        self.network_activity_textbox.configure(state="disabled") 
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.process_list_textbox.insert(ctk.END, "Cliquez sur 'Démarrer le Moniteur' pour commencer à lister les processus...")

    def toggle_monitoring(self):
        if not self.monitoring_active:
            self.start_monitoring()
            self.toggle_button.configure(text="Arrêter le Moniteur", fg_color="red")
            self.status_label.configure(text="Statut: En cours d'exécution", text_color="green")
            self.kill_button.configure(state="normal")
            self.disassemble_exe_button.configure(state="normal")
            self.trace_syscalls_button.configure(state="disabled") 
            self.update_process_list_display()
            print("Moniteur de processus démarré.")
        else:
            self.stop_monitoring()
            self.toggle_button.configure(text="Démarrer le Moniteur", fg_color="#3B8ED0")
            self.status_label.configure(text="Statut: Arrêté", text_color="red")
            self.kill_button.configure(state="disabled")
            self.trace_syscalls_button.configure(state="disabled")
            self.disassemble_exe_button.configure(state="disabled")
            self.process_list_textbox.delete("1.0", ctk.END)
            self.process_list_textbox.insert(ctk.END, "Moniteur arrêté. Cliquez sur 'Démarrer le Moniteur' pour relancer.")
            print("Moniteur de processus arrêté.")

    def start_monitoring(self):
        self.monitoring_active = True
        self.process_refresh_thread = threading.Thread(target=self._refresh_processes_loop, daemon=True)
        self.process_refresh_thread.start()

    def stop_monitoring(self):
        self.monitoring_active = False
        if self.process_refresh_thread and self.process_refresh_thread.is_alive():
            time.sleep(0.1)
        self.stop_syscall_tracing() 
        self.reset_selected_process()

    def _refresh_processes_loop(self):
        while self.monitoring_active:
            self.after(0, self.update_process_list_display)
            if self.selected_pid:
                self.after(0, self.update_selected_process_details)
            self.after(0, self.fetch_and_store_network_data) # Fetch and store, then filtering happens
            time.sleep(1)

    def update_process_list_display(self):
        self.process_list_textbox.delete("1.0", ctk.END)
        
        header = f"{'PID':<8} {'Status':<10} {'CPU%':<8} {'Mem (MB)':<12} {'Nom':<30} {'Utilisateur':<20}\n"
        self.process_list_textbox.insert(ctk.END, header)
        self.process_list_textbox.insert(ctk.END, "-" * 100 + "\n")

        processes = []
        for p in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info', 'username']):
            try:
                cpu_percent = p.cpu_percent(interval=None)
                mem_info = p.memory_info()
                mem_usage_mb = mem_info.rss / (1024 * 1024)

                processes.append({
                    'pid': p.pid,
                    'name': p.name(),
                    'status': p.status(),
                    'cpu_percent': cpu_percent,
                    'mem_usage_mb': mem_usage_mb,
                    'username': p.username()
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception as e:
                print(f"Erreur lors de la récupération des infos processus: {e} pour PID {p.pid}")
                continue
        
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

        for proc in processes:
            line = f"{proc['pid']:<8} {proc['status']:<10} {proc['cpu_percent']:<8.1f} {proc['mem_usage_mb']:<12.1f} {proc['name']:<30} {proc['username']:<20}\n"
            self.process_list_textbox.insert(ctk.END, line)
            
        self.process_list_textbox.yview_moveto(0)

    def on_process_list_click(self, event):
        try:
            index = self.process_list_textbox.index(f"@{event.x},{event.y}")
            line_num = int(index.split('.')[0])

            if line_num <= 2:
                self.reset_selected_process()
                return

            line_content = self.process_list_textbox.get(f"{line_num}.0", f"{line_num}.end")
            pid_str = line_content[0:8].strip()
            new_selected_pid = int(pid_str)
            
            if new_selected_pid == self.selected_pid:
                return

            self.selected_pid = new_selected_pid
            
            try:
                self.selected_process_obj = psutil.Process(self.selected_pid)
                process_name = self.selected_process_obj.name()
                self.selected_pid_label.configure(text=f"PID sélectionné: {self.selected_pid}")
                self.selected_name_label.configure(text=f"Nom: {process_name}")
                self.kill_button.configure(state="normal")
                self.trace_syscalls_button.configure(state="disabled") 
                self.disassemble_exe_button.configure(state="normal")

                self.process_list_textbox.tag_remove("highlight", "1.0", ctk.END)
                self.process_list_textbox.tag_add("highlight", f"{line_num}.0", f"{line_num}.end")
                self.process_list_textbox.tag_config("highlight", background="#3B8ED0", foreground="white")

                self.update_selected_process_details()
                self.tab_view.set("Détails du Processus")
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.reset_selected_process()
                CTkMessagebox.show_warning("Processus Introuvable", f"Le processus (PID: {new_selected_pid}) n'existe plus ou l'accès est refusé.")

        except (ValueError, IndexError):
            self.reset_selected_process()
            print("Clic hors d'un processus valide ou erreur d'extraction.")

    def reset_selected_process(self):
        self.selected_pid = None
        self.selected_process_obj = None
        self.selected_pid_label.configure(text="PID sélectionné: Aucun")
        self.selected_name_label.configure(text="Nom: N/A")
        self.kill_button.configure(state="disabled")
        self.trace_syscalls_button.configure(state="disabled")
        self.disassemble_exe_button.configure(state="disabled")
        self.process_list_textbox.tag_remove("highlight", "1.0", ctk.END)
        self.details_textbox.delete("1.0", ctk.END)
        self.details_textbox.insert(ctk.END, "Sélectionnez un processus dans la liste pour voir les détails.")
        self.stop_syscall_tracing()
        self.disassembly_textbox.configure(state="normal")
        self.disassembly_textbox.delete("1.0", ctk.END)
        self.disassembly_textbox.insert(ctk.END, "Le désassemblage de l'exécutable du processus sélectionné apparaîtra ici.\n")
        self.disassembly_textbox.insert(ctk.END, "Assurez-vous que 'objdump' est installé sur votre système (e.g., sudo apt install binutils).\n")
        self.disassembly_textbox.configure(state="disabled")
        
        self.network_activity_textbox.configure(state="normal") 
        self.network_activity_textbox.delete("1.0", ctk.END)
        self.network_activity_textbox.insert(ctk.END, "Statistiques réseau et connexions apparaîtront ici.")
        self.network_activity_textbox.configure(state="disabled")
        
        # Clear filter inputs and reset checkboxes
        self.filter_ip_entry.delete(0, ctk.END)
        self.filter_port_entry.delete(0, ctk.END)
        self.filter_protocol_entry.delete(0, ctk.END)
        self.filter_keyword_entry.delete(0, ctk.END)
        self.filter_global_var.set(True)
        self.filter_interfaces_var.set(True)
        self.filter_connections_var.set(True)
        self.structured_network_data = { # Clear structured data
            'global_stats': {},
            'interfaces': [],
            'connections': []
        }

    def update_selected_process_details(self):
        """Populates the details textbox with comprehensive info for the selected process."""
        if not self.selected_process_obj:
            self.details_textbox.delete("1.0", ctk.END)
            self.details_textbox.insert(ctk.END, "Sélectionnez un processus pour voir les détails.")
            return

        self.details_textbox.delete("1.0", ctk.END)
        try:
            p = self.selected_process_obj
            details = []
            
            details.append(f"--- Informations Générales (PID: {p.pid}) ---")
            details.append(f"Nom: {p.name()}")
            details.append(f"Exécutable: {p.exe()}")
            details.append(f"Chemin de travail: {p.cwd()}")
            details.append(f"Ligne de commande: {' '.join(p.cmdline())}")
            details.append(f"Statut: {p.status()}")
            details.append(f"Utilisateur: {p.username()}")
            details.append(f"PID Parent: {p.ppid()}")
            details.append(f"Date de création: {datetime.fromtimestamp(p.create_time()).strftime('%Y-%m-%d %H:%M:%S')}")
            details.append(f"Nombre de threads: {p.num_threads()}")
            details.append(f"Nombre de descripteurs de fichiers: {p.num_fds()}")
            
            details.append(f"\n--- Utilisation des Ressources ---")
            details.append(f"CPU%: {p.cpu_percent(interval=0.1):.2f}%")
            mem_info = p.memory_info()
            details.append(f"Mémoire RSS: {mem_info.rss / (1024 * 1024):.2f} MB")
            details.append(f"Mémoire VMS: {mem_info.vms / (1024 * 1024):.2f} MB")
            details.append(f"E/S (Lu/Écrit): {p.io_counters().read_bytes / (1024*1024):.2f} MB / {p.io_counters().write_bytes / (1024*1024):.2f} MB")

            details.append(f"\n--- Fichiers Ouverts ---")
            open_files = p.open_files()
            if open_files:
                for f in open_files:
                    details.append(f"- {f.path} (Mode: {f.mode}, Fd: {f.fd})")
            else:
                details.append("Aucun fichier ouvert.")

            # Process-specific Network Connections
            details.append(f"\n--- Connexions Réseau du Processus (PID {p.pid}) ---")
            try:
                connections = p.connections(kind='inet') 
                if connections:
                    for conn in connections:
                        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                        details.append(f"- Famille: {conn.family.name}, Type: {conn.type.name}, Statut: {conn.status}, Local: {laddr}, Distant: {raddr}")
                else:
                    details.append("Aucune connexion réseau pour ce processus.")
            except psutil.AccessDenied:
                details.append("Accès refusé pour lister les connexions. Exécutez en tant qu'administrateur (sudo).")


            self.details_textbox.insert(ctk.END, "\n".join(details))

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            self.details_textbox.delete("1.0", ctk.END)
            self.details_textbox.insert(ctk.END, f"Impossible d'obtenir les détails du processus (PID: {self.selected_pid}): {e}\n"
                                                 "Il a peut-être terminé ou vous n'avez pas les permissions nécessaires.")
        except Exception as e:
            self.details_textbox.delete("1.0", ctk.END)
            self.details_textbox.insert(ctk.END, f"Une erreur inattendue est survenue lors de l'obtention des détails: {e}")

    def kill_selected_process(self):
        if self.selected_pid is None:
            return
        
        try:
            process = psutil.Process(self.selected_pid)
            process_name = process.name()
            response = CTkMessagebox.ask_yes_no(
                f"Confirmer l'arrêt du processus",
                f"Êtes-vous sûr de vouloir tuer le processus '{process_name}' (PID: {self.selected_pid})?",
                icon="warning"
            )
            
            if response == "yes":
                process.terminate()
                self.status_label.configure(text=f"Tentative d'arrêt de {self.selected_pid}...", text_color="orange")
                self.after(500, self.update_process_list_display)
                self.reset_selected_process()
            else:
                self.status_label.configure(text="Opération annulée.", text_color="grey")

        except psutil.NoSuchProcess:
            CTkMessagebox.showerror("Erreur", f"Le processus (PID: {self.selected_pid}) n'existe plus.")
            self.reset_selected_process()
        except psutil.AccessDenied:
            CTkMessagebox.showerror("Erreur", f"Accès refusé pour tuer le processus (PID: {self.selected_pid}). Exécutez en tant qu'administrateur (sudo).")
        except Exception as e:
            CTkMessagebox.showerror("Erreur Inconnue", f"Une erreur inattendue est survenue: {e}")
        finally:
            self.reset_selected_process()

    def start_syscall_tracing(self):
        CTkMessagebox.show_error("Fonctionnalité Désactivée", 
                                 "Le traçage des appels système (via strace ou ptrace) n'est pas activé dans cette version du moniteur.")
        self.stop_syscall_button.configure(state="disabled")


    def stop_syscall_tracing(self):
        if self.debugger: 
            try:
                self.debugger.quit()
            except Exception as e:
                print(f"Error quitting debugger: {e}")
            self.debugger = None
        if self.syscall_thread and self.syscall_thread.is_alive():
            pass 
        
        self.syscall_output_textbox.configure(state="normal")
        self.syscall_output_textbox.delete("1.0", ctk.END)
        self.syscall_output_textbox.insert(ctk.END, "Le traçage des appels système est désactivé.\n")
        self.syscall_output_textbox.configure(state="disabled")
        self.stop_syscall_button.configure(state="disabled")


    def disassemble_executable(self):
        if not self.selected_process_obj:
            CTkMessagebox.show_warning("Aucun Processus Sélectionné", "Veuillez sélectionner un processus pour désassembler son exécutable.")
            return

        if sys.platform != "linux":
            CTkMessagebox.show_error("Plateforme Non Supportée", "La désassemblage d'exécutables avec 'objdump' n'est disponible que sous Linux.")
            return

        try:
            exe_path = self.selected_process_obj.exe()
            if not exe_path or not os.path.exists(exe_path):
                CTkMessagebox.showerror("Exécutable Introuvable", f"Impossible de trouver l'exécutable pour PID {self.selected_pid} : {exe_path}")
                return

            self.disassembly_textbox.configure(state="normal")
            self.disassembly_textbox.delete("1.0", ctk.END)
            self.disassembly_textbox.insert(ctk.END, f"Désassemblage de: {exe_path}\n")
            self.disassembly_textbox.insert(ctk.END, "Veuillez patienter...\n")
            self.disassembly_textbox.configure(state="disabled")
            self.tab_view.set("Désassemblage Executable")

            threading.Thread(target=self._run_objdump_in_thread, 
                             args=(exe_path, self.disassembly_textbox), 
                             daemon=True).start()

        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            CTkMessagebox.showerror("Erreur d'accès", f"Impossible d'accéder à l'exécutable du processus (PID: {self.selected_pid}): {e}")
            self.disassembly_textbox.configure(state="normal")
            self.disassembly_textbox.delete("1.0", ctk.END)
            self.disassembly_textbox.insert(ctk.END, f"ERREUR: Impossible d'accéder à l'exécutable: {e}")
            self.disassembly_textbox.configure(state="disabled")
        except Exception as e:
            CTkMessagebox.showerror("Erreur Inconnue", f"Une erreur inattendue est survenue: {e}")
            self.disassembly_textbox.configure(state="normal")
            self.disassembly_textbox.delete("1.0", ctk.END)
            self.disassembly_textbox.insert(ctk.END, f"ERREUR INCONNUE: {e}")
            self.disassembly_textbox.configure(state="disabled")

    def _run_objdump_in_thread(self, exe_path, output_textbox):
        try:
            command = ['objdump', '-d', '-M', 'intel', '-w', exe_path]
            
            process = subprocess.run(command, capture_output=True, text=True, check=True)
            
            self.after(0, lambda: output_textbox.configure(state="normal"))
            self.after(0, lambda: output_textbox.delete("1.0", ctk.END))
            self.after(0, lambda: output_textbox.insert(ctk.END, process.stdout))
            self.after(0, lambda: output_textbox.configure(state="disabled"))

        except FileNotFoundError:
            self.after(0, lambda: output_textbox.configure(state="normal"))
            self.after(0, lambda: output_textbox.delete("1.0", ctk.END))
            self.after(0, lambda: output_textbox.insert(ctk.END, "ERREUR: 'objdump' introuvable. Veuillez l'installer (par ex., 'sudo apt install binutils').\n"))
            self.after(0, lambda: output_textbox.configure(state="disabled"))
            self.after(0, lambda: CTkMessagebox.showerror("Erreur", "La commande 'objdump' n'a pas été trouvée. Veuillez l'installer sur votre système Linux (paquet binutils)."))
        except subprocess.CalledProcessError as e:
            self.after(0, lambda: output_textbox.configure(state="normal"))
            self.after(0, lambda: output_textbox.delete("1.0", ctk.END))
            self.after(0, lambda: output_textbox.insert(ctk.END, f"Erreur lors de l'exécution d'objdump:\n{e.stderr}\n"))
            self.after(0, lambda: output_textbox.configure(state="disabled"))
            self.after(0, lambda: CTkMessagebox.showerror("Erreur Désassemblage", f"Erreur lors du désassemblage: {e.stderr}"))
        except Exception as e:
            self.after(0, lambda: output_textbox.configure(state="normal"))
            self.after(0, lambda: output_textbox.delete("1.0", ctk.END))
            self.after(0, lambda: output_textbox.insert(ctk.END, f"Une erreur inattendue est survenue lors du désassemblage: {e}\n"))
            self.after(0, lambda: output_textbox.configure(state="disabled"))
            self.after(0, lambda: CTkMessagebox.showerror("Erreur Inconnue", f"Une erreur inattendue est survenue: {e}"))

    def get_size_human_readable(self, bytes_val):
        """Converts bytes to human-readable format (B, KB, MB, GB)."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB" 

    def fetch_and_store_network_data(self):
        """Fetches raw network data and stores it in a structured format."""
        
        # --- Global Stats ---
        global_stats = {}
        try:
            net_io = psutil.net_io_counters()
            current_time = time.time()
            time_diff = current_time - self.last_net_time

            bytes_sent_diff = net_io.bytes_sent - self.last_net_io_counters.bytes_sent
            bytes_recv_diff = net_io.bytes_recv - self.last_net_io_counters.bytes_recv

            send_speed_bps = (bytes_sent_diff * 8) / time_diff if time_diff > 0 else 0 
            recv_speed_bps = (bytes_recv_diff * 8) / time_diff if time_diff > 0 else 0

            global_stats = {
                'bytes_sent_total': net_io.bytes_sent,
                'bytes_recv_total': net_io.bytes_recv,
                'packets_sent_total': net_io.packets_sent,
                'packets_recv_total': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout,
                'send_speed_bps': send_speed_bps,
                'recv_speed_bps': recv_speed_bps
            }
            self.last_net_io_counters = net_io
            self.last_net_time = current_time
        except Exception as e:
            print(f"Error fetching global network stats: {e}")

        self.structured_network_data['global_stats'] = global_stats

        # --- Interface Stats ---
        interfaces_data = []
        try:
            net_if_stats = psutil.net_if_stats()
            net_if_addrs = psutil.net_if_addrs()
            net_io_per_nic = psutil.net_io_counters(pernic=True)

            for interface_name, stats in net_if_stats.items():
                interface_info = {
                    'name': interface_name,
                    'isup': stats.isup,
                    'duplex': stats.duplex.name,
                    'speed': stats.speed,
                    'mtu': stats.mtu,
                    'addresses': [],
                    'io_counters': {}
                }

                if interface_name in net_if_addrs:
                    for addr in net_if_addrs[interface_name]:
                        addr_info = {
                            'address': addr.address,
                            'family': addr.family.name,
                            'netmask': addr.netmask,
                            'broadcast': addr.broadcast,
                            'mac': addr.mac
                        }
                        interface_info['addresses'].append(addr_info)

                if interface_name in net_io_per_nic:
                    io_nic = net_io_per_nic[interface_name]
                    interface_info['io_counters'] = {
                        'bytes_sent': io_nic.bytes_sent,
                        'bytes_recv': io_nic.bytes_recv,
                        'packets_sent': io_nic.packets_sent,
                        'packets_recv': io_nic.packets_recv,
                        'errin': io_nic.errin,
                        'errout': io_nic.errout,
                        'dropin': io_nic.dropin,
                        'dropout': io_nic.dropout
                    }
                interfaces_data.append(interface_info)
        except Exception as e:
            print(f"Error fetching interface network stats: {e}")
        self.structured_network_data['interfaces'] = interfaces_data

        # --- Process Connections ---
        connections_data = []
        try:
            for p in psutil.process_iter(['pid', 'name']):
                try:
                    p_connections = p.connections(kind='inet')
                    if p_connections:
                        for conn in p_connections:
                            conn_info = {
                                'pid': p.pid,
                                'process_name': p.name(),
                                'family': conn.family.name,
                                'type': conn.type.name,
                                'status': conn.status,
                                'laddr_ip': conn.laddr.ip if conn.laddr else None,
                                'laddr_port': conn.laddr.port if conn.laddr else None,
                                'raddr_ip': conn.raddr.ip if conn.raddr else None,
                                'raddr_port': conn.raddr.port if conn.raddr else None,
                            }
                            connections_data.append(conn_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            print(f"Error fetching process connections: {e}")
        self.structured_network_data['connections'] = connections_data

        # After fetching and storing, apply the current filters to update the display
        self.apply_network_filter()

    def apply_network_filter(self, event=None):
        """Applies filters to the structured network data and updates the display."""
        
        display_output = []

        # Get filter values (case-insensitive for strings, try converting port to int)
        filter_ip = self.filter_ip_entry.get().strip().lower()
        filter_port_str = self.filter_port_entry.get().strip()
        filter_port = None
        if filter_port_str:
            try:
                filter_port = int(filter_port_str)
            except ValueError:
                display_output.append(f"Erreur: Le port '{filter_port_str}' n'est pas un nombre valide.")
                filter_port = None # Invalidate filter if not a number
        
        filter_protocol = self.filter_protocol_entry.get().strip().lower()
        filter_keyword = self.filter_keyword_entry.get().strip().lower()

        # --- Global Stats ---
        if self.filter_global_var.get() and self.structured_network_data['global_stats']:
            gs = self.structured_network_data['global_stats']
            section_lines = [
                "--- Statistiques Réseau Globales ---",
                f"Total Envoyé: {self.get_size_human_readable(gs.get('bytes_sent_total', 0))}",
                f"Total Reçu: {self.get_size_human_readable(gs.get('bytes_recv_total', 0))}",
                f"Paquets Envoyés: {gs.get('packets_sent_total', 0)}",
                f"Paquets Reçus: {gs.get('packets_recv_total', 0)}",
                f"Erreurs en Sortie: {gs.get('errout', 0)}, en Entrée: {gs.get('errin', 0)}",
                f"Paquets Perdus en Sortie: {gs.get('dropout', 0)}, en Entrée: {gs.get('dropin', 0)}",
                f"Vitesse d'Envoi: {self.get_size_human_readable(gs.get('send_speed_bps', 0)/8)}/s (Bytes) | {gs.get('send_speed_bps', 0)/1_000_000:.2f} Mbps",
                f"Vitesse de Réception: {self.get_size_human_readable(gs.get('recv_speed_bps', 0)/8)}/s (Bytes) | {gs.get('recv_speed_bps', 0)/1_000_000:.2f} Mbps",
                "\n"
            ]
            # Apply keyword filter to the generated section lines
            if filter_keyword:
                filtered_section_lines = [line for line in section_lines if filter_keyword in line.lower()]
                if filtered_section_lines and len(filtered_section_lines) > 1: # Only add if actual data found
                    display_output.extend(filtered_section_lines)
            else:
                display_output.extend(section_lines)

        # --- Interface Stats ---
        if self.filter_interfaces_var.get() and self.structured_network_data['interfaces']:
            interface_lines_header_added = False
            for if_data in self.structured_network_data['interfaces']:
                
                # Check specific filters for interfaces (IP, Keyword)
                passes_ip_filter = True
                if filter_ip:
                    passes_ip_filter = any(filter_ip in addr['address'].lower() for addr in if_data.get('addresses', []))

                # Build interface-specific lines to apply keyword filter on
                current_if_lines = []
                current_if_lines.append(f"Interface: {if_data['name']}")
                current_if_lines.append(f"  Statut: {'UP' if if_data['isup'] else 'DOWN'}")
                current_if_lines.append(f"  Duplex: {if_data['duplex']}, Vitesse: {if_data['speed']} Mbps")
                current_if_lines.append(f"  MTU: {if_data['mtu']}")
                
                for addr_info in if_data['addresses']:
                    current_if_lines.append(f"    Adresse: {addr_info['address']} ({addr_info['family']})")
                    if addr_info['netmask']: current_if_lines.append(f"    Masque: {addr_info['netmask']}")
                    if addr_info['broadcast']: current_if_lines.append(f"    Broadcast: {addr_info['broadcast']}")
                    if addr_info['mac']: current_if_lines.append(f"    MAC: {addr_info['mac']}")

                if if_data['io_counters']:
                    io_nic = if_data['io_counters']
                    current_if_lines.append(f"  Bytes Envoyés: {self.get_size_human_readable(io_nic['bytes_sent'])}")
                    current_if_lines.append(f"  Bytes Reçus: {self.get_size_human_readable(io_nic['bytes_recv'])}")
                    current_if_lines.append(f"  Paquets Envoyés: {io_nic['packets_sent']}, Reçus: {io_nic['packets_recv']}")
                    current_if_lines.append(f"  Erreurs: Entrée={io_nic['errin']}, Sortie={io_nic['errout']}")
                    current_if_lines.append(f"  Chutes: Entrée={io_nic['dropin']}, Sortie={io_nic['dropout']}")
                
                # Check general keyword filter on the combined interface lines
                passes_keyword_filter = True
                if filter_keyword:
                    passes_keyword_filter = any(filter_keyword in line.lower() for line in current_if_lines)

                if passes_ip_filter and passes_keyword_filter:
                    if not interface_lines_header_added:
                        display_output.append("--- Statistiques par Interface Réseau ---")
                        interface_lines_header_added = True
                    display_output.extend(current_if_lines)
                    display_output.append("\n") # Add a separator

        # --- Process Connections ---
        if self.filter_connections_var.get() and self.structured_network_data['connections']:
            connections_lines_header_added = False
            for conn_data in self.structured_network_data['connections']:
                
                # Check specific filters for connections (IP, Port, Protocol, Keyword)
                passes_ip_filter = True
                if filter_ip:
                    laddr_ip_lower = conn_data['laddr_ip'].lower() if conn_data['laddr_ip'] else ""
                    raddr_ip_lower = conn_data['raddr_ip'].lower() if conn_data['raddr_ip'] else ""
                    passes_ip_filter = (filter_ip in laddr_ip_lower) or (filter_ip in raddr_ip_lower)
                
                passes_port_filter = True
                if filter_port is not None:
                    passes_port_filter = (conn_data['laddr_port'] == filter_port) or (conn_data['raddr_port'] == filter_port)
                
                passes_protocol_filter = True
                if filter_protocol:
                    passes_protocol_filter = filter_protocol in conn_data['type'].lower() # e.g., 'tcp' in 'SOCK_STREAM' for TCP, 'udp' for UDP
                
                # Build connection-specific line to apply keyword filter on
                laddr = f"{conn_data['laddr_ip']}:{conn_data['laddr_port']}" if conn_data['laddr_ip'] else "N/A"
                raddr = f"{conn_data['raddr_ip']}:{conn_data['raddr_port']}" if conn_data['raddr_ip'] else "N/A"
                conn_line = f"- PID: {conn_data['pid']}, Nom: {conn_data['process_name']}, Famille: {conn_data['family']}, Type: {conn_data['type']}, Statut: {conn_data['status']}, Local: {laddr}, Distant: {raddr}"
                
                passes_keyword_filter = True
                if filter_keyword:
                    passes_keyword_filter = filter_keyword in conn_line.lower()

                if passes_ip_filter and passes_port_filter and passes_protocol_filter and passes_keyword_filter:
                    if not connections_lines_header_added:
                        display_output.append("--- Connexions Réseau des Processus ---")
                        connections_lines_header_added = True
                    display_output.append(conn_line)
            if connections_lines_header_added:
                display_output.append("\n")


        # Update textbox
        self.network_activity_textbox.configure(state="normal")
        self.network_activity_textbox.delete("1.0", ctk.END)
        if not display_output:
            self.network_activity_textbox.insert(ctk.END, "Aucune donnée réseau ne correspond aux filtres appliqués.")
        else:
            self.network_activity_textbox.insert(ctk.END, "\n".join(display_output))
        self.network_activity_textbox.yview_moveto(0)
        self.network_activity_textbox.configure(state="disabled")

    def on_closing(self):
        """Handles application shutdown."""
        self.stop_monitoring()
        print("Moniteur de processus terminé.")
        self.destroy()

if __name__ == "__main__":
    psutil.cpu_percent(interval=None) 

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = ProcessMonitorApp()
    app.mainloop()