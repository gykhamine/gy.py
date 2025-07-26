import customtkinter as ctk
import subprocess
import sys
import os

class SystemdServiceManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestionnaire de Services Systemd")
        self.geometry("900x700")

        # --- Configuration de la grille de la fenêtre principale ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # La liste des services prendra de l'espace

        # --- Cadre des messages de statut ---
        self.status_label = ctk.CTkLabel(self, text="Chargement des services...",
                                         text_color="gray", height=20)
        self.status_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # --- Cadre principal pour la liste et les actions ---
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- Liste des services ---
        self.service_listbox = ctk.CTkScrollableFrame(main_frame, label_text="Services Systemd Détectés (.service)")
        self.service_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.service_listbox.grid_columnconfigure(0, weight=1) # Permet aux éléments de la liste de s'étendre

        self.service_widgets = {} # Dictionnaire pour stocker les widgets de service pour la mise à jour

        # --- Cadre des actions ---
        actions_frame = ctk.CTkFrame(main_frame)
        actions_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        actions_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1) # Répartit les boutons verticalement

        self.selected_service_label = ctk.CTkLabel(actions_frame, text="Service Sélectionné: Aucun", wraplength=150)
        self.selected_service_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        self.start_button = ctk.CTkButton(actions_frame, text="Démarrer", command=lambda: self._execute_action("start"))
        self.start_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.stop_button = ctk.CTkButton(actions_frame, text="Arrêter", command=lambda: self._execute_action("stop"))
        self.stop_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.restart_button = ctk.CTkButton(actions_frame, text="Redémarrer", command=lambda: self._execute_action("restart"))
        self.restart_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.enable_button = ctk.CTkButton(actions_frame, text="Activer (au démarrage)", command=lambda: self._execute_action("enable"))
        self.enable_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.disable_button = ctk.CTkButton(actions_frame, text="Désactiver (au démarrage)", command=lambda: self._execute_action("disable"))
        self.disable_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        self.refresh_button = ctk.CTkButton(actions_frame, text="Actualiser la liste", command=self._list_systemd_services)
        self.refresh_button.grid(row=6, column=0, padx=10, pady=20, sticky="ew")
        
        self.selected_service_name = None # Pour garder en mémoire le service actuellement sélectionné

        # Vérifier si on est sur Linux et avec les droits suffisants
        self._check_environment_and_load_services()

    def _update_status(self, message, color="gray"):
        """Met à jour le texte et la couleur du label de statut."""
        self.status_label.configure(text=message, text_color=color)
        self.update_idletasks()

    def _check_environment_and_load_services(self):
        """Vérifie l'OS et les permissions avant de charger les services."""
        if sys.platform != "linux":
            self._update_status("Ce script est uniquement compatible avec Linux (Systemd).", "red")
            self._disable_all_buttons()
            return
        
        # Vérifier si 'systemctl' est disponible
        try:
            subprocess.run(["systemctl", "--version"], capture_output=True, check=True)
        except FileNotFoundError:
            self._update_status("La commande 'systemctl' est introuvable. Systemd n'est peut-être pas installé.", "red")
            self._disable_all_buttons()
            return

        # Vérifier si le script est lancé avec sudo (pour les actions de contrôle)
        if os.geteuid() == 0: # geteuid() retourne 0 si l'utilisateur est root (sudo)
            self._update_status("Exécuté avec des privilèges administrateur (sudo). Vous pouvez contrôler les services.", "green")
            self._list_systemd_services()
        else:
            self._update_status("Ce script nécessite des privilèges administrateur (sudo) pour Démarrer/Arrêter/Activer/Désactiver les services. Exécutez avec 'sudo python votre_script.py'", "orange")
            self._list_systemd_services(only_status=True) # Charge juste la liste sans permettre les actions
            self._disable_action_buttons()

    def _disable_all_buttons(self):
        """Désactive tous les boutons d'action."""
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="disabled")
        self.restart_button.configure(state="disabled")
        self.enable_button.configure(state="disabled")
        self.disable_button.configure(state="disabled")
        self.refresh_button.configure(state="disabled") # Disable refresh too if systemctl not found

    def _disable_action_buttons(self):
        """Désactive uniquement les boutons d'action qui nécessitent sudo."""
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="disabled")
        self.restart_button.configure(state="disabled")
        self.enable_button.configure(state="disabled")
        self.disable_button.configure(state="disabled")
        # Keep refresh enabled to try again

    def _enable_action_buttons(self):
        """Active les boutons d'action."""
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="normal")
        self.restart_button.configure(state="normal")
        self.enable_button.configure(state="normal")
        self.disable_button.configure(state="normal")

    def _list_systemd_services(self, only_status=False):
        """Liste les services systemd et les affiche dans l'interface."""
        self._update_status("Récupération des services systemd...", "gray")
        
        # Effacer les widgets précédents
        for widget in self.service_listbox.winfo_children():
            widget.destroy()
        self.service_widgets = {} # Réinitialiser le dictionnaire

        try:
            # systemctl list-units --type=service --all: liste tous les services (actifs, inactifs, etc.)
            # --no-legend: Supprime la ligne d'en-tête
            # --plain: Sortie brute, pas de couleurs ou de formatage pour pager
            result = subprocess.run(
                ["systemctl", "list-units", "--type=service", "--all", "--no-legend", "--plain"],
                capture_output=True, text=True, check=True, encoding='utf-8', errors='replace'
            )
            
            services_raw = result.stdout.strip().splitlines()
            
            if not services_raw:
                self._update_status("Aucun service Systemd trouvé.", "orange")
                empty_label = ctk.CTkLabel(self.service_listbox, text="Aucun service Systemd trouvé.")
                empty_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
                return

            row_num = 0
            for line in services_raw:
                parts = line.split()
                if len(parts) >= 4: # S'assurer qu'il y a assez de colonnes
                    service_name = parts[0]
                    load_state = parts[1] # loaded, not-found, etc.
                    active_state = parts[2] # active, inactive, failed, etc.
                    sub_state = parts[3] # running, exited, dead, etc.
                    description = " ".join(parts[4:]) if len(parts) > 4 else ""

                    # Créer une ligne pour chaque service
                    service_frame = ctk.CTkFrame(self.service_listbox)
                    service_frame.grid(row=row_num, column=0, padx=5, pady=2, sticky="ew")
                    service_frame.grid_columnconfigure(0, weight=1) # Le label du service prend de l'espace

                    # Détecter la couleur du statut
                    status_color = "gray"
                    if active_state == "active":
                        status_color = "green"
                    elif active_state == "inactive" or active_state == "dead":
                        status_color = "red"
                    elif active_state == "failed":
                        status_color = "red"
                    elif active_state == "activating" or active_state == "deactivating":
                        status_color = "orange"

                    service_label_text = f"**{service_name}** ({active_state}/{sub_state}) - {description}"
                    service_label = ctk.CTkLabel(service_frame, text=service_label_text,
                                                 justify="left", fg_color="transparent",
                                                 font=ctk.CTkFont(size=12, weight="bold" if active_state == "active" else "normal"),
                                                 text_color=status_color, wraplength=self.service_listbox.winfo_width() - 50) # Ajuster la largeur du wrap
                    service_label.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

                    # Bouton de sélection
                    select_button = ctk.CTkButton(service_frame, text="Sélectionner", width=90,
                                                  command=lambda name=service_name: self._select_service(name))
                    select_button.grid(row=0, column=1, padx=5, pady=2, sticky="e")
                    
                    self.service_widgets[service_name] = {
                        "frame": service_frame,
                        "label": service_label,
                        "select_button": select_button,
                        "active_state": active_state,
                        "sub_state": sub_state
                    }
                    row_num += 1
            
            if not only_status: # Si le script a les permissions
                self._update_status(f"{len(self.service_widgets)} services Systemd listés. Sélectionnez un service pour agir.", "blue")
                self._enable_action_buttons()
            else: # Si le script n'a pas les permissions sudo
                self._update_status(f"{len(self.service_widgets)} services Systemd listés. Permissions insuffisantes pour agir.", "orange")


        except subprocess.CalledProcessError as e:
            self._update_status(f"Erreur lors de la liste des services: {e.stderr}", "red")
            error_label = ctk.CTkLabel(self.service_listbox, text=f"Erreur: Impossible de lister les services.\n{e.stderr}", text_color="red")
            error_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            self._disable_action_buttons() # Désactiver les actions si la liste échoue
        except Exception as e:
            self._update_status(f"Une erreur inattendue est survenue: {e}", "red")
            error_label = ctk.CTkLabel(self.service_listbox, text=f"Erreur inattendue: {e}", text_color="red")
            error_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            self._disable_action_buttons()

    def _select_service(self, service_name):
        """Sélectionne un service et met à jour le label."""
        # Désélectionner visuellement le service précédent
        if self.selected_service_name and self.selected_service_name in self.service_widgets:
            prev_frame = self.service_widgets[self.selected_service_name]["frame"]
            prev_frame.configure(fg_color=ctk.CTkFrame(self).cget("fg_color")) # Réinitialiser la couleur de fond

        self.selected_service_name = service_name
        self.selected_service_label.configure(text=f"Service Sélectionné: {service_name}")
        
        # Mettre en évidence le service sélectionné
        if service_name in self.service_widgets:
            current_frame = self.service_widgets[service_name]["frame"]
            current_frame.configure(fg_color=self.cget("fg_color")[1]) # Utilise la couleur secondaire de la fenêtre

        self._update_status(f"Service '{service_name}' sélectionné.", "blue")

    def _execute_action(self, action):
        """Exécute une action systemctl sur le service sélectionné."""
        if not self.selected_service_name:
            self._update_status("Veuillez sélectionner un service d'abord.", "orange")
            return

        if os.geteuid() != 0: # Double-vérification des permissions
            self._update_status("Erreur: Les actions de contrôle nécessitent des privilèges administrateur (sudo).", "red")
            return
        
        # Demander confirmation pour les actions dangereuses
        if action in ["stop", "disable"] and not ctk.CTkMessagebox.ask_yes_no(
            f"Confirmer l'action '{action}'",
            f"Êtes-vous sûr de vouloir '{action}' le service '{self.selected_service_name}'? Cela pourrait affecter le système.",
            icon="warning"
        ):
            self._update_status(f"Action '{action}' annulée pour '{self.selected_service_name}'.", "gray")
            return

        self._update_status(f"Exécution de '{action}' sur '{self.selected_service_name}'...", "orange")
        self.update_idletasks() # Force GUI update

        try:
            command = ["systemctl", action, self.selected_service_name]
            result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', errors='replace')
            
            # Recharger l'état du service après l'action
            self._list_systemd_services()
            self._select_service(self.selected_service_name) # Re-sélectionner pour rafraîchir la couleur/statut

            self._update_status(f"'{action}' sur '{self.selected_service_name}' réussi. Sortie: {result.stdout.strip()}", "green")

        except subprocess.CalledProcessError as e:
            self._update_status(f"Erreur lors de '{action}' sur '{self.selected_service_name}': {e.stderr.strip()}", "red")
        except Exception as e:
            self._update_status(f"Une erreur inattendue est survenue lors de l'action '{action}': {e}", "red")
        
        self.after(5000, lambda: self._update_status(f"Prêt. Service sélectionné: {self.selected_service_name}", "gray"))


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = SystemdServiceManagerApp()
    app.mainloop()