import os
import subprocess
import customtkinter as ctk
from tkinter import scrolledtext, messagebox
import threading
import stat # For file permissions

class BinaryExplorerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Explorateur de Binaires /bin")
        self.geometry("1400x800")

        # Configure grid for main layout
        self.grid_columnconfigure(0, weight=1) # Left panel for file list
        self.grid_columnconfigure(1, weight=3) # Right panel for objdump output
        self.grid_rowconfigure(0, weight=1)

        self.current_hover_thread = None # To manage objdump execution threads

        # --- Left Panel: File List ---
        self.file_list_frame = ctk.CTkFrame(self)
        self.file_list_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.file_list_frame.grid_rowconfigure(1, weight=1) # Allow scrollable frame to expand
        self.file_list_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.file_list_frame, text="/bin Directory Contents",
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=(10, 5), sticky="n")

        self.scrollable_file_list = ctk.CTkScrollableFrame(self.file_list_frame, label_text="Fichiers Exécutables")
        self.scrollable_file_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.scrollable_file_list.grid_columnconfigure(0, weight=1) # Name
        self.scrollable_file_list.grid_columnconfigure(1, weight=1) # Size
        self.scrollable_file_list.grid_columnconfigure(2, weight=1) # Permissions

        # --- Right Panel: Objdump Output ---
        self.objdump_output_frame = ctk.CTkFrame(self)
        self.objdump_output_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.objdump_output_frame.grid_rowconfigure(1, weight=1) # Allow textbox to expand
        self.objdump_output_frame.grid_columnconfigure(0, weight=1)

        self.current_binary_label = ctk.CTkLabel(self.objdump_output_frame, text="Survolez un fichier pour voir son désassemblage",
                                                 font=ctk.CTkFont(size=16, weight="bold"), wraplength=500)
        self.current_binary_label.grid(row=0, column=0, pady=(10, 5), sticky="n")

        self.objdump_textbox = scrolledtext.ScrolledText(
            self.objdump_output_frame,
            wrap=ctk.WORD,
            font=("Consolas", 10),
            bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkTextbox"]["fg_color"]),
            fg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkTextbox"]["text_color"]),
            insertbackground=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkTextbox"]["text_color"]),
            relief="flat"
        )
        self.objdump_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.objdump_textbox.insert(ctk.END, "Le désassemblage s'affichera ici.\n")
        self.objdump_textbox.configure(state="disabled") # Make it read-only

        # Load binaries after GUI is ready
        self.after(100, self.load_bin_files)

    def load_bin_files(self):
        """Loads and displays files from /bin directory into the table."""
        bin_path = "/bin"
        if not os.path.isdir(bin_path):
            messagebox.showerror("Error", f"Le répertoire '{bin_path}' n'existe pas ou n'est pas accessible.")
            return

        # Clear existing entries in the scrollable frame
        for widget in self.scrollable_file_list.winfo_children():
            widget.destroy()

        # Add table headers
        ctk.CTkLabel(self.scrollable_file_list, text="Nom du Fichier", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=2, sticky="ew")
        ctk.CTkLabel(self.scrollable_file_list, text="Taille (octets)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ctk.CTkLabel(self.scrollable_file_list, text="Permissions", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=5, pady=2, sticky="ew")

        row_idx = 1
        files = sorted(os.listdir(bin_path)) # Get files and sort them

        for filename in files:
            filepath = os.path.join(bin_path, filename)
            if os.path.isfile(filepath) and os.access(filepath, os.X_OK): # Only show executable files
                try:
                    file_stat = os.stat(filepath)
                    file_size = file_stat.st_size
                    file_permissions = stat.filemode(file_stat.st_mode)

                    # File Name Label (for hover effect)
                    name_label = ctk.CTkLabel(self.scrollable_file_list, text=filename, anchor="w", cursor="hand2", text_color="cyan")
                    name_label.grid(row=row_idx, column=0, padx=5, pady=1, sticky="ew")
                    
                    # Bind hover events
                    # We pass the filepath to the event handlers
                    name_label.bind("<Enter>", lambda event, path=filepath: self.on_file_hover_enter(event, path))
                    name_label.bind("<Leave>", self.on_file_hover_leave)

                    # Size Label
                    ctk.CTkLabel(self.scrollable_file_list, text=f"{file_size}", anchor="w").grid(row=row_idx, column=1, padx=5, pady=1, sticky="ew")

                    # Permissions Label
                    ctk.CTkLabel(self.scrollable_file_list, text=file_permissions, anchor="w").grid(row=row_idx, column=2, padx=5, pady=1, sticky="ew")

                    row_idx += 1
                except Exception as e:
                    # print(f"Could not get info for {filepath}: {e}") # For debugging
                    pass # Skip files we can't get info for

    def on_file_hover_enter(self, event, filepath):
        """Called when mouse enters a file name label."""
        if self.current_hover_thread and self.current_hover_thread.is_alive():
            # If a previous objdump is running, try to stop it (though not strictly necessary for hover)
            # For a simpler approach, we just let it finish and then update with the new one.
            pass

        self.current_binary_label.configure(text=f"Désassemblage de: {os.path.basename(filepath)}")
        self.objdump_textbox.configure(state="normal")
        self.objdump_textbox.delete(1.0, ctk.END)
        self.objdump_textbox.insert(ctk.END, f"Chargement du désassemblage pour {os.path.basename(filepath)}...\n")
        self.objdump_textbox.configure(state="disabled")
        self.update_idletasks() # Update GUI immediately

        # Start objdump in a new thread to keep UI responsive
        self.current_hover_thread = threading.Thread(target=self._run_objdump_threaded, args=(filepath,))
        self.current_hover_thread.daemon = True # Allow app to exit even if thread is running
        self.current_hover_thread.start()

    def on_file_hover_leave(self, event):
        """Called when mouse leaves a file name label."""
        # We might want to clear the display, but clearing on hover out can be annoying
        # if you just move the mouse slightly. Let's keep the last displayed content.
        # Alternatively, uncomment the lines below to clear on leave:
        # self.current_binary_label.configure(text="Survolez un fichier pour voir son désassemblage")
        # self.objdump_textbox.configure(state="normal")
        # self.objdump_textbox.delete(1.0, ctk.END)
        # self.objdump_textbox.insert(ctk.END, "Le désassemblage s'affichera ici.\n")
        # self.objdump_textbox.configure(state="disabled")
        pass

    def _run_objdump_threaded(self, filepath):
        """Executes objdump and updates the UI from a separate thread."""
        try:
            result = subprocess.run(
                ['objdump', '-d', filepath],
                capture_output=True,
                text=True,
                check=False,
                errors='ignore'
            )
            objdump_output = result.stdout if result.returncode == 0 else f"Erreur:\n{result.stderr}"
        except FileNotFoundError:
            objdump_output = "Erreur: La commande 'objdump' est introuvable."
        except Exception as e:
            objdump_output = f"Erreur inattendue: {e}"

        # Update GUI from the main thread
        self.after(0, lambda: self._update_objdump_display(objdump_output))

    def _update_objdump_display(self, text_content):
        """Updates the objdump text box in the main thread."""
        self.objdump_textbox.configure(state="normal")
        self.objdump_textbox.delete(1.0, ctk.END)
        self.objdump_textbox.insert(ctk.END, text_content)
        self.objdump_textbox.configure(state="disabled")
        self.objdump_textbox.see(ctk.TOP) # Scroll to the top of the output

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

    app = BinaryExplorerApp()
    app.mainloop()