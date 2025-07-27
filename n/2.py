import customtkinter as ctk
import sqlite3
import threading
import subprocess
import os
import io
import time

# For real audio capture (using PyAudio)
import pyaudio
import numpy as np

# For real camera capture
import cv2

# --- Database Management ---
class CommandDB:
    def __init__(self, db_name="commands.db"):
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

# --- Command Execution ---
class CommandRunner:
    def __init__(self, base_path=None):
        self.base_path = base_path if base_path else os.getcwd()

    def execute_command_in_thread(self, command_string):
        def run():
            try:
                process = subprocess.run(command_string, shell=True, cwd=self.base_path, capture_output=True, text=True, check=False)
                print(f"\n--- Output for command: '{command_string}' ---")
                if process.stdout:
                    print(f"STDOUT:\n{process.stdout.strip()}")
                if process.stderr:
                    print(f"STDERR:\n{process.stderr.strip()}")
                if process.returncode != 0:
                    print(f"Command exited with error code: {process.returncode}")
                print(f"--- End output for command: '{command_string}' ---\n")
            except Exception as e:
                print(f"Error executing command '{command_string}': {e}")
        thread = threading.Thread(target=run)
        thread.start()
        return thread

# --- Real Audio Capture (using PyAudio, Output to Console in Raw Decimal) ---
class AudioRecorder:
    def __init__(self, update_callback=None):
        self.is_recording = False
        self.audio_thread = None
        self.update_callback = update_callback 
        
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16 # 16-bit resolution
        self.channels = 1     # Mono audio
        self.fs = 44100       # Sample rate 44.1kHz
        self.p = None         # PyAudio object
        self.stream = None    # PyAudio stream object

    def start_recording(self):
        if self.is_recording:
            return

        try:
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=self.sample_format,
                                      channels=self.channels,
                                      rate=self.fs,
                                      frames_per_buffer=self.chunk,
                                      input=True)
            self.is_recording = True
            self.audio_thread = threading.Thread(target=self._record_audio)
            self.audio_thread.start()
            print("\n--- Real Audio Stream Started (Raw Decimal Output) ---")
        except Exception as e:
            print(f"Error starting audio stream: {e}")
            self.is_recording = False
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.p:
                self.p.terminate()

    def _record_audio(self):
        try:
            while self.is_recording:
                data = self.stream.read(self.chunk, exception_on_overflow=False) 
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # Print raw decimal values of the audio samples
                # Only print a slice to avoid console overload, adjust as needed
                print(f"Raw Audio (first 100 samples): {audio_data[:100].tolist()} ...")
                # To print ALL samples: print(f"Raw Audio: {audio_data.tolist()}")

                if self.update_callback:
                    # Pass the raw data string (or a representation) to the callback if needed
                    self.update_callback(f"Raw Audio: {audio_data.tolist()}\n")
                
        except Exception as e:
            print(f"Error in audio stream thread: {e}")
        finally:
            self.is_recording = False
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.p:
                self.p.terminate()
            print("--- Real Audio Stream Ended ---")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            print("Real Audio recording stopped.")
            
# --- Real Camera Capture (Output to Console in Raw Matrix) ---
class CameraRecorder:
    def __init__(self, update_callback=None):
        self.is_recording = False
        self.camera_thread = None
        self.update_callback = update_callback 
        self.cap = None # OpenCV VideoCapture object
        self.frame_counter = 0

    def start_recording(self):
        if self.is_recording:
            return

        try:
            self.cap = cv2.VideoCapture(0) # 0 for default camera
            if not self.cap.isOpened():
                raise IOError("Cannot open webcam. Check if it's connected and not in use, or try a different index (1, 2...).")
            
            self.is_recording = True
            self.camera_thread = threading.Thread(target=self._record_camera)
            self.camera_thread.start()
            print("\n--- Real Camera Stream Started (Raw Matrix Output) ---")
        except Exception as e:
            print(f"Error starting camera stream: {e}")
            self.is_recording = False
            if self.cap:
                self.cap.release() 

    def _record_camera(self):
        try:
            while self.is_recording:
                ret, frame = self.cap.read() 
                if not ret:
                    print("Failed to grab frame from camera. Is it still connected or in use?")
                    time.sleep(0.1) 
                    continue
                
                self.frame_counter += 1
                
                # Print the full raw pixel matrix for the frame, but only every N frames
                # Be aware: this will print A LOT of data. Adjust 'print_every_n_frames'
                # to a higher value if your console gets overwhelmed.
                print_every_n_frames = 30 # Print approximately once per second at 30 FPS
                
                if self.frame_counter % print_every_n_frames == 0:
                    print(f"\n--- Camera Frame {self.frame_counter} (Raw Matrix, Top-Left 5x5 Slice) ---")
                    # Print a small slice of the matrix (e.g., top-left 5x5 pixels)
                    # This is still a lot of data, but better than the entire frame.
                    # Adjust [0:5, 0:5] to change the slice size.
                    print(frame[0:5, 0:5]) 
                    print("--------------------------------------------------\n")
                    # To print the ENTIRE frame matrix (EXTREMELY VERBOSE):
                    # print(f"\n--- Camera Frame {self.frame_counter} (FULL Raw Matrix) ---")
                    # print(frame)
                    # print("--------------------------------------------------\n")


                if self.update_callback:
                    # Pass a representation of the data to callback
                    self.update_callback(f"Camera Frame {self.frame_counter}: Raw data captured.\n")
                
                # A small sleep to prevent 100% CPU usage if `read()` is too fast
                time.sleep(0.01) 

        except Exception as e:
            print(f"Error in camera stream thread: {e}")
        finally:
            self.is_recording = False
            if self.cap:
                self.cap.release() 
            print("--- Real Camera Stream Ended ---")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            print("Real Camera recording stopped.")

# --- Configuration Panel (Separate Window) ---
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
            print(f"Command '{command}' configured to action '{action}'.") # Log to console
        else:
            self.main_app.show_message("Veuillez entrer une commande et une action.")
            print("Error: Command and action cannot be empty.") # Log to console

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
        print(f"Command '{command_text}' deleted.") # Log to console

    def load_command_for_edit(self, command_text, action_command):
        self.command_entry.delete(0, ctk.END)
        self.command_entry.insert(0, command_text)
        self.action_entry.delete(0, ctk.END)
        self.action_entry.insert(0, action_command)

    def on_closing(self):
        self.destroy()

# --- Main Application ---
class AICommanderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Commander Prompt")
        self.geometry("700x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.db_manager = CommandDB()
        
        script_dir = os.path.abspath(os.path.dirname(__file__))
        print(f"Application root directory: {script_dir}")
        self.command_runner = CommandRunner(base_path=script_dir)

        self.audio_recorder = AudioRecorder(update_callback=self.dummy_update_callback) 
        self.camera_recorder = CameraRecorder(update_callback=self.dummy_update_callback)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=0) 
        self.grid_rowconfigure(2, weight=0) 

        self.message_label = ctk.CTkLabel(self, text="Enter a command or use the buttons...", font=("Arial", 18), wraplength=650)
        self.message_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.prompt_entry = ctk.CTkEntry(self, placeholder_text="Type 'help' for commands...", font=("Arial", 24))
        self.prompt_entry.grid(row=1, column=0, padx=50, pady=20, sticky="ew")
        self.prompt_entry.bind("<Return>", self.process_prompt)

        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, pady=10)
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.microphone_button = ctk.CTkButton(button_frame, text="🎙️ Microphone", command=self.toggle_microphone)
        self.microphone_button.grid(row=0, column=0, padx=10)

        self.camera_button = ctk.CTkButton(button_frame, text="📸 Camera", command=self.toggle_camera)
        self.camera_button.grid(row=0, column=1, padx=10)

        self.config_button = ctk.CTkButton(button_frame, text="⚙️ Configure", command=self.open_config_panel)
        self.config_button.grid(row=0, column=2, padx=10)

        self.submit_button = ctk.CTkButton(button_frame, text="Execute", command=lambda: self.process_prompt(None))
        self.submit_button.grid(row=0, column=3, padx=10)

        self.prompt_entry.focus_set()

        self.db_manager.add_command("help", "echo 'Available commands:'")
        self.db_manager.add_command("test", "echo 'This is a test command!'")
        self.db_manager.add_command("date", "date") 
        self.db_manager.add_command("time", "date +%T") 

    def dummy_update_callback(self, *args, **kwargs):
        pass

    def show_message(self, message):
        self.message_label.configure(text=message)
        self.after(3000, lambda: self.message_label.configure(text="Enter a command or use the buttons..."))

    def process_prompt(self, event=None):
        command_text = self.prompt_entry.get().strip()
        self.prompt_entry.delete(0, ctk.END)
        
        if command_text:
            if command_text == "help":
                all_commands = self.db_manager.get_all_commands()
                help_message = "Available Commands:\n"
                if all_commands:
                    help_message += "\n".join([f"  - {cmd[0]}" for cmd in all_commands])
                else:
                    help_message += "  (No commands configured yet)"
                
                self.show_message("Check console for available commands.")
                print(f"\n--- HELP --- \n{help_message}\n--- END HELP ---")
            else:
                action = self.db_manager.get_action(command_text)
                if action:
                    self.show_message(f"Executing: '{action}'")
                    print(f"\nGUI: Executing system command: '{action}'")
                    self.command_runner.execute_command_in_thread(action)
                else:
                    self.show_message(f"Command '{command_text}' not recognized.")
                    print(f"\nGUI: Command '{command_text}' not recognized.")
        else:
            self.show_message("Please enter a command.")
            print("\nGUI: Please enter a command.")
        self.prompt_entry.focus_set()

    def toggle_microphone(self):
        if self.audio_recorder.is_recording:
            self.audio_recorder.stop_recording()
            self.microphone_button.configure(text="🎙️ Microphone")
            self.show_message("Audio recording stopped.")
        else:
            self.audio_recorder.start_recording()
            self.microphone_button.configure(text="🛑 Stop Microphone")
            self.show_message("Audio stream started (check console).")

    def toggle_camera(self):
        if self.camera_recorder.is_recording:
            self.camera_recorder.stop_recording()
            self.camera_button.configure(text="📸 Camera")
            self.show_message("Camera recording stopped.")
        else:
            self.camera_recorder.start_recording()
            self.camera_button.configure(text="🛑 Stop Camera")
            self.show_message("Camera stream started (check console).")

    def open_config_panel(self):
        config_panel = ConfigurationPanel(self, self.db_manager, self)
        config_panel.grab_set()
        self.show_message("Configuration panel opened.")
        print("\nGUI: Configuration panel opened.")

    def on_closing(self):
        print("\nGUI: Window closing event detected. Cleaning up...")
        self.db_manager.close()
        self.audio_recorder.stop_recording()
        self.camera_recorder.stop_recording()
        self.destroy()

if __name__ == "__main__":
    app = AICommanderApp()
    app.mainloop()