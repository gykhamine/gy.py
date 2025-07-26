import customtkinter as ctk
import subprocess
import sys
import os
import re

class FirewalldManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestionnaire de Pare-feu Firewalld")
        self.geometry("1000x750")

        # --- Configure main window grid ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # The tabview will expand vertically

        # --- Status label ---
        self.status_label = ctk.CTkLabel(self, text="Vérification de Firewalld...",
                                         text_color="gray", height=20)
        self.status_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # --- Tabview for different sections ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # --- Tab 1: Zone Info ---
        self.tab_zones = self.tabview.add("Informations sur les Zones")
        self.tab_zones.grid_columnconfigure(0, weight=1)
        self.tab_zones.grid_rowconfigure(2, weight=1) # Content textbox will expand

        ctk.CTkLabel(self.tab_zones, text="Zone Active Actuelle:").grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")
        self.active_zone_label = ctk.CTkLabel(self.tab_zones, text="Chargement...", font=ctk.CTkFont(size=14, weight="bold"))
        self.active_zone_label.grid(row=1, column=0, padx=10, pady=(0,10), sticky="w")

        ctk.CTkLabel(self.tab_zones, text="Détails de la Zone (Services, Ports, etc.):").grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")
        self.zone_details_textbox = ctk.CTkTextbox(self.tab_zones, wrap="word", height=200, font=("Courier New", 10))
        self.zone_details_textbox.grid(row=3, column=0, padx=10, pady=(0,10), sticky="nsew")
        self.zone_details_textbox.configure(state="disabled")

        ctk.CTkLabel(self.tab_zones, text="Toutes les Zones Disponibles:").grid(row=4, column=0, padx=10, pady=(10,0), sticky="w")
        self.all_zones_textbox = ctk.CTkTextbox(self.tab_zones, wrap="word", height=100, font=("Courier New", 10))
        self.all_zones_textbox.grid(row=5, column=0, padx=10, pady=(0,10), sticky="nsew")
        self.all_zones_textbox.configure(state="disabled")

        self.reload_button_zones = ctk.CTkButton(self.tab_zones, text="Recharger Firewalld", command=self._reload_firewalld)
        self.reload_button_zones.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        # --- Tab 2: Add/Remove Services/Ports ---
        self.tab_services_ports = self.tabview.add("Ajouter/Supprimer Services & Ports")
        self.tab_services_ports.grid_columnconfigure(0, weight=1)
        self.tab_services_ports.grid_columnconfigure(1, weight=1)

        # Service management
        ctk.CTkLabel(self.tab_services_ports, text="Gérer les Services:").grid(row=0, column=0, columnspan=2, padx=10, pady=(10,0), sticky="w")
        self.service_entry = ctk.CTkEntry(self.tab_services_ports, placeholder_text="Nom du service (ex: http, ssh)")
        self.service_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.add_service_button = ctk.CTkButton(self.tab_services_ports, text="Ajouter Service (Permanent)", command=lambda: self._add_remove_rule("service", self.service_entry.get(), "add"))
        self.add_service_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.remove_service_button = ctk.CTkButton(self.tab_services_ports, text="Supprimer Service (Permanent)", command=lambda: self._add_remove_rule("service", self.service_entry.get(), "remove"))
        self.remove_service_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Port management
        ctk.CTkLabel(self.tab_services_ports, text="Gérer les Ports:").grid(row=3, column=0, columnspan=2, padx=10, pady=(10,0), sticky="w")
        self.port_entry = ctk.CTkEntry(self.tab_services_ports, placeholder_text="Port/Protocole (ex: 80/tcp, 443/udp)")
        self.port_entry.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
        self.add_port_button = ctk.CTkButton(self.tab_services_ports, text="Ajouter Port (Permanent)", command=lambda: self._add_remove_rule("port", self.port_entry.get(), "add"))
        self.add_port_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        
        self.remove_port_button = ctk.CTkButton(self.tab_services_ports, text="Supprimer Port (Permanent)", command=lambda: self._add_remove_rule("port", self.port_entry.get(), "remove"))
        self.remove_port_button.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        self.reload_button_services_ports = ctk.CTkButton(self.tab_services_ports, text="Recharger Firewalld (Appliquer les changements)", command=self._reload_firewalld)
        self.reload_button_services_ports.grid(row=6, column=0, columnspan=2, padx=10, pady=20, sticky="ew")


        self.active_zone = "public" # Default active zone, will be updated dynamically

        # Initial check and load
        self._check_environment_and_load_firewalld()

    def _update_textbox(self, textbox, content):
        """Updates the content of a CTkTextbox and sets it to read-only."""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", content)
        textbox.configure(state="disabled")

    def _update_status(self, message, color="gray"):
        """Updates the text and color of the status label."""
        self.status_label.configure(text=message, text_color=color)
        self.update_idletasks()

    def _check_environment_and_load_firewalld(self):
        """Verifies OS, firewalld availability, and sudo permissions."""
        if sys.platform != "linux":
            self._update_status("Ce script est uniquement compatible avec Linux (Firewalld).", "red")
            self._disable_all_controls()
            return
        
        try:
            subprocess.run(["firewall-cmd", "--version"], capture_output=True, check=True)
        except FileNotFoundError:
            self._update_status("La commande 'firewall-cmd' est introuvable. Firewalld n'est peut-être pas installé ou en cours d'exécution.", "red")
            self._disable_all_controls()
            return

        if os.geteuid() == 0:
            self._update_status("Exécuté avec des privilèges administrateur (sudo). Vous pouvez gérer Firewalld.", "green")
            self._load_firewalld_info()
        else:
            self._update_status("Ce script nécessite des privilèges administrateur (sudo) pour gérer Firewalld. Exécutez avec 'sudo python votre_script.py'", "orange")
            self._disable_all_controls() # Disable for safety if not sudo

    def _disable_all_controls(self):
        """Disables all interactive elements."""
        self.service_entry.configure(state="disabled")
        self.port_entry.configure(state="disabled")
        self.add_service_button.configure(state="disabled")
        self.remove_service_button.configure(state="disabled")
        self.add_port_button.configure(state="disabled")
        self.remove_port_button.configure(state="disabled")
        self.reload_button_zones.configure(state="disabled")
        self.reload_button_services_ports.configure(state="disabled")

    def _enable_all_controls(self):
        """Enables all interactive elements."""
        self.service_entry.configure(state="normal")
        self.port_entry.configure(state="normal")
        self.add_service_button.configure(state="normal")
        self.remove_service_button.configure(state="normal")
        self.add_port_button.configure(state="normal")
        self.remove_port_button.configure(state="normal")
        self.reload_button_zones.configure(state="normal")
        self.reload_button_services_ports.configure(state="normal")

    def _run_firewall_cmd(self, command_args, sudo_required=True):
        """Helper to run firewall-cmd commands safely."""
        base_command = ["firewall-cmd"]
        if sudo_required and os.geteuid() != 0:
            self._update_status("Erreur: Privilèges administrateur (sudo) requis pour cette opération.", "red")
            return None, "Privilèges insuffisants."

        try:
            result = subprocess.run(
                base_command + command_args,
                capture_output=True,
                text=True,
                check=True, # Raise CalledProcessError if command fails
                encoding='utf-8',
                errors='replace'
            )
            return result.stdout.strip(), None
        except subprocess.CalledProcessError as e:
            return None, e.stderr.strip()
        except FileNotFoundError:
            return None, "La commande 'firewall-cmd' est introuvable."
        except Exception as e:
            return None, f"Une erreur inattendue est survenue: {e}"

    def _load_firewalld_info(self):
        """Loads and displays current firewalld zone info."""
        self._update_status("Chargement des informations Firewalld...", "gray")
        self._enable_all_controls() # Ensure controls are enabled if sudo

        # Get active zone
        output, error = self._run_firewall_cmd(["--get-active-zone"], sudo_required=False)
        if error:
            self._update_status(f"Erreur lors de la récupération de la zone active: {error}", "red")
            self.active_zone_label.configure(text="Erreur!")
            self._update_textbox(self.zone_details_textbox, "Impossible de récupérer la zone active.")
            return
        
        self.active_zone = output.strip() if output else "public" # Default to public if empty
        self.active_zone_label.configure(text=self.active_zone)

        # List all zone details
        output, error = self._run_firewall_cmd([f"--zone={self.active_zone}", "--list-all"], sudo_required=False)
        if error:
            self._update_status(f"Erreur lors de la liste des détails de la zone: {error}", "red")
            self._update_textbox(self.zone_details_textbox, f"Impossible de lister les détails de la zone '{self.active_zone}':\n{error}")
        else:
            self._update_textbox(self.zone_details_textbox, output)
            self._update_status(f"Informations sur la zone '{self.active_zone}' chargées.", "blue")

        # List all zones
        output, error = self._run_firewall_cmd(["--get-zones"], sudo_required=False)
        if error:
            self._update_status(f"Erreur lors de la liste de toutes les zones: {error}", "red")
            self._update_textbox(self.all_zones_textbox, f"Impossible de lister toutes les zones:\n{error}")
        else:
            self._update_textbox(self.all_zones_textbox, output.replace(" ", "\n")) # One zone per line

    def _add_remove_rule(self, rule_type, rule_value, action):
        """Adds or removes a service or port."""
        if not rule_value:
            self._update_status(f"Veuillez entrer une valeur pour le {rule_type}.", "orange")
            return
        
        confirm_message = f"Êtes-vous sûr de vouloir '{action}' le {rule_type} '{rule_value}' dans la zone '{self.active_zone}' de manière PERMANENTE ?\n" \
                          "Un rechargement sera nécessaire pour appliquer les changements."
        
        if not ctk.CTkMessagebox.ask_yes_no(f"Confirmer l'{action.capitalize()} du {rule_type}", confirm_message, icon="warning"):
            self._update_status(f"Action '{action}' annulée pour le {rule_type} '{rule_value}'.", "gray")
            return

        command_args = [f"--zone={self.active_zone}"]
        if rule_type == "service":
            command_args.append(f"--{action}-service={rule_value}")
        elif rule_type == "port":
            command_args.append(f"--{action}-port={rule_value}")
        
        command_args.append("--permanent") # Apply permanently

        self._update_status(f"Exécution de '{action}' {rule_type} '{rule_value}'...", "orange")
        self.update_idletasks()

        output, error = self._run_firewall_cmd(command_args, sudo_required=True)

        if error:
            self._update_status(f"Erreur lors de l'{action} du {rule_type}: {error}", "red")
        else:
            self._update_status(f"'{action.capitalize()}' du {rule_type} '{rule_value}' réussi. N'oubliez pas de recharger Firewalld !", "green")
            # We don't reload automatically here, force user to click reload

    def _reload_firewalld(self):
        """Reloads the firewalld configuration."""
        if not ctk.CTkMessagebox.ask_yes_no(
            "Confirmer le Rechargement",
            "Êtes-vous sûr de vouloir recharger Firewalld ? Tous les changements temporaires seront perdus et les changements permanents seront appliqués.",
            icon="question"
        ):
            self._update_status("Rechargement de Firewalld annulé.", "gray")
            return

        self._update_status("Rechargement de Firewalld...", "orange")
        self.update_idletasks()

        output, error = self._run_firewall_cmd(["--reload"], sudo_required=True)

        if error:
            self._update_status(f"Erreur lors du rechargement de Firewalld: {error}", "red")
        else:
            self._update_status("Firewalld rechargé avec succès. Les changements sont appliqués.", "green")
            self._load_firewalld_info() # Refresh info after reload
        
        self.after(5000, lambda: self._update_status("Prêt. Firewalld géré.", "gray"))


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = FirewalldManagerApp()
    app.mainloop()