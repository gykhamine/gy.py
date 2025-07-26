import customtkinter as ctk
import threading
import time
import psutil
import os
import sys

class ProcessMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Moniteur de Processus en Temps Réel")
        self.geometry("1000x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Row for process list textbox

        self.monitoring_active = False
        self.process_refresh_thread = None
        self.selected_pid = None # To store the PID of the selected process

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

        # --- Selected Process Info Frame ---
        self.selected_process_frame = ctk.CTkFrame(self)
        self.selected_process_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.selected_process_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.selected_pid_label = ctk.CTkLabel(self.selected_process_frame, text="PID sélectionné: Aucun", font=ctk.CTkFont(size=14, weight="bold"))
        self.selected_pid_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.selected_name_label = ctk.CTkLabel(self.selected_process_frame, text="Nom: N/A", font=ctk.CTkFont(size=14, weight="bold"))
        self.selected_name_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.kill_button = ctk.CTkButton(self.selected_process_frame,
                                         text="Tuer le Processus Sélectionné",
                                         command=self.kill_selected_process,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         fg_color="red",
                                         hover_color="#CC0000",
                                         height=40,
                                         state="disabled") # Disabled until a process is selected
        self.kill_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        # --- Process List Display ---
        self.process_list_textbox = ctk.CTkTextbox(self, width=900, height=500, wrap="none", font=ctk.CTkFont(family="Consolas", size=12))
        self.process_list_textbox.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.process_list_textbox.bind("<Button-1>", self.on_process_list_click) # Bind click event

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initial prompt
        self.process_list_textbox.insert(ctk.END, "Cliquez sur 'Démarrer le Moniteur' pour commencer à lister les processus...")

    def toggle_monitoring(self):
        if not self.monitoring_active:
            self.start_monitoring()
            self.toggle_button.configure(text="Arrêter le Moniteur", fg_color="red")
            self.status_label.configure(text="Statut: En cours d'exécution", text_color="green")
            self.kill_button.configure(state="normal") # Enable kill button when monitoring
            self.update_process_list_display() # Initial display update
            print("Moniteur de processus démarré.")
        else:
            self.stop_monitoring()
            self.toggle_button.configure(text="Démarrer le Moniteur", fg_color="#3B8ED0") # Default blue
            self.status_label.configure(text="Statut: Arrêté", text_color="red")
            self.kill_button.configure(state="disabled") # Disable kill button
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
            # Give the thread a moment to stop its loop
            time.sleep(0.1) 
        self.reset_selected_process()

    def _refresh_processes_loop(self):
        while self.monitoring_active:
            # Use self.after to schedule GUI update on the main thread
            self.after(0, self.update_process_list_display)
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
                # Get CPU usage with a timeout to avoid blocking if process is gone
                cpu_percent = p.cpu_percent(interval=0.1) # interval=0 for non-blocking if called repeatedly
                mem_info = p.memory_info()
                mem_usage_mb = mem_info.rss / (1024 * 1024) # Resident Set Size
                
                processes.append({
                    'pid': p.pid,
                    'name': p.name(),
                    'status': p.status(),
                    'cpu_percent': cpu_percent,
                    'mem_usage_mb': mem_usage_mb,
                    'username': p.username()
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Ignore processes that no longer exist or are inaccessible
                continue
            except Exception as e:
                # Log other unexpected errors
                print(f"Erreur lors de la récupération des infos processus: {e} pour PID {p.pid}")
                continue
        
        # Sort processes by CPU usage descending
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

        for proc in processes:
            line = f"{proc['pid']:<8} {proc['status']:<10} {proc['cpu_percent']:<8.1f} {proc['mem_usage_mb']:<12.1f} {proc['name']:<30} {proc['username']:<20}\n"
            self.process_list_textbox.insert(ctk.END, line)
        
        # Scroll to top to always see the most active processes first
        self.process_list_textbox.yview_moveto(0)

    def on_process_list_click(self, event):
        """Handles clicks on the process list textbox to select a process."""
        try:
            # Get the line number of the clicked text
            index = self.process_list_textbox.index(f"@{event.x},{event.y}")
            line_num = int(index.split('.')[0])

            # Skip header lines (1-based index for textbox lines)
            if line_num <= 2: # Header and separator are lines 1 and 2
                self.reset_selected_process()
                return

            # Get the content of the clicked line
            line_content = self.process_list_textbox.get(f"{line_num}.0", f"{line_num}.end")
            
            # Extract PID from the line content
            # Assuming PID is the first column and fixed width
            pid_str = line_content[0:8].strip()
            self.selected_pid = int(pid_str)
            
            # Extract name
            name_str = line_content[38:68].strip() # Based on header formatting
            
            self.selected_pid_label.configure(text=f"PID sélectionné: {self.selected_pid}")
            self.selected_name_label.configure(text=f"Nom: {name_str}")
            self.kill_button.configure(state="normal")

            # Highlight the selected line (optional, but good for UX)
            self.process_list_textbox.tag_remove("highlight", "1.0", ctk.END)
            self.process_list_textbox.tag_add("highlight", f"{line_num}.0", f"{line_num}.end")
            self.process_list_textbox.tag_config("highlight", background="#3B8ED0", foreground="white") # CustomTkinter blue
            
        except (ValueError, IndexError):
            self.reset_selected_process()
            print("Clic hors d'un processus valide ou erreur d'extraction.")

    def reset_selected_process(self):
        self.selected_pid = None
        self.selected_pid_label.configure(text="PID sélectionné: Aucun")
        self.selected_name_label.configure(text="Nom: N/A")
        self.kill_button.configure(state="disabled")
        self.process_list_textbox.tag_remove("highlight", "1.0", ctk.END) # Remove highlight

    def kill_selected_process(self):
        if self.selected_pid is None:
            return
        
        try:
            process = psutil.Process(self.selected_pid)
            process_name = process.name()
            # Confirmation dialog (simple CustomTkinter message box)
            response = ctk.CTkMessagebox.ask_yes_no(
                f"Confirmer l'arrêt du processus",
                f"Êtes-vous sûr de vouloir tuer le processus '{process_name}' (PID: {self.selected_pid})?",
                icon="warning"
            )
            
            if response == "yes":
                process.terminate() # or process.kill() for a stronger termination
                self.status_label.configure(text=f"Tentative d'arrêt de {self.selected_pid}...", text_color="orange")
                # Give a moment for process to terminate and list to refresh
                self.after(500, self.update_process_list_display) 
                self.reset_selected_process()
            else:
                self.status_label.configure(text="Opération annulée.", text_color="grey")

        except psutil.NoSuchProcess:
            ctk.CTkMessagebox.showerror("Erreur", f"Le processus (PID: {self.selected_pid}) n'existe plus.")
        except psutil.AccessDenied:
            ctk.CTkMessagebox.showerror("Erreur", f"Accès refusé pour tuer le processus (PID: {self.selected_pid}). Exécutez en tant qu'administrateur.")
        except Exception as e:
            ctk.CTkMessagebox.showerror("Erreur Inconnue", f"Une erreur inattendue est survenue: {e}")
        finally:
            self.reset_selected_process()


    def on_closing(self):
        """Handles application shutdown."""
        self.stop_monitoring()
        print("Moniteur de processus terminé.")
        self.destroy()

if __name__ == "__main__":
    # Ensure psutil.cpu_percent() is called once at start with interval=None
    # This initializes it for subsequent non-blocking calls.
    psutil.cpu_percent(interval=None) 

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    # Check if messagebox is available, if not, import it
    try:
        from CTkMessagebox import CTkMessagebox # Try standard import
    except ImportError:
        # Fallback for older/different setups, or if user hasn't installed it
        # You might need to install CTkMessagebox: pip install CTkMessagebox
        print("CTkMessagebox not found. Falling back to simple print for alerts.")
        class CTkMessagebox: # Mock class for basic functionality
            @staticmethod
            def ask_yes_no(title, message, icon=None):
                print(f"ALERT: {title}\n{message} (Type 'yes' to proceed, anything else to cancel)")
                return input().lower()
            @staticmethod
            def showerror(title, message):
                print(f"ERROR: {title}\n{message}")
        
    app = ProcessMonitorApp()
    app.mainloop()