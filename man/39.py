import customtkinter as ctk
from threading import Thread
import subprocess
import sys
import tkinter.filedialog as filedialog
import datetime
import os
import signal # Pour envoyer des signaux aux processus
import psutil # Pour une meilleure gestion des processus
import platform # Pour détecter l'OS et ouvrir le dossier de captures

class AircrackNGApp:
    def __init__(self, master):
        self.master = master
        master.title("Aircrack-ng GUI Avancée")
        master.geometry("1200x800")
        master.protocol("WM_DELETE_WINDOW", self._on_closing)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.current_process = None
        self.capture_dir = "aircrack_captures" # Nom plus spécifique
        os.makedirs(self.capture_dir, exist_ok=True)

        # --- Initialisation des attributs avant leur utilisation ---
        # Ces éléments doivent être définis avant d'être référencés
        # par exemple dans update_status ou update_results,
        # ou par les méthodes qui appellent update_status/update_results
        
        # Le status_bar est un des premiers éléments à être utilisés
        self.status_bar = ctk.CTkLabel(master, text="Démarrage de l'application...", anchor="w", font=ctk.CTkFont(size=12))
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # Les méthodes update_status et update_results dépendent de status_bar et results_text
        # et doivent donc être définies avant d'être appelées par d'autres méthodes dans __init__
        self.results_text = ctk.CTkTextbox(None, wrap="word") # Temporairement None pour éviter circularité
        self.results_text.configure(state="disabled")

        # Définition des méthodes de mise à jour (nécessaire avant tout appel)
        self.update_status("Initialisation de l'interface...", "black")

    def update_results(self, text):
        """Met à jour la zone de texte des résultats."""
        if not self.results_text.winfo_exists(): # Vérifier si le widget existe avant de l'utiliser
            print(f"DEBUG: results_text widget does not exist. Output: {text}")
            return # Sortir si le widget n'est pas encore prêt

        self.results_text.configure(state="normal")
        self.results_text.insert("end", text)
        self.results_text.configure(state="disabled")
        self.results_text.see("end")

    def update_status(self, message, color="black"):
        """Met à jour la barre de statut."""
        if not self.status_bar.winfo_exists(): # Vérifier si le widget existe avant de l'utiliser
            print(f"DEBUG: status_bar widget does not exist. Status: {message}")
            return # Sortir si le widget n'est pas encore prêt
            
        self.status_bar.configure(text=message, text_color=color)
        print(f"STATUS: {message}") # Pour le débogage en console

    def _on_closing(self):
        """Arrête le processus en cours et ferme l'application."""
        self.update_status("Fermeture de l'application...", "orange")
        self.stop_current_command()
        self.master.destroy()

    def _create_input_field(self, name, label_text, default_value=""):
        """Crée et initialise un champ d'entrée générique."""
        frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w")
        entry = ctk.CTkEntry(frame, width=300)
        if default_value:
            entry.insert(0, default_value)
        
        self.inputs[name] = {"frame": frame, "label": label, "entry": entry}
        return frame, label, entry # Retourne les widgets pour un packing ultérieur

    def _create_dropdown_field(self, name, label_text, options):
        """Crée un champ d'entrée avec un menu déroulant."""
        frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w")
        option_menu = ctk.CTkOptionMenu(frame, values=options)
        
        self.inputs[name] = {"frame": frame, "label": label, "entry": option_menu, "type": "dropdown"}
        return frame, label, option_menu # Retourne les widgets

    def _create_file_input_field(self, name, label_text, file_type):
        """Crée et initialise un champ d'entrée de fichier avec un bouton de sélection."""
        frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w")
        entry = ctk.CTkEntry(frame, width=250)
        button = ctk.CTkButton(frame, text="Parcourir...", width=80, 
                                command=lambda n=name, ft=file_type: self._browse_file(n, ft))
        
        self.inputs[name] = {"frame": frame, "label": label, "entry": entry, "button": button}
        return frame, label, entry, button # Retourne les widgets

    def _browse_file(self, entry_name, file_type):
        """Ouvre une boîte de dialogue pour sélectionner un fichier."""
        initial_dir = os.path.join(os.getcwd(), self.capture_dir)
        if not os.path.exists(initial_dir):
            initial_dir = os.getcwd()

        filetypes_map = {
            ".cap": [("Capture Files", "*.cap *.pcap"), ("All Files", "*.*")],
            ".txt": [("Text Files", "*.txt"), ("All Files", "*.*")]
        }
        
        file_path = filedialog.askopenfilename(initialdir=initial_dir, 
                                                filetypes=filetypes_map.get(file_type, [("All Files", "*.*")]))

        if file_path:
            self.inputs[entry_name]["entry"].delete(0, "end")
            self.inputs[entry_name]["entry"].insert(0, file_path)
            self.update_status(f"Fichier sélectionné : {os.path.basename(file_path)}", "blue")

    def _hide_all_inputs(self):
        """Cache tous les champs d'entrée."""
        for input_widgets in self.inputs.values():
            input_widgets["frame"].pack_forget()

    def _refresh_interfaces(self):
        """Détecte les interfaces Wi-Fi disponibles et met à jour le menu déroulant."""
        self.update_status("Détection des interfaces Wi-Fi...", "blue")
        interfaces = []
        try:
            # Tenter d'utiliser 'iw dev' en premier pour une meilleure détection Wi-Fi
            result_iw = subprocess.run(['iw', 'dev'], capture_output=True, text=True, check=True)
            for line in result_iw.stdout.splitlines():
                if "Interface" in line:
                    iface_name = line.split("Interface")[1].strip()
                    if iface_name not in interfaces:
                        interfaces.append(iface_name)
            
            # Si iw n'a rien trouvé ou n'est pas installé, essayer 'ip -br link'
            if not interfaces:
                result_ip = subprocess.run(['ip', '-br', 'link', 'show', 'type', 'wireless'], capture_output=True, text=True, check=True)
                for line in result_ip.stdout.splitlines():
                    parts = line.split()
                    if parts and parts[0] != "lo" and not parts[0].startswith("docker"):
                        if parts[0] not in interfaces:
                            interfaces.append(parts[0])

            if not interfaces:
                self.update_status("Aucune interface Wi-Fi détectée. Vérifiez 'iw' ou 'ip' et les droits root.", "orange")
                interfaces = ["Aucune interface détectée"]

            self.inputs["interface"]["entry"].configure(values=interfaces)
            if interfaces and interfaces[0] != "Aucune interface détectée":
                self.inputs["interface"]["entry"].set(interfaces[0])
            
        except FileNotFoundError as e:
            self.update_status(f"Commande '{e.filename}' non trouvée. Assurez-vous qu'elle est installée et dans le PATH. Impossible de détecter les interfaces.", "red")
            self.inputs["interface"]["entry"].configure(values=["Outil non trouvé"])
            self.inputs["interface"]["entry"].set("Outil non trouvé")
        except subprocess.CalledProcessError as e:
            self.update_status(f"Erreur d'exécution ({e.cmd}): {e.stderr.strip()}. Assurez-vous d'avoir les droits root. Impossible de détecter les interfaces.", "red")
            self.inputs["interface"]["entry"].configure(values=["Erreur (root?)"])
            self.inputs["interface"]["entry"].set("Erreur (root?)")
        except Exception as e:
            self.update_status(f"Erreur inattendue lors de la détection des interfaces: {e}", "red")
            self.inputs["interface"]["entry"].configure(values=["Erreur de détection"])
            self.inputs["interface"]["entry"].set("Erreur de détection")

        self.update_status(f"Interfaces Wi-Fi détectées: {', '.join(interfaces) if interfaces else 'Aucune'}", "blue")

    def on_task_label_click(self, event, task_data, label):
        """
        Gère le clic sur un label de tâche.
        Met en surbrillance l'option sélectionnée et affiche les champs d'entrée pertinents.
        """
        # S'assurer que les widgets existent avant de les manipuler
        if not (hasattr(self, 'run_button') and self.run_button.winfo_exists() and
                hasattr(self, 'stop_button') and self.stop_button.winfo_exists() and
                hasattr(self, 'open_capture_dir_button') and self.open_capture_dir_button.winfo_exists()):
            self.update_status("L'interface n'est pas encore entièrement chargée. Veuillez patienter.", "orange")
            return

        if self.selected_label_widget:
            self.selected_label_widget.configure(fg_color="transparent")
        
        self.selected_label_widget = label
        self.selected_label_widget.configure(fg_color=ctk.ThemeManager.theme["CTkOptionMenu"]["button_color"])
        
        self.selected_task_data = task_data
        self.update_status(f"Tâche sélectionnée : {label.cget('text')} - Prête à être configurée.", "black")
        self.run_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

        self._hide_all_inputs()

        # Affiche seulement les champs requis pour la tâche sélectionnée
        for input_name in task_data["inputs"]:
            if input_name in self.inputs:
                frame = self.inputs[input_name]["frame"]
                label_widget = self.inputs[input_name]["label"]
                input_widget = self.inputs[input_name]["entry"]
                
                frame.pack(fill="x", pady=5, padx=10)
                label_widget.pack(side="left", padx=(0, 5))
                input_widget.pack(side="left", expand=True, fill="x")
                if "button" in self.inputs[input_name]:
                    self.inputs[input_name]["button"].pack(side="left", padx=(5,0))
            else:
                self.update_status(f"Erreur: Champ d'entrée inconnu requis: {input_name}", "red")
        
        # Afficher les notes spécifiques à la tâche
        notes = task_data.get("notes", "Aucune note pour cette tâche.")
        if task_data.get("root_required", False):
            notes = "⚠️ Nécessite des **privilèges root (sudo)**. " + notes
            self.notes_label.configure(text_color="red")
        else:
            self.notes_label.configure(text_color="gray")
        self.notes_label.configure(text=f"Notes: {notes}")
        self.notes_label.pack(pady=(0,10), padx=10, fill="x")
        
        # Repack buttons to be at the bottom of inputs
        self.run_button.pack_forget()
        self.run_button.pack(pady=10, padx=10, anchor="e")
        self.stop_button.pack_forget()
        self.stop_button.pack(pady=5, padx=10, anchor="e")
        self.open_capture_dir_button.pack_forget()
        self.open_capture_dir_button.pack(pady=5, padx=10, anchor="e")


    def start_aircrack_ng_command(self):
        """Construit et lance la commande Aircrack-ng."""
        if self.current_process and self.current_process.poll() is None:
            self.update_status("Une commande est déjà en cours. Arrêtez-la d'abord.", "orange")
            return

        task_data = self.selected_task_data
        if not task_data:
            self.update_status("Veuillez sélectionner une tâche Aircrack-ng.", "red")
            return

        command_template = task_data["cmd"]
        required_inputs = task_data["inputs"]
        
        cmd_vars = {}
        for input_name in required_inputs:
            if input_name in self.inputs:
                # Récupère la valeur, que ce soit d'un CTkEntry ou CTkOptionMenu
                if self.inputs[input_name].get("type") == "dropdown":
                    value = self.inputs[input_name]["entry"].get().strip()
                    if value == "Aucune interface détectée" or value == "Outil non trouvé" or value == "Erreur (root?)":
                        self.update_status(f"Erreur: Interface non valide sélectionnée pour '{input_name}'.", "red")
                        return
                else:
                    value = self.inputs[input_name]["entry"].get().strip()

                if not value:
                    self.update_status(f"Erreur: Le champ '{self.inputs[input_name]['label'].cget('text')}' est requis.", "red")
                    return
                cmd_vars[input_name] = value
            else:
                self.update_status(f"Erreur interne: Champ '{input_name}' non trouvé.", "red")
                return

        # Gestion spéciale pour les chemins de fichiers de sortie auto-générés
        output_path_set = False
        if "{output_path}" in command_template:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{cmd_vars.get('bssid', 'unknown_ap').replace(':', '')}_{timestamp}" 
            output_path = os.path.join(self.capture_dir, output_filename)
            cmd_vars["output_path"] = output_path
            self.update_status(f"Fichier de capture sera créé : {output_path}.cap", "blue")
            output_path_set = True

        try:
            full_command_str = command_template.format(**cmd_vars)
            # Utiliser shlex.split serait plus robuste pour des commandes complexes avec des espaces,
            # mais pour l'instant, un simple split() est suffisant si les guillemets sont gérés
            # directement dans le template de commande comme c'est le cas ici pour les chemins.
            command_list = full_command_str.split() 
        except KeyError as e:
            self.update_status(f"Erreur de configuration: Variable manquante pour la commande ({e}).", "red")
            return

        self.update_status(f"Exécution de : {' '.join(command_list)}...", "blue")
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("end", f"Exécution : {' '.join(command_list)}\n\n")
        self.results_text.configure(state="disabled")

        self.run_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        # Exécuter dans un thread séparé pour ne pas bloquer l'interface
        command_thread = Thread(target=self._run_subprocess, args=(command_list, task_data.get("post_process", None)))
        command_thread.daemon = True # Permet au thread de s'arrêter si le programme principal se ferme
        command_thread.start()

    def stop_current_command(self):
        """Arrête le processus Aircrack-ng en cours."""
        if self.current_process and self.current_process.poll() is None:
            self.update_status("Tentative d'arrêt de la commande...", "orange")
            try:
                # Utiliser psutil pour tuer le processus et ses enfants
                process = psutil.Process(self.current_process.pid)
                for proc in process.children(recursive=True):
                    proc.send_signal(signal.SIGTERM) # Envoie un signal de terminaison
                process.send_signal(signal.SIGTERM)
                
                # Attendre un court instant que le processus se termine
                try:
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    self.update_status("Le processus ne s'est pas arrêté, tentative de tuer (SIGKILL)...", "red")
                    process.kill()
                    process.wait()

                self.current_process = None
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                self.update_status("Commande arrêtée.", "green")
            except psutil.NoSuchProcess:
                self.update_status("Le processus n'existe plus ou a déjà été tué.", "green")
                self.current_process = None
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
            except Exception as e:
                self.update_status(f"Erreur lors de l'arrêt du processus: {e}", "red")
        else: # This block handles the case where current_process is None or already dead
            self.update_status("Aucune commande active à arrêter.", "orange")
            self.current_process = None
            self.run_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

    def _run_subprocess(self, command_list, post_process_func=None):
        """Exécute une commande shell et capture sa sortie."""
        try:
            self.current_process = subprocess.Popen(
                command_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1 # Lecture ligne par ligne
            )

            full_output_buffer = [] # Pour collecter toute la sortie pour le post-traitement

            # Lecture de la sortie en temps réel
            for line in iter(self.current_process.stdout.readline, ''):
                if line:
                    full_output_buffer.append(line)
                    self.master.after(0, self.update_results, line)
                if self.current_process.poll() is not None:
                    break
            
            self.current_process.stdout.close()

            remaining_output, stderr_output = self.current_process.communicate()
            if remaining_output:
                full_output_buffer.append(remaining_output)
                self.master.after(0, self.update_results, remaining_output)
            
            if stderr_output:
                full_output_buffer.append("\n--- Sortie Erreur (stderr) ---\n" + stderr_output)
                self.master.after(0, self.update_results, "\n--- Sortie Erreur (stderr) ---\n" + stderr_output)
            
            return_code = self.current_process.returncode
            if return_code != 0:
                self.master.after(0, self.update_status, f"Commande terminée avec erreur: {return_code}", "red")
            else:
                self.master.after(0, self.update_status, "Commande terminée avec succès.", "green")
                if post_process_func:
                    self.master.after(0, post_process_func, "".join(full_output_buffer))

        except FileNotFoundError:
            error_message = f"Erreur : La commande '{command_list[0]}' n'a pas été trouvée.\n" \
                            "Veuillez vous assurer que Aircrack-ng est installé et que son chemin est configuré (PATH)."
            self.master.after(0, self.update_results, error_message)
            self.master.after(0, self.update_status, "Erreur : Outil Aircrack-ng non trouvé", "red")
            print(error_message, file=sys.stderr)
        except PermissionError:
             error_message = f"Erreur de permission : Vous devez probablement exécuter ce script avec 'sudo'.\n" \
                             f"Exemple : sudo python {sys.argv[0]}"
             self.master.after(0, self.update_results, error_message)
             self.master.after(0, self.update_status, "Erreur : Permissions insuffisantes (Besoin de sudo)", "red")
             print(error_message, file=sys.stderr)
        except Exception as e:
            error_message = f"Une erreur inattendue est survenue : {e}"
            self.master.after(0, self.update_results, error_message)
            self.master.after(0, self.update_status, "Erreur inattendue", "red")
            print(error_message, file=sys.stderr)
        finally:
            self.current_process = None
            self.master.after(0, self.run_button.configure, state="normal")
            self.master.after(0, self.stop_button.configure, state="disabled")

    def _open_capture_directory(self):
        """Ouvre le dossier où les fichiers de capture sont enregistrés."""
        try:
            path = os.path.abspath(self.capture_dir)
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True) # Créer au cas où il aurait été supprimé
            
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin": # macOS
                subprocess.Popen(["open", path])
            else: # Linux et autres UNIX-like
                subprocess.Popen(["xdg-open", path]) # Nécessite xdg-utils
            self.update_status(f"Ouverture du dossier : {path}", "green")
        except FileNotFoundError:
            self.update_status(f"Erreur : Impossible de trouver un gestionnaire de fichiers pour ouvrir {self.capture_dir}. Assurez-vous d'avoir 'xdg-open' ou un équivalent.", "red")
        except Exception as e:
            self.update_status(f"Erreur lors de l'ouverture du dossier : {e}", "red")

# --- Reprise de __init__ pour l'ordre correct des éléments de l'interface ---
# C'est important que les widgets et leurs placements soient cohérents.
# Le corps de __init__ tel qu'il était est maintenant un ensemble de blocs.
# Les attributs "self.results_text" et "self.status_bar" ont été définis au début de __init__
# et leurs méthodes update_* ont été définies juste après.
# Maintenant, nous reprenons la construction de l'interface dans l'ordre logique.

        # --- Début de la construction de l'interface principale ---
        self.main_layout_frame = ctk.CTkFrame(master)
        self.main_layout_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.main_layout_frame.grid_columnconfigure(0, weight=0)
        self.main_layout_frame.grid_columnconfigure(1, weight=1)
        self.main_layout_frame.grid_rowconfigure(0, weight=1)

        self.left_panel_frame = ctk.CTkFrame(self.main_layout_frame)
        self.left_panel_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        self.task_label = ctk.CTkLabel(self.left_panel_frame, text="Tâches Aircrack-ng :", font=ctk.CTkFont(size=16, weight="bold"))
        self.task_label.pack(pady=(15, 5), padx=10, anchor="w")

        self.tasks_scroll_frame = ctk.CTkScrollableFrame(self.left_panel_frame, width=320, height=600)
        self.tasks_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Dictionnaire des tâches (inchangé)
        self.aircrack_tasks = {
            "--- GESTION DE L'INTERFACE (airmon-ng) ---": "",
            "Détecter Interfaces Wi-Fi": {
                "cmd": "ip -br link show type wireless", # Commande plus rapide pour la détection
                "inputs": [],
                "post_process": self._detect_interfaces,
                "notes": "Détecte les interfaces Wi-Fi disponibles. Nécessite root.",
                "root_required": True
            },
            "Basculer en Mode Moniteur": {
                "cmd": "airmon-ng start {interface}",
                "inputs": ["interface"],
                "notes": "Met l'interface Wi-Fi en mode moniteur (ex: wlan0 -> wlan0mon). Nécessite root.",
                "root_required": True
            },
            "Basculer en Mode Géré": {
                "cmd": "airmon-ng stop {monitor_interface}",
                "inputs": ["monitor_interface"],
                "notes": "Remet l'interface en mode géré (ex: wlan0mon -> wlan0). Nécessite root.",
                "root_required": True
            },
            "Tuer Processus Interferants": {
                "cmd": "airmon-ng check kill",
                "inputs": [],
                "notes": "Arrête les processus (NetworkManager, wpa_supplicant...) qui pourraient gêner le mode moniteur. Recommandé. Nécessite root.",
                "root_required": True
            },

            "--- CAPTURE DE PAQUETS (airodump-ng) ---": "",
            "Scanner APs à Proximité": {
                "cmd": "airodump-ng {monitor_interface}",
                "inputs": ["monitor_interface"],
                "notes": "Affiche les APs et clients en temps réel. Utilisez le bouton STOP pour arrêter. Nécessite root.",
                "root_required": True
            },
            "Capturer Handshake WPA/WPA2": {
                "cmd": "airodump-ng -c {channel} --bssid {bssid} -w \"{output_path}\" {monitor_interface}",
                "inputs": ["monitor_interface", "bssid", "channel"],
                "notes": "Capture le trafic pour un AP. Un fichier .cap sera créé automatiquement. Utilisez le bouton STOP pour arrêter. Nécessite root.",
                "root_required": True
            },
            "Capturer WEP (pour Craquage)": {
                "cmd": "airodump-ng -c {channel} --bssid {bssid} -w \"{output_path}\" {monitor_interface}",
                "inputs": ["monitor_interface", "bssid", "channel"],
                "notes": "Collecte des IVs WEP. Un fichier .cap sera créé automatiquement. Utilisez le bouton STOP pour arrêter. Nécessite root.",
                "root_required": True
            },
            "Capturer sur Canal Spécifique": {
                "cmd": "airodump-ng -c {channel} {monitor_interface}",
                "inputs": ["monitor_interface", "channel"],
                "notes": "Capture tout le trafic sur un canal donné. Utilisez le bouton STOP pour arrêter. Nécessite root.",
                "root_required": True
            },

            "--- ATTAQUES D'INJECTION (aireplay-ng) ---": "",
            "Désauthentifier un Client": {
                "cmd": "aireplay-ng --deauth 0 -a {bssid} -c {client_mac} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid", "client_mac"],
                "notes": "Déconnecte un client pour forcer un nouveau handshake. 0 pour continuer. Utilisez le bouton STOP. Nécessite root.",
                "root_required": True
            },
            "Désauthentifier Tous les Clients d'un AP": {
                "cmd": "aireplay-ng --deauth 0 -a {bssid} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid"],
                "notes": "Déconnecte tous les clients d'un AP. 0 pour continuer. Utilisez le bouton STOP. Nécessite root.",
                "root_required": True
            },
            "Attaque de Rejeu ARP (WEP)": {
                "cmd": "aireplay-ng -3 -b {bssid} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid"],
                "notes": "Réinjecte des paquets ARP pour accélérer la collecte d'IVs WEP. Utilisez le bouton STOP. Nécessite root.",
                "root_required": True
            },
            "Attaque d'Authentification Fausse (WEP)": {
                "cmd": "aireplay-ng -1 0 -a {bssid} -h {your_mac} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid", "your_mac"],
                "notes": "Fausse authentification pour WEP. Remplacez {your_mac} par votre MAC en mode moniteur. Utilisez le bouton STOP. Nécessite root.",
                "root_required": True
            },

            "--- CRAQUAGE DE MOTS DE PASSE (aircrack-ng) ---": "",
            "Craquer WEP (.cap)": {
                "cmd": "aircrack-ng {cap_file}",
                "inputs": ["cap_file"],
                "notes": "Craque une clé WEP à partir d'un fichier .cap. Nécessite suffisamment d'IVs. Ne nécessite généralement pas root.",
                "root_required": False
            },
            "Craquer WPA/WPA2 (.cap + Wordlist)": {
                "cmd": "aircrack-ng -a2 -b {bssid} -w \"{wordlist_file}\" \"{cap_file}\"",
                "inputs": ["cap_file", "wordlist_file", "bssid"],
                "notes": "Craque un handshake WPA/WPA2 avec une liste de mots. Nécessite un handshake et un bon dictionnaire. Ne nécessite généralement pas root.",
                "root_required": False
            },
            "Craquer WPA/WPA2 (sans BSSID)": {
                "cmd": "aircrack-ng -a2 -w \"{wordlist_file}\" \"{cap_file}\"",
                "inputs": ["cap_file", "wordlist_file"],
                "notes": "Tente de craquer le handshake WPA/WPA2 sans BSSID, utile si un seul est présent. Ne nécessite généralement pas root.",
                "root_required": False
            },
            "Afficher Infos du Fichier .cap": {
                "cmd": "aircrack-ng {cap_file}",
                "inputs": ["cap_file"],
                "notes": "Affiche les APs et handshakes trouvés dans un fichier .cap. Utile pour vérifier son contenu. Ne nécessite généralement pas root.",
                "root_required": False
            }
        }

        self.selected_task_data = {}
        self.selected_label_widget = None

        # Création des labels pour chaque tâche (inchangé)
        for i, (text, data) in enumerate(self.aircrack_tasks.items()):
            if text.startswith("---"):
                category_label = ctk.CTkLabel(self.tasks_scroll_frame, text=text, font=ctk.CTkFont(size=13, weight="bold"), text_color="gray")
                category_label.pack(pady=(10, 2), padx=5, anchor="w")
            else:
                task_label = ctk.CTkLabel(self.tasks_scroll_frame, text=text,
                                            font=ctk.CTkFont(size=12), fg_color="transparent",
                                            corner_radius=5, padx=5, pady=2, anchor="w")
                task_label.pack(fill="x", pady=1, padx=5)
                task_label.bind("<Button-1>", lambda event, data=data, label=task_label: self.on_task_label_click(event, data, label))

        self.right_side_container_frame = ctk.CTkFrame(self.main_layout_frame)
        self.right_side_container_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        self.right_side_container_frame.grid_rowconfigure(0, weight=0)
        self.right_side_container_frame.grid_rowconfigure(1, weight=1)

        self.input_frame = ctk.CTkFrame(self.right_side_container_frame)
        self.input_frame.grid(row=0, column=0, sticky="new", padx=0, pady=0)
        
        self.inputs = {} # Dictionnaire pour stocker les références des champs d'entrée

        # Définition des champs d'entrée et ajout à self.inputs
        self._create_dropdown_field("interface", "Interface Wi-Fi (initiale):", [""])
        self.inputs["interface"]["button"] = ctk.CTkButton(self.inputs["interface"]["frame"], text="Actualiser", width=80, command=self._refresh_interfaces)
        self.inputs["interface"]["button"].pack(side="left", padx=(5,0))

        self._create_input_field("monitor_interface", "Interface Moniteur (ex: wlan0mon):")
        self._create_input_field("bssid", "BSSID Cible (MAC AP):")
        self._create_input_field("client_mac", "MAC Client Cible:")
        self._create_input_field("channel", "Canal Wi-Fi (ex: 6):")
        self._create_input_field("your_mac", "Votre MAC (mode moniteur):")

        self._create_file_input_field("cap_file", "Fichier de Capture (.cap):", ".cap")
        self._create_file_input_field("wordlist_file", "Fichier de Wordlist (.txt):", ".txt")

        # Boutons d'action
        self.run_button = ctk.CTkButton(self.input_frame, text="Lancer la Commande", command=self.start_aircrack_ng_command, state="disabled")
        self.run_button.pack(pady=10, padx=10, anchor="e")

        self.stop_button = ctk.CTkButton(self.input_frame, text="STOP Commande", command=self.stop_current_command, state="disabled", fg_color="red", hover_color="#8B0000")
        self.stop_button.pack(pady=5, padx=10, anchor="e")
        
        self.open_capture_dir_button = ctk.CTkButton(self.input_frame, text="Ouvrir Dossier Captures", command=self._open_capture_directory)
        self.open_capture_dir_button.pack(pady=5, padx=10, anchor="e")

        self.notes_label = ctk.CTkLabel(self.input_frame, text="Notes: ", wraplength=480, justify="left", font=ctk.CTkFont(size=12, slant="italic"))
        self.notes_label.pack(pady=(0,10), padx=10, fill="x")

        # Configuration finale de la zone des résultats
        self.results_frame = ctk.CTkFrame(self.right_side_container_frame)
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.results_label = ctk.CTkLabel(self.results_frame, text="Sortie de la commande Aircrack-ng :", font=ctk.CTkFont(size=14, weight="bold"))
        self.results_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        # Maintenant, nous pouvons réassigner et packer results_text correctement
        self.results_text = ctk.CTkTextbox(self.results_frame, wrap="word")
        self.results_text.pack(pady=(0, 10), padx=10, fill="both", expand=True)
        self.results_text.configure(state="disabled")

        # Rafraîchir les interfaces au démarrage (appelé après que tous les widgets nécessaires soient créés)
        self.update_status("Application prête. Détection des interfaces Wi-Fi...", "blue")
        self._refresh_interfaces()


if __name__ == "__main__":
    # Vérifier si le script est lancé avec sudo sur Linux/macOS
    if platform.system() in ["Linux", "Darwin"] and os.geteuid() != 0:
        print("ERREUR: Ce script doit être exécuté avec les privilèges root (sudo) pour fonctionner correctement.")
        print(f"Exemple: sudo python3 {sys.argv[0]}")
        sys.exit(1)
    
    root = ctk.CTk()
    app = AircrackNGApp(root)
    root.mainloop()