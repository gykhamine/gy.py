import customtkinter as ctk
from threading import Thread
import subprocess
import sys
import tkinter.filedialog as filedialog # Pour le sélecteur de fichiers

class AircrackNGApp:
    def __init__(self, master):
        self.master = master
        master.title("Aircrack-ng GUI Simplifiée")
        master.geometry("1100x780") # Taille de fenêtre ajustée

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # --- Cadre Principal (utilisation de grid) ---
        self.main_layout_frame = ctk.CTkFrame(master)
        self.main_layout_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.main_layout_frame.grid_columnconfigure(0, weight=0) # Colonne gauche (tâches)
        self.main_layout_frame.grid_columnconfigure(1, weight=1) # Colonne droite (entrées + résultats)
        self.main_layout_frame.grid_rowconfigure(0, weight=1)

        # --- Cadre Gauche pour la Liste Défilante des Tâches Aircrack-ng ---
        self.left_panel_frame = ctk.CTkFrame(self.main_layout_frame)
        self.left_panel_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        self.task_label = ctk.CTkLabel(self.left_panel_frame, text="Tâches Aircrack-ng :", font=ctk.CTkFont(size=16, weight="bold"))
        self.task_label.pack(pady=(15, 5), padx=10, anchor="w")

        self.tasks_scroll_frame = ctk.CTkScrollableFrame(self.left_panel_frame, width=320, height=600)
        self.tasks_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Dictionnaire des tâches Aircrack-ng
        # Chaque tâche a un template de commande, des champs d'entrée requis et des notes.
        self.aircrack_tasks = {
            "--- GESTION DE L'INTERFACE (airmon-ng) ---": "",
            "Démarrer Mode Moniteur": {
                "cmd": "airmon-ng start {interface}",
                "inputs": ["interface"],
                "notes": "Met l'interface Wi-Fi en mode moniteur. Ex: wlan0 -> wlan0mon. Nécessite root.",
                "root_required": True
            },
            "Arrêter Mode Moniteur": {
                "cmd": "airmon-ng stop {monitor_interface}",
                "inputs": ["monitor_interface"],
                "notes": "Arrête le mode moniteur sur l'interface. Ex: wlan0mon -> wlan0. Nécessite root.",
                "root_required": True
            },
            "Vérifier Processus Interferants": {
                "cmd": "airmon-ng check kill",
                "inputs": [],
                "notes": "Arrête les processus qui pourraient interférer avec le mode moniteur (NetworkManager, wpa_supplicant...). Nécessite root.",
                "root_required": True
            },

            "--- CAPTURE DE PAQUETS (airodump-ng) ---": "",
            "Scanner APs à Proximité": {
                "cmd": "airodump-ng {monitor_interface}",
                "inputs": ["monitor_interface"],
                "notes": "Affiche les points d'accès (APs) et les clients. Arrêter avec Ctrl+C dans le terminal où le script est lancé. Nécessite root.",
                "root_required": True
            },
            "Capturer Handshake WPA/WPA2": {
                "cmd": "airodump-ng -c {channel} --bssid {bssid} -w {output_file} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid", "channel", "output_file"],
                "notes": "Capture le trafic pour un AP. Attendez un handshake. (Ex: output_file sans .cap, il l'ajoutera). Nécessite root.",
                "root_required": True
            },
            "Capturer WEP (pour Craquage)": {
                "cmd": "airodump-ng -c {channel} --bssid {bssid} -w {output_file} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid", "channel", "output_file"],
                "notes": "Collecte des IVs WEP. Nécessite root.",
                "root_required": True
            },
            "Capturer sur Canal Spécifique": {
                "cmd": "airodump-ng -c {channel} {monitor_interface}",
                "inputs": ["monitor_interface", "channel"],
                "notes": "Capture tout le trafic sur un canal donné. Nécessite root.",
                "root_required": True
            },

            "--- ATTAQUES D'INJECTION (aireplay-ng) ---": "",
            "Désauthentifier un Client": {
                "cmd": "aireplay-ng --deauth 0 -a {bssid} -c {client_mac} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid", "client_mac"],
                "notes": "Déconnecte un client pour forcer un nouveau handshake. 0 pour continuer. Nécessite root.",
                "root_required": True
            },
            "Désauthentifier Tous les Clients d'un AP": {
                "cmd": "aireplay-ng --deauth 0 -a {bssid} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid"],
                "notes": "Déconnecte tous les clients. 0 pour continuer. Nécessite root.",
                "root_required": True
            },
            "Attaque de Rejeu ARP (WEP)": {
                "cmd": "aireplay-ng -3 -b {bssid} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid"],
                "notes": "Réinjecte des paquets ARP pour accélérer la collecte d'IVs WEP. Nécessite root.",
                "root_required": True
            },
            "Attaque d'Authentification Fausse (WEP)": {
                "cmd": "aireplay-ng -1 0 -a {bssid} -h {your_mac} {monitor_interface}",
                "inputs": ["monitor_interface", "bssid", "your_mac"],
                "notes": "Fausse authentification pour WEP. Remplacez {your_mac} par votre adresse MAC en mode moniteur. Nécessite root.",
                "root_required": True
            },

            "--- CRAQUAGE DE MOTS DE PASSE (aircrack-ng) ---": "",
            "Craquer WEP (.cap)": {
                "cmd": "aircrack-ng {cap_file}",
                "inputs": ["cap_file"],
                "notes": "Craque une clé WEP à partir d'un fichier .cap. Nécessite suffisamment d'IVs. Peut ne pas nécessiter root si le fichier est accessible.",
                "root_required": False
            },
            "Craquer WPA/WPA2 (.cap + Wordlist)": {
                "cmd": "aircrack-ng -a2 -b {bssid} -w {wordlist_file} {cap_file}",
                "inputs": ["cap_file", "wordlist_file", "bssid"],
                "notes": "Craque un handshake WPA/WPA2 avec une liste de mots. Nécessite root pour accéder au GPU si pris en charge, mais pas toujours nécessaire pour l'outil lui-même si le fichier est accessible.",
                "root_required": False
            },
            "Craquer WPA/WPA2 (sans BSSID)": {
                "cmd": "aircrack-ng -a2 -w {wordlist_file} {cap_file}",
                "inputs": ["cap_file", "wordlist_file"],
                "notes": "Tente de craquer le handshake WPA/WPA2 sans BSSID, utile si le cap ne contient qu'un seul handshake. Nécessite root pour GPU/fichier.",
                "root_required": False
            },
            "Afficher Informations du Fichier .cap": {
                "cmd": "aircrack-ng {cap_file}", # Aircrack-ng affiche info si pas de wordlist
                "inputs": ["cap_file"],
                "notes": "Affiche les APs et handshakes trouvés dans un fichier .cap. Utile pour vérifier. Nécessite root si le fichier est protégé.",
                "root_required": False
            }
        }

        self.selected_task_data = {} # Pour stocker les données de la tâche sélectionnée
        self.selected_label_widget = None # Pour garder une référence au label actuellement sélectionné

        # Création des labels pour chaque tâche
        for i, (text, data) in enumerate(self.aircrack_tasks.items()):
            if text.startswith("---"): # C'est un titre de catégorie
                category_label = ctk.CTkLabel(self.tasks_scroll_frame, text=text, font=ctk.CTkFont(size=13, weight="bold"), text_color="gray")
                category_label.pack(pady=(10, 2), padx=5, anchor="w")
            else: # C'est une tâche
                task_label = ctk.CTkLabel(self.tasks_scroll_frame, text=text,
                                            font=ctk.CTkFont(size=12), fg_color="transparent",
                                            corner_radius=5, padx=5, pady=2, anchor="w")
                task_label.pack(fill="x", pady=1, padx=5)
                task_label.bind("<Button-1>", lambda event, data=data, label=task_label: self.on_task_label_click(event, data, label))

        # --- Cadre Conteneur Droit (pour les entrées et les résultats) ---
        self.right_side_container_frame = ctk.CTkFrame(self.main_layout_frame)
        self.right_side_container_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        self.right_side_container_frame.grid_rowconfigure(0, weight=0) # Ligne du haut (entrées)
        self.right_side_container_frame.grid_rowconfigure(1, weight=1) # Ligne du bas (résultats)

        # --- Cadre en Haut à Droite pour les Champs d'Entrée Dynamiques ---
        self.input_frame = ctk.CTkFrame(self.right_side_container_frame)
        self.input_frame.grid(row=0, column=0, sticky="new", padx=0, pady=0)
        
        # Initialisation de tous les champs d'entrée, cachés par défaut
        self.inputs = {}

        self._create_input_field("interface", "Interface Wi-Fi (ex: wlan0):")
        self._create_input_field("monitor_interface", "Interface Moniteur (ex: wlan0mon):")
        self._create_input_field("bssid", "BSSID Cible (MAC AP):")
        self._create_input_field("client_mac", "MAC Client Cible:")
        self._create_input_field("channel", "Canal Wi-Fi (ex: 6):")
        self._create_input_field("your_mac", "Votre MAC (mode moniteur):")

        self._create_file_input_field("output_file", "Fichier de Sortie (.cap):", ".cap")
        self._create_file_input_field("cap_file", "Fichier de Capture (.cap):", ".cap")
        self._create_file_input_field("wordlist_file", "Fichier de Wordlist (.txt):", ".txt")

        # Bouton Lancer le Scan
        self.run_button = ctk.CTkButton(self.input_frame, text="Lancer la Commande Aircrack-ng", command=self.start_aircrack_ng_command, state="disabled")
        self.run_button.pack(pady=10, padx=10, anchor="e")

        # Zone pour afficher les notes
        self.notes_label = ctk.CTkLabel(self.input_frame, text="Notes: ", wraplength=450, justify="left", font=ctk.CTkFont(size=12, slant="italic"))
        self.notes_label.pack(pady=(0,10), padx=10, fill="x")

        # --- Zone d'affichage des résultats (en bas à droite) ---
        self.results_frame = ctk.CTkFrame(self.right_side_container_frame)
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        self.results_label = ctk.CTkLabel(self.results_frame, text="Sortie de la commande Aircrack-ng :", font=ctk.CTkFont(size=14, weight="bold"))
        self.results_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.results_text = ctk.CTkTextbox(self.results_frame, wrap="word")
        self.results_text.pack(pady=(0, 10), padx=10, fill="both", expand=True)
        self.results_text.configure(state="disabled")

        # --- Barre de statut ---
        self.status_bar = ctk.CTkLabel(master, text="Prêt (Sélectionnez une tâche)", anchor="w", font=ctk.CTkFont(size=12))
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=10)

    def _create_input_field(self, name, label_text, default_value=""):
        """Crée et initialise un champ d'entrée générique."""
        frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w")
        entry = ctk.CTkEntry(frame, width=300)
        if default_value:
            entry.insert(0, default_value)
        
        self.inputs[name] = {"frame": frame, "label": label, "entry": entry}

    def _create_file_input_field(self, name, label_text, file_type):
        """Crée et initialise un champ d'entrée de fichier avec un bouton de sélection."""
        frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w")
        entry = ctk.CTkEntry(frame, width=250)
        button = ctk.CTkButton(frame, text="Parcourir...", width=80, 
                                command=lambda n=name, ft=file_type: self._browse_file(n, ft))
        
        self.inputs[name] = {"frame": frame, "label": label, "entry": entry, "button": button}

    def _browse_file(self, entry_name, file_type):
        """Ouvre une boîte de dialogue pour sélectionner un fichier."""
        initial_dir = "./"
        if "cap" in file_type:
            file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Capture Files", "*.cap *.pcap"), ("All Files", "*.*")])
        elif "txt" in file_type:
            file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        else:
            file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("All Files", "*.*")])

        if file_path:
            self.inputs[entry_name]["entry"].delete(0, "end")
            self.inputs[entry_name]["entry"].insert(0, file_path)

    def _hide_all_inputs(self):
        """Cache tous les champs d'entrée."""
        for input_widgets in self.inputs.values():
            input_widgets["frame"].pack_forget()

    def on_task_label_click(self, event, task_data, label):
        """
        Gère le clic sur un label de tâche.
        Met en surbrillance l'option sélectionnée et affiche les champs d'entrée pertinents.
        """
        if self.selected_label_widget:
            self.selected_label_widget.configure(fg_color="transparent")
        
        self.selected_label_widget = label
        self.selected_label_widget.configure(fg_color=ctk.ThemeManager.theme["CTkOptionMenu"]["button_color"])
        
        self.selected_task_data = task_data
        self.update_status(f"Tâche sélectionnée : {label.cget('text')} - Prête à être configurée.", "black")
        self.run_button.configure(state="normal") # Activer le bouton de lancement

        self._hide_all_inputs() # Cache tous les champs d'abord

        # Affiche seulement les champs requis pour la tâche sélectionnée
        for input_name in task_data["inputs"]:
            if input_name in self.inputs:
                frame = self.inputs[input_name]["frame"]
                label_widget = self.inputs[input_name]["label"]
                entry_widget = self.inputs[input_name]["entry"]
                
                frame.pack(fill="x", pady=5, padx=10)
                label_widget.pack(side="left", padx=(0, 5))
                entry_widget.pack(side="left", expand=True, fill="x")
                if "button" in self.inputs[input_name]:
                    self.inputs[input_name]["button"].pack(side="left", padx=(5,0))
            else:
                self.update_status(f"Erreur: Champ d'entrée inconnu requis: {input_name}", "red")
        
        # Afficher les notes spécifiques à la tâche
        notes = task_data.get("notes", "Aucune note pour cette tâche.")
        if task_data.get("root_required", False):
            notes = "⚠️ Nécessite des **privilèges root (sudo)** pour fonctionner correctement. " + notes
            self.notes_label.configure(text_color="red")
        else:
            self.notes_label.configure(text_color="gray")
        self.notes_label.configure(text=f"Notes: {notes}")
        self.notes_label.pack(pady=(0,10), padx=10, fill="x")
        self.run_button.pack_forget() # Repack button to be at the bottom of inputs
        self.run_button.pack(pady=10, padx=10, anchor="e")


    def start_aircrack_ng_command(self):
        """Construit et lance la commande Aircrack-ng."""
        task_data = self.selected_task_data
        if not task_data:
            self.update_status("Veuillez sélectionner une tâche Aircrack-ng.", "red")
            return

        command_template = task_data["cmd"]
        required_inputs = task_data["inputs"]
        
        # Collecte les valeurs des champs d'entrée
        cmd_vars = {}
        for input_name in required_inputs:
            if input_name in self.inputs:
                value = self.inputs[input_name]["entry"].get().strip()
                if not value:
                    self.update_status(f"Erreur: Le champ '{self.inputs[input_name]['label'].cget('text')}' est requis.", "red")
                    return
                cmd_vars[input_name] = value
            else:
                self.update_status(f"Erreur interne: Champ '{input_name}' non trouvé.", "red")
                return

        # Construction de la commande finale
        try:
            full_command_str = command_template.format(**cmd_vars)
            nmap_command_parts = full_command_str.split() # Simple split for now
        except KeyError as e:
            self.update_status(f"Erreur de configuration: Variable manquante pour la commande ({e}).", "red")
            return

        self.update_status(f"Exécution de : {full_command_str}...", "blue")
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("end", f"Exécution : {full_command_str}\n\n")
        self.results_text.configure(state="disabled")

        # Exécution de la commande dans un thread séparé
        command_thread = Thread(target=self._run_subprocess, args=(nmap_command_parts,))
        command_thread.start()

    def _run_subprocess(self, command_list):
        """Exécute une commande shell et capture sa sortie."""
        try:
            # Popen pour gérer la sortie en temps réel ou de longues exécutions
            process = subprocess.Popen(
                command_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1 # Line-buffered output
            )

            # Lecture de la sortie en temps réel
            while True:
                output_line = process.stdout.readline()
                if output_line == '' and process.poll() is not None:
                    break
                if output_line:
                    self.master.after(0, self.update_results, output_line) # Update GUI from main thread
            
            # Attendre la fin du processus et capturer le reste de la sortie et les erreurs
            remaining_output, stderr_output = process.communicate()
            if remaining_output:
                self.master.after(0, self.update_results, remaining_output)
            
            if stderr_output:
                self.master.after(0, self.update_results, "\n--- Sortie Erreur (stderr) ---\n" + stderr_output)
            
            return_code = process.returncode
            if return_code != 0:
                self.master.after(0, self.update_status, f"Commande terminée avec erreur: {return_code}", "red")
            else:
                self.master.after(0, self.update_status, "Commande terminée avec succès.", "green")

        except FileNotFoundError:
            error_message = f"Erreur : La commande '{command_list[0]}' n'a pas été trouvée.\n" \
                            "Veuillez vous assurer qu'Aircrack-ng est installé et que son chemin est configuré (PATH)."
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

    def update_results(self, text):
        """Met à jour la zone de texte des résultats."""
        self.results_text.configure(state="normal")
        self.results_text.insert("end", text)
        self.results_text.configure(state="disabled")
        self.results_text.see("end")

    def update_status(self, message, color="black"):
        """Met à jour la barre de statut."""
        self.status_bar.configure(text=message, text_color=color)

if __name__ == "__main__":
    root = ctk.CTk()
    app = AircrackNGApp(root)
    root.mainloop()