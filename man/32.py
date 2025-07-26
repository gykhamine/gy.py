import customtkinter as ctk
import threading
import time
import os
import datetime
from pynput import keyboard, mouse
import pygame

# --- Configuration Constants ---
LOG_FILE = "activity_log.txt"
# No longer logging cursor position to file every X seconds, as it's real-time displayed.
# If you still want it logged periodically, add back CURSOR_LOG_INTERVAL and related logic.
DISPLAY_UPDATE_INTERVAL_MS = 100 # Update mouse position display every 100 milliseconds

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Moniteur d'Activité Système Intégré")
        self.geometry("1000x700") # Slightly larger window for new display
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Row for textbox

        # --- Monitoring State Variables ---
        self.monitoring_active = False
        self.keyboard_listener = None
        self.mouse_listener = None
        self.controllers_thread = None
        self.mouse_display_thread = None # New thread for real-time mouse display

        # --- GUI Elements ---
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(2, weight=1)

        self.instruction_label = ctk.CTkLabel(self.control_frame,
                                            text="Cliquez sur le bouton pour démarrer ou arrêter la surveillance des activités (clavier, souris, manette).",
                                            wraplength=700, font=ctk.CTkFont(size=14, weight="bold"))
        self.instruction_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        self.status_label = ctk.CTkLabel(self.control_frame, text="Statut: Service arrêté", text_color="red", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.toggle_button = ctk.CTkButton(self.control_frame,
                                           text="Démarrer la surveillance",
                                           command=self.toggle_monitoring,
                                           font=ctk.CTkFont(size=14, weight="bold"),
                                           height=40)
        self.toggle_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.clear_button = ctk.CTkButton(self.control_frame,
                                          text="Effacer le journal",
                                          command=self.clear_log,
                                          font=ctk.CTkFont(size=14),
                                          height=40)
        self.clear_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        # --- Real-time Mouse Position Display ---
        self.mouse_position_frame = ctk.CTkFrame(self)
        self.mouse_position_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.mouse_position_frame.grid_columnconfigure(0, weight=1)

        self.mouse_position_label_title = ctk.CTkLabel(self.mouse_position_frame,
                                                      text="Position Actuelle du Curseur:",
                                                      font=ctk.CTkFont(size=16, weight="bold"))
        self.mouse_position_label_title.pack(pady=(5,0))

        self.mouse_position_label = ctk.CTkLabel(self.mouse_position_frame,
                                                 text="X: ---, Y: ---",
                                                 font=ctk.CTkFont(size=48, weight="bold"), # Large font for display
                                                 text_color="#2CC985") # Greenish color
        self.mouse_position_label.pack(pady=(0,5))


        # --- Log Textbox ---
        self.log_textbox = ctk.CTkTextbox(self, width=780, height=500, wrap="word", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_textbox.grid(row=2, column=0, padx=20, pady=10, sticky="nsew") # Moved to row 2

        # --- Initial Setup ---
        self.update_log_from_file() # Initial log load
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Ensure clean shutdown

    # --- Logging Function ---
    def write_log(self, message):
        """Fonction pour écrire un message avec un horodatage dans le fichier."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    # --- Monitoring Callbacks (for pynput) ---
    def on_press(self, key):
        try:
            self.write_log(f"Clavier - Touche pressée : {key.char}")
        except AttributeError:
            self.write_log(f"Clavier - Touche spéciale : {key}")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.write_log(f"Souris - Clic à ({x}, {y}) avec le bouton {button}")

    # --- Monitoring Threads Functions ---
    def update_mouse_position_display(self):
        """Updates the mouse position label in real-time."""
        while self.monitoring_active: # Loop as long as monitoring is active
            try:
                x, y = mouse.Controller().position
                # Update the label on the main thread using after()
                self.after(0, lambda x=x, y=y: self.mouse_position_label.configure(text=f"X: {x}, Y: {y}"))
                time.sleep(DISPLAY_UPDATE_INTERVAL_MS / 1000.0) # Convert ms to seconds
            except Exception as e:
                # Log errors but keep trying to update
                # self.write_log(f"Erreur lors de la mise à jour de la position du curseur : {e}") # Too frequent logging
                time.sleep(DISPLAY_UPDATE_INTERVAL_MS / 1000.0)

    def monitor_controllers(self):
        """Moniteur pour les contrôleurs de jeu."""
        try:
            pygame.init()
            joystick_count = pygame.joystick.get_count()
            if joystick_count > 0:
                for i in range(joystick_count):
                    joystick = pygame.joystick.Joystick(i)
                    joystick.init()
                    self.write_log(f"Manette - Contrôleur détecté : {joystick.get_name()} (ID: {i})")
            else:
                self.write_log("Manette - Aucun contrôleur de jeu détecté.")
            
            while self.monitoring_active:
                for event in pygame.event.get(): 
                    if event.type == pygame.JOYBUTTONDOWN:
                        self.write_log(f"Manette - Bouton {event.button} pressé sur {pygame.joystick.Joystick(event.joystick).get_name()}")
                    elif event.type == pygame.JOYAXISMOTION:
                        joystick_name = pygame.joystick.Joystick(event.joystick).get_name()
                        self.write_log(f"Manette - Axe {event.axis} bougé ({event.value:.2f}) sur {joystick_name}")
                time.sleep(0.01)
        except Exception as e:
            self.write_log(f"Erreur du moniteur de manette : {e}")
        finally:
            if pygame.get_init():
                pygame.quit()

    # --- Monitoring Control ---
    def start_monitoring_threads(self):
        """Starts all monitoring threads."""
        self.monitoring_active = True
        self.write_log("Service de surveillance démarré.")

        # Keyboard and Mouse Listener (pynput listeners block, so they are main threads)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

        # Real-time Mouse Position Display Thread
        self.mouse_display_thread = threading.Thread(target=self.update_mouse_position_display, daemon=True)
        self.mouse_display_thread.start()

        # Controller Monitoring Thread
        self.controllers_thread = threading.Thread(target=self.monitor_controllers, daemon=True)
        self.controllers_thread.start()

    def stop_monitoring_threads(self):
        """Stops all monitoring threads."""
        self.monitoring_active = False # Signal threads to stop their loops
        self.write_log("Service de surveillance arrêté.")

        # Stop pynput listeners first
        if self.keyboard_listener and self.keyboard_listener.is_alive():
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        if self.mouse_listener and self.mouse_listener.is_alive():
            self.mouse_listener.stop()
            self.mouse_listener = None
        
        # Give a moment for threads to acknowledge the 'monitoring_active' flag and exit
        time.sleep(0.1) 

    # --- GUI Actions ---
    def toggle_monitoring(self):
        """Toggles the monitoring service on/off."""
        if not self.monitoring_active:
            self.clear_log_content_only()
            self.start_monitoring_threads()
            self.toggle_button.configure(text="Arrêter la surveillance", fg_color="red")
            self.status_label.configure(text="Statut: Service en cours d'exécution", text_color="green")
            print("Surveillance démarrée.")
        else:
            self.stop_monitoring_threads()
            self.toggle_button.configure(text="Démarrer la surveillance", fg_color="#3B8ED0")
            self.status_label.configure(text="Statut: Service arrêté", text_color="red")
            self.mouse_position_label.configure(text="X: ---, Y: ---") # Reset display
            print("Surveillance arrêtée.")

    def update_log_from_file(self):
        """Met à jour la fenêtre en lisant le fichier journal."""
        def read_file():
            try:
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r", encoding="utf-8") as f:
                        content = f.read()
                        self.log_textbox.delete("1.0", ctk.END)
                        self.log_textbox.insert(ctk.END, content)
                        self.log_textbox.see(ctk.END)
                else:
                    self.log_textbox.delete("1.0", ctk.END)
                    self.log_textbox.insert(ctk.END, "Le fichier journal n'existe pas encore. Démarrez le service de surveillance pour commencer à enregistrer les activités.")
            except Exception as e:
                self.log_textbox.delete("1.0", ctk.END)
                self.log_textbox.insert(ctk.END, f"Erreur lors de la lecture du fichier journal: {e}")
        
        read_thread = threading.Thread(target=read_file)
        read_thread.daemon = True
        read_thread.start()
        
        self.after(1000, self.update_log_from_file)

    def clear_log(self):
        """Efface le contenu du fichier journal et de la textbox."""
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    f.write("")
            self.log_textbox.delete("1.0", ctk.END)
            self.log_textbox.insert(ctk.END, "Journal effacé.")
            print("Journal d'activité effacé.")
        except Exception as e:
            print(f"Erreur lors de l'effacement du journal: {e}")
            self.log_textbox.delete("1.0", ctk.END)
            self.log_textbox.insert(ctk.END, f"Erreur lors de l'effacement du journal: {e}")

    def clear_log_content_only(self):
        """Efface le contenu du fichier journal SANS toucher à la textbox."""
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    f.write("")
        except Exception as e:
            print(f"Erreur lors de l'effacement du journal avant le démarrage du service: {e}")

    def on_closing(self):
        """Called when the application window is closed."""
        self.stop_monitoring_threads()
        print("Service de surveillance terminé lors de la fermeture de l'application.")
        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()