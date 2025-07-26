import customtkinter as ctk
import sys
import pkgutil # Used to find all modules available, not just imported ones

class ModuleListerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Liste des Modules Python Installés")
        self.geometry("800x600")

        # Configure main window grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Allow the textbox to expand

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Modules Python Installés", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # Module List Textbox (Scrollable)
        self.module_list_textbox = ctk.CTkTextbox(self, wrap="word")
        self.module_list_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.module_list_textbox.configure(state="disabled") # Read-only

        # Status Label (at the bottom)
        self.status_label = ctk.CTkLabel(self, text="Cliquez sur 'Rafraîchir' pour lister les modules.")
        self.status_label.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # Refresh Button
        self.refresh_button = ctk.CTkButton(self, text="Rafraîchir la Liste", command=self.list_modules)
        self.refresh_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Automatically list modules on startup
        self.list_modules()

    def _update_textbox(self, textbox, content):
        """Helper to update and manage textbox state."""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", content)
        textbox.configure(state="disabled")

    def list_modules(self):
        """Fetches and displays all installed Python modules."""
        self.status_label.configure(text="Chargement des modules, veuillez patienter...")
        self.update_idletasks() # Force GUI update to show status message

        try:
            # Method 1: Get names of all currently loaded modules
            loaded_modules = sorted(sys.modules.keys())

            # Method 2: Discover all modules available in sys.path
            # This is more comprehensive as it finds modules not yet imported
            discoverable_modules = set()
            for finder, name, ispkg in pkgutil.iter_modules():
                discoverable_modules.add(name)
            
            # Combine and sort for a comprehensive list
            all_unique_modules = sorted(list(set(loaded_modules) | discoverable_modules))

            output_content = []
            output_content.append(f"Nombre total de modules trouvés : {len(all_unique_modules)}\n")
            output_content.append("--- Liste des Modules ---")
            for module_name in all_unique_modules:
                output_content.append(f"- {module_name}")

            self._update_textbox(self.module_list_textbox, "\n".join(output_content))
            self.status_label.configure(text=f"Liste mise à jour. {len(all_unique_modules)} modules trouvés.")

        except Exception as e:
            self.status_label.configure(text=f"Une erreur est survenue : {e}")
            self._update_textbox(self.module_list_textbox, f"Impossible de charger la liste des modules.\nErreur: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ModuleListerApp()
    app.mainloop()