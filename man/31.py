# main_app.py

import customtkinter as ctk
import subprocess
import threading
import time

# Nom du fichier et du script de service
LOG_FILE = "activity_log.txt"
SERVICE_SCRIPT = "30.py"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Moniteur d'activité")
        self.geometry("800x600")

        self.log_textbox = ctk.CTkTextbox(self, width=780, height=500)
        self.log_textbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.monitor_process = None
        self.update_thread = None
        
        # Bouton pour démarrer/arrêter le service
        self.button = ctk.CTkButton(self, text="Démarrer la surveillance", command=self.toggle_monitoring)
        self.button.pack(pady=10)

        self.update_log_from_file()

    def toggle_monitoring(self):
        """Démarre ou arrête le service de surveillance."""
        if self.monitor_process is None or self.monitor_process.poll() is not None:
            # Démarrer le service en arrière-plan
            self.monitor_process = subprocess.Popen(["python", SERVICE_SCRIPT])
            self.button.configure(text="Arrêter la surveillance")
            print("Surveillance démarrée.")
        else:
            # Arrêter le service
            self.monitor_process.terminate()
            self.monitor_process = None
            self.button.configure(text="Démarrer la surveillance")
            print("Surveillance arrêtée.")

    def update_log_from_file(self):
        """Met à jour la fenêtre en lisant le fichier journal."""
        def read_file():
            try:
                with open(LOG_FILE, "r") as f:
                    content = f.read()
                    self.log_textbox.delete("1.0", ctk.END)
                    self.log_textbox.insert(ctk.END, content)
                    self.log_textbox.see(ctk.END)
            except FileNotFoundError:
                pass
        
        # Utiliser un thread pour éviter de bloquer l'interface
        read_thread = threading.Thread(target=read_file)
        read_thread.start()
        
        self.after(1000, self.update_log_from_file) # Rafraîchit toutes les secondes

if __name__ == "__main__":
    app = App()
    app.mainloop()