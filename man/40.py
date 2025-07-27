import customtkinter
import os
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox, StringVar

class PolkitRuleGeneratorApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Générateur de Règles Polkit (Tout en Une Fenêtre)")
        self.geometry("950x850") # Slightly larger to accommodate action list
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1) # More rows for action list

        # --- Sidebar Frame ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=12, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Polkit Rules", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Mode d'apparence:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Mise à l'échelle de l'UI:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        # --- Main Frame Widgets ---

        # Action ID Selection / Search
        self.action_id_label = customtkinter.CTkLabel(self, text="ID de l'action Polkit (Rechercher et sélectionner) :")
        self.action_id_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        
        # All available Polkit actions (display_text, actual_id)
        self.polkit_actions_map = self.get_polkit_actions_with_description()
        
        # Entry for typing and displaying selected action ID
        self.action_search_entry = customtkinter.CTkEntry(self, placeholder_text="Tapez un ID ou une description pour filtrer...")
        self.action_search_entry.grid(row=0, column=2, columnspan=2, padx=20, pady=10, sticky="ew")
        self.action_search_entry.bind("<KeyRelease>", self.filter_action_list) # Bind for live filtering

        # Scrollable frame for filtered action list
        self.action_list_frame = customtkinter.CTkScrollableFrame(self, label_text="Actions Polkit Filtrées", height=200) # Fixed height
        self.action_list_frame.grid(row=1, column=1, columnspan=3, padx=20, pady=10, sticky="nsew")
        self.action_list_frame.grid_columnconfigure(0, weight=1)

        # Variable to hold the selected radio button value
        self.selected_action_radio_var = StringVar()
        # Initialize the list of actions
        self.filter_action_list() 


        # Target Type Selection (Group or User)
        self.target_type_label = customtkinter.CTkLabel(self, text="Cible (Groupe ou Utilisateur):")
        self.target_type_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        self.target_type_options = ["Groupe", "Utilisateur"]
        self.target_type_combobox = customtkinter.CTkComboBox(self, values=self.target_type_options,
                                                              command=self.on_target_type_change)
        self.target_type_combobox.set("Groupe")
        self.target_type_combobox.grid(row=2, column=2, columnspan=2, padx=20, pady=10, sticky="ew")

        # Group/User Selection
        self.group_user_label = customtkinter.CTkLabel(self, text="Sélectionnez le groupe:")
        self.group_user_label.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        
        self.groups = self.get_system_groups()
        self.users = self.get_system_users()
        
        # Initialisation du combobox avec les groupes
        self.group_user_combobox = customtkinter.CTkComboBox(self, values=self.groups if self.groups else ["Aucun groupe trouvé"])
        if self.groups:
            self.group_user_combobox.set(self.groups[0])
        else:
             self.group_user_combobox.set("Aucun groupe trouvé")
        self.group_user_combobox.grid(row=3, column=2, columnspan=2, padx=20, pady=10, sticky="ew")


        # Result Type Selection
        self.result_type_label = customtkinter.CTkLabel(self, text="Type de résultat Polkit:")
        self.result_type_label.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        self.result_type_options = ["auth_self_keep", "yes", "no", "auth_self", "auth_admin", "auth_admin_keep"]
        self.result_type_combobox = customtkinter.CTkComboBox(self, values=self.result_type_options)
        self.result_type_combobox.set("auth_self_keep") # Default value
        self.result_type_combobox.grid(row=4, column=2, columnspan=2, padx=20, pady=10, sticky="ew")

        # Output Filename Input
        self.filename_label = customtkinter.CTkLabel(self, text="Nom du fichier de sortie (.rules):")
        self.filename_label.grid(row=5, column=1, padx=20, pady=10, sticky="w")
        self.filename_entry = customtkinter.CTkEntry(self, placeholder_text="90-custom-rule.rules")
        self.filename_entry.grid(row=5, column=2, columnspan=2, padx=20, pady=10, sticky="ew")
        self.filename_entry.insert(0, "90-generated-rule.rules")

        # Generate Button
        self.generate_button = customtkinter.CTkButton(self, text="Générer la Règle Polkit", command=self.generate_rule)
        self.generate_button.grid(row=6, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        # Output Text Box for Rule Content
        self.output_label = customtkinter.CTkLabel(self, text="Contenu de la Règle et Instructions:")
        self.output_label.grid(row=7, column=1, padx=20, pady=10, sticky="w")
        self.output_textbox = customtkinter.CTkTextbox(self, width=250, height=150)
        self.output_textbox.grid(row=8, column=1, columnspan=3, padx=20, pady=10, sticky="nsew")

        # Set default values for appearance
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def get_polkit_actions_with_description(self):
        """
        Scanne les répertoires d'actions Polkit pour trouver les IDs d'action
        et leurs descriptions/résumés pour un affichage plus lisible et compact.
        Retourne une liste de (display_text, actual_id)
        """
        action_data = [] # Stores (display_text, actual_id)
        # Chemins standards pour les fichiers .policy
        action_dirs = [
            "/usr/share/polkit-1/actions/",
            "/var/lib/polkit-1/localauthority/10-vendor.d/",
            "/var/lib/polkit-1/localauthority/50-local.d/"
        ]
        
        MAX_DESC_LEN = 80 # Maximum length for the displayed description

        for adir in action_dirs:
            if not os.path.exists(adir):
                continue
            for root_dir, _, files in os.walk(adir):
                for file in files:
                    if file.endswith(".policy"):
                        filepath = os.path.join(root_dir, file)
                        try:
                            tree = ET.parse(filepath)
                            root_element = tree.getroot()
                            for action_element in root_element.findall('action'):
                                action_id = action_element.get('id')
                                if not action_id:
                                    continue

                                description_text = ""
                                summary_text = ""
                                
                                # Look for description and summary in preferred locale (e.g., system locale or en)
                                # and then fallback to any available
                                for lang_code in [os.getenv('LANG', 'en_US').split('.')[0], 'en_US', 'en']:
                                    for desc_elem in action_element.findall(f"description[@{{http://www.w3.org/XML/1998/namespace}}lang='{lang_code}']"):
                                        if desc_elem.text:
                                            description_text = desc_elem.text.strip()
                                            break
                                    if description_text:
                                        break
                                
                                if not description_text: # Fallback to any description if no specific language found
                                    for desc_elem in action_element.findall('description'):
                                        if desc_elem.text:
                                            description_text = desc_elem.text.strip()
                                            break

                                for lang_code in [os.getenv('LANG', 'en_US').split('.')[0], 'en_US', 'en']:
                                    for summ_elem in action_element.findall(f"summary[@{{http://www.w3.org/XML/1998/namespace}}lang='{lang_code}']"):
                                        if summ_elem.text:
                                            summary_text = summ_elem.text.strip()
                                            break
                                    if summary_text:
                                        break
                                        
                                if not summary_text: # Fallback to any summary if no specific language found
                                    for summ_elem in action_element.findall('summary'):
                                        if summ_elem.text:
                                            summary_text = summ_elem.text.strip()
                                            break


                                # Prioritize summary, then description, then just ID for context_text
                                context_text = ""
                                if summary_text:
                                    context_text = summary_text
                                elif description_text:
                                    context_text = description_text
                                
                                # Truncate context_text for display if too long
                                if len(context_text) > MAX_DESC_LEN:
                                    context_text = context_text[:MAX_DESC_LEN-3] + "..." # -3 for "..."
                                
                                display_text = action_id
                                if context_text:
                                    display_text = f"{action_id} ({context_text})"
                                
                                # Avoid duplicates and prioritize the best display text
                                found_existing = False
                                for i, (old_display, old_id) in enumerate(action_data):
                                    if old_id == action_id:
                                        found_existing = True
                                        if ("(" in display_text and not "(" in old_display) or \
                                           (context_text and not old_display.strip().endswith(')') ) or \
                                           (context_text and len(context_text) > len(old_display.split('(')[-1].strip(')') if '(' in old_display else "")):
                                            action_data[i] = (display_text, action_id)
                                        break
                                if not found_existing:
                                    action_data.append((display_text, action_id))

                        except ET.ParseError as e:
                            print(f"Erreur d'analyse XML dans {filepath}: {e}")
                        except Exception as e:
                            print(f"Erreur inattendue lors de la lecture de {filepath}: {e}")
        
        # Sort by actual action ID for consistency
        action_data.sort(key=lambda x: x[1])
        return action_data if action_data else [("Aucune action trouvée", "")]

    def get_system_groups(self):
        """
        Récupère la liste des groupes système à partir de /etc/group.
        """
        groups = []
        try:
            with open("/etc/group", "r") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        parts = line.split(":")
                        if len(parts) > 0:
                            groups.append(parts[0])
            groups.sort()
        except FileNotFoundError:
            messagebox.showwarning("Avertissement", "/etc/group non trouvé. Impossible de lister les groupes.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture de /etc/group: {e}")
        return groups if groups else ["Aucun groupe trouvé"]

    def get_system_users(self):
        """
        Récupère la liste des utilisateurs système à partir de /etc/passwd.
        """
        users = []
        try:
            with open("/etc/passwd", "r") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        parts = line.split(":")
                        if len(parts) > 0:
                            try:
                                uid = int(parts[2])
                                # Include common system users like 'root' regardless of UID < 1000
                                # And all users with UID >= 1000
                                if uid >= 1000 or parts[0] in ["root", "daemon", "bin", "sys", "adm", "lp", "sync", "shutdown", "halt", "mail", "news", "uucp", "operator", "games", "gopher", "ftp", "nobody", "systemd-network", "dbus", "avahi", "cups", "colord", "geoclue", "pulse", "rtkit", "saned", "sshd", "systemd-timesync", "usbmux", "git", "www-data", "systemd-resolve"]:
                                    users.append(parts[0])
                            except ValueError:
                                continue # Skip lines where UID is not a number
            users.sort()
        except FileNotFoundError:
            messagebox.showwarning("Avertissement", "/etc/passwd non trouvé. Impossible de lister les utilisateurs.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture de /etc/passwd: {e}")
        return users if users else ["Aucun utilisateur trouvé"]

    def filter_action_list(self, event=None):
        """
        Filtre la liste des actions Polkit et met à jour le CTkScrollableFrame.
        """
        search_term = self.action_search_entry.get().strip().lower()
        
        # Clear existing widgets in the scrollable frame
        for widget in self.action_list_frame.winfo_children():
            widget.destroy()

        filtered_actions = []
        for display_text, actual_id in self.polkit_actions_map:
            if search_term in display_text.lower() or search_term in actual_id.lower():
                filtered_actions.append((display_text, actual_id))
        
        if not filtered_actions:
            customtkinter.CTkLabel(self.action_list_frame, text="Aucune action correspondante trouvée.").pack(padx=10, pady=5, anchor="w")
            return

        # Populate the scrollable frame with filtered actions
        # Using RadioButtons to allow easy selection and update of the entry
        for display_text, actual_id in filtered_actions:
            radio_button = customtkinter.CTkRadioButton(
                self.action_list_frame,
                text=display_text,
                value=actual_id,
                variable=self.selected_action_radio_var,
                command=self.on_action_radio_select
            )
            radio_button.pack(padx=10, pady=2, anchor="w")
            # If the current entry text matches this action, select it
            if self.action_search_entry.get() == display_text:
                radio_button.select()


    def on_action_radio_select(self):
        """
        Met à jour le champ de saisie d'action principal avec l'action sélectionnée
        dans le CTkScrollableFrame.
        """
        selected_actual_id = self.selected_action_radio_var.get()
        selected_display_text = ""
        # Find the display text associated with the selected actual_id
        for display_text, actual_id in self.polkit_actions_map:
            if actual_id == selected_actual_id:
                selected_display_text = display_text
                break
        
        self.action_search_entry.delete(0, 'end')
        self.action_search_entry.insert(0, selected_display_text)
        # We might want to "hide" the scrollable frame or make it smaller after selection
        # For now, it stays visible.

    def on_target_type_change(self, selected_type):
        """
        Met à jour la liste déroulante des groupes/utilisateurs en fonction du type sélectionné.
        """
        if selected_type == "Groupe":
            self.group_user_label.configure(text="Sélectionnez le groupe:")
            self.group_user_combobox.configure(values=self.groups if self.groups else ["Aucun groupe trouvé"])
            if self.groups:
                self.group_user_combobox.set(self.groups[0])
            else:
                self.group_user_combobox.set("Aucun groupe trouvé")
        else: # Utilisateur
            self.group_user_label.configure(text="Sélectionnez l'utilisateur:")
            self.group_user_combobox.configure(values=self.users if self.users else ["Aucun utilisateur trouvé"])
            if self.users:
                self.group_user_combobox.set(self.users[0])
            else:
                self.group_user_combobox.set("Aucun utilisateur trouvé")

    def generate_rule(self):
        # The actual ID to use for the rule is stored in selected_action_radio_var
        selected_action_id = self.selected_action_radio_var.get()
        
        # If no radio button was explicitly selected, try to get from entry as fallback
        # This might happen if user types but doesn't select a radio button
        if not selected_action_id:
            entry_text = self.action_search_entry.get().strip()
            # Try to match entry text to an actual_id in polkit_actions_map
            for display_text, actual_id in self.polkit_actions_map:
                if entry_text == display_text:
                    selected_action_id = actual_id
                    break
            if not selected_action_id:
                messagebox.showerror("Erreur", "L'ID de l'action Polkit n'est pas valide ou n'a pas été sélectionné. Veuillez le choisir dans la liste filtrée.")
                return

        target_type = self.target_type_combobox.get()
        target_name = self.group_user_combobox.get()
        result_type = self.result_type_combobox.get()
        filename = self.filename_entry.get().strip()

        if selected_action_id == "Aucune action trouvée" or not selected_action_id:
            messagebox.showerror("Erreur", "Veuillez sélectionner un ID d'action Polkit valide.")
            return
        if (target_type == "Groupe" and target_name == "Aucun groupe trouvé") or \
           (target_type == "Utilisateur" and target_name == "Aucun utilisateur trouvé") or \
           not target_name:
            messagebox.showerror("Erreur", f"Veuillez sélectionner un {target_type} valide.")
            return
        if not filename:
            messagebox.showerror("Erreur", "Le nom du fichier de sortie est requis.")
            return
        if not filename.endswith(".rules"):
            filename += ".rules"

        valid_results = {
            "yes": "polkit.Result.YES",
            "no": "polkit.Result.NO",
            "auth_self": "polkit.Result.AUTH_SELF",
            "auth_self_keep": "polkit.Result.AUTH_SELF_KEEP",
            "auth_admin": "polkit.Result.AUTH_ADMIN",
            "auth_admin_keep": "polkit.Result.AUTH_ADMIN_KEEP",
        }

        if result_type not in valid_results:
            messagebox.showerror("Erreur", f"Le type de résultat '{result_type}' n'est pas valide.")
            return

        # Generate the JavaScript rule content based on target type
        rule_content = f"""// Polkit rule generated by CustomTkinter app for action: {selected_action_id}
// Allows {target_type.lower()} '{target_name}' to perform this action with result type: {result_type}

polkit.addRule(function(action, subject) {{
    if (action.id == "{selected_action_id}") {{
        """
        if target_type == "Groupe":
            rule_content += f"""if (subject.isInGroup("{target_name}")) {{
            return {valid_results[result_type]};
        }}"""
        else: # Utilisateur
            rule_content += f"""if (subject.user == "{target_name}") {{
            return {valid_results[result_type]};
        }}"""
        
        rule_content += """
    }
});
"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".rules",
                initialfile=filename,
                title="Enregistrer la règle Polkit",
                filetypes=[("Polkit Rules", "*.rules"), ("Tous les fichiers", "*.*")]
            )
            
            if not file_path:
                self.output_textbox.delete("1.0", "end")
                self.output_textbox.insert("1.0", "Génération annulée par l'utilisateur.")
                return

            with open(file_path, "w") as f:
                f.write(rule_content)
            
            output_message = f"Fichier de règle Polkit '{os.path.basename(file_path)}' généré avec succès à:\n{file_path}\n\n"
            output_message += "--- Contenu du fichier ---\n"
            output_message += rule_content
            output_message += "\n\n--- Instructions d'installation ---\n"
            output_message += f"Pour appliquer cette règle, **copiez le fichier '{os.path.basename(file_path)}' dans**:\n"
            output_message += "  **/etc/polkit-1/rules.d/** (pour les règles locales, **recommandé**)\n"
            output_message += "  OU\n"
            output_message += "  **/usr/share/polkit-1/rules.d/** (pour les règles de paquets, moins courant pour la personnalisation)\n\n"
            output_message += "Exemple de commande pour copier (nécessite des droits root):\n"
            output_message += f"**sudo cp \"{file_path}\" /etc/polkit-1/rules.d/**"
            output_message += "\n\nAprès avoir copié le fichier, les changements devraient être pris en compte immédiatement,"
            output_message += "\nmais un redémarrage du service polkitd (sudo systemctl restart polkit.service) ou du système peut être nécessaire dans certains cas."

            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", output_message)
            messagebox.showinfo("Succès", f"La règle a été générée et enregistrée sous:\n{file_path}")

        except IOError as e:
            messagebox.showerror("Erreur d'écriture", f"Erreur lors de l'écriture du fichier '{file_path}': {e}")
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", f"Erreur lors de la génération: {e}")

if __name__ == "__main__":
    app = PolkitRuleGeneratorApp()
    app.mainloop()