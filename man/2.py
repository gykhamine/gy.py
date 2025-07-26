import customtkinter as ctk
import subprocess
import sys
import os

class ManPageViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Afficheur de Pages de Manuel (man)")
        self.geometry("1000x700") # Generous initial window size

        # --- Configure main window grid ---
        self.grid_columnconfigure(0, weight=1) # Allow the single column to expand horizontally
        self.grid_rowconfigure(2, weight=1)    # Allow the output frame row to expand vertically

        # --- Command input frame ---
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1) # Allow the command entry to expand

        self.command_label = ctk.CTkLabel(input_frame, text="Nom de la Commande (pour man):")
        self.command_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.command_entry = ctk.CTkEntry(input_frame, placeholder_text="Ex: ls, grep, python")
        self.command_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Set a default command based on OS for convenience
        if sys.platform != "win32":
            self.command_entry.insert(0, "ls")

        self.execute_button = ctk.CTkButton(input_frame, text="Afficher la Page man", command=self.display_man_page)
        self.execute_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # --- Status label ---
        # Using CTkLabel for dynamic status messages and color changes
        self.status_label = ctk.CTkLabel(self, text="Entrez le nom d'une commande ci-dessus pour afficher sa page de manuel.",
                                         text_color="gray", height=20)
        self.status_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # --- Output frame for man page content ---
        # Removed 'label_text' from CTkFrame as it's not a supported argument for this widget.
        output_frame = ctk.CTkFrame(self) # CORRECTED LINE
        output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew") # Stretches in all directions

        # --- Add a title label INSIDE the output_frame ---
        output_title_label = ctk.CTkLabel(output_frame, text="Contenu de la Page de Manuel", font=ctk.CTkFont(size=16, weight="bold"))
        output_title_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Configure the grid of the OUTPUT FRAME itself
        output_frame.grid_columnconfigure(0, weight=1) # Allow the single column to expand
        output_frame.grid_rowconfigure(1, weight=1)    # Allow the textbox row to expand (row 0 is for the title label)

        # Using a monospace font for better readability of man pages
        self.output_textbox = ctk.CTkTextbox(output_frame, wrap="none", font=("Courier New", 10))
        # Placed in row 1, because row 0 is now used by output_title_label
        self.output_textbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.output_textbox.configure(state="disabled")

    def _update_textbox(self, textbox, content):
        """Updates the content of a CTkTextbox and sets it to read-only."""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", content)
        textbox.configure(state="disabled")

    def _update_status(self, message, color="gray"):
        """Updates the text and color of the status label."""
        self.status_label.configure(text=message, text_color=color)
        self.update_idletasks() # Force immediate GUI update

    def display_man_page(self):
        """Executes the 'man' command for the specified command and displays its output."""
        command_name = self.command_entry.get().strip()

        # Clear previous output and update status before execution
        self._update_status(f"Recherche de la page man pour '{command_name}'...", "orange")
        self._update_textbox(self.output_textbox, "") # Clear previous output

        if sys.platform == "win32":
            self._update_status("La commande 'man' n'est pas disponible par défaut sur Windows. Ce script est pour Unix-like.", "red")
            self._update_textbox(self.output_textbox,
                                 "La commande 'man' n'est pas une commande standard sur les systèmes Windows.\n"
                                 "Ce script est conçu pour les systèmes Unix-like (Linux, macOS, WSL).")
            return

        if not command_name:
            self._update_status("Veuillez entrer le nom d'une commande pour afficher sa page man.", "red")
            return

        try:
            # Prepare environment for 'man'
            env = os.environ.copy()
            # Force language to 'C' (default English) for more consistent output
            env["LANG"] = "C"

            # Execute 'man' command
            result = subprocess.run(
                ["man", "-P", "cat", "-E", "utf-8", command_name],
                capture_output=True,
                text=True,
                check=False, # Important: do not raise an exception if man returns a non-zero code
                encoding='utf-8',
                errors='replace', # Replace undecodable characters
                env=env # Use the modified environment
            )

            # Analyze return code and output
            if result.returncode != 0:
                # man command failed
                error_output = result.stderr.strip()
                if "No manual entry for" in error_output or "pas de page de manuel pour" in error_output:
                     self._update_status(f"Page man introuvable pour '{command_name}'.", "red")
                     self._update_textbox(self.output_textbox,
                                          f"La page de manuel pour '{command_name}' n'a pas été trouvée.\n"
                                          f"Veuillez vérifier l'orthographe ou essayer une autre commande.")
                else:
                    self._update_status(f"Erreur lors de l'exécution de man (Code {result.returncode}). Voir la sortie.", "red")
                    self._update_textbox(self.output_textbox,
                                         f"Une erreur est survenue lors de l'exécution de 'man {command_name}'.\n"
                                         f"Code de retour : {result.returncode}\n"
                                         f"Erreur STDERR : \n{error_output}")
            else:
                # Success: display standard output from man
                self._update_textbox(self.output_textbox, result.stdout)
                self._update_status(f"Page man pour '{command_name}' affichée avec succès.", "green")

        except FileNotFoundError:
            # Error if 'man' command itself is not found
            self._update_status("Erreur : La commande 'man' est introuvable sur votre système.", "red")
            self._update_textbox(self.output_textbox,
                                 "La commande 'man' n'a pas été trouvée.\n"
                                 "Veuillez vous assurer qu'elle est installée et accessible via votre PATH.")
        except Exception as e:
            # Catch any other unexpected errors
            self._update_status(f"Une erreur inattendue est survenue : {type(e).__name__} - {e}", "red")

        # Reset status message after a short delay
        self.after(5000, lambda: self._update_status("Prêt. Entrez le nom d'une commande ci-dessus.", "gray"))


if __name__ == "__main__":
    # Configure default customtkinter appearance
    ctk.set_appearance_mode("System") # "System", "Dark", "Light"
    ctk.set_default_color_theme("blue") # "blue", "dark-blue", "green"

    app = ManPageViewerApp()
    app.mainloop()