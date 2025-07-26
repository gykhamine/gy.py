import customtkinter as ctk
import sys
import pydoc # Used to get the help documentation as a string

class HelpApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aide sur Fonctions/Classes de Module")
        self.geometry("800x700")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # The result textbox should expand

        # Module Input
        self.module_label = ctk.CTkLabel(self, text="Nom du Module:")
        self.module_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.module_entry = ctk.CTkEntry(self, width=300)
        self.module_entry.grid(row=0, column=0, padx=120, pady=5, sticky="w")
        self.module_entry.insert(0, "os") # Default value

        # Object (Function/Class) Input
        self.object_label = ctk.CTkLabel(self, text="Nom de la Fonction/Classe (Optionnel):")
        self.object_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.object_entry = ctk.CTkEntry(self, width=300)
        self.object_entry.grid(row=1, column=0, padx=260, pady=5, sticky="w")
        # self.object_entry.insert(0, "times_result") # Example if you want a default

        # Get Help Button
        self.get_help_button = ctk.CTkButton(self, text="Obtenir l'aide", command=self.get_help_documentation)
        self.get_help_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Result Textbox
        self.help_textbox = ctk.CTkTextbox(self, wrap="word")
        self.help_textbox.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.help_textbox.insert("end", "Entrez un nom de module (et éventuellement une fonction/classe) pour obtenir son aide.\n")
        self.help_textbox.configure(state="disabled") # Make it read-only initially

    def get_help_documentation(self):
        module_name = self.module_entry.get().strip()
        object_name = self.object_entry.get().strip()

        self.help_textbox.configure(state="normal") # Enable editing to clear and insert
        self.help_textbox.delete("1.0", "end") # Clear previous results

        if not module_name:
            self.help_textbox.insert("end", "Veuillez entrer un nom de module.\n")
            self.help_textbox.configure(state="disabled")
            return

        try:
            # Dynamically import the module
            if module_name not in sys.modules:
                __import__(module_name)
            module = sys.modules[module_name]

            target_obj = module
            if object_name:
                # If an object name is provided, try to get it from the module
                try:
                    target_obj = getattr(module, object_name)
                except AttributeError:
                    self.help_textbox.insert("end", f"La fonction ou classe '{object_name}' est introuvable dans le module '{module_name}'.\n")
                    self.help_textbox.configure(state="disabled")
                    return

            # Use pydoc.render_doc to get the help string
            # pydoc.render_doc(obj, renderer=pydoc.plaintext) is key for getting string output
            help_content = pydoc.render_doc(target_obj, renderer=pydoc.plaintext)
            self.help_textbox.insert("end", help_content)

        except ModuleNotFoundError:
            self.help_textbox.insert("end", f"Le module '{module_name}' est introuvable.\n")
        except Exception as e:
            self.help_textbox.insert("end", f"Une erreur inattendue s'est produite : {e}\n")
        finally:
            self.help_textbox.configure(state="disabled") # Make it read-only again

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = HelpApp()
    app.mainloop()