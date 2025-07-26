import customtkinter as ctk
import subprocess
import sys
import os
import re

# Attempt to import CTkMessagebox
try:
    # This is the expected path for newer versions
    from customtkinter.windows.widgets.ctk_messagebox import CTkMessagebox
except ImportError:
    # Fallback for slightly older versions where it might be directly in ctk,
    # or if the user has manually placed ctk_messagebox.py
    try:
        # If it's directly available under the main customtkinter module
        if hasattr(ctk, 'CTkMessagebox'):
            CTkMessagebox = ctk.CTkMessagebox
        else:
            # If it's a very old version or missing, this print will be shown
            print("Error: CTkMessagebox is not available. Please ensure customtkinter is up-to-date or manually add ctk_messagebox.py.")
            # Define a dummy class to prevent crashes, but confirmation dialogs won't work
            class CTkMessagebox:
                @staticmethod
                def ask_yes_no(title, message, icon):
                    print(f"ATTENTION: {title}\n{message} (Répondez 'oui' ou 'non' dans la console, car CTkMessagebox est manquant):")
                    response = input().lower()
                    return response == 'oui' or response == 'yes'
                @staticmethod
                def show_info(title, message, icon):
                    print(f"INFO: {title}\n{message}")
                @staticmethod
                def show_error(title, message, icon):
                    print(f"ERREUR: {title}\n{message}")
    except Exception as e:
        print(f"Critical Error during CTkMessagebox fallback: {e}. Application may not function correctly.")
        # If even the fallback causes an error, create a minimal dummy to prevent immediate crash
        class CTkMessagebox:
            @staticmethod
            def ask_yes_no(title, message, icon):
                print(f"WARNING: CTkMessagebox is completely unavailable. Cannot show dialog: {message}")
                return True # Default to yes to allow program to continue, but notify user
            @staticmethod
            def show_info(title, message, icon): pass
            @staticmethod
            def show_error(title, message, icon): pass


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
        self.zone_details_textbox.configure(state="disabled") # This textbox is already scrollable

        ctk.CTkLabel(self.tab_zones, text="Toutes les Zones Disponibles:").grid(row=4, column=0, padx=10, pady=(10,0), sticky="w")
        self.all_zones_textbox = ctk.CTkTextbox(self.tab_zones, wrap="word", height=100, font=("Courier New", 10))
        self.all_zones_textbox.grid(row=5, column=0, padx=10, pady=(0,10), sticky="nsew")
        self.all_zones_textbox.configure(state="disabled") # This textbox is already scrollable

        self.reload_button_zones = ctk.CTkButton(self.tab_zones, text="Recharger Firewalld", command=self._reload_firewalld)
        self.reload_button_zones.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        # --- Tab 2: Manage Ports Only ---
        self.tab_ports = self.tabview.add("Gérer les Ports") # Renamed tab for clarity
        self.tab_ports.grid_columnconfigure(0, weight=1)
        self.tab_ports.grid_columnconfigure(1, weight=1)

        # Port management
        ctk.CTkLabel(self.tab_ports, text="Gérer les Ports:").grid(row=0, column=0, columnspan=2, padx=10, pady=(10,0), sticky="w")
        
        self.common_ports = [
            "", # Added an empty option to start
            "20/tcp (FTP Data)", "21/tcp (FTP Control)", "22/tcp (SSH)", "23/tcp (Telnet)", "25/tcp (SMTP)", 
            "53/tcp (DNS)", "53/udp (DNS)", "67/udp (DHCP Client)", "68/udp (DHCP Server)",
            "80/tcp (HTTP)", "110/tcp (POP3)", "143/tcp (IMAP)", "161/udp (SNMP)", "162/udp (SNMP Trap)",
            "389/tcp (LDAP)", "443/tcp (HTTPS)", "445/tcp (SMB/CIFS)", "587/tcp (SMTP Submission)", 
            "636/tcp (LDAPS)", "993/tcp (IMAPS)", "995/tcp (POP3S)", "1723/tcp (PPTP)",
            "3306/tcp (MySQL)", "3389/tcp (RDP)", "5432/tcp (PostgreSQL)", 
            "5900/tcp (VNC)", "8000/tcp (HTTP Alt)", "8080/tcp (HTTP Alt)", "8443/tcp (HTTPS Alt)",
            "10000/tcp (Webmin)", "10000/udp (Webmin)", "27017/tcp (MongoDB)",
            "5000/tcp (UPnP/Flask Dev)", "5000/udp (UPnP)", "5060/tcp (SIP)", "5060/udp (SIP)",
            "8008/tcp (HTTP Alt)", "8088/tcp (HTTP Alt)", "9000/tcp (Jenkins/Python HTTP)",
            "9090/tcp (Prometheus/HTTP Proxy)", "9100/tcp (Node Exporter)", "9200/tcp (Elasticsearch)",
            "9300/tcp (Elasticsearch transport)", "9411/tcp (Zipkin)", "9412/tcp (Zipkin Debug)",
            "11211/tcp (Memcached)", "11211/udp (Memcached)", "25565/tcp (Minecraft Server)",
            "6000/tcp (X11)", "6001/tcp (X11)", "6002/tcp (X11)", # More X11 ports
            "6379/tcp (Redis)", "6380/tcp (Redis Sentinel)",
            "8181/tcp (Apache Tomcat)", "8282/tcp (Custom Web)", "8383/tcp (Custom Web)",
            "8500/tcp (Consul Web UI)", "8600/tcp (Consul DNS)",
            "9999/tcp (Custom Dev)", "12345/tcp (Custom Dev)", "15000/tcp (Custom API)"
        ]
        # CTkComboBox for ports - removed unsupported dropdown_height/width
        self.port_combobox = ctk.CTkComboBox(self.tab_ports,
                                             values=self.common_ports,
                                             state="disabled",
                                             dropdown_fg_color=("gray75", "gray25"),
                                             dropdown_hover_color=("gray70", "gray30"),
                                             dropdown_text_color=("black", "white"))
        self.port_combobox.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.add_port_button = ctk.CTkButton(self.tab_ports, text="Ajouter Port (Permanent)", command=lambda: self._add_remove_rule("port", self._clean_port_selection(self.port_combobox.get()), "add"))
        self.add_port_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.remove_port_button = ctk.CTkButton(self.tab_ports, text="Supprimer Port (Permanent)", command=lambda: self._add_remove_rule("port", self._clean_port_selection(self.port_combobox.get()), "remove"))
        self.remove_port_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.reload_button_ports = ctk.CTkButton(self.tab_ports, text="Recharger Firewalld (Appliquer les changements)", command=self._reload_firewalld)
        self.reload_button_ports.grid(row=3, column=0, columnspan=2, padx=10, pady=20, sticky="ew")


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
            self._populate_comboboxes() # Populate after confirming sudo
        else:
            self._update_status("Ce script nécessite des privilèges administrateur (sudo) pour gérer Firewalld. Exécutez avec 'sudo python votre_script.py'", "orange")
            self._disable_all_controls() # Disable for safety if not sudo

    def _disable_all_controls(self):
        """Disables all interactive elements."""
        self.port_combobox.configure(state="disabled")
        self.add_port_button.configure(state="disabled")
        self.remove_port_button.configure(state="disabled")
        self.reload_button_zones.configure(state="disabled")
        self.reload_button_ports.configure(state="disabled")

    def _enable_all_controls(self):
        """Enables all interactive elements."""
        self.port_combobox.configure(state="normal")
        self.add_port_button.configure(state="normal")
        self.remove_port_button.configure(state="normal")
        self.reload_button_zones.configure(state="normal")
        self.reload_button_ports.configure(state="normal")

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

    def _populate_comboboxes(self):
        """Populates service and port comboboxes. (Services part is removed)"""
        self._update_status("Chargement des ports connus...", "gray")
        
        # Set default for ports (already defined in self.common_ports)
        if self.common_ports:
            self.port_combobox.set("") # Set to empty by default
        else:
            self.port_combobox.set("Aucun port commun")


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

    def _clean_port_selection(self, selected_value):
        """Cleans the port string, removing descriptive text in parentheses."""
        match = re.match(r"(\d+/(?:tcp|udp))\s*\(.*\)", selected_value)
        if match:
            return match.group(1)
        return selected_value.strip()

    def _add_remove_rule(self, rule_type, rule_value, action):
        """Adds or removes a service or port."""
        if not rule_value:
            self._update_status(f"Veuillez entrer ou sélectionner une valeur pour le {rule_type}.", "orange")
            return
        
        # Clean port value if it comes from the combobox with description
        if rule_type == "port":
            rule_value = self._clean_port_selection(rule_value)

        confirm_message = f"Êtes-vous sûr de vouloir '{action}' le {rule_type} '{rule_value}' dans la zone '{self.active_zone}' de manière PERMANENTE ?\n" \
                          "Un rechargement sera nécessaire pour appliquer les changements."
        
        # Use the (potentially dummy) CTkMessagebox
        if not CTkMessagebox.ask_yes_no(f"Confirmer l'{action.capitalize()} du {rule_type}", confirm_message, icon="warning"):
            self._update_status(f"Action '{action}' annulée pour le {rule_type} '{rule_value}'.", "gray")
            return

        command_args = [f"--zone={self.active_zone}"]
        if rule_type == "port":
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
        # Use the (potentially dummy) CTkMessagebox
        if not CTkMessagebox.ask_yes_no(
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