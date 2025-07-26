import customtkinter as ctk
import subprocess
import sys
import os

class LauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tableau de Bord de Lancement")
        self.geometry("500x350")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1) # Give all rows some weight

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="DIR", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=20)

        # Status Label (to show messages)
        self.status_label = ctk.CTkLabel(self, text="Prêt à lancer les scripts.", text_color="gray")
        self.status_label.grid(row=5, column=0, pady=(10, 20))

        # Buttons for each script
        # We'll use lambda to pass arguments to the command function
        # Using os.path.join to ensure cross-platform compatibility for file paths
        current_dir = os.path.dirname(os.path.abspath(__file__))

        self.button_script1 = ctk.CTkButton(self, text="liste",
                                            command=lambda: self.run_external_script(os.path.join(current_dir, "1/10.py"), "liste"))
        self.button_script1.grid(row=1, column=0, padx=50, pady=5, sticky="ew")

        self.button_script2 = ctk.CTkButton(self, text="module-info",
                                            command=lambda: self.run_external_script(os.path.join(current_dir, "1/5.py"), "module-info"))
        self.button_script2.grid(row=2, column=0, padx=50, pady=5, sticky="ew")

        self.button_script3 = ctk.CTkButton(self, text="aide",
                                            command=lambda: self.run_external_script(os.path.join(current_dir, "1/7.py"), "aide"))
        self.button_script3.grid(row=3, column=0, padx=50, pady=5, sticky="ew")

        self.button_script4 = ctk.CTkButton(self, text="class-info",
                                            command=lambda: self.run_external_script(os.path.join(current_dir, "1/8.py"), "class-info"))
        self.button_script4.grid(row=4, column=0, padx=50, pady=5, sticky="ew")

    def run_external_script(self, script_path, script_name):
        """
        Exécute un script Python externe en tant que processus séparé.
        Affiche les messages de statut dans l'interface CTk.
        """
        self.status_label.configure(text=f"Lancement de {script_name}...", text_color="orange")
        self.update_idletasks() # Force GUI update

        try:
            # sys.executable est le chemin vers l'interpréteur Python actuel.
            # Cela garantit que le script est exécuté avec la même version de Python.
            # creationflags=subprocess.DETACHED_PROCESS pour Windows pour ne pas bloquer
            # ou Popen sans wait() si vous ne voulez pas attendre la fin du processus
            
            # Pour un lancement simple et non bloquant, utilisez Popen.
            # shell=True peut être utilisé, mais il est préférable de passer la commande
            # comme une liste pour éviter les problèmes de sécurité/complexité.
            
            subprocess.Popen([sys.executable, script_path])
            
            self.status_label.configure(text=f"{script_name} lancé avec succès !", text_color="green")

        except FileNotFoundError:
            self.status_label.configure(text=f"Erreur : '{script_path}' non trouvé. Vérifiez le chemin.", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Erreur lors du lancement de {script_name} : {e}", text_color="red")
        finally:
            # Réinitialiser le message après un court délai ou sur le prochain événement
            self.after(3000, lambda: self.status_label.configure(text="Prêt à lancer les scripts.", text_color="gray"))


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Ou "Dark", "Light"
    ctk.set_default_color_theme("blue") # Ou "dark-blue", "green"

    app = LauncherApp()
    app.mainloop()