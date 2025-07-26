import customtkinter as ctk
import os
import threading
from tkinter import filedialog, messagebox
import re # For regular expressions
import sys

# --- Constants ---
C_CPP_EXTENSIONS = ('.c', '.h', '.cpp', '.hpp', '.cc', '.hh', '.ipp', '.tpp')
MAX_FILE_PREVIEW_SIZE = 1024 * 100 # Max size for file content preview (100 KB)
MAX_PARSE_FILE_SIZE = 1024 * 500 # Max size for C/CPP parsing (500 KB)

# --- Regex Patterns for C/C++ Parsing ---
# Basic function declaration (handles return type, name, params, but can be imperfect)
# Attempts to capture: ReturnType FunctionName(Parameters)
FUNCTION_PATTERN = re.compile(
    r'^\s*(?:(?:static|inline|virtual|friend|explicit|extern)\s+)?'  # Optional keywords
    r'(?:[a-zA-Z_][a-zA-Z0-9_]*\s+)?' # Optional storage class (e.g. extern)
    r'(?:[a-zA-Z_][a-zA-Z0-9_]*(?:\s*\*+\s*|\s*&+\s*)*\s+)+' # Return type (e.g., int*, const char&)
    r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(' # Function name (Group 1) and opening parenthesis
    r'([^)]*)' # Parameters (Group 2)
    r'\)\s*(?:const)?\s*(?:noexcept)?\s*(?:override)?\s*;' # Closing parenthesis, optional qualifiers, semicolon
    , re.MULTILINE
)

# Class declaration: class ClassName { ... };
CLASS_PATTERN = re.compile(r'^\s*(?:template\s*<[^>]+>\s*)?(?:class|struct)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::[^\{]*)?\{', re.MULTILINE)

# Struct declaration (might overlap with class, but often separate for clarity)
STRUCT_PATTERN = re.compile(r'^\s*(?:template\s*<[^>]+>\s*)?struct\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::[^\{]*)?\{', re.MULTILINE)

# Enum declaration: enum EnumName { ... }; or enum class EnumName { ... };
ENUM_PATTERN = re.compile(r'^\s*enum(?:\s+class|\s+struct)?\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::[^\{]*)?\{', re.MULTILINE)

# Macro definition: #define MACRO_NAME value or #define MACRO_NAME(params) value
MACRO_PATTERN = re.compile(r'^\s*#define\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\([^)]*\))?\s+.*', re.MULTILINE)

# Global Variable (simple attempt: Type var_name;)
# This is very basic and prone to false positives (e.g., local vars)
GLOBAL_VAR_PATTERN = re.compile(
    r'^\s*(?:extern|static|const)?\s+' # Optional keywords
    r'(?:[a-zA-Z_][a-zA-Z0-9_]*(?:\s*\*+\s*|\s*&+\s*)*\s+)+' # Type (e.g., int*, std::string&)
    r'([a-zA-Z_][a-zA-Z0-9_]*)\s*;' # Variable name (Group 1) and semicolon
    , re.MULTILINE
)

class DirectoryTreeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Explorateur C/C++ et Analyseur Dir()")
        self.geometry("1400x850") # Make window wider

        # Configure main grid
        self.grid_columnconfigure(0, weight=1) # For the tree
        self.grid_columnconfigure(1, weight=2) # For the file preview/dir() output
        self.grid_rowconfigure(2, weight=1) # For the text areas

        # --- Path Selection Frame ---
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        self.path_frame.grid_columnconfigure(0, weight=1)

        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Chemin du répertoire à analyser")
        self.path_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.path_entry.insert(0, os.path.expanduser("~")) # Default path: home directory

        self.browse_button = ctk.CTkButton(self.path_frame, text="Parcourir", command=self.browse_directory)
        self.browse_button.grid(row=0, column=1, padx=(5, 10), pady=10)

        # --- Analyze Button and Status Label ---
        self.analyze_button = ctk.CTkButton(self, text="Analyser le Répertoire", command=self.start_analysis)
        self.analyze_button.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="Sélectionnez un répertoire et cliquez sur Analyser.", text_color="gray")
        self.status_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(50, 10), sticky="ew")

        # --- Tree Textbox (Left Panel) ---
        ctk.CTkLabel(self, text="Structure de l'Arborescence:").grid(row=2, column=0, padx=(10, 5), pady=(0, 0), sticky="sw")
        self.tree_textbox = ctk.CTkTextbox(self, wrap="none", width=680, height=600, font=("Courier New", 10))
        self.tree_textbox.grid(row=3, column=0, padx=(10, 5), pady=(0, 10), sticky="nsew")
        self.tree_textbox.configure(state="disabled")

        # --- Preview/Dir() Textbox (Right Panel) ---
        ctk.CTkLabel(self, text="Aperçu du Fichier / Simulation dir():").grid(row=2, column=1, padx=(5, 10), pady=(0, 0), sticky="sw")
        self.preview_textbox = ctk.CTkTextbox(self, wrap="none", width=680, height=600, font=("Courier New", 10))
        self.preview_textbox.grid(row=3, column=1, padx=(5, 10), pady=(0, 10), sticky="nsew")
        self.preview_textbox.configure(state="disabled")

        self.analysis_thread = None
        self.file_paths_map = {} # Maps textbox line numbers to full file paths

        # Bind click event to the tree textbox
        self.tree_textbox.bind("<Button-1>", self.on_tree_click)

    # --- UI Update Methods ---
    def update_status(self, message, color="gray"):
        self.status_label.configure(text=message, text_color=color)
        self.update_idletasks()

    def update_tree_textbox(self, content):
        self.tree_textbox.configure(state="normal")
        self.tree_textbox.delete("1.0", "end")
        self.tree_textbox.insert("end", content)
        self.tree_textbox.configure(state="disabled")

    def update_preview_textbox(self, content):
        self.preview_textbox.configure(state="normal")
        self.preview_textbox.delete("1.0", "end")
        self.preview_textbox.insert("end", content)
        self.preview_textbox.configure(state="disabled")

    # --- Directory Browse ---
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, directory)

    # --- Analysis Management (Threading) ---
    def start_analysis(self):
        target_path = self.path_entry.get()

        if not target_path or not os.path.isdir(target_path):
            self.update_status(f"Erreur : '{target_path}' n'est pas un répertoire valide.", "red")
            return
            
        if self.analysis_thread and self.analysis_thread.is_alive():
            self.update_status("Analyse déjà en cours...", "orange")
            return

        self.update_status(f"Début de l'analyse de '{target_path}'... Cela peut prendre un moment.", "blue")
        self.analyze_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.path_entry.configure(state="disabled")

        self.update_tree_textbox(f"Analyse de '{target_path}' en cours...\n")
        self.update_preview_textbox("")

        self.analysis_thread = threading.Thread(target=self._run_analysis_task, args=(target_path,))
        self.analysis_thread.start()

    def _run_analysis_task(self, target_path):
        """Actual analysis task run in a separate thread."""
        tree_output, file_paths_map = self.generate_tree_structure(target_path)
        
        self.file_paths_map = file_paths_map # Store file path map for click handling

        # Update UI components on the main thread
        self.after(0, lambda: self.update_tree_textbox(tree_output)) 
        self.after(0, lambda: self.analyze_button.configure(state="normal"))
        self.after(0, lambda: self.browse_button.configure(state="normal"))
        self.after(0, lambda: self.path_entry.configure(state="normal"))
        self.after(0, lambda: self.update_status(f"Analyse de '{target_path}' terminée.", "green"))

    # --- Tree Generation and C/C++ Parsing ---
    def generate_tree_structure(self, start_path):
        """
        Generates a text-based tree representation of a directory.
        Returns the tree string and a map of line numbers to file paths for clickable items.
        """
        output_buffer = []
        file_paths_map = {} 
        line_counter = 0

        if not os.path.exists(start_path):
            self.update_status(f"Erreur : Le chemin '{start_path}' n'existe pas.", "red")
            return f"Erreur : Le chemin '{start_path}' n'existe pas.", {}

        if not os.path.isdir(start_path):
            self.update_status(f"Erreur : '{start_path}' n'est pas un répertoire.", "red")
            return f"Erreur : '{start_path}' n'est pas un répertoire.", {}
            
        if not os.access(start_path, os.R_OK):
            self.update_status(f"Erreur : Permissions insuffisantes pour lire '{start_path}'.", "red")
            return (f"Erreur : Permissions insuffisantes pour lire '{start_path}'.\n"
                    f"Veuillez choisir un répertoire accessible ou exécuter le script avec 'sudo' si nécessaire."), {}

        output_buffer.append(f"{os.path.basename(start_path)}/\n")
        line_counter += 1
        
        def _build_tree(current_path, current_level, last_item_flags):
            nonlocal line_counter 
            
            try:
                contents = sorted(os.listdir(current_path))
            except PermissionError:
                output_buffer.append(f"{'│   ' * current_level}├── <Accès refusé>\n")
                line_counter += 1
                return
            except Exception as e:
                output_buffer.append(f"{'│   ' * current_level}├── <Erreur: {e}>\n")
                line_counter += 1
                return

            readable_contents = []
            for item in contents:
                item_path = os.path.join(current_path, item)
                try:
                    if os.access(item_path, os.R_OK):
                        readable_contents.append(item)
                    else:
                        # Only append if we know it's not readable
                        output_buffer.append(f"{'│   ' * current_level}├── {item} <Non lisible>\n")
                        line_counter += 1
                except OSError:
                    # Catch OS errors like broken symlinks
                    output_buffer.append(f"{'│   ' * current_level}├── {item} <Erreur d'accès/Symlink cassé>\n")
                    line_counter += 1
                    pass 

            for i, item in enumerate(readable_contents):
                item_path = os.path.join(current_path, item)
                is_last = (i == len(readable_contents) - 1)
                
                current_prefix = ""
                for flag in last_item_flags:
                    current_prefix += "    " if flag else "│   "
                
                if is_last:
                    current_prefix += "└── "
                else:
                    current_prefix += "├── "
                
                if os.path.isdir(item_path):
                    output_buffer.append(f"{current_prefix}{item}/\n")
                    line_counter += 1
                    _build_tree(item_path, current_level + 1, last_item_flags + [is_last])
                elif os.path.isfile(item_path):
                    file_extension = os.path.splitext(item)[1].lower()
                    if file_extension in C_CPP_EXTENSIONS:
                        output_buffer.append(f"{current_prefix}{item} [C/C++]\n")
                    else:
                        output_buffer.append(f"{current_prefix}{item}\n")
                    
                    line_counter += 1
                    file_paths_map[line_counter - 1] = item_path 
            
        try:
            _build_tree(start_path, 0, [])
        except Exception as e:
            self.update_status(f"Une erreur est survenue pendant l'analyse : {e}", "red")
            output_buffer.append(f"\nErreur lors de l'analyse : {e}")

        return "".join(output_buffer), file_paths_map

    def on_tree_click(self, event):
        """Handles clicks in the tree textbox to display file content or dir() simulation."""
        index = self.tree_textbox.index(f"@{event.x},{event.y}")
        line_num = int(float(index)) 

        full_path = self.file_paths_map.get(line_num - 1) 

        if full_path and os.path.isfile(full_path):
            self.update_status(f"Chargement de l'aperçu/dir() de '{os.path.basename(full_path)}'...", "blue")
            
            file_extension = os.path.splitext(full_path)[1].lower()
            if file_extension in C_CPP_EXTENSIONS:
                # Perform dir() simulation for C/C++ files
                self._simulate_c_cpp_dir(full_path)
            else:
                # Show regular file preview for other files
                self._show_file_preview(full_path)
        elif full_path:
            self.update_preview_textbox(f"'{os.path.basename(full_path)}' n'est pas un fichier cliquable ou est un répertoire.")
            self.update_status("Sélectionnez un fichier pour voir l'aperçu.", "gray")
        else:
            self.update_preview_textbox("")
            self.update_status("Sélectionnez un fichier pour voir l'aperçu.", "gray")

    def _show_file_preview(self, file_path):
        """Displays the content of a general text file."""
        try:
            file_size = os.path.getsize(file_path)
            if file_size > MAX_FILE_PREVIEW_SIZE:
                preview_content = (f"Le fichier est trop volumineux ({file_size / 1024:.2f} KB) pour être affiché entièrement. "
                                   f"Taille maximale : {MAX_FILE_PREVIEW_SIZE / 1024} KB.\n\n"
                                   f"--- Début de l'aperçu ---\n")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    preview_content += f.read(MAX_FILE_PREVIEW_SIZE)
                preview_content += "\n\n--- Fin de l'aperçu ---"
                self.update_preview_textbox(preview_content)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self.update_preview_textbox(content)
            self.update_status(f"Aperçu de '{os.path.basename(file_path)}' chargé.", "green")
        except Exception as e:
            self.update_status(f"Erreur lors de la lecture du fichier : {e}", "red")
            self.update_preview_textbox(f"Impossible de lire le fichier '{file_path}':\n{e}")

    def _simulate_c_cpp_dir(self, file_path):
        """
        Simulates dir() for C/C++ files by parsing their content using regex.
        """
        try:
            file_size = os.path.getsize(file_path)
            if file_size > MAX_PARSE_FILE_SIZE:
                self.update_preview_textbox(f"Le fichier est trop volumineux ({file_size / 1024:.2f} KB) pour la simulation dir(). "
                                            f"Taille maximale : {MAX_PARSE_FILE_SIZE / 1024} KB.\n\n"
                                            f"--- Aperçu de début de fichier ---\n")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content_to_parse = f.read(MAX_PARSE_FILE_SIZE)
                self.preview_textbox.insert("end", content_to_parse) # Show some content even if not fully parsed
                self.preview_textbox.insert("end", "\n\n--- Fin de l'aperçu ---")
                self.update_status(f"Fichier trop grand pour la simulation dir(). Aperçu limité.", "orange")
                return

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            functions = sorted(list(set(m.group(1) for m in FUNCTION_PATTERN.finditer(content))))
            classes = sorted(list(set(m.group(1) for m in CLASS_PATTERN.finditer(content))))
            structs = sorted(list(set(m.group(1) for m in STRUCT_PATTERN.finditer(content))))
            enums = sorted(list(set(m.group(1) for m in ENUM_PATTERN.finditer(content))))
            macros = sorted(list(set(m.group(1) for m in MACRO_PATTERN.finditer(content))))
            global_vars = sorted(list(set(m.group(1) for m in GLOBAL_VAR_PATTERN.finditer(content))))

            output = [f"--- Simulation dir() pour '{os.path.basename(file_path)}' ---\n"]
            output.append("\nFonctions:\n")
            if functions:
                for func in functions:
                    output.append(f"  - {func}()\n")
            else:
                output.append("  (Aucune fonction trouvée)\n")

            output.append("\nClasses:\n")
            if classes:
                for cls in classes:
                    output.append(f"  - {cls}\n")
            else:
                output.append("  (Aucune classe trouvée)\n")

            output.append("\nStructures (Structs):\n")
            if structs:
                for s in structs:
                    output.append(f"  - {s}\n")
            else:
                output.append("  (Aucune structure trouvée)\n")
            
            output.append("\nÉnumérations (Enums):\n")
            if enums:
                for e in enums:
                    output.append(f"  - {e}\n")
            else:
                output.append("  (Aucune énumération trouvée)\n")

            output.append("\nMacros (#define):\n")
            if macros:
                for m in macros:
                    output.append(f"  - {m}\n")
            else:
                output.append("  (Aucune macro trouvée)\n")

            output.append("\nVariables Globales (estimation):\n")
            if global_vars:
                for gv in global_vars:
                    output.append(f"  - {gv}\n")
            else:
                output.append("  (Aucune variable globale estimée)\n")

            output.append("\n" + "="*50 + "\n")
            output.append("\nContenu du fichier:\n")
            # Show original file content after dir() simulation
            output.append(content)

            self.update_preview_textbox("".join(output))
            self.update_status(f"Simulation dir() pour '{os.path.basename(file_path)}' terminée.", "green")

        except Exception as e:
            self.update_status(f"Erreur lors de la simulation dir() ou de la lecture du fichier : {e}", "red")
            self.update_preview_textbox(f"Impossible de simuler dir() pour '{file_path}':\n{e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = DirectoryTreeApp()
    app.mainloop()