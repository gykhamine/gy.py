import customtkinter as ctk
import os
import threading
from tkinter import filedialog # Pour la sélection de dossier

class DirectoryTreeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Explorateur d'Arborescence de Répertoire")
        self.geometry("900x700")

        # Configurer la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Pour la zone de texte principale

        # Frame pour la sélection de dossier
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.path_frame.grid_columnconfigure(0, weight=1)

        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Chemin du répertoire à analyser")
        self.path_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.path_entry.insert(0, os.path.expanduser("~")) # Chemin par défaut: dossier personnel

        self.browse_button = ctk.CTkButton(self.path_frame, text="Parcourir", command=self.browse_directory)
        self.browse_button.grid(row=0, column=1, padx=(5, 10), pady=10)

        # Bouton d'Analyse et Label de Statut
        self.analyze_button = ctk.CTkButton(self, text="Analyser le Répertoire", command=self.start_analysis)
        self.analyze_button.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="Sélectionnez un répertoire et cliquez sur Analyser.", text_color="gray")
        self.status_label.grid(row=1, column=0, padx=10, pady=(50, 10), sticky="ew")

        # Zone de Texte pour les Résultats
        self.results_textbox = ctk.CTkTextbox(self, wrap="none", width=880, height=550, font=("Courier New", 10))
        self.results_textbox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.results_textbox.configure(state="disabled") # Lecture seule

        self.analysis_thread = None

    def update_status(self, message, color="gray"):
        """Met à jour le message de statut dans l'interface."""
        self.status_label.configure(text=message, text_color=color)
        self.update_idletasks()

    def update_results(self, content):
        """Met à jour la zone de texte des résultats."""
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("end", content)
        self.results_textbox.configure(state="disabled")

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

        self.update_status(f"Début de l'analyse de '{target_path}'... Cela peut prendre un moment.", "blue")
        self.analyze_button.configure(state="disabled") # Désactiver le bouton pendant l'analyse
        self.browse_button.configure(state="disabled")
        self.path_entry.configure(state="disabled")

        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("end", f"Analyse de '{target_path}' en cours...\n")
        self.results_textbox.configure(state="disabled")

        self.analysis_thread = threading.Thread(target=self._run_analysis_task, args=(target_path,))
        self.analysis_thread.start()

    def _run_analysis_task(self, target_path):
        """Tâche d'analyse réelle exécutée dans un thread."""
        results = self.generate_tree_structure(target_path)
        
        # Mettre à jour l'UI dans le thread principal
        self.after(0, lambda: self.update_results(results)) 
        self.after(0, lambda: self.analyze_button.configure(state="normal")) # Réactiver le bouton
        self.after(0, lambda: self.browse_button.configure(state="normal"))
        self.after(0, lambda: self.path_entry.configure(state="normal"))
        self.after(0, lambda: self.update_status(f"Analyse de '{target_path}' terminée.", "green"))

    def generate_tree_structure(self, start_path):
        """
        Génère une représentation textuelle de l'arborescence d'un répertoire.
        """
        output_buffer = []

        if not os.path.exists(start_path):
            self.update_status(f"Erreur : Le chemin '{start_path}' n'existe pas.", "red")
            return f"Erreur : Le chemin '{start_path}' n'existe pas."

        if not os.path.isdir(start_path):
            self.update_status(f"Erreur : '{start_path}' n'est pas un répertoire.", "red")
            return f"Erreur : '{start_path}' n'est pas un répertoire."
            
        # Check if the directory is readable
        if not os.access(start_path, os.R_OK):
            self.update_status(f"Erreur : Permissions insuffisantes pour lire '{start_path}'.", "red")
            return (f"Erreur : Permissions insuffisantes pour lire '{start_path}'.\n"
                    f"Veuillez choisir un répertoire accessible ou exécuter le script avec 'sudo' si nécessaire.")

        output_buffer.append(f"{os.path.basename(start_path)}/\n")
        
        # Le préfixe pour chaque niveau de profondeur
        # pipe: pour les branches qui continuent
        # elbow: pour la dernière branche d'un niveau
        # space: pour l'indentation
        # tee: non utilisé directement mais pour référence
        
        # On va stocker l'arborescence complète dans une liste de tuples (niveau, nom, type)
        # pour la formater ensuite. Ou plus simplement, on va construire directement la sortie.

        try:
            # os.walk parcourt le répertoire de manière récursive
            # On utilise le paramètre topdown=True par défaut
            for root, dirs, files in os.walk(start_path):
                level = root.replace(start_path, '').count(os.sep)
                # Calcule l'indentation
                indent = '│   ' * level
                
                # Trie les dossiers et fichiers pour une sortie cohérente
                dirs.sort()
                files.sort()

                # Les dossiers seront ajoutés après les fichiers du niveau précédent pour un affichage cohérent
                # ou juste avant leurs propres contenus

                # Si c'est le répertoire de base, on l'a déjà affiché.
                if root != start_path:
                    # Détermine si c'est le dernier dossier du niveau supérieur
                    parent_dir = os.path.dirname(root)
                    siblings = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
                    is_last_sibling = (os.path.basename(root) == siblings[-1]) if siblings else True

                    # Ajuste le préfixe pour le dossier courant
                    # Pour les dossiers, on affiche le dossier lui-même
                    # Si c'est le dernier élément au niveau de son parent, c'est un '└──'
                    # Sinon, c'est un '├──'
                    prefix = '└── ' if is_last_sibling and not files and not dirs else '├── ' # Simplified, consider actual content for parent branch
                    
                    # More robust prefix for the directory line itself
                    # Check if current 'root' is the last directory among its siblings
                    parent_contents = sorted(os.listdir(parent_dir))
                    is_last_item_in_parent = (os.path.basename(root) == parent_contents[-1])

                    # Calculate proper indent for the parent branch before the current folder
                    parent_indent = '│   ' * (level - 1) if level > 0 else ''
                    if level > 0:
                        parent_siblings = sorted([f for f in os.listdir(os.path.dirname(root)) if os.path.isdir(os.path.join(os.path.dirname(root), f))])
                        if os.path.basename(root) == parent_siblings[-1] and not [f for f in os.listdir(os.path.dirname(root)) if os.path.isfile(os.path.join(os.path.dirname(root), f))]:
                            # If this is the last directory, and there are no files after it in the parent
                            parent_indent = '    ' * (level - 1)
                        elif os.path.basename(root) == parent_siblings[-1] and any(os.path.isfile(os.path.join(os.path.dirname(root), f)) for f in os.listdir(os.path.dirname(root))):
                             # If this is the last directory, but there are files after it in the parent
                             parent_indent = '│   ' * (level - 1)
                        else:
                            parent_indent = '│   ' * (level - 1)

                    # Simplified branch prefix for the folder line
                    branch_prefix = '└── ' if is_last_item_in_parent and not files and not dirs else '├── '
                    # If this is the last directory AND there are no files in its parent after it, then use spaces
                    # This logic is tricky with os.walk, easier to build the tree and then print
                    
                    # Rebuilding the display logic using a list and then formatting
                    # This is more complex to do directly with os.walk's iteration.
                    # Let's collect all items and then print them hierarchically.
                    pass # We will re-implement this with a clearer structure below

            # Re-implementing tree structure for better schematic representation
            # This approach builds the structure in a list of strings directly
            # rather than trying to manage deeply nested os.walk levels directly
            
            # Helper function for recursive tree generation
            def _build_tree(current_path, current_level, prefix="", last_item_flags=None):
                if last_item_flags is None:
                    last_item_flags = []

                contents = sorted(os.listdir(current_path))
                
                # Filter out unreadable items to avoid crashes
                readable_contents = []
                for item in contents:
                    item_path = os.path.join(current_path, item)
                    try:
                        os.access(item_path, os.R_OK)
                        readable_contents.append(item)
                    except OSError:
                        # Skip unreadable items, don't even try to check isdir/isfile
                        pass # Silently skip or add a warning to output_buffer

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
                        # Recurse for subdirectories
                        _build_tree(item_path, current_level + 1, prefix, last_item_flags + [is_last])
                    elif os.path.isfile(item_path):
                        output_buffer.append(f"{current_prefix}{item}\n")
            
            _build_tree(start_path, 0)
            self.update_status(f"Analyse terminée avec succès pour '{start_path}'.", "green")

        except PermissionError:
            self.update_status(f"Erreur de permission : Accès refusé à un sous-répertoire de '{start_path}'.", "red")
            return (f"Erreur de permission : Accès refusé à un sous-répertoire de '{start_path}'.\n"
                    f"Veuillez vérifier les permissions ou exécuter le script avec 'sudo' si nécessaire.")
        except Exception as e:
            self.update_status(f"Une erreur est survenue pendant l'analyse : {e}", "red")
            output_buffer.append(f"\nErreur lors de l'analyse : {e}")

        return "".join(output_buffer)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

    app = DirectoryTreeApp()
    app.mainloop()