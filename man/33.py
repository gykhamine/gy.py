import customtkinter as ctk
import threading
import time
import os
import datetime
from pynput import keyboard, mouse
import pygame
import psutil

# --- Configuration Constants ---
LOG_FILE = "activity_log.txt"
DISPLAY_UPDATE_INTERVAL_MS = 100 # Update mouse position display every 100 milliseconds
SYSTEM_METRICS_UPDATE_INTERVAL_MS = 1000 # Update CPU/Memory every 1 second

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Moniteur d'Activité Système Intégré")
        self.geometry("1100x750") # Larger window for the dashboard
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Row for log textbox

        # --- Monitoring State Variables ---
        self.monitoring_active = False
        self.keyboard_listener = None
        self.mouse_listener = None # This listener will now handle all mouse events
        self.controllers_thread = None
        self.mouse_display_thread = None
        self.system_metrics_thread = None

        # --- GUI Elements - Control Frame ---
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(2, weight=1)

        self.instruction_label = ctk.CTkLabel(self.control_frame,
                                            text="Cliquez sur le bouton pour démarrer ou arrêter la surveillance des activités (clavier, souris complète, manette) et des métriques système.",
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

        # --- GUI Elements - Real-time Dashboard Frame ---
        self.dashboard_frame = ctk.CTkFrame(self)
        self.dashboard_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.dashboard_frame.grid_columnconfigure((0, 1, 2), weight=1) # Three columns for dashboard items

        # Mouse Position Display
        self.mouse_pos_subframe = ctk.CTkFrame(self.dashboard_frame)
        self.mouse_pos_subframe.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.mouse_pos_subframe.grid_rowconfigure((0,1), weight=1)
        self.mouse_pos_subframe.grid_columnconfigure(0, weight=1)

        self.mouse_position_label_title = ctk.CTkLabel(self.mouse_pos_subframe,
                                                      text="Curseur (X, Y):",
                                                      font=ctk.CTkFont(size=16, weight="bold"))
        self.mouse_position_label_title.grid(row=0, column=0, pady=(5,0))

        self.mouse_position_label = ctk.CTkLabel(self.mouse_pos_subframe,
                                                 text="---", # Initial text
                                                 font=ctk.CTkFont(size=36, weight="bold"),
                                                 text_color="#2CC985")
        self.mouse_position_label.grid(row=1, column=0, pady=(0,5))

        # CPU Usage Display
        self.cpu_usage_subframe = ctk.CTkFrame(self.dashboard_frame)
        self.cpu_usage_subframe.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.cpu_usage_subframe.grid_rowconfigure((0,1), weight=1)
        self.cpu_usage_subframe.grid_columnconfigure(0, weight=1)

        self.cpu_usage_label_title = ctk.CTkLabel(self.cpu_usage_subframe,
                                                  text="CPU Utilisation:",
                                                  font=ctk.CTkFont(size=16, weight="bold"))
        self.cpu_usage_label_title.grid(row=0, column=0, pady=(5,0))

        self.cpu_usage_label = ctk.CTkLabel(self.cpu_usage_subframe,
                                            text="--- %",
                                            font=ctk.CTkFont(size=36, weight="bold"),
                                            text_color="#F1C40F")
        self.cpu_usage_label.grid(row=1, column=0, pady=(0,5))

        # Memory Usage Display
        self.mem_usage_subframe = ctk.CTkFrame(self.dashboard_frame)
        self.mem_usage_subframe.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        self.mem_usage_subframe.grid_rowconfigure((0,1), weight=1)
        self.mem_usage_subframe.grid_columnconfigure(0, weight=1)

        self.mem_usage_label_title = ctk.CTkLabel(self.mem_usage_subframe,
                                                 text="RAM Utilisation:",
                                                 font=ctk.CTkFont(size=16, weight="bold"))
        self.mem_usage_label_title.grid(row=0, column=0, pady=(5,0))

        self.mem_usage_label = ctk.CTkLabel(self.mem_usage_subframe,
                                            text="--- MB / --- MB",
                                            font=ctk.CTkFont(size=28, weight="bold"),
                                            text_color="#3498DB")
        self.mem_usage_label.grid(row=1, column=0, pady=(0,5))

        # --- Log Textbox ---
        self.log_textbox = ctk.CTkTextbox(self, width=780, height=500, wrap="word", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_textbox.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # --- Initial Setup ---
        self.update_log_from_file()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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
        """Callback for mouse button presses and releases."""
        if pressed:
            self.write_log(f"Souris - Clic pressé à ({x}, {y}) avec le bouton {button}")
        else:
            self.write_log(f"Souris - Clic relâché à ({x}, {y}) avec le bouton {button}")

    def on_move(self, x, y):
        """Callback for mouse movement. Logs every movement."""
        self.write_log(f"Souris - Mouvement à ({x}, {y})")

    def on_scroll(self, x, y, dx, dy):
        """Callback for mouse scroll wheel activity."""
        log_message = f"Souris - Molette défilée à ({x}, {y})"
        
        vertical_scroll_info = ""
        if dy > 0:
            vertical_scroll_info = "vers le haut"
        elif dy < 0:
            vertical_scroll_info = "vers le bas"

        horizontal_scroll_info = ""
        if dx > 0:
            horizontal_scroll_info = "vers la droite"
        elif dx < 0:
            horizontal_scroll_info = "vers la gauche"
        
        if vertical_scroll_info and horizontal_scroll_info:
            log_message += f", vertical {vertical_scroll_info}, horizontal {horizontal_scroll_info}"
        elif vertical_scroll_info:
            log_message += f", {vertical_scroll_info}"
        elif horizontal_scroll_info:
            log_message += f", {horizontal_scroll_info}"
        
        self.write_log(log_message)


    # --- Monitoring Threads Functions ---
    def update_mouse_position_display(self):
        """Updates the mouse position label in real-time."""
        while self.monitoring_active:
            try:
                x, y = mouse.Controller().position
                self.after(0, lambda x=x, y=y: self.mouse_position_label.configure(text=f"{x}, {y}"))
                time.sleep(DISPLAY_UPDATE_INTERVAL_MS / 1000.0)
            except Exception as e:
                time.sleep(DISPLAY_UPDATE_INTERVAL_MS / 1000.0)

    def update_system_metrics_display(self):
        """Updates CPU and Memory usage labels."""
        while self.monitoring_active:
            try:
                cpu_percent = psutil.cpu_percent(interval=None) # Non-blocking
                mem_info = psutil.virtual_memory()
                mem_used_mb = mem_info.used / (1024 * 1024)
                mem_total_mb = mem_info.total / (1024 * 1024)

                self.after(0, lambda: self.cpu_usage_label.configure(text=f"{cpu_percent:.1f} %"))
                self.after(0, lambda: self.mem_usage_label.configure(text=f"{mem_used_mb:.0f} MB / {mem_total_mb:.0f} MB"))
                
                time.sleep(SYSTEM_METRICS_UPDATE_INTERVAL_MS / 1000.0)
            except Exception as e:
                self.write_log(f"Erreur lors de la mise à jour des métriques système : {e}")
                time.sleep(SYSTEM_METRICS_UPDATE_INTERVAL_MS / 1000.0)

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

        # Keyboard and Mouse Listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        # Mouse listener now includes on_click (both press/release), on_move, and on_scroll
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll)
        self.keyboard_listener.start()
        self.mouse_listener.start()

        # Real-time Mouse Position Display Thread
        self.mouse_display_thread = threading.Thread(target=self.update_mouse_position_display, daemon=True)
        self.mouse_display_thread.start()

        # System Metrics Display Thread
        self.system_metrics_thread = threading.Thread(target=self.update_system_metrics_display, daemon=True)
        self.system_metrics_thread.start()

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
            # Reset dashboard displays
            self.mouse_position_label.configure(text="---")
            self.cpu_usage_label.configure(text="--- %")
            self.mem_usage_label.configure(text="--- MB / --- MB")
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