import customtkinter as ctk
import os
import sys

class ResizableCommandsListerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Commandes Système par Répertoire (Redimensionnable)")
        self.geometry("1000x700") # Taille initiale, mais la fenêtre est redimensionnable

        # --- Configuration de la grille de la FENÊTRE PRINCIPALE ---
        # Permet à la colonne 0 (tout le contenu) de s'étendre
        self.grid_columnconfigure(0, weight=1)
        # Permet à la ligne 2 (où se trouve le conteneur des cadres des répertoires) de s'étendre
        self.grid_rowconfigure(2, weight=1)

        # --- Section du titre et du bouton ---
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(header_frame, text="Commandes disponibles dans les répertoires système", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=5)

        self.list_button = ctk.CTkButton(header_frame, text="Lister les Commandes", command=self.list_commands_in_frames)
        self.list_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # --- Cadre pour les messages d'état ---
        self.status_textbox = ctk.CTkTextbox(self, wrap="word", height=50)
        self.status_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.status_textbox.insert("end", "Prêt à lister les commandes des répertoires /bin et /sbin.\n")
        self.status_textbox.configure(state="disabled")

        # --- Conteneur des cadres de chaque répertoire ---
        # Ce cadre doit s'étendre pour que ses enfants puissent aussi s'étendre
        self.directories_container_frame = ctk.CTkFrame(self)
        self.directories_container_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew") # TRÈS IMPORTANT : sticky="nsew"
        
        # --- Configuration de la grille du CONTENEUR des cadres de répertoires ---
        # Les deux colonnes (pour /bin et /sbin) doivent s'étendre
        self.directories_container_frame.grid_columnconfigure((0, 1), weight=1)
        # La seule ligne de ce conteneur doit s'étendre
        self.directories_container_frame.grid_rowconfigure(0, weight=1)

        # Dictionnaire pour stocker les références aux cadres et textboxes
        self.directory_frames = {}
        self.target_paths = ["/bin", "/sbin"] # Les répertoires cibles

        # Création dynamique des cadres pour chaque répertoire
        for i, path in enumerate(self.target_paths):
            frame = ctk.CTkScrollableFrame(self.directories_container_frame, label_text=f"Commandes dans {path}")
            frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew") # TRÈS IMPORTANT : sticky="nsew"
            
            # --- Configuration de la grille de CHAQUE CADRE DE RÉPERTOIRE ---
            # La colonne 0 (pour le textbox à l'intérieur) doit s'étendre
            frame.grid_columnconfigure(0, weight=1)
            # La ligne 0 (pour le textbox à l'intérieur) doit s'étendre
            frame.grid_rowconfigure(0, weight=1)

            textbox = ctk.CTkTextbox(frame, wrap="word")
            textbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") # TRÈS IMPORTANT : sticky="nsew"
            textbox.configure(state="disabled")

            self.directory_frames[path] = textbox

        # Lancer la liste automatiquement au démarrage
        self.list_commands_in_frames()

    def _update_textbox(self, textbox, content):
        """Fonction utilitaire pour mettre à jour et gérer l'état d'un CTkTextbox."""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", content)
        textbox.configure(state="disabled")

    def _update_status(self, message, color="gray"):
        """Fonction utilitaire pour mettre à jour le textbox de statut."""
        self.status_textbox.configure(state="normal")
        self.status_textbox.delete("1.0", "end")
        self.status_textbox.insert("end", message)
        self.status_textbox.configure(state="disabled", text_color=color)

    def list_commands_in_frames(self):
        """
        Liste les commandes exécutables dans chaque répertoire cible
        et les affiche dans leurs cadres respectifs.
        """
        self._update_status("Initialisation de l'analyse...", "gray")
        for path in self.target_paths:
            self._update_textbox(self.directory_frames[path], "")

        if sys.platform == "win32":
            self._update_status("Ce script est conçu pour les systèmes Unix-like (/bin, /sbin).", "orange")
            for path in self.target_paths:
                self._update_textbox(self.directory_frames[path],
                                     f"Le répertoire '{path}' n'est pas standard sur Windows.\n"
                                     "Ce script est optimisé pour Linux/macOS.")
            return

        total_found_commands = 0
        all_errors_occurred = []

        for path in self.target_paths:
            current_output_lines = []
            current_output_lines.append(f"--- Commandes dans {path} ---\n")

            if not os.path.isdir(path):
                current_output_lines.append(f"Le répertoire '{path}' n'existe pas ou n'est pas accessible.")
                all_errors_occurred.append(f"Répertoire manquant/inaccessible: {path}")
                self._update_textbox(self.directory_frames[path], "\n".join(current_output_lines))
                continue

            try:
                entries_in_path = os.listdir(path)
                path_commands = []
                for entry in entries_in_path:
                    full_path = os.path.join(path, entry)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        path_commands.append(entry)

                path_commands.sort()
                total_found_commands += len(path_commands)

                if path_commands:
                    for cmd in path_commands:
                        current_output_lines.append(f"- {cmd}")
                else:
                    current_output_lines.append(f"Aucune commande exécutable trouvée dans '{path}'.")
                
                current_output_lines.append(f"\n({len(path_commands)} commandes trouvées dans {path})")

                self._update_textbox(self.directory_frames[path], "\n".join(current_output_lines))

            except PermissionError:
                current_output_lines.append(f"Erreur de permission : Accès refusé à '{path}'.")
                all_errors_occurred.append(f"Permission refusée: {path}")
                self._update_textbox(self.directory_frames[path], "\n".join(current_output_lines))
            except Exception as e:
                current_output_lines.append(f"Erreur inattendue lors de la lecture de '{path}' : {e}")
                all_errors_occurred.append(f"Erreur générique ({type(e).__name__}): {path}")
                self._update_textbox(self.directory_frames[path], "\n".join(current_output_lines))
            
            self.update_idletasks() # Force GUI update after each directory processed

        if all_errors_occurred:
            self._update_status(f"Analyse terminée avec des erreurs: {', '.join(all_errors_occurred)}", "red")
        else:
            self._update_status(f"Analyse terminée. {total_found_commands} commandes exécutables trouvées au total.", "green")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ResizableCommandsListerApp()
    app.mainloop()