import customtkinter as ctk
import os
import threading
from tkinter import filedialog, messagebox
import re # Pour les expressions régulières
import sys

# --- Constantes ---
JS_EXTENSIONS = ('.js', '.mjs')
MAX_FILE_PREVIEW_SIZE = 1024 * 100 # Taille maximale pour l'aperçu du fichier (100 KB)
MAX_PARSE_FILE_SIZE = 1024 * 500 # Taille maximale pour l'analyse JS (500 KB)

# --- Regex Patterns pour l'analyse JavaScript ---
# Function declaration: function funcName() { ... } or funcName = function() { ... }
FUNCTION_PATTERN_JS = re.compile(
    r'(?:^|\s|\W)(?:function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(|([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\(|([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(.*?\)\s*=>)'
)

# Class declaration: class ClassName { ... }
CLASS_PATTERN_JS = re.compile(r'^\s*class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)(?:\s+extends\s+[a-zA-Z_$][a-zA-Z0-9_$]*)?\s*\{', re.MULTILINE)

# Variable declarations: var, let, const
VAR_DECL_PATTERN_JS = re.compile(r'^\s*(?:var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)(?:\s*=|\s*;)', re.MULTILINE)

# Exports (e.g., export function, export const, export default)
EXPORT_PATTERN_JS = re.compile(r'^\s*export\s+(?:(?:default\s+)?(?:function|class|var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)|([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:function|\()|\{([^}]+)\})', re.MULTILINE)


class DirectoryTreeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Explorateur d'Arborescence et Analyseur JS (avec Dossiers Cachés)")
        self.geometry("1400x850") # Fenêtre plus large

        # Configurer la grille principale
        self.grid_columnconfigure(0, weight=1) # Pour l'arbre
        self.grid_columnconfigure(1, weight=2) # Pour l'aperçu du fichier/dir()
        self.grid_rowconfigure(2, weight=1) # Pour les zones de texte

        # --- Frame pour la sélection de dossier ---
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        self.path_frame.grid_columnconfigure(0, weight=1)

        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Chemin du répertoire à analyser")
        self.path_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.path_entry.insert(0, os.path.expanduser("~")) # Chemin par défaut: dossier personnel

        self.browse_button = ctk.CTkButton(self.path_frame, text="Parcourir", command=self.browse_directory)
        self.browse_button.grid(row=0, column=1, padx=(5, 10), pady=10)

        # --- Bouton d'Analyse et Label de Statut ---
        self.analyze_button = ctk.CTkButton(self, text="Analyser le Répertoire", command=self.start_analysis)
        self.analyze_button.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="Sélectionnez un répertoire et cliquez sur Analyser.", text_color="gray")
        self.status_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(50, 10), sticky="ew")

        # --- Zone de Texte pour l'Arborescence (Panneau Gauche) ---
        ctk.CTkLabel(self, text="Structure de l'Arborescence:").grid(row=2, column=0, padx=(10, 5), pady=(0, 0), sticky="sw")
        self.tree_textbox = ctk.CTkTextbox(self, wrap="none", width=680, height=600, font=("Courier New", 10))
        self.tree_textbox.grid(row=3, column=0, padx=(10, 5), pady=(0, 10), sticky="nsew")
        self.tree_textbox.configure(state="disabled")

        # --- Zone de Texte pour l'Aperçu/Dir() (Panneau Droit) ---
        ctk.CTkLabel(self, text="Aperçu du Fichier / Simulation dir():").grid(row=2, column=1, padx=(5, 10), pady=(0, 0), sticky="sw")
        self.preview_textbox = ctk.CTkTextbox(self, wrap="none", width=680, height=600, font=("Courier New", 10))
        self.preview_textbox.grid(row=3, column=1, padx=(5, 10), pady=(0, 10), sticky="nsew")
        self.preview_textbox.configure(state="disabled")

        self.analysis_thread = None
        self.file_paths_map = {} # Associe les numéros de ligne de la textbox aux chemins complets

        # Associer l'événement de clic à la zone de texte de l'arbre
        self.tree_textbox.bind("<Button-1>", self.on_tree_click)

    # --- Méthodes de mise à jour de l'UI ---
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

    # --- Navigation dans les répertoires ---
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, directory)

    # --- Gestion de l'Analyse (Threading) ---
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
        """Tâche d'analyse réelle exécutée dans un thread séparé."""
        tree_output, file_paths_map = self.generate_tree_structure(target_path)
        
        self.file_paths_map = file_paths_map # Stocke l'association ligne/chemin pour la gestion des clics

        # Met à jour les composants de l'UI sur le thread principal
        self.after(0, lambda: self.update_tree_textbox(tree_output)) 
        self.after(0, lambda: self.analyze_button.configure(state="normal"))
        self.after(0, lambda: self.browse_button.configure(state="normal"))
        self.after(0, lambda: self.path_entry.configure(state="normal"))
        self.after(0, lambda: self.update_status(f"Analyse de '{target_path}' terminée.", "green"))

    # --- Génération de l'Arborescence et Analyse JS ---
    def generate_tree_structure(self, start_path):
        """
        Génère une représentation textuelle de l'arborescence d'un répertoire.
        Inclut les dossiers/fichiers cachés.
        Retourne la chaîne de l'arbre et une carte des chemins de fichiers pour les clics.
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
                # Lire tous les éléments, y compris les cachés (ceux commençant par '.')
                contents = [item for item in os.listdir(current_path)]
                contents.sort(key=lambda x: (not os.path.isdir(os.path.join(current_path, x)), x.lower())) # Dossiers d'abord, puis alphabétique
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
                        output_buffer.append(f"{'│   ' * current_level}├── {item} <Non lisible>\n")
                        line_counter += 1
                except OSError:
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
                    if file_extension in JS_EXTENSIONS:
                        output_buffer.append(f"{current_prefix}{item} [JS]\n")
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
        """Gère les clics dans la zone de texte de l'arbre pour afficher le contenu ou la simulation dir()."""
        index = self.tree_textbox.index(f"@{event.x},{event.y}")
        line_num = int(float(index)) 

        full_path = self.file_paths_map.get(line_num - 1) 

        if full_path and os.path.isfile(full_path):
            self.update_status(f"Chargement de l'aperçu/dir() de '{os.path.basename(full_path)}'...", "blue")
            
            file_extension = os.path.splitext(full_path)[1].lower()
            if file_extension in JS_EXTENSIONS:
                # Effectue la simulation dir() pour les fichiers JavaScript
                self._simulate_js_dir(full_path)
            else:
                # Affiche l'aperçu du fichier pour les autres types de fichiers
                self._show_file_preview(full_path)
        elif full_path:
            self.update_preview_textbox(f"'{os.path.basename(full_path)}' n'est pas un fichier cliquable ou est un répertoire.")
            self.update_status("Sélectionnez un fichier pour voir l'aperçu.", "gray")
        else:
            self.update_preview_textbox("")
            self.update_status("Sélectionnez un fichier pour voir l'aperçu.", "gray")

    def _show_file_preview(self, file_path):
        """Affiche le contenu d'un fichier texte général."""
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

    def _simulate_js_dir(self, file_path):
        """
        Simule dir() pour les fichiers JavaScript en analysant leur contenu avec des regex.
        """
        try:
            file_size = os.path.getsize(file_path)
            if file_size > MAX_PARSE_FILE_SIZE:
                self.update_preview_textbox(f"Le fichier est trop volumineux ({file_size / 1024:.2f} KB) pour la simulation dir(). "
                                            f"Taille maximale : {MAX_PARSE_FILE_SIZE / 1024} KB.\n\n"
                                            f"--- Aperçu de début de fichier ---\n")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content_to_parse = f.read(MAX_PARSE_FILE_SIZE)
                self.preview_textbox.insert("end", content_to_parse) # Affiche un peu de contenu même si non entièrement analysé
                self.preview_textbox.insert("end", "\n\n--- Fin de l'aperçu ---")
                self.update_status(f"Fichier trop grand pour la simulation dir(). Aperçu limité.", "orange")
                return

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            functions = []
            for m in FUNCTION_PATTERN_JS.finditer(content):
                # Group 1 for function funcName(), Group 2 for funcName = function(), Group 3 for arrow functions
                if m.group(1): functions.append(m.group(1))
                if m.group(2): functions.append(m.group(2))
                if m.group(3): functions.append(m.group(3))
            functions = sorted(list(set(functions))) # Supprime les doublons et trie

            classes = sorted(list(set(m.group(1) for m in CLASS_PATTERN_JS.finditer(content))))
            
            variables = []
            for m in VAR_DECL_PATTERN_JS.finditer(content):
                variables.append(m.group(1))
            variables = sorted(list(set(variables)))

            exports = []
            for m in EXPORT_PATTERN_JS.finditer(content):
                if m.group(1): # For named exports (function, class, var, let, const)
                    exports.append(m.group(1))
                elif m.group(2): # For export varName = function() etc.
                    exports.append(m.group(2))
                elif m.group(3): # For object destructuring exports { item1, item2 }
                    exports.extend([s.strip() for s in m.group(3).split(',')])
            exports = sorted(list(set(exports)))


            output = [f"--- Simulation dir() pour '{os.path.basename(file_path)}' (JavaScript) ---\n"]
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

            output.append("\nVariables/Constantes (var, let, const):\n")
            if variables:
                for var in variables:
                    output.append(f"  - {var}\n")
            else:
                output.append("  (Aucune variable trouvée)\n")
            
            output.append("\nExports (estimation):\n")
            if exports:
                for exp in exports:
                    output.append(f"  - {exp}\n")
            else:
                output.append("  (Aucun export trouvé)\n")

            output.append("\n" + "="*50 + "\n")
            output.append("\nContenu du fichier:\n")
            # Affiche le contenu original du fichier après la simulation dir()
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