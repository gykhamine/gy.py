import customtkinter as ctk
import os
import subprocess
import sys
import threading # Pour exécuter les opérations en arrière-plan et ne pas bloquer l'interface

# Configuration de base pour CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue") # Thèmes: "blue" (standard), "green", "dark-blue"

class NginxConfiguratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Configuration Nginx pour CTK (avec CustomTkinter)")
        self.geometry("700x550")

        # Variables pour les entrées utilisateur
        self.site_name_var = ctk.StringVar(value="mon_site_gui")
        self.server_name_var = ctk.StringVar(value="mon_site_gui.local")

        # --- Widgets de l'interface ---

        # Frame principale
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Titre
        self.title_label = ctk.CTkLabel(self.main_frame, text="Assistant de Configuration Nginx pour CTK", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(10, 20))

        # Entrée Nom du site
        self.site_name_label = ctk.CTkLabel(self.main_frame, text="Nom du site (ex: mon_app) :")
        self.site_name_label.pack(pady=(10, 0))
        self.site_name_entry = ctk.CTkEntry(self.main_frame, textvariable=self.site_name_var, width=300)
        self.site_name_entry.pack(pady=5)

        # Entrée Nom de domaine (server_name)
        self.server_name_label = ctk.CTkLabel(self.main_frame, text="Nom de domaine (server_name, ex: mon_app.com) :")
        self.server_name_label.pack(pady=(10, 0))
        self.server_name_entry = ctk.CTkEntry(self.main_frame, textvariable=self.server_name_var, width=300)
        self.server_name_entry.pack(pady=5)

        # Bouton de configuration
        self.config_button = ctk.CTkButton(self.main_frame, text="Configurer Nginx", command=self.start_nginx_config)
        self.config_button.pack(pady=20)

        # Zone de texte pour les logs et le statut
        self.log_textbox = ctk.CTkTextbox(self.main_frame, width=550, height=180, wrap="word")
        self.log_textbox.pack(pady=10)
        self.log_textbox.insert("end", "Prêt à configurer Nginx. Entrez les détails et cliquez sur 'Configurer Nginx'.\n")
        self.log_textbox.configure(state="disabled") # Rendre le texte non modifiable

        # Informations pour CTK
        self.ctk_info_label = ctk.CTkLabel(self.main_frame, text="""
        --- Instructions pour CTK ---
        Une fois Nginx configuré, CTK devra être paramétré pour collecter les journaux.
        Les journaux d'accès et d'erreur seront dans :
        /var/log/nginx/<nom_du_site>-access.log
        /var/log/nginx/<nom_du_site>-error.log
        Consultez la documentation CyberArk CTK pour la configuration des sources de journaux.
        """, justify="left", wraplength=550, font=ctk.CTkFont(size=12))
        self.ctk_info_label.pack(pady=(10, 0))

    def update_log(self, message):
        """Met à jour la zone de texte des logs."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end") # Faire défiler vers le bas
        self.log_textbox.configure(state="disabled")

    def run_command(self, command, check_error=True):
        """Exécute une commande shell avec sudo et gère les erreurs."""
        try:
            process = subprocess.run(command, shell=True, check=check_error, capture_output=True, text=True, encoding='utf-8')
            self.update_log(f"Commande exécutée: {command.split()[0]}... Succès.")
            if process.stdout:
                self.update_log(process.stdout.strip())
            return True
        except subprocess.CalledProcessError as e:
            error_msg = f"Erreur lors de l'exécution de la commande: {command.split()[0]}..."
            self.update_log(error_msg)
            self.update_log(f"Sortie d'erreur: {e.stderr.strip()}")
            return False
        except FileNotFoundError:
            error_msg = f"Erreur: Commande '{command.split()[0]}' introuvable. Assurez-vous qu'elle est dans votre PATH."
            self.update_log(error_msg)
            return False

    def start_nginx_config(self):
        """Lance la configuration Nginx dans un thread séparé."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end") # Efface les logs précédents
        self.log_textbox.configure(state="disabled")
        self.update_log("Démarrage de la configuration Nginx...")
        self.config_button.configure(state="disabled", text="Configuration en cours...") # Désactiver le bouton

        # Lancer la fonction de configuration dans un thread séparé pour ne pas bloquer l'interface
        config_thread = threading.Thread(target=self._configure_nginx_task)
        config_thread.start()

    def _configure_nginx_task(self):
        """Logique de configuration Nginx."""
        site_name = self.site_name_var.get().strip()
        server_name = self.server_name_var.get().strip()

        if not site_name or not server_name:
            self.update_log("Erreur: Le nom du site et le nom de domaine ne peuvent pas être vides.")
            self.config_button.configure(state="normal", text="Configurer Nginx")
            return

        site_root = f"/var/www/{site_name}"
        nginx_conf_path = f"/etc/nginx/sites-available/{site_name}.conf"
        nginx_enabled_path = f"/etc/nginx/sites-enabled/{site_name}.conf"
        nginx_access_log = f"/var/log/nginx/{site_name}-access.log"
        nginx_error_log = f"/var/log/nginx/{site_name}-error.log"

        # 1. Vérifier et installer Nginx
        self.update_log("Vérification de l'installation de Nginx...")
        if not self.run_command("which nginx", check_error=False):
            self.update_log("Nginx n'est pas installé. Tentative d'installation...")
            if not self.run_command("sudo apt update"):
                self.update_log("Échec de 'sudo apt update'. Vérifiez votre connexion ou vos dépôts.")
                self.config_button.configure(state="normal", text="Configurer Nginx")
                return
            if not self.run_command("sudo apt install -y nginx"):
                self.update_log("Échec de l'installation de Nginx. Veuillez vérifier les permissions ou les paquets.")
                self.config_button.configure(state="normal", text="Configurer Nginx")
                return
            self.update_log("Nginx installé avec succès.")
        else:
            self.update_log("Nginx est déjà installé.")

        # 2. Créer la structure de répertoires
        self.update_log(f"Création du répertoire racine du site : {site_root}")
        if not self.run_command(f"sudo mkdir -p {site_root}"):
            self.config_button.configure(state="normal", text="Configurer Nginx")
            return

        # 3. Générer une page HTML simple
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Bienvenue sur {site_name} (GUI)</title>
    <style>
        body {{
            width: 80%;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <h1>Bonjour de Nginx configuré via GUI !</h1>
    <p>Ce site est servi par Nginx et ses journaux ({nginx_access_log}, {nginx_error_log}) sont prêts à être collectés par CTK.</p>
    <p>Visitez : http://{server_name}</p>
</body>
</html>
"""
        self.update_log(f"Création de la page HTML simple dans : {site_root}/index.html")
        try:
            # Écrire dans un fichier temporaire puis le déplacer avec sudo
            with open("temp_index.html", "w") as f:
                f.write(html_content.strip())
            if not self.run_command(f"sudo mv temp_index.html {site_root}/index.html"):
                self.config_button.configure(state="normal", text="Configurer Nginx")
                return
        except IOError as e:
            self.update_log(f"Erreur lors de l'écriture du fichier HTML temporaire: {e}")
            self.config_button.configure(state="normal", text="Configurer Nginx")
            return

        # 4. Créer le fichier de configuration Nginx
        nginx_conf_content = f"""
server {{
    listen 80;
    server_name {server_name};

    root {site_root};
    index index.html index.htm;

    location / {{
        try_files $uri $uri/ =404;
    }}

    # Configuration des journaux d'accès et d'erreur pour ce site
    access_log {nginx_access_log};
    error_log {nginx_error_log};
}}
"""
        self.update_log(f"Création du fichier de configuration Nginx pour le site : {nginx_conf_path}")
        try:
            with open("temp_nginx.conf", "w") as f:
                f.write(nginx_conf_content.strip())
            if not self.run_command(f"sudo mv temp_nginx.conf {nginx_conf_path}"):
                self.config_button.configure(state="normal", text="Configurer Nginx")
                return
        except IOError as e:
            self.update_log(f"Erreur lors de l'écriture du fichier de conf Nginx temporaire: {e}")
            self.config_button.configure(state="normal", text="Configurer Nginx")
            return

        # 5. Activer le site
        self.update_log(f"Activation du site en créant un lien symbolique : {nginx_enabled_path}")
        if os.path.exists(nginx_enabled_path) or os.path.islink(nginx_enabled_path):
            self.update_log("Lien symbolique existant, suppression...")
            if not self.run_command(f"sudo rm {nginx_enabled_path}"):
                self.config_button.configure(state="normal", text="Configurer Nginx")
                return
        if not self.run_command(f"sudo ln -s {nginx_conf_path} {nginx_enabled_path}"):
            self.config_button.configure(state="normal", text="Configurer Nginx")
            return

        # 6. Vérifier la syntaxe de la configuration Nginx
        self.update_log("Vérification de la syntaxe de la configuration Nginx...")
        if not self.run_command("sudo nginx -t"):
            self.update_log("Erreur: La syntaxe de la configuration Nginx est invalide. Veuillez vérifier les logs ci-dessus.")
            self.config_button.configure(state="normal", text="Configurer Nginx")
            return
        self.update_log("Syntaxe Nginx valide.")

        # 7. Redémarrer le service Nginx
        self.update_log("Redémarrage de Nginx pour appliquer les changements...")
        if not self.run_command("sudo systemctl restart nginx"):
            self.update_log("Erreur: Échec du redémarrage de Nginx. Veuillez vérifier le statut du service.")
            self.config_button.configure(state="normal", text="Configurer Nginx")
            return

        self.update_log(f"\nConfiguration Nginx terminée pour '{site_name}' sur {server_name}.")
        self.update_log(f"Vous pouvez maintenant accéder à http://{server_name}.")
        self.update_log(f"N'oubliez pas d'ajouter '{server_name}' à votre fichier /etc/hosts pour le tester localement.")
        self.update_log("Pensez à configurer CTK pour collecter les journaux aux chemins spécifiés.")
        self.config_button.configure(state="normal", text="Configurer Nginx")


if __name__ == "__main__":
    # Vérifier si le script est exécuté avec sudo
    if os.geteuid() != 0:
        print("Ce script CustomTkinter doit être exécuté avec des privilèges sudo.")
        print("Veuillez exécuter : sudo python3 votre_script_gui.py")
        sys.exit(1)

    app = NginxConfiguratorApp()
    app.mainloop()