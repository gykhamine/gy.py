import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox, scrolledtext, StringVar
import re

class Instruction:
    """Représente une instruction désassemblée."""
    def __init__(self, address, opcode, mnemonic, operands, comment=""):
        self.address = address
        self.opcode = opcode
        self.mnemonic = mnemonic
        self.operands = operands
        self.comment = comment

    def __repr__(self):
        return f"Instr(Addr={self.address}, Opcode='{self.opcode}', Mnemonic='{self.mnemonic}', Operands='{self.operands}')"

    def format_for_display(self, show_address=True, show_opcode=True, show_mnemonic=True, show_operands=True, show_comment=False):
        parts = []
        if show_address:
            parts.append(f"{self.address}:")
        if show_opcode:
            parts.append(f"{self.opcode:<20}") # Pad opcode for alignment
        if show_mnemonic:
            parts.append(f"{self.mnemonic}")
        if show_operands:
            parts.append(f"{self.operands}")
        if show_comment and self.comment:
            parts.append(f" # {self.comment}")
        return "  ".join(parts).strip()


class ObjdumpViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analyseur de Binaires (objdump) - CustomTkinter")
        self.geometry("1200x800") # Encore plus grand pour l'analyse détaillée
        self.grid_columnconfigure(0, weight=0) # Sidebar for controls
        self.grid_columnconfigure(1, weight=1) # Main display area
        self.grid_rowconfigure(0, weight=1) # Allow main area to expand

        self.binaries_found = {} # Stores {filename: filepath}
        self.current_parsed_instructions = [] # Stores parsed Instruction objects
        self.current_binary_path = None

        # --- Left Sidebar for Controls ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1) # Push content to top

        ctk.CTkLabel(self.sidebar_frame, text="Paramètres d'Affichage", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        self.var_show_address = ctk.BooleanVar(value=True)
        self.checkbox_address = ctk.CTkCheckBox(self.sidebar_frame, text="Afficher Adresses", variable=self.var_show_address, command=self.update_display)
        self.checkbox_address.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.var_show_opcode = ctk.BooleanVar(value=True)
        self.checkbox_opcode = ctk.CTkCheckBox(self.sidebar_frame, text="Afficher Opcode", variable=self.var_show_opcode, command=self.update_display)
        self.checkbox_opcode.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.var_show_mnemonic = ctk.BooleanVar(value=True)
        self.checkbox_mnemonic = ctk.CTkCheckBox(self.sidebar_frame, text="Afficher Mnemonique", variable=self.var_show_mnemonic, command=self.update_display)
        self.checkbox_mnemonic.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        self.var_show_operands = ctk.BooleanVar(value=True)
        self.checkbox_operands = ctk.CTkCheckBox(self.sidebar_frame, text="Afficher Opérandes", variable=self.var_show_operands, command=self.update_display)
        self.checkbox_operands.grid(row=4, column=0, padx=20, pady=5, sticky="w")

        self.var_show_comment = ctk.BooleanVar(value=False)
        self.checkbox_comment = ctk.CTkCheckBox(self.sidebar_frame, text="Afficher Commentaires", variable=self.var_show_comment, command=self.update_display)
        self.checkbox_comment.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        ctk.CTkLabel(self.sidebar_frame, text="Sélection du Binaire:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=6, column=0, padx=20, pady=(20, 5), sticky="n")

        self.binary_combobox = ctk.CTkComboBox(
            self.sidebar_frame,
            values=["Scanning for binaries..."],
            state="readonly",
            command=self.load_selected_binary_objdump
        )
        self.binary_combobox.set("Scanning for binaries...") # Initial value
        self.binary_combobox.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.output_textbox = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=ctk.WORD,
            font=("Consolas", 10),
            bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkTextbox"]["fg_color"]),
            fg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkTextbox"]["text_color"]),
            insertbackground=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkTextbox"]["text_color"]),
            relief="flat"
        )
        self.output_textbox.grid(row=0, column=0, sticky="nsew")
        self.output_textbox.insert(ctk.END, "Scanning /bin and /sbin for executables. Please wait...\n")
        self.output_textbox.configure(state="disabled")

        # Start scanning in a separate thread to keep GUI responsive
        self.after(100, self.scan_binaries_async)

    def scan_binaries_async(self):
        """Starts the binary scanning process."""
        self.scan_directories(['/bin', '/sbin'])
        if self.binaries_found:
            self.binary_combobox.configure(values=list(self.binaries_found.keys()))
            # Try to pre-select a common binary like 'ls' or the first one
            if 'ls' in self.binaries_found:
                self.binary_combobox.set('ls')
                self.load_selected_binary_objdump('ls')
            else:
                first_binary = list(self.binaries_found.keys())[0]
                self.binary_combobox.set(first_binary)
                self.load_selected_binary_objdump(first_binary)
        else:
            self.binary_combobox.configure(values=["No executables found."])
            self.binary_combobox.set("No executables found.")
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete(1.0, ctk.END)
            self.output_textbox.insert(ctk.END, "No executable files found in /bin or /sbin.")
            self.output_textbox.configure(state="disabled")

    def scan_directories(self, directories):
        """Scans specified directories for executable files."""
        temp_binaries = {}
        for directory in directories:
            if not os.path.isdir(directory):
                self.output_textbox.configure(state="normal")
                self.output_textbox.insert(ctk.END, f"Warning: Directory '{directory}' does not exist or is not accessible.\n")
                self.output_textbox.configure(state="disabled")
                continue

            for root, _, files in os.walk(directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    if not os.path.islink(filepath) and os.path.isfile(filepath):
                        try:
                            if os.access(filepath, os.X_OK):
                                temp_binaries[filename] = filepath
                        except Exception:
                            pass # Ignore files that can't be accessed/checked
        self.binaries_found = dict(sorted(temp_binaries.items()))

    def execute_objdump(self, filepath):
        """Executes objdump -d on a given file and returns its raw output."""
        try:
            result = subprocess.run(
                ['objdump', '-d', filepath],
                capture_output=True,
                text=True,
                check=False,
                errors='ignore' # Ignore decoding errors for robustness
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error executing objdump on {filepath}:\n{result.stderr}"
        except FileNotFoundError:
            messagebox.showerror("Erreur", "La commande objdump n'est pas trouvée. Assurez-vous qu'elle est installée et dans votre PATH.")
            return "Erreur: La commande objdump n'est pas trouvée."
        except Exception as e:
            return f"Une erreur inattendue est survenue: {e}"

    def parse_objdump_output(self, raw_output):
        """
        Analyse la sortie brute de objdump -d et retourne une liste d'objets Instruction.
        """
        instructions = []
        current_section = ""
        # Regex pour capturer adresse, opcode, mnemonique, opérandes, et commentaires
        # Ex:   401000:       55                      push   %rbp
        # Ex:   401001:       48 89 e5                mov    %rsp,%rbp
        # Ex:   401004:       83 ec 10                sub    $0x10,%rsp
        instruction_pattern = re.compile(
            r"^\s*([0-9a-f]+):\s+([0-9a-f\s]+?)\s+([a-zA-Z_.]+)\s*([^#\n]*)(?:\s*#\s*(.*))?$"
        )

        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue

            # Capture des en-têtes de section comme ".text:"
            if re.match(r"^[0-9a-f]+ <\w+>:$", line) or re.match(r"Disassembly of section \.[\w\.]+:$", line):
                current_section = line
                # On peut ajouter une instruction spéciale pour marquer la section
                instructions.append(Instruction(address=line, opcode="", mnemonic="", operands="", comment=""))
                continue

            match = instruction_pattern.match(line)
            if match:
                address = match.group(1)
                opcode = match.group(2).strip()
                mnemonic = match.group(3).strip()
                operands = match.group(4).strip()
                comment = match.group(5) if match.group(5) else ""
                instructions.append(Instruction(address, opcode, mnemonic, operands, comment))
            # else:
            #     # Pour débug, afficher les lignes non parsées
            #     # print(f"Non parsé: {line}")
        return instructions

    def load_selected_binary_objdump(self, selected_binary_name):
        """Charge le binaire sélectionné, exécute objdump, analyse la sortie et met à jour l'affichage."""
        if selected_binary_name in ["Scanning for binaries...", "No executables found."]:
            return

        self.current_binary_path = self.binaries_found.get(selected_binary_name)
        if self.current_binary_path:
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete(1.0, ctk.END)
            self.output_textbox.insert(ctk.END, f"Chargement et analyse de : {self.current_binary_path}\n\n")
            self.update_idletasks() # Met à jour la GUI immédiatement

            raw_output = self.execute_objdump(self.current_binary_path)
            self.current_parsed_instructions = self.parse_objdump_output(raw_output)
            
            self.update_display() # Affiche la sortie analysée

        else:
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete(1.0, ctk.END)
            self.output_textbox.insert(ctk.END, f"Erreur : Chemin non trouvé pour '{selected_binary_name}'")
            self.output_textbox.configure(state="disabled")

    def update_display(self):
        """Met à jour le texte affiché en fonction des préférences de l'utilisateur."""
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete(1.0, ctk.END)

        if not self.current_parsed_instructions:
            self.output_textbox.insert(ctk.END, "Pas de données d'objdump à afficher pour ce binaire ou la sortie est vide.")
            self.output_textbox.configure(state="disabled")
            return

        show_address = self.var_show_address.get()
        show_opcode = self.var_show_opcode.get()
        show_mnemonic = self.var_show_mnemonic.get()
        show_operands = self.var_show_operands.get()
        show_comment = self.var_show_comment.get()

        for instr in self.current_parsed_instructions:
            # Gérer les lignes de section qui ne sont pas des instructions classiques
            if not instr.mnemonic and not instr.opcode and not instr.operands:
                self.output_textbox.insert(ctk.END, f"{instr.address}\n")
                continue

            formatted_line = instr.format_for_display(
                show_address, show_opcode, show_mnemonic, show_operands, show_comment
            )
            self.output_textbox.insert(ctk.END, formatted_line + "\n")

        self.output_textbox.configure(state="disabled")
        self.output_textbox.see(ctk.END) # Scroll to end


if __name__ == "__main__":
    # Paramètres d'apparence de CustomTkinter
    ctk.set_appearance_mode("System")  # Ou "Dark", "Light"
    ctk.set_default_color_theme("blue") # Ou "dark-blue", "green"

    app = ObjdumpViewerApp()
    app.mainloop()