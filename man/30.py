# monitor_service.py

import datetime
import threading
from pynput import keyboard, mouse
import pygame
import psutil

# Nom du fichier pour enregistrer les logs
LOG_FILE = "activity_log.txt"

def write_log(message):
    """Fonction pour écrire un message avec un horodatage dans le fichier."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def monitor_keyboard_mouse():
    """Moniteur pour le clavier et la souris."""
    def on_press(key):
        try:
            write_log(f"Clavier - Touche pressée : {key.char}")
        except AttributeError:
            write_log(f"Clavier - Touche spéciale : {key}")

    def on_click(x, y, button, pressed):
        if pressed:
            write_log(f"Souris - Clic à ({x}, {y}) avec le bouton {button}")
    
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()
    
    keyboard_listener.join()
    mouse_listener.join()

def monitor_controllers():
    """Moniteur pour les contrôleurs de jeu."""
    try:
        pygame.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            write_log(f"Manette - Contrôleur détecté : {joystick.get_name()}")
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    write_log(f"Manette - Bouton {event.button} pressé")
                # Ajoutez d'autres événements si nécessaire
    except Exception as e:
        write_log(f"Erreur du moniteur de manette : {e}")

if __name__ == "__main__":
    # Démarre tous les moniteurs en arrière-plan
    write_log("Service de surveillance démarré.")
    
    keyboard_mouse_thread = threading.Thread(target=monitor_keyboard_mouse, daemon=True)
    controllers_thread = threading.Thread(target=monitor_controllers, daemon=True)
    
    keyboard_mouse_thread.start()
    controllers_thread.start()
    
    # Attend indéfiniment que les threads soient actifs
    keyboard_mouse_thread.join()
    controllers_thread.join()