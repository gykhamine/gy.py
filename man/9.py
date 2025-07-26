import customtkinter as ctk
import os
import threading
from tkinter import filedialog, messagebox # Pour la sélection de dossier et les messages
import sys

# Constantes pour les extensions C/C++
C_CPP_EXTENSIONS = ('.c', '.h', '.cpp', '.hpp', '.cc', '.hh', '.ipp', '.tpp')
MAX_FILE_PREVIEW_SIZE = 1024 * 50 # Taille maximale pour l'aperçu du fichier (50 KB)

class DirectoryTreeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Explorateur d'Arborescence (C/C++ Aware)")
        self.geometry("1200x800")

        # Configurer la grille principale
        self.grid_columnconfigure(0, weight=1) # Pour l'arbre
        self.grid_columnconfigure(1, weight=2) # Pour l'aperçu du fichier
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

        # --- Zone de Texte pour l'Arborescence ---
        ctk.CTkLabel(self, text="Structure de l'Arborescence:").grid(row=2, column=0, padx=(10, 5), pady=(0, 0), sticky="sw")
        self.tree_textbox = ctk.CTkTextbox(self, wrap="none", width=580, height=550, font=("Courier New", 10))
        self.tree_textbox.grid(row=3, column=0, padx=(10, 5), pady=(0, 10), sticky="nsew")
        self.tree_textbox.configure(state="disabled") # Lecture seule

        # --- Zone de Texte pour l'Aperçu du Fichier ---
        ctk.CTkLabel(self, text="Aperçu du Fichier:").grid(row=2, column=1, padx=(5, 10), pady=(0, 0), sticky="sw")
        self.preview_textbox = ctk.CTkTextbox(self, wrap="none", width=580, height=550, font=("Courier New", 10))
        self.preview_textbox.grid(row=3, column=1, padx=(5, 10), pady=(0, 10), sticky="nsew")
        self.preview_textbox.configure(state="disabled") # Lecture seule

        self.analysis_thread = None
        self.current_base_path = "" # Chemin de base du répertoire analysé

        # Associer l'événement de clic à la zone de texte de l'arbre
        self.tree_textbox.bind("<Button-1>", self.on_tree_click)

    def update_status(self, message, color="gray"):
        """Met à jour le message de statut dans l'interface."""
        self.status_label.configure(text=message, text_color=color)
        self.update_idletasks()

    def update_tree_textbox(self, content):
        """Met à jour la zone de texte de l'arbre."""
        self.tree_textbox.configure(state="normal")
        self.tree_textbox.delete("1.0", "end")
        self.tree_textbox.insert("end", content)
        self.tree_textbox.configure(state="disabled")

    def update_preview_textbox(self, content):
        """Met à jour la zone de texte de l'aperçu."""
        self.preview_textbox.configure(state="normal")
        self.preview_textbox.delete("1.0", "end")
        self.preview_textbox.insert("end", content)
        self.preview_textbox.configure(state="disabled")

    def browse_directory(self):
        """Ouvre une boîte de dialogue pour sélectionner un répertoire."""
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, directory)

    def start_analysis(self):
        """Démarre l'analyse dans un thread séparé pour ne pas bloquer l'interface."""
        target_path = self.path_entry.get()

        if not target_path:
            self.update_status("Veuillez sélectionner un répertoire à analyser.", "orange")
            return

        if not os.path.isdir(target_path):
            self.update_status(f"Erreur : '{target_path}' n'est pas un répertoire valide.", "red")
            return
            
        if self.analysis_thread and self.analysis_thread.is_alive():
            self.update_status("Analyse déjà en cours...", "orange")
            return

        self.current_base_path = target_path # Enregistrer le chemin de base pour les clics
        self.update_status(f"Début de l'analyse de '{target_path}'... Cela peut prendre un moment.", "blue")
        self.analyze_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.path_entry.configure(state="disabled")

        self.update_tree_textbox(f"Analyse de '{target_path}' en cours...\n")
        self.update_preview_textbox("") # Vider l'aperçu

        self.analysis_thread = threading.Thread(target=self._run_analysis_task, args=(target_path,))
        self.analysis_thread.start()

    def _run_analysis_task(self, target_path):
        """Tâche d'analyse réelle exécutée dans un thread."""
        tree_output, file_paths_map = self.generate_tree_structure(target_path)
        
        # Stocker la carte des chemins pour la gestion des clics
        self.file_paths_map = file_paths_map 

        # Mettre à jour l'UI dans le thread principal
        self.after(0, lambda: self.update_tree_textbox(tree_output)) 
        self.after(0, lambda: self.analyze_button.configure(state="normal"))
        self.after(0, lambda: self.browse_button.configure(state="normal"))
        self.after(0, lambda: self.path_entry.configure(state="normal"))
        self.after(0, lambda: self.update_status(f"Analyse de '{target_path}' terminée.", "green"))

    def generate_tree_structure(self, start_path):
        """
        Génère une représentation textuelle de l'arborescence d'un répertoire.
        Retourne la chaîne de l'arbre et une carte des chemins de fichiers pour les clics.
        """
        output_buffer = []
        # Store full paths for clickable items: {line_number_in_textbox: full_path}
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
        
        # Helper function for recursive tree generation
        def _build_tree(current_path, current_level, last_item_flags):
            nonlocal line_counter # Permet de modifier line_counter de la fonction parente
            
            try:
                contents = sorted(os.listdir(current_path))
            except PermissionError:
                output_buffer.append(f"{'│   ' * current_level}├── <Accès refusé>\n")
                line_counter += 1
                return # Stop recursion for this unreadable directory
            except Exception as e:
                output_buffer.append(f"{'│   ' * current_level}├── <Erreur: {e}>\n")
                line_counter += 1
                return # Stop recursion

            readable_contents = []
            for item in contents:
                item_path = os.path.join(current_path, item)
                try:
                    # Check readability before attempting further ops
                    if os.access(item_path, os.R_OK):
                        readable_contents.append(item)
                    else:
                        output_buffer.append(f"{'│   ' * current_level}├── {item} <Non lisible>\n")
                        line_counter += 1
                except OSError:
                    # e.g., broken symlinks can raise OSError on os.access
                    output_buffer.append(f"{'│   ' * current_level}├── {item} <Erreur d'accès/Symlink cassé>\n")
                    line_counter += 1
                    pass 

            for i, item in enumerate(readable_contents):
                item_path = os.path.join(current_path, item)
                is_last = (i == len(readable_contents) - 1)
                
                # Build the current line prefix based on parent's last_item_flags
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
                    # Recurse for subdirectories
                    _build_tree(item_path, current_level + 1, last_item_flags + [is_last])
                elif os.path.isfile(item_path):
                    file_extension = os.path.splitext(item)[1].lower()
                    if file_extension in C_CPP_EXTENSIONS:
                        output_buffer.append(f"{current_prefix}{item} [C/C++]\n")
                    else:
                        output_buffer.append(f"{current_prefix}{item}\n")
                    
                    line_counter += 1
                    # Store mapping for clickable files
                    file_paths_map[line_counter - 1] = item_path # Line number is 1-based in Tkinter, but we use 0-based for map
            
        try:
            _build_tree(start_path, 0, [])
        except Exception as e:
            self.update_status(f"Une erreur est survenue pendant l'analyse : {e}", "red")
            output_buffer.append(f"\nErreur lors de l'analyse : {e}")

        return "".join(output_buffer), file_paths_map

    def on_tree_click(self, event):
        """Gère les clics dans la zone de texte de l'arbre pour afficher le contenu du fichier."""
        # Obtenir la ligne sur laquelle l'utilisateur a cliqué
        index = self.tree_textbox.index(f"@{event.x},{event.y}")
        line_num = int(float(index)) # Convertir "1.0" -> 1.0 -> 1

        # Utiliser la carte des chemins pour trouver le fichier correspondant
        # Tkinter line index is 1-based, our map is 0-based for convenience
        full_path = self.file_paths_map.get(line_num - 1) 

        if full_path and os.path.isfile(full_path):
            self.update_status(f"Chargement de l'aperçu de '{os.path.basename(full_path)}'...", "blue")
            try:
                file_size = os.path.getsize(full_path)
                if file_size > MAX_FILE_PREVIEW_SIZE:
                    self.update_preview_textbox(f"Le fichier est trop volumineux ({file_size / 1024:.2f} KB) pour être affiché entièrement. "
                                                f"Taille maximale : {MAX_FILE_PREVIEW_SIZE / 1024} KB.\n\n"
                                                f"--- Début de l'aperçu (premiers {MAX_FILE_PREVIEW_SIZE} octets) ---\n")
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(MAX_FILE_PREVIEW_SIZE)
                        self.preview_textbox.insert("end", content)
                    self.preview_textbox.insert("end", "\n\n--- Fin de l'aperçu ---")
                else:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self.update_preview_textbox(content)
                self.update_status(f"Aperçu de '{os.path.basename(full_path)}' chargé.", "green")
            except Exception as e:
                self.update_status(f"Erreur lors de la lecture du fichier : {e}", "red")
                self.update_preview_textbox(f"Impossible de lire le fichier '{full_path}':\n{e}")
        elif full_path:
            self.update_preview_textbox(f"'{os.path.basename(full_path)}' n'est pas un fichier ou n'est pas cliquable.")
            self.update_status("Sélectionnez un fichier pour voir l'aperçu.", "gray")
        else:
            self.update_preview_textbox("") # Clear preview if nothing is selected or it's a directory
            self.update_status("Sélectionnez un fichier pour voir l'aperçu.", "gray")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

    app = DirectoryTreeApp()
    app.mainloop()