import customtkinter as ctk
import subprocess
import sys
import os
import re

class HelpCommandAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analyseur de la Commande 'help' (Shell Builtins)")
        self.geometry("900x650") # Taille de fenêtre ajustée pour 'help'

        # --- Configuration de la grille de la FENÊTRE PRINCIPALE ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # La ligne du cadre de sortie prend tout l'espace vertical

        # --- Cadre de saisie de la commande ---
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        self.command_label = ctk.CTkLabel(input_frame, text="Commande Interne du Shell (pour help):")
        self.command_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.command_entry = ctk.CTkEntry(input_frame, placeholder_text="Ex: cd, echo, for, if, read")
        self.command_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Suggestion de commande par défaut
        if sys.platform != "win32": # 'help' est spécifique aux shells Unix-like
            self.command_entry.insert(0, "cd")
        else:
            self.command_entry.insert(0, "dir") # Exemple plus pertinent pour Windows CMD

        self.execute_button = ctk.CTkButton(input_frame, text="Analyser 'help'", command=self.analyze_help_command)
        self.execute_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # --- Label des messages de statut ---
        self.status_label = ctk.CTkLabel(self, text="Entrez le nom d'une commande interne du shell à analyser.",
                                         text_color="gray", height=20)
        self.status_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # --- Cadre de la sortie d'analyse ---
        self.analysis_scroll_frame = ctk.CTkScrollableFrame(self, label_text="Résultat de l'Analyse 'help'")
        self.analysis_scroll_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.analysis_scroll_frame.grid_columnconfigure(0, weight=1)

        # Placeholder label for initial state
        self.placeholder_label = ctk.CTkLabel(self.analysis_scroll_frame, text="La sortie de l'analyse 'help' apparaîtra ici.",
                                              text_color="gray", font=ctk.CTkFont(size=14))
        self.placeholder_label.grid(row=0, column=0, padx=20, pady=50, sticky="nsew")


    def _update_textbox(self, textbox, content):
        """Met à jour le contenu d'un CTkTextbox et le rend en lecture seule."""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", content)
        textbox.configure(state="disabled")

    def _update_status(self, message, color="gray"):
        """Met à jour le texte et la couleur du label de statut."""
        self.status_label.configure(text=message, text_color=color)
        self.update_idletasks()

    def _clear_analysis_frame(self):
        """Efface tous les widgets du cadre défilant d'analyse."""
        for widget in self.analysis_scroll_frame.winfo_children():
            widget.destroy()
        # Remet le placeholder après nettoyage
        self.placeholder_label = ctk.CTkLabel(self.analysis_scroll_frame, text="La sortie de l'analyse 'help' apparaîtra ici.",
                                              text_color="gray", font=ctk.CTkFont(size=14))
        self.placeholder_label.grid(row=0, column=0, padx=20, pady=50, sticky="nsew")

    def _add_section_to_frame(self, frame, title, content, row, font_size=12, bold=False):
        """Ajoute une section titrée avec du contenu à un cadre donné."""
        title_font = ctk.CTkFont(size=font_size, weight="bold" if bold else "normal")
        section_label = ctk.CTkLabel(frame, text=title, font=title_font, justify="left")
        section_label.grid(row=row, column=0, padx=5, pady=(10, 0), sticky="w")
        
        content_textbox = ctk.CTkTextbox(frame, wrap="word", height=min(len(content.splitlines()) * 18 + 20, 300))
        content_textbox.grid(row=row + 1, column=0, padx=10, pady=(0, 10), sticky="ew")
        content_textbox.insert("end", content)

        # CORRECTED LINE: Provide a default font if the condition is false
        font_to_apply = ("TkFixedFont", 10) if "SYNTAXE" in title or "UTILISATION" in title else ("Arial", 12) 
        content_textbox.configure(state="disabled", font=font_to_apply) # Apply the chosen font
        
        return row + 2

    def analyze_help_command(self):
        """Exécute 'help', analyse la sortie et l'affiche de manière organisée."""
        command_name = self.command_entry.get().strip()

        self._update_status(f"Analyse de la commande 'help {command_name}'...", "orange")
        self._clear_analysis_frame()
        self.update_idletasks()

        if sys.platform == "win32":
            self._update_status("La commande 'help' est spécifique aux shells Unix-like (Bash, Zsh). Sur Windows, utilisez 'help [commande]' dans CMD.", "red")
            self._add_section_to_frame(self.analysis_scroll_frame, "Erreur de Plateforme",
                                      "Ce script est conçu pour les systèmes Unix-like (Linux, macOS, WSL) où la commande 'help' est disponible via Bash ou Zsh.\n"
                                      "Sur Windows (CMD), la commande 'help' fonctionne différemment. Essayez 'help dir' ou 'help copy'.", 0, bold=True, font_size=14)
            # Pour Windows, on peut simuler une "help" simple pour CMD
            if command_name:
                self._update_status(f"Tentative d'exécution de 'help {command_name}' sur Windows CMD...", "orange")
                self._execute_windows_help(command_name)
            return

        if not command_name:
            self._update_status("Veuillez entrer le nom d'une commande interne du shell.", "red")
            self._add_section_to_frame(self.analysis_scroll_frame, "Saisie Manquante",
                                      "Veuillez entrer le nom d'une commande interne du shell (ex: cd, echo) dans le champ ci-dessus.", 0, bold=True, font_size=14)
            return

        try:
            # Exécuter 'help <command_name>' via le shell
            # On utilise shell=True car 'help' est une commande intégrée au shell
            result = subprocess.run(
                f"help {command_name}", # Construire la commande comme une chaîne
                shell=True,
                capture_output=True,
                text=True,
                check=False,
                encoding='utf-8',
                errors='replace'
            )

            if result.returncode != 0:
                error_output = result.stderr.strip() + "\n" + result.stdout.strip() # help met souvent l'erreur en stdout
                self._update_status(f"Erreur: Commande '{command_name}' introuvable ou problème (Code {result.returncode}).", "red")
                self._add_section_to_frame(self.analysis_scroll_frame, "Erreur 'help'",
                                          f"La commande interne '{command_name}' n'a pas été trouvée ou une erreur est survenue.\n"
                                          f"Message du shell :\n{error_output}", 0, bold=True, font_size=14)
                return

            help_content = result.stdout.strip()
            
            # --- Analyse spécifique de la sortie de 'help' ---
            current_row = 0
            
            # La sortie de 'help' commence souvent par la syntaxe/description sur la première ligne
            lines = help_content.splitlines()
            
            # 1. Syntaxe / Description générale
            # La première ligne est souvent la syntaxe ou un résumé
            if lines:
                syntax_section = lines[0].strip()
                if len(lines) > 1:
                    # Le reste des lignes forme la description détaillée
                    description_section = "\n".join(lines[1:]).strip()
                    if description_section:
                        syntax_section += "\n\nDescription:\n" + description_section
                
                current_row = self._add_section_to_frame(self.analysis_scroll_frame,
                                                          f"Syntaxe et Description de '{command_name}'",
                                                          syntax_section,
                                                          current_row, bold=True, font_size=16)

            # 2. Tentative d'extraction des options et arguments (plus simple que pour man)
            # Les options sont souvent introduites par des tirets, et les arguments en crochets <> ou parenthèses ()
            options_args_pattern = re.compile(r"^\s*(-\-?[a-zA-Z0-9,\s\[\]\<\>\|]+.*)")
            
            options_arguments_found = []
            for line in lines:
                match = options_args_pattern.match(line)
                if match:
                    options_arguments_found.append(match.group(1).strip())
            
            if options_arguments_found:
                # Filtrer les doublons et les lignes vides
                options_arguments_output = "\n".join(sorted(list(set(options_arguments_found))))
                if options_arguments_output:
                    current_row = self._add_section_to_frame(self.analysis_scroll_frame,
                                                              "Options et Arguments (Détectés)",
                                                              options_arguments_output,
                                                              current_row, bold=True, font_size=14)

            # Si l'analyse n'a pas produit grand chose, afficher la sortie brute
            if not options_arguments_found and current_row == 0:
                 current_row = self._add_section_to_frame(self.analysis_scroll_frame,
                                            "Sortie 'help' brute (analyse partielle ou échec)",
                                            help_content,
                                            current_row, font_size=12)
            
            # Supprimer le placeholder si l'analyse a réussi
            if self.placeholder_label:
                self.placeholder_label.destroy()
                self.placeholder_label = None

            self._update_status(f"Analyse terminée pour 'help {command_name}'.", "green")

        except Exception as e:
            self._update_status(f"Une erreur inattendue est survenue : {type(e).__name__} - {e}", "red")
            self._add_section_to_frame(self.analysis_scroll_frame, "Erreur Inattendue",
                                      f"Une erreur s'est produite lors de l'analyse : {e}", 0, bold=True, font_size=14)

        self.after(5000, lambda: self._update_status("Prêt. Entrez le nom d'une commande interne du shell.", "gray"))

    def _execute_windows_help(self, command_name):
        """Simule l'exécution de 'help [commande]' sur Windows CMD."""
        try:
            # On tente 'help <command>'
            result = subprocess.run(
                f"help {command_name}",
                shell=True,
                capture_output=True,
                text=True,
                check=False,
                encoding='cp850', # Souvent l'encodage par défaut de la console Windows
                errors='replace'
            )
            output = result.stdout.strip() + "\n" + result.stderr.strip() # Combine for full output

            if result.returncode != 0 or not output.strip():
                # Si 'help' ne trouve pas la commande, on peut essayer la commande directement
                result_alt = subprocess.run(
                    command_name, 
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False,
                    encoding='cp850',
                    errors='replace'
                )
                output_alt = result_alt.stdout.strip() + "\n" + result_alt.stderr.strip()
                if output_alt.strip() and output_alt.strip() != output.strip(): 
                    output = f"'{command_name}' n'est pas une commande HELP reconnue ou valide.\n" \
                             f"Tentative d'exécution directe de '{command_name}' (peut inclure l'aide intégrée):\n\n" + output_alt
                else:
                    output = f"Aucune aide trouvée pour '{command_name}' sur Windows CMD."
                
                self._update_status(f"Aucune aide trouvée pour '{command_name}' sur Windows CMD.", "red")
                self._add_section_to_frame(self.analysis_scroll_frame, "Aide Windows CMD", output, 0, bold=True, font_size=14)
            else:
                self._update_status(f"Aide affichée pour '{command_name}' (Windows CMD).", "green")
                self._add_section_to_frame(self.analysis_scroll_frame, f"Aide pour '{command_name}' (Windows CMD)", output, 0, bold=True, font_size=14)
        except Exception as e:
            self._update_status(f"Erreur d'exécution de l'aide sur Windows : {e}", "red")
            self._add_section_to_frame(self.analysis_scroll_frame, "Erreur Windows CMD", f"Erreur lors de l'exécution : {e}", 0, bold=True, font_size=14)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = HelpCommandAnalyzerApp()
    app.mainloop()