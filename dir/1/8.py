import customtkinter as ctk
import inspect
import sys

class ClassAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analyseur de Classe Python")
        self.geometry("900x700") # Taille ajustée pour une meilleure visibilité des deux cadres

        # Configurer la grille principale de la fenêtre
        self.grid_columnconfigure(0, weight=1) # Permet à la colonne de s'étendre
        self.grid_rowconfigure(2, weight=1)    # Permet au conteneur des cadres de s'étendre

        # --- Cadre pour les entrées utilisateur ---
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1) # Pour que les champs de saisie s'étendent

        # Invite pour le nom du module
        self.module_label = ctk.CTkLabel(input_frame, text="Nom du Module:")
        self.module_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.module_entry = ctk.CTkEntry(input_frame)
        self.module_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.module_entry.insert(0, "os") # Valeur par défaut pour l'exemple

        # Invite pour le nom de la classe
        self.class_label = ctk.CTkLabel(input_frame, text="Nom de la Classe:")
        self.class_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.class_entry = ctk.CTkEntry(input_frame)
        self.class_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.class_entry.insert(0, "times_result") # Valeur par défaut pour l'exemple

        # Bouton d'analyse
        self.analyze_button = ctk.CTkButton(input_frame, text="Analyser la Classe", command=self.analyze_class_attributes)
        self.analyze_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # --- Cadre pour les messages d'état/erreur ---
        self.status_textbox = ctk.CTkTextbox(self, wrap="word", height=50)
        self.status_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.status_textbox.insert("end", "Entrez un module et une classe, puis cliquez sur 'Analyser'.\n")
        self.status_textbox.configure(state="disabled") # En lecture seule par défaut

        # --- Conteneur pour les cadres des résultats (Méthodes et Attributs) ---
        results_container_frame = ctk.CTkFrame(self)
        results_container_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        results_container_frame.grid_columnconfigure((0, 1), weight=1) # Deux colonnes égales
        results_container_frame.grid_rowconfigure(0, weight=1) # Une ligne qui s'étire

        # Cadre pour les Méthodes
        self.methods_frame = ctk.CTkScrollableFrame(results_container_frame, label_text="Méthodes de la Classe")
        self.methods_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.methods_frame.grid_columnconfigure(0, weight=1) # Permet au textbox de s'étendre dans ce cadre

        self.methods_textbox = ctk.CTkTextbox(self.methods_frame, wrap="word")
        self.methods_textbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.methods_textbox.configure(state="disabled") # En lecture seule

        # Cadre pour les Attributs
        self.attributes_frame = ctk.CTkScrollableFrame(results_container_frame, label_text="Attributs de la Classe")
        self.attributes_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.attributes_frame.grid_columnconfigure(0, weight=1) # Permet au textbox de s'étendre dans ce cadre

        self.attributes_textbox = ctk.CTkTextbox(self.attributes_frame, wrap="word")
        self.attributes_textbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.attributes_textbox.configure(state="disabled") # En lecture seule

    def _update_textbox(self, textbox, content):
        """Fonction utilitaire pour mettre à jour et gérer l'état d'un CTkTextbox."""
        textbox.configure(state="normal") # Rendre le texte modifiable pour la mise à jour
        textbox.delete("1.0", "end")      # Effacer le contenu existant
        textbox.insert("end", content)    # Insérer le nouveau contenu
        textbox.configure(state="disabled") # Remettre en lecture seule

    def analyze_class_attributes(self):
        """Récupère et catégorise les attributs de la classe spécifiée."""
        module_name = self.module_entry.get().strip()
        class_name = self.class_entry.get().strip()

        # Effacer les résultats précédents et les messages d'état
        self._update_textbox(self.status_textbox, "")
        self._update_textbox(self.methods_textbox, "")
        self._update_textbox(self.attributes_textbox, "")

        if not module_name or not class_name:
            self._update_textbox(self.status_textbox, "Erreur : Veuillez entrer un nom de module et un nom de classe.")
            return

        try:
            # Importation dynamique du module
            if module_name not in sys.modules:
                __import__(module_name)
            module = sys.modules[module_name]

            # Obtenir la classe depuis le module
            target_class = getattr(module, class_name)

            # Vérifier si l'objet est bien une classe
            if not inspect.isclass(target_class):
                self._update_textbox(self.status_textbox, f"Erreur : '{class_name}' dans le module '{module_name}' n'est pas une classe valide.")
                return

            self._update_textbox(self.status_textbox, f"Analyse en cours pour : {module_name}.{class_name}...")

            all_members = dir(target_class)

            # Listes pour stocker les noms des membres classés
            methods_output_lines = []
            attributes_output_lines = []

            # Dictionnaires temporaires pour une meilleure organisation interne
            categorized_methods = {
                "Méthodes d'instance/fonctions": [],
                "Méthodes statiques": [],
                "Méthodes de classe": []
            }
            categorized_attributes = {
                "Attributs de données/variables": [],
                "Propriétés": [],
                "Attributs spéciaux (Dunder)": [],
                "Autres/Non classés": []
            }

            for member_name in all_members:
                try:
                    # Tente d'obtenir le membre pour inspection
                    member = getattr(target_class, member_name)

                    # Classification des MÉTHODES
                    if inspect.isfunction(member) or inspect.ismethod(member):
                        # On doit inspecter le descripteur sur la classe elle-même pour les @staticmethod et @classmethod
                        descriptor = getattr(target_class, member_name, None)
                        if isinstance(descriptor, staticmethod):
                            categorized_methods["Méthodes statiques"].append(member_name)
                        elif isinstance(descriptor, classmethod):
                            categorized_methods["Méthodes de classe"].append(member_name)
                        else:
                            # C'est une méthode d'instance, ou une fonction normale si c'est une fonction dans le module
                            categorized_methods["Méthodes d'instance/fonctions"].append(member_name)
                    # Classification des ATTRIBUTS
                    elif isinstance(member, property):
                        categorized_attributes["Propriétés"].append(member_name)
                    elif member_name.startswith('__') and member_name.endswith('__'):
                        # Attributs "dunder" ou "magiques"
                        categorized_attributes["Attributs spéciaux (Dunder)"].append(member_name)
                    elif not inspect.iscallable(member):
                        # Si non callable, c'est probablement un attribut de données
                        categorized_attributes["Attributs de données/variables"].append(member_name)
                    else:
                        # Tout le reste qui n'a pas été explicitement classé
                        categorized_attributes["Autres/Non classés"].append(member_name)

                except AttributeError:
                    # Certains attributs peuvent lever AttributeError même pour dir()
                    categorized_attributes["Autres/Non classés"].append(f"{member_name} (Accès Impossible)")
                except Exception as e:
                    # Gérer d'autres exceptions imprévues lors de l'accès
                    categorized_attributes["Autres/Non classés"].append(f"{member_name} (Erreur: {type(e).__name__})")

            # --- Remplir le cadre des MÉTHODES ---
            methods_output_lines.append(f"Analyse des méthodes de '{class_name}':\n")
            for category, members in categorized_methods.items():
                methods_output_lines.append(f"--- {category} ({len(members)}) ---")
                if members:
                    for member in sorted(members):
                        methods_output_lines.append(f"- {member}")
                else:
                    methods_output_lines.append("Aucun.")
                methods_output_lines.append("") # Ligne vide pour la séparation

            self._update_textbox(self.methods_textbox, "\n".join(methods_output_lines))

            # --- Remplir le cadre des ATTRIBUTS ---
            attributes_output_lines.append(f"Analyse des attributs de '{class_name}':\n")
            for category, members in categorized_attributes.items():
                attributes_output_lines.append(f"--- {category} ({len(members)}) ---")
                if members:
                    for member in sorted(members):
                        attributes_output_lines.append(f"- {member}")
                else:
                    attributes_output_lines.append("Aucun.")
                attributes_output_lines.append("") # Ligne vide pour la séparation

            self._update_textbox(self.attributes_textbox, "\n".join(attributes_output_lines))
            self._update_textbox(self.status_textbox, f"Analyse terminée pour : {module_name}.{class_name}.")


        except ModuleNotFoundError:
            self._update_textbox(self.status_textbox, f"Erreur : Le module '{module_name}' est introuvable.")
        except AttributeError:
            self._update_textbox(self.status_textbox, f"Erreur : La classe '{class_name}' est introuvable dans le module '{module_name}'.")
        except Exception as e:
            self._update_textbox(self.status_textbox, f"Une erreur inattendue s'est produite : {type(e).__name__} - {e}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ClassAnalyzerApp()
    app.mainloop()