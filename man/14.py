import os
import subprocess
import customtkinter as ctk
from tkinter import scrolledtext, messagebox

class SimpleBinaryDisassembler(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Désassembleur de Binaires Simple")
        self.geometry("1200x700")

        # Configure grid for main layout
        self.grid_columnconfigure(0, weight=1) # Left panel for input
        self.grid_columnconfigure(1, weight=3) # Right panel for objdump output
        self.grid_rowconfigure(0, weight=1)

        # --- Left Panel: Input ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.input_frame.grid_rowconfigure(3, weight=1) # Push content to top
        self.input_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.input_frame, text="Chemin du Fichier Binaire",
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=(10, 5), sticky="n")

        self.filepath_entry = ctk.CTkEntry(self.input_frame, placeholder_text="/bin/ls ou /usr/bin/python3", width=300)
        self.filepath_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.filepath_entry.bind("<Return>", self.on_disassemble_button_click) # Allow pressing Enter

        self.disassemble_button = ctk.CTkButton(self.input_frame, text="Désassembler", command=self.on_disassemble_button_click)
        self.disassemble_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Add a browse button for convenience, even with manual entry
        self.browse_button = ctk.CTkButton(self.input_frame, text="Parcourir le Système de Fichiers...", command=self.browse_file)
        self.browse_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")


        # --- Right Panel: Objdump Output ---
        self.objdump_output_frame = ctk.CTkFrame(self)
        self.objdump_output_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.objdump_output_frame.grid_rowconfigure(1, weight=1) # Allow textbox to expand
        self.objdump_output_frame.grid_columnconfigure(0, weight=1)

        self.current_binary_label = ctk.CTkLabel(self.objdump_output_frame, text="Entrez un chemin de fichier et cliquez sur Désassembler",
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

    def browse_file(self):
        """
        Ouvre une boîte de dialogue pour permettre à l'utilisateur de sélectionner un fichier.
        """
        filepath = filedialog.askopenfilename(
            title="Sélectionner un Fichier Binaire",
            initialdir="/", # Commence à la racine pour une liberté totale
            filetypes=[("Tous les fichiers", "*.*")] # Voir tous les fichiers par défaut
        )
        if filepath:
            self.filepath_entry.delete(0, ctk.END) # Clear existing text
            self.filepath_entry.insert(0, filepath) # Insert selected path
            self.on_disassemble_button_click() # Automatically disassemble

    def on_disassemble_button_click(self, event=None):
        """Called when Disassemble button is clicked or Enter is pressed in entry."""
        filepath = self.filepath_entry.get().strip()

        if not filepath:
            messagebox.showwarning("Attention", "Veuillez entrer un chemin de fichier.")
            return

        if not os.path.exists(filepath):
            messagebox.showerror("Erreur", f"Le fichier '{filepath}' n'existe pas.")
            return

        # Update display with loading message
        self.current_binary_label.configure(text=f"Désassemblage de: {os.path.basename(filepath)}")
        self.objdump_textbox.configure(state="normal")
        self.objdump_textbox.delete(1.0, ctk.END)
        self.objdump_textbox.insert(ctk.END, f"Chargement du désassemblage pour {os.path.basename(filepath)}...\n")
        self.objdump_textbox.configure(state="disabled")
        self.update_idletasks() # Update GUI immediately

        # Run objdump and display result
        self.execute_objdump_and_display(filepath)

    def execute_objdump_and_display(self, filepath):
        """Executes objdump -d on a given file and displays its output."""
        try:
            # objdump can analyze files that are not marked as executable
            if not os.path.isfile(filepath):
                objdump_output = f"Erreur: Le chemin '{filepath}' n'est pas un fichier valide."
            else:
                result = subprocess.run(
                    ['objdump', '-d', filepath],
                    capture_output=True,
                    text=True,
                    check=False,
                    errors='ignore' # Ignore decoding errors
                )
                if result.returncode == 0:
                    objdump_output = result.stdout
                else:
                    objdump_output = (f"Erreur lors de l'exécution de objdump sur {filepath}:\n"
                                      f"Code de sortie: {result.returncode}\n{result.stderr}")
        except FileNotFoundError:
            objdump_output = "Erreur: La commande 'objdump' est introuvable. " \
                             "Veuillez vous assurer qu'elle est installée (paquet binutils) et dans votre PATH système."
        except Exception as e:
            objdump_output = f"Une erreur inattendue est survenue: {e}"

        self.objdump_textbox.configure(state="normal")
        self.objdump_textbox.delete(1.0, ctk.END)
        self.objdump_textbox.insert(ctk.END, objdump_output)
        self.objdump_textbox.configure(state="disabled")
        self.objdump_textbox.see(ctk.TOP) # Scroll to the top of the output

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

    app = SimpleBinaryDisassembler()
    app.mainloop()