import customtkinter as ctk
import datetime
from tkinter import filedialog, messagebox

class HTMLGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Générateur de Page HTML")
        self.geometry("700x550") # Taille de la fenêtre
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Cadre principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # --- Widgets pour la saisie des paramètres HTML ---

        # Titre de la page
        self.title_label = ctk.CTkLabel(self.main_frame, text="Titre de la page HTML :")
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.title_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Mon Super Titre")
        self.title_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.title_entry.insert(0, "Ma Page Générée") # Valeur par défaut

        # Message d'accueil
        self.message_label = ctk.CTkLabel(self.main_frame, text="Message d'accueil :")
        self.message_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.message_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Bonjour le monde !")
        self.message_entry.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.message_entry.insert(0, "Bienvenue sur ma page ! Ceci est un contenu dynamique.") # Valeur par défaut


        # Éléments de la liste
        self.list_label = ctk.CTkLabel(self.main_frame, text="Éléments de la liste (séparés par des virgules) :")
        self.list_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        self.list_entry = ctk.CTkEntry(self.main_frame, placeholder_text="élément 1, élément 2, élément 3")
        self.list_entry.grid(row=5, column=0, padx=10, pady=(0, 20), sticky="ew")
        self.list_entry.insert(0, "Pommes, Bananes, Oranges") # Valeur par défaut

        # Bouton de génération
        self.generate_button = ctk.CTkButton(self.main_frame, text="Générer et Sauvegarder le HTML", command=self.generate_and_save_html)
        self.generate_button.grid(row=6, column=0, padx=10, pady=10)

        # --- Affichage du HTML généré (optionnel, mais utile pour le débogage) ---
        self.html_output_label = ctk.CTkLabel(self.main_frame, text="Aperçu du HTML généré :")
        self.html_output_label.grid(row=7, column=0, padx=10, pady=(20, 0), sticky="w")
        self.html_output_text = ctk.CTkTextbox(self.main_frame, height=150, width=500, wrap="word")
        self.html_output_text.grid(row=8, column=0, padx=10, pady=(0, 10), sticky="ew")


    def generate_html_content(self, titre, message_accueil, elements_liste):
        """
        Génère la chaîne de caractères HTML.
        Similaire à la fonction du script précédent.
        """
        date_du_jour = datetime.date.today().strftime("%d/%m/%Y")

        liste_html = ""
        for element in elements_liste:
            if element.strip(): # Assurez-vous que l'élément n'est pas vide après nettoyage
                liste_html += f"            <li>{element.strip()}</li>\n"

        html_template = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titre}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f4f4f4;
            color: #333;
            line-height: 1.6;
        }}
        h1 {{
            color: #0056b3;
            text-align: center;
            padding-bottom: 10px;
            border-bottom: 2px solid #0056b3;
        }}
        p {{
            font-size: 1.1em;
            text-align: center;
        }}
        ul {{
            list-style-type: disc;
            margin: 20px auto;
            max-width: 600px;
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        footer {{
            margin-top: 50px;
            font-size: 0.8em;
            color: #666;
            text-align: center;
            border-top: 1px solid #ccc;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    <h1>{titre}</h1>
    <p>{message_accueil}</p>

    <h2>Contenu de la liste :</h2>
    <ul>
{liste_html.strip()}
    </ul>

    <footer>
        <p>Page générée automatiquement par l'application Python le {date_du_jour}.</p>
    </footer>
</body>
</html>
"""
        return html_template

    def generate_and_save_html(self):
        """
        Récupère les données des champs de saisie, génère le HTML
        et demande à l'utilisateur où sauvegarder le fichier.
        """
        titre = self.title_entry.get()
        message = self.message_entry.get()
        # Divise la chaîne des éléments par les virgules et nettoie les espaces
        elements_str = self.list_entry.get()
        elements_liste = [item.strip() for item in elements_str.split(',') if item.strip()]

        # Vérification minimale des entrées
        if not titre or not message:
            messagebox.showwarning("Attention", "Veuillez remplir au moins le titre et le message d'accueil.")
            return

        # Générer le contenu HTML
        html_content = self.generate_html_content(titre, message, elements_liste)

        # Afficher le HTML généré dans la zone de texte
        self.html_output_text.delete("1.0", "end") # Efface le contenu précédent
        self.html_output_text.insert("1.0", html_content)

        # Demander à l'utilisateur où sauvegarder le fichier
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("Fichiers HTML", "*.html"), ("Tous les fichiers", "*.*")],
            title="Sauvegarder la page HTML sous..."
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                messagebox.showinfo("Succès", f"La page HTML a été sauvegardée avec succès à :\n{file_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue lors de la sauvegarde : {e}")
        else:
            messagebox.showinfo("Annulé", "Sauvegarde annulée.")

# --- Lancement de l'application ---
if __name__ == "__main__":
    app = HTMLGeneratorApp()
    app.mainloop()