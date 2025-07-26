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

class ProcessMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Moniteur de Processus Avancé")
        self.geometry("1400x900") # Increased size to accommodate new tabs/info
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Row for main content (tabview)

        self.monitoring_active = False
        self.process_refresh_thread = None
        self.selected_pid = None # To store the PID of the selected process
        self.selected_process_obj = None # To store the psutil.Process object of the selected PID
        self.syscall_thread = None
        self.syscall_process = None # To hold the Popen object for strace

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
        self.selected_process_actions_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1) # Added more columns for buttons

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
                                                    text="Tracer Appels Système (strace)",
                                                    command=self.start_syscall_tracing,
                                                    font=ctk.CTkFont(size=14, weight="bold"),
                                                    fg_color="orange",
                                                    hover_color="#CC8800",
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
        self.tab_view.add("Appels Système (strace)")
        self.tab_view.add("Désassemblage Executable") # New tab for disassembly

        # --- Tab 1: Process List Display ---
        self.process_list_textbox = ctk.CTkTextbox(self.tab_view.tab("Liste des Processus"), wrap="none", font=ctk.CTkFont(family="Consolas", size=12))
        self.process_list_textbox.pack(fill="both", expand=True)
        self.process_list_textbox.bind("<Button-1>", self.on_process_list_click) # Bind click event

        # --- Tab 2: Detailed Process Information ---
        self.details_textbox = ctk.CTkTextbox(self.tab_view.tab("Détails du Processus"), wrap="word", font=ctk.CTkFont(family="Consolas", size=12))
        self.details_textbox.pack(fill="both", expand=True)
        self.details_textbox.insert(ctk.END, "Sélectionnez un processus dans la liste pour voir les détails ici.")

        # --- Tab 3: System Call Trace Output ---
        self.syscall_output_textbox = ctk.CTkTextbox(self.tab_view.tab("Appels Système (strace)"), wrap="none", font=ctk.CTkFont(family="Consolas", size=12))
        self.syscall_output_textbox.pack(fill="both", expand=True)
        self.syscall_output_textbox.insert(ctk.END, "Le traçage des appels système (strace) apparaîtra ici. Nécessite des privilèges 'sudo' pour de nombreux processus.\n")
        self.syscall_output_textbox.insert(ctk.END, "Assurez-vous que 'strace' est installé sur votre système (e.g., sudo apt install strace).")
        
        self.stop_syscall_button = ctk.CTkButton(self.tab_view.tab("Appels Système (strace)"),
                                                 text="Arrêter le Traçage",
                                                 command=self.stop_syscall_tracing,
                                                 fg_color="red",
                                                 hover_color="#CC0000",
                                                 state="disabled")
        self.stop_syscall_button.pack(pady=5)

        # --- Tab 4: Disassembly Output ---
        self.disassembly_textbox = ctk.CTkTextbox(self.tab_view.tab("Désassemblage Executable"), wrap="none", font=ctk.CTkFont(family="Consolas", size=12))
        self.disassembly_textbox.pack(fill="both", expand=True)
        self.disassembly_textbox.insert(ctk.END, "Le désassemblage de l'exécutable du processus sélectionné apparaîtra ici.\n")
        self.disassembly_textbox.insert(ctk.END, "Assurez-vous que 'objdump' est installé sur votre système (e.g., sudo apt install binutils).")
        self.disassembly_textbox.configure(state="disabled") # Make it read-only initially

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initial prompt
        self.process_list_textbox.insert(ctk.END, "Cliquez sur 'Démarrer le Moniteur' pour commencer à lister les processus...")

    def toggle_monitoring(self):
        if not self.monitoring_active:
            self.start_monitoring()
            self.toggle_button.configure(text="Arrêter le Moniteur", fg_color="red")
            self.status_label.configure(text="Statut: En cours d'exécution", text_color="green")
            self.kill_button.configure(state="normal")
            self.trace_syscalls_button.configure(state="normal")
            self.disassemble_exe_button.configure(state="normal") # Enable disassembly button
            self.update_process_list_display() # Initial display update
            print("Moniteur de processus démarré.")
        else:
            self.stop_monitoring()
            self.toggle_button.configure(text="Démarrer le Moniteur", fg_color="#3B8ED0") # Default blue
            self.status_label.configure(text="Statut: Arrêté", text_color="red")
            self.kill_button.configure(state="disabled")
            self.trace_syscalls_button.configure(state="disabled")
            self.disassemble_exe_button.configure(state="disabled") # Disable disassembly button
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
        self.stop_syscall_tracing() # Stop any active strace
        self.reset_selected_process()

    def _refresh_processes_loop(self):
        while self.monitoring_active:
            self.after(0, self.update_process_list_display)
            if self.selected_pid:
                self.after(0, self.update_selected_process_details)
            time.sleep(1) # Refresh every 1 second

    def update_process_list_display(self):
        """Fetches and updates the list of processes in the textbox."""
        self.process_list_textbox.delete("1.0", ctk.END)
        
        header = f"{'PID':<8} {'Status':<10} {'CPU%':<8} {'Mem (MB)':<12} {'Nom':<30} {'Utilisateur':<20}\n"
        self.process_list_textbox.insert(ctk.END, header)
        self.process_list_textbox.insert(ctk.END, "-" * 100 + "\n")

        processes = []
        for p in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info', 'username']):
            try:
                cpu_percent = p.cpu_percent(interval=None) # Non-blocking if called repeatedly
                mem_info = p.memory_info()
                mem_usage_mb = mem_info.rss / (1024 * 1024) # Resident Set Size (RSS)

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
            
        self.process_list_textbox.yview_moveto(0) # Scroll to top

    def on_process_list_click(self, event):
        """Handles clicks on the process list textbox to select a process."""
        try:
            index = self.process_list_textbox.index(f"@{event.x},{event.y}")
            line_num = int(index.split('.')[0])

            if line_num <= 2: # Header and separator are lines 1 and 2
                self.reset_selected_process()
                return

            line_content = self.process_list_textbox.get(f"{line_num}.0", f"{line_num}.end")
            pid_str = line_content[0:8].strip()
            new_selected_pid = int(pid_str)
            
            # If the same PID is clicked again, do nothing or toggle off
            if new_selected_pid == self.selected_pid:
                # self.reset_selected_process() # Optional: click twice to deselect
                return

            self.selected_pid = new_selected_pid
            
            try:
                self.selected_process_obj = psutil.Process(self.selected_pid)
                process_name = self.selected_process_obj.name()
                self.selected_pid_label.configure(text=f"PID sélectionné: {self.selected_pid}")
                self.selected_name_label.configure(text=f"Nom: {process_name}")
                self.kill_button.configure(state="normal")
                self.trace_syscalls_button.configure(state="normal")
                self.disassemble_exe_button.configure(state="normal") # Enable disassembly button

                self.process_list_textbox.tag_remove("highlight", "1.0", ctk.END)
                self.process_list_textbox.tag_add("highlight", f"{line_num}.0", f"{line_num}.end")
                self.process_list_textbox.tag_config("highlight", background="#3B8ED0", foreground="white")

                # Update detailed info tab
                self.update_selected_process_details()
                self.tab_view.set("Détails du Processus") # Switch to details tab
                
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
        self.disassemble_exe_button.configure(state="disabled") # Disable disassembly button
        self.process_list_textbox.tag_remove("highlight", "1.0", ctk.END) # Remove highlight
        self.details_textbox.delete("1.0", ctk.END)
        self.details_textbox.insert(ctk.END, "Sélectionnez un processus dans la liste pour voir les détails.")
        self.stop_syscall_tracing() # Ensure strace is stopped if selection is reset
        self.disassembly_textbox.configure(state="normal")
        self.disassembly_textbox.delete("1.0", ctk.END)
        self.disassembly_textbox.insert(ctk.END, "Le désassemblage de l'exécutable du processus sélectionné apparaîtra ici.\n")
        self.disassembly_textbox.insert(ctk.END, "Assurez-vous que 'objdump' est installé sur votre système (e.g., sudo apt install binutils).")
        self.disassembly_textbox.configure(state="disabled")

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

            details.append(f"\n--- Connexions Réseau ---")
            connections = p.connections(kind='inet') # 'inet' for TCP/UDP IPv4/IPv6
            if connections:
                for conn in connections:
                    laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    details.append(f"- Famille: {conn.family.name}, Type: {conn.type.name}, Statut: {conn.status}, Local: {laddr}, Distant: {raddr}")
            else:
                details.append("Aucune connexion réseau.")

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
                process.terminate() # or process.kill() for a stronger termination
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
        if not self.selected_pid:
            CTkMessagebox.show_warning("Aucun Processus Sélectionné", "Veuillez sélectionner un processus pour tracer les appels système.")
            return

        if sys.platform != "linux":
            CTkMessagebox.show_error("Plateforme Non Supportée", "Le traçage des appels système avec 'strace' n'est disponible que sous Linux.")
            return

        self.stop_syscall_tracing()

        self.syscall_output_textbox.configure(state="normal") # Enable for writing
        self.syscall_output_textbox.delete("1.0", ctk.END)
        self.syscall_output_textbox.insert(ctk.END, f"Démarrage du traçage des appels système pour PID: {self.selected_pid}...\n")
        self.syscall_output_textbox.insert(ctk.END, "NOTE: Cela nécessite généralement des privilèges root (sudo).\n")
        self.syscall_output_textbox.insert(ctk.END, "Vous pourriez être invité à entrer votre mot de passe.\n")
        self.syscall_output_textbox.insert(ctk.END, "--------------------------------------------------------\n")
        self.syscall_output_textbox.configure(state="disabled") # Disable after initial message
        
        self.tab_view.set("Appels Système (strace)")
        self.stop_syscall_button.configure(state="normal")

        self.syscall_thread = threading.Thread(target=self._run_strace_in_thread, daemon=True)
        self.syscall_thread.start()

    def _run_strace_in_thread(self):
        pid_to_trace = self.selected_pid
        if not pid_to_trace:
            return

        command = ['sudo', 'strace', '-p', str(pid_to_trace), '-f', '-tt', '-T', '-s', '256']
        
        try:
            self.syscall_process = subprocess.Popen(command, 
                                                    stdout=subprocess.PIPE, 
                                                    stderr=subprocess.PIPE,
                                                    text=True, 
                                                    bufsize=1, 
                                                    universal_newlines=True)

            while True:
                line = self.syscall_process.stderr.readline()
                if not line and self.syscall_process.poll() is not None:
                    break
                if line:
                    self.after(0, lambda l=line: self._append_to_syscall_textbox(l))
                time.sleep(0.01)

            stdout, stderr = self.syscall_process.communicate()
            if stdout:
                self.after(0, lambda s=stdout: self._append_to_syscall_textbox(f"\n[strace STDOUT]\n{s}"))

            self.after(0, lambda: self._append_to_syscall_textbox("\n--- Traçage des appels système terminé ---\n"))
            self.after(0, lambda: self.stop_syscall_button.configure(state="disabled"))
            self.syscall_process = None

        except FileNotFoundError:
            self.after(0, lambda: self._append_to_syscall_textbox("\nERREUR: 'strace' introuvable. Veuillez l'installer (par ex., 'sudo apt install strace').\n"))
            self.after(0, lambda: CTkMessagebox.showerror("Erreur", "La commande 'strace' n'a pas été trouvée. Veuillez l'installer sur votre système Linux."))
            self.after(0, lambda: self.stop_syscall_button.configure(state="disabled"))
        except psutil.NoSuchProcess:
            self.after(0, lambda: self._append_to_syscall_textbox("\nERREUR: Le processus cible n'existe plus.\n"))
            self.after(0, lambda: self.stop_syscall_button.configure(state="disabled"))
        except Exception as e:
            self.after(0, lambda: self._append_to_syscall_textbox(f"\nERREUR lors du traçage: {e}\n"))
            self.after(0, lambda: CTkMessagebox.showerror("Erreur Traçage", f"Une erreur est survenue lors du traçage des appels système: {e}"))
            self.after(0, lambda: self.stop_syscall_button.configure(state="disabled"))
        finally:
            if self.syscall_process and self.syscall_process.poll() is None:
                self.syscall_process.terminate()
                self.syscall_process.wait(timeout=2)
            self.syscall_process = None

    def _append_to_syscall_textbox(self, text):
        self.syscall_output_textbox.configure(state="normal")
        self.syscall_output_textbox.insert(ctk.END, text)
        self.syscall_output_textbox.yview_moveto(1)
        self.syscall_output_textbox.configure(state="disabled")

    def stop_syscall_tracing(self):
        if self.syscall_process and self.syscall_process.poll() is None:
            try:
                self.syscall_process.terminate()
                self.syscall_process.wait(timeout=2)
                print(f"strace pour PID {self.selected_pid} arrêté.")
            except Exception as e:
                print(f"Erreur lors de l'arrêt de strace: {e}")
            finally:
                self.syscall_process = None
                self._append_to_syscall_textbox("\n--- Traçage arrêté par l'utilisateur ---\n")
                self.stop_syscall_button.configure(state="disabled")
        elif self.syscall_process:
            self.syscall_process = None
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
            self.tab_view.set("Désassemblage Executable") # Switch to disassembly tab

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

    def on_closing(self):
        """Handles application shutdown."""
        self.stop_monitoring()
        print("Moniteur de processus terminé.")
        self.destroy()

if __name__ == "__main__":
    psutil.cpu_percent(interval=None) # Required for first non-blocking call to cpu_percent

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = ProcessMonitorApp()
    app.mainloop()