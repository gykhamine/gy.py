import customtkinter as ctk
import sqlite3
import threading
import subprocess
import os # Importation de os
import io
import time

class CommandDB:
    def __init__(self, db_name="commands.db"):
        # Le fichier de base de données sera créé dans le répertoire courant
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS commands (
                command_text TEXT UNIQUE,
                action_command TEXT
            )
        """)
        self.conn.commit()

    def add_command(self, command_text, action_command):
        try:
            self.cursor.execute("INSERT INTO commands (command_text, action_command) VALUES (?, ?)",
                                (command_text, action_command))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_action(self, command_text):
        self.cursor.execute("SELECT action_command FROM commands WHERE command_text = ?", (command_text,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_all_commands(self):
        self.cursor.execute("SELECT command_text, action_command FROM commands")
        return self.cursor.fetchall()

    def update_command(self, old_command_text, new_command_text, new_action_command):
        try:
            self.cursor.execute("UPDATE commands SET command_text = ?, action_command = ? WHERE command_text = ?",
                                (new_command_text, new_action_command, old_command_text))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def delete_command(self, command_text):
        self.cursor.execute("DELETE FROM commands WHERE command_text = ?", (command_text,))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

class CommandRunner:
    def __init__(self, base_path=None):
        # Si un base_path est fourni, il sera utilisé comme répertoire de travail pour les commandes.
        # Sinon, subprocess.Popen utilisera le répertoire de travail courant du script.
        self.base_path = base_path if base_path else os.getcwd() # Récupère le répertoire de travail courant

    def execute_command_in_thread(self, command_string):
        def run():
            try:
                # Exécute la commande avec le répertoire de travail spécifié (self.base_path)
                # Si base_path est os.getcwd(), c'est le répertoire où le script a été lancé.
                subprocess.Popen(command_string, shell=True, cwd=self.base_path)
            except Exception as e:
                print(f"Erreur lors de l'exécution de la commande '{command_string}': {e}")
        thread = threading.Thread(target=run)
        thread.start()
        return thread

class AudioRecorder:
    def __init__(self, update_callback=None):
        self.is_recording = False
        self.audio_thread = None
        self.update_callback = update_callback

    def start_recording(self):
        if self.is_recording:
            return

        self.is_recording = True
        self.audio_thread = threading.Thread(target=self._record_audio)
        self.audio_thread.start()

    def _record_audio(self):
        try:
            for i in range(50):
                if not self.is_recording:
                    break
                simulated_data = f"{i * 0.012345:.6f}"
                if self.update_callback:
                    self.update_callback(simulated_data + "\n")
                time.sleep(0.1)
        except Exception as e:
            print(f"Erreur lors de l'enregistrement audio: {e}")
        finally:
            self.is_recording = False
            if self.update_callback:
                self.update_callback("--- Fin du flux audio ---\n")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False

class CameraRecorder:
    def __init__(self, update_callback=None):
        self.is_recording = False
        self.camera_thread = None
        self.update_callback = update_callback

    def start_recording(self):
        if self.is_recording:
            return

        self.is_recording = True
        self.camera_thread = threading.Thread(target=self._record_camera)
        self.camera_thread.start()

    def _record_camera(self):
        try:
            for r in range(20):
                if not self.is_recording:
                    break
                line_data = ""
                for c in range(10):
                    decimal_val = (r * c * 0.001) % 1.0
                    line_data += f"{decimal_val:.6f} "
                if self.update_callback:
                    self.update_callback(line_data.strip() + "\n")
                time.sleep(0.2)
        except Exception as e:
            print(f"Erreur lors de l'enregistrement caméra: {e}")
        finally:
            self.is_recording = False
            if self.update_callback:
                self.update_callback("--- Fin du flux caméra ---\n")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False

class ConfigurationPanel(ctk.CTkToplevel):
    def __init__(self, master, db_manager, main_app):
        super().__init__(master)
        self.title("Configuration des Commandes")
        self.geometry("600x400")
        self.db_manager = db_manager
        self.main_app = main_app
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(self, text="Ajouter/Modifier une Commande", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self, text="Commande:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.command_entry = ctk.CTkEntry(self, width=200)
        self.command_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self, text="Action:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.action_entry = ctk.CTkEntry(self, width=200)
        self.action_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        add_button = ctk.CTkButton(self, text="Ajouter/Modifier", command=self.add_or_update_command)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self, text="Commandes Existantes:", font=("Arial", 14)).grid(row=4, column=0, columnspan=2, pady=10)

        self.commands_frame = ctk.CTkScrollableFrame(self)
        self.commands_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.update_commands_list()

    def add_or_update_command(self):
        command = self.command_entry.get().strip()
        action = self.action_entry.get().strip()
        if command and action:
            if not self.db_manager.update_command(command, command, action):
                self.db_manager.add_command(command, action)
            self.update_commands_list()
            self.command_entry.delete(0, ctk.END)
            self.action_entry.delete(0, ctk.END)
            self.main_app.show_message(f"Commande '{command}' configurée.")
            self.main_app.update_command_display()
        else:
            self.main_app.show_message("Veuillez entrer une commande et une action.")

    def update_commands_list(self):
        for widget in self.commands_frame.winfo_children():
            widget.destroy()

        commands = self.db_manager.get_all_commands()
        for i, (cmd, act) in enumerate(commands):
            cmd_label = ctk.CTkLabel(self.commands_frame, text=f"Commande: {cmd}", anchor="w")
            cmd_label.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
            act_label = ctk.CTkLabel(self.commands_frame, text=f"Action: {act}", anchor="w")
            act_label.grid(row=i, column=1, padx=5, pady=2, sticky="ew")

            delete_button = ctk.CTkButton(self.commands_frame, text="Supprimer", width=80,
                                         command=lambda c=cmd: self.delete_command(c))
            delete_button.grid(row=i, column=2, padx=5, pady=2)

            edit_button = ctk.CTkButton(self.commands_frame, text="Modifier", width=80,
                                        command=lambda c=cmd, a=act: self.load_command_for_edit(c, a))
            edit_button.grid(row=i, column=3, padx=5, pady=2)

    def delete_command(self, command_text):
        self.db_manager.delete_command(command_text)
        self.update_commands_list()
        self.main_app.show_message(f"Commande '{command_text}' supprimée.")
        self.main_app.update_command_display()

    def load_command_for_edit(self, command_text, action_command):
        self.command_entry.delete(0, ctk.END)
        self.command_entry.insert(0, command_text)
        self.action_entry.delete(0, ctk.END)
        self.action_entry.insert(0, action_command)

    def on_closing(self):
        self.main_app.update_command_display()
        self.destroy()


class AICommanderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Commander Prompt")
        self.geometry("1200x800")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.db_manager = CommandDB()
        
        # Obtenir le répertoire du script en cours d'exécution
        # C'est le "root" que vous souhaitez pour les chemins relatifs
        script_dir = os.path.abspath(os.path.dirname(__file__))
        print(f"Répertoire du script (root pour les commandes) : {script_dir}")
        self.command_runner = CommandRunner(base_path=script_dir) # Passer le répertoire au CommandRunner

        self.audio_recorder = AudioRecorder(self.update_audio_display)
        self.camera_recorder = CameraRecorder(self.update_camera_display)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # Panneau de message
        self.message_label = ctk.CTkLabel(self, text="Prêt à l'écoute...", font=("Arial", 18), wraplength=350)
        self.message_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Zone d'affichage du flux audio
        ctk.CTkLabel(self, text="Flux Audio (Décimal)", font=("Arial", 14)).grid(row=0, column=1, pady=5, sticky="s")
        self.audio_display = ctk.CTkTextbox(self, width=350, height=200, wrap="word", font=("Courier New", 10))
        self.audio_display.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.audio_display.insert("end", "Aucun flux audio (décimal)...\n")
        self.audio_display.configure(state="disabled")

        # Zone d'affichage du flux caméra
        ctk.CTkLabel(self, text="Flux Caméra (Décimal)", font=("Arial", 14)).grid(row=1, column=1, pady=5, sticky="s")
        self.camera_display = ctk.CTkTextbox(self, width=350, height=200, wrap="word", font=("Courier New", 10))
        self.camera_display.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.camera_display.insert("end", "Aucun flux caméra (décimal)...\n")
        self.camera_display.configure(state="disabled")

        # Zone d'affichage des commandes configurées
        ctk.CTkLabel(self, text="Commandes Configurées (DB)", font=("Arial", 14)).grid(row=0, column=2, pady=5, sticky="s")
        self.command_config_display = ctk.CTkTextbox(self, width=350, height=400, wrap="word", font=("Courier New", 10))
        self.command_config_display.grid(row=0, column=2, rowspan=2, padx=20, pady=10, sticky="nsew")
        self.command_config_display.insert("end", "Chargement des commandes...\n")
        self.command_config_display.configure(state="disabled")
        self.update_command_display()

        # Champ de saisie du prompt
        self.prompt_entry = ctk.CTkEntry(self, placeholder_text="Entrez votre commande ici...", font=("Arial", 24))
        self.prompt_entry.grid(row=2, column=0, columnspan=3, padx=50, pady=30, sticky="ew")
        self.prompt_entry.bind("<Return>", self.process_prompt)

        # Cadre pour les boutons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Boutons
        self.microphone_button = ctk.CTkButton(button_frame, text="🎙️ Microphone", command=self.toggle_microphone)
        self.microphone_button.grid(row=0, column=0, padx=10)

        self.camera_button = ctk.CTkButton(button_frame, text="📸 Caméra", command=self.toggle_camera)
        self.camera_button.grid(row=0, column=1, padx=10)

        self.config_button = ctk.CTkButton(button_frame, text="⚙️ Configurer Commandes", command=self.open_config_panel)
        self.config_button.grid(row=0, column=2, padx=10)

        self.submit_button = ctk.CTkButton(button_frame, text="Exécuter", command=lambda: self.process_prompt(None))
        self.submit_button.grid(row=0, column=3, padx=10)

        self.prompt_entry.focus_set()

    def show_message(self, message):
        self.message_label.configure(text=message)
        self.after(5000, lambda: self.message_label.configure(text="Prêt à l'écoute..."))

    def process_prompt(self, event=None):
        command_text = self.prompt_entry.get().strip()
        if command_text:
            action = self.db_manager.get_action(command_text)
            if action:
                self.show_message(f"Exécution de: '{action}'")
                self.command_runner.execute_command_in_thread(action)
            else:
                self.show_message(f"Commande '{command_text}' non reconnue.")
            self.prompt_entry.delete(0, ctk.END)
        else:
            self.show_message("Veuillez entrer une commande.")
        self.prompt_entry.focus_set()

    def update_audio_display(self, data):
        self.audio_display.configure(state="normal")
        self.audio_display.insert("end", data)
        self.audio_display.see("end")
        self.audio_display.configure(state="disabled")

    def update_camera_display(self, data):
        self.camera_display.configure(state="normal")
        self.camera_display.insert("end", data)
        self.camera_display.see("end")
        self.camera_display.configure(state="disabled")

    def update_command_display(self):
        """Met à jour le panneau d'affichage des commandes configurées."""
        self.command_config_display.configure(state="normal")
        self.command_config_display.delete("1.0", "end")
        
        commands = self.db_manager.get_all_commands()
        if not commands:
            self.command_config_display.insert("end", "Aucune commande configurée.\n")
        else:
            self.command_config_display.insert("end", "COMMANDES:\n")
            self.command_config_display.insert("end", "---------------------\n")
            for cmd, act in commands:
                self.command_config_display.insert("end", f"'{cmd}' => '{act}'\n")
            self.command_config_display.insert("end", "---------------------\n")
        
        self.command_config_display.configure(state="disabled")

    def toggle_microphone(self):
        if self.audio_recorder.is_recording:
            self.audio_recorder.stop_recording()
            self.microphone_button.configure(text="🎙️ Microphone")
            self.show_message("Enregistrement audio arrêté.")
        else:
            self.audio_display.configure(state="normal")
            self.audio_display.delete("1.0", "end")
            self.audio_display.insert("end", "Démarrage du flux audio (décimal)...\n")
            self.audio_display.configure(state="disabled")
            self.audio_recorder.start_recording()
            self.microphone_button.configure(text="🛑 Stop Microphone")
            self.show_message("Flux audio démarré (simulé en décimal).")

    def toggle_camera(self):
        if self.camera_recorder.is_recording:
            self.camera_recorder.stop_recording()
            self.camera_button.configure(text="📸 Caméra")
            self.show_message("Enregistrement caméra arrêté.")
        else:
            self.camera_display.configure(state="normal")
            self.camera_display.delete("1.0", "end")
            self.camera_display.insert("end", "Démarrage du flux caméra (décimal)...\n")
            self.camera_display.configure(state="disabled")
            self.camera_recorder.start_recording()
            self.camera_button.configure(text="🛑 Stop Camera")
            self.show_message("Flux caméra démarré (simulé en décimal).")

    def open_config_panel(self):
        config_panel = ConfigurationPanel(self, self.db_manager, self)
        config_panel.grab_set()

    def on_closing(self):
        print("Événement de fermeture de la fenêtre détecté. Nettoyage...")
        self.db_manager.close()
        self.audio_recorder.stop_recording()
        self.camera_recorder.stop_recording()
        self.destroy()

if __name__ == "__main__":
    app = AICommanderApp()
    app.mainloop()