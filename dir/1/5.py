import inspect
import customtkinter
import sys

# Configure CustomTkinter appearance
customtkinter.set_appearance_mode("System")  # Options: "System" (default), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Options: "blue" (default), "dark-blue", "green"

def classify_module_members(module_name):
    """
    Retrieves a module, inspects its members, and returns a dictionary
    with results classified by type and origin.
    """
    results = {
        "defined_classes": [],
        "imported_classes": [],
        "defined_functions": [],
        "imported_functions": [],
        "defined_variables": [], # Variables directly set in the module
        "imported_variables": [], # Variables imported from other modules
        "builtins": [],
        "sub_modules": [],
        "others": [],
        "error": None
    }

    try:
        if module_name in sys.modules:
            module = sys.modules[module_name]
        else:
            module = __import__(module_name)
    except ImportError:
        results["error"] = f"Erreur : Le module '{module_name}' n'a pas été trouvé. Assurez-vous qu'il est installé (par ex., pip install {module_name})."
        return results
    except Exception as e:
        results["error"] = f"Erreur lors du chargement du module '{module_name}' : {e}"
        return results

    members = dir(module)

    for member_name in members:
        if member_name.startswith('__') and member_name.endswith('__'):
            results["builtins"].append(member_name)
            continue

        try:
            member = getattr(module, member_name)

            # Determine if the member is defined in the current module or imported
            # This check is heuristic and might not be perfect for all edge cases
            is_defined_in_module = False
            if hasattr(member, '__module__'):
                # Check if the member's __module__ attribute matches our module_name
                # or if it's a direct attribute of the module's dict (more reliable)
                if member.__module__ == module_name or (hasattr(module, '__dict__') and member_name in module.__dict__ and module.__dict__[member_name] is member):
                    is_defined_in_module = True
            elif inspect.ismodule(member): # Sub-modules are always considered imported/separate
                 is_defined_in_module = False
            # For other cases, if it's a direct attribute of the module and not a module itself
            elif hasattr(module, '__dict__') and member_name in module.__dict__ and module.__dict__[member_name] is member:
                is_defined_in_module = True


            if inspect.isclass(member):
                if is_defined_in_module:
                    results["defined_classes"].append(member_name)
                else:
                    origin = getattr(member, '__module__', 'Inconnu')
                    results["imported_classes"].append(f"{member_name} (from {origin})")
            elif inspect.isfunction(member):
                if is_defined_in_module:
                    results["defined_functions"].append(member_name)
                else:
                    origin = getattr(member, '__module__', 'Inconnu')
                    results["imported_functions"].append(f"{member_name} (from {origin})")
            elif inspect.ismodule(member):
                results["sub_modules"].append(member_name)
            elif callable(member): # Other callables (like C-implemented built-ins, methods of the module itself)
                if is_defined_in_module:
                    # Treat as a defined function for simplicity if it's part of the module's dict
                    results["defined_functions"].append(member_name)
                else:
                    origin = getattr(member, '__module__', 'Inconnu')
                    results["imported_functions"].append(f"{member_name} (from {origin})")
            else: # Variables and other attributes
                if is_defined_in_module:
                    results["defined_variables"].append(member_name)
                else:
                    origin = getattr(member, '__module__', 'Inconnu') # May not have __module__
                    results["imported_variables"].append(f"{member_name} (from {origin})")

        except AttributeError:
            results["others"].append(member_name)
        except Exception as e:
            results["others"].append(f"{member_name} (Erreur: {e})")

    # Sort all lists alphabetically
    for key in results:
        if isinstance(results[key], list):
            results[key].sort()

    return results


### Application CustomTkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Inspecteur de Module Avancé")
        self.geometry("900x700") # Taille de fenêtre augmentée

        # Configure grid for dynamic resizing (Input frame at top, ScrollableFrame below)
        self.grid_rowconfigure(0, weight=0) # Input frame doesn't expand vertically
        self.grid_rowconfigure(1, weight=1) # Scrollable frame expands vertically
        self.grid_columnconfigure(0, weight=1) # Main column expands horizontally

        # --- Input Frame (at the top) ---
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="new")
        self.input_frame.grid_columnconfigure(0, weight=0) # Label
        self.input_frame.grid_columnconfigure(1, weight=1) # Entry expands
        self.input_frame.grid_columnconfigure(2, weight=0) # Button

        self.module_label = customtkinter.CTkLabel(self.input_frame, text="Nom du Module :")
        self.module_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self.module_entry = customtkinter.CTkEntry(self.input_frame, placeholder_text="ex: math, os, customtkinter")
        self.module_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.module_entry.bind("<Return>", self.on_enter_key)

        self.inspect_button = customtkinter.CTkButton(self.input_frame, text="Inspecter Module", command=self.inspect_selected_module)
        self.inspect_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="e")

        # --- Scrollable Frame for Results (below input) ---
        self.results_scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Membres du Module par Type et Origine")
        self.results_scrollable_frame.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nsew")
        self.results_scrollable_frame.grid_columnconfigure(0, weight=1) # Allow content frames to expand horizontally

        # Dictionary to hold the CTkTextbox for each category
        self.category_textboxes = {}
        self.create_category_frames()

        # Set default module to inspect on launch
        self.module_entry.insert(0, "customtkinter")
        self.inspect_selected_module()

    def create_category_frames(self):
        """Creates the frames and textboxes for each category within the scrollable frame."""
        categories = {
            "defined_classes": "Classes définies dans ce module",
            "imported_classes": "Classes importées",
            "defined_functions": "Fonctions définies dans ce module",
            "imported_functions": "Fonctions importées (et autres callables)",
            "defined_variables": "Variables définies dans ce module",
            "imported_variables": "Variables importées",
            "sub_modules": "Sous-modules",
            "builtins": "Attributs intégrés/spéciaux (__dunder__)",
            "others": "Autres (non classés / avertissements)"
        }

        row_counter = 0
        for key, title in categories.items():
            # Frame for each category
            category_frame = customtkinter.CTkFrame(self.results_scrollable_frame)
            category_frame.grid(row=row_counter, column=0, padx=5, pady=5, sticky="ew")
            category_frame.grid_columnconfigure(0, weight=1) # Allow textbox to expand

            # Label for the category
            label = customtkinter.CTkLabel(category_frame, text=title, font=customtkinter.CTkFont(weight="bold"))
            label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

            # Textbox for the category members
            textbox = customtkinter.CTkTextbox(category_frame, height=80, wrap="word", state="disabled") # Set a default height
            textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
            self.category_textboxes[key] = textbox
            row_counter += 1

    def on_enter_key(self, event=None):
        """Called when the Enter key is pressed in the module_entry."""
        self.inspect_selected_module()

    def inspect_selected_module(self):
        """Gets the module name from the input field and displays its info."""
        module_name = self.module_entry.get().strip()
        if module_name:
            self.display_module_info(module_name)
        else:
            self.clear_all_textboxes()
            if "defined_classes" in self.category_textboxes:
                textbox = self.category_textboxes["defined_classes"]
                textbox.configure(state="normal")
                textbox.insert("end", "Veuillez entrer le nom d'un module à inspecter.")
                textbox.configure(state="disabled")

    def display_module_info(self, module_name):
        """Fetches and displays module information in the respective CTkTextboxes."""
        self.clear_all_textboxes() # Clear all previous content

        results = classify_module_members(module_name)

        if results["error"]:
            if "defined_classes" in self.category_textboxes:
                textbox = self.category_textboxes["defined_classes"]
                textbox.configure(state="normal")
                textbox.insert("end", results["error"])
                textbox.configure(state="disabled")
            return

        # Populate each textbox with its respective content
        for category, textbox in self.category_textboxes.items():
            textbox.configure(state="normal") # Enable editing temporarily
            if category in results and results[category]:
                formatted_list = [f"- {item}" for item in results[category]]
                textbox.insert("end", "\n".join(formatted_list))
            else:
                textbox.insert("end", "Aucun élément dans cette catégorie.")
            textbox.configure(state="disabled") # Make text read-only again

    def clear_all_textboxes(self):
        """Clears the content of all category textboxes."""
        for textbox in self.category_textboxes.values():
            textbox.configure(state="normal") # Enable editing temporarily
            textbox.delete("1.0", "end")
            textbox.configure(state="disabled") # Disable again

if __name__ == "__main__":
    app = App()
    app.mainloop()