import customtkinter as ctk
import os
import tkinter as tk
from bs4 import BeautifulSoup, NavigableString
import re

# --- DÉFINITION DU CHEMIN RACINE ---
BASE_PATH = "/Gykhamine/Gykhamine/4/1/Gybliotek-main"

# Créez le répertoire de base si ce n'est pas déjà fait
if not os.path.exists(BASE_PATH):
    try:
        os.makedirs(BASE_PATH)
        print(f"Le chemin de base '{BASE_PATH}' a été créé.")
    except OSError as e:
        print(f"Erreur lors de la création du chemin de base '{BASE_PATH}': {e}")
        # Message d'avertissement si le répertoire ne peut pas être créé.

def _get_text_with_inline_spacing(element):
    """
    Extracts text from an element, ensuring a space between inline children.
    Handles NavigableString (text nodes) and Tag elements.
    """
    if isinstance(element, NavigableString):
        return str(element)
    if not hasattr(element, 'children'):
        return element.get_text(separator=' ', strip=True)

    parts = []
    for child in element.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif child.name in ['br', 'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'pre', 'article', 'section', 'main']:
            parts.append(_get_text_with_inline_spacing(child))
            parts.append('\n')
        else:
            parts.append(_get_text_with_inline_spacing(child))
            if child.next_sibling and not isinstance(child.next_sibling, NavigableString):
                parts.append(' ')

    clean_text = re.sub(r'\s+', ' ', ''.join(parts)).strip()
    return clean_text


def extract_and_format_clean_text(file_path):
    """
    Extrait et formate le texte d'un fichier HTML, en garantissant un espace
    entre le contenu de chaque balise importante, gérant les erreurs d'affichage,
    supprimant les lignes dupliquées et ajoutant un saut de ligne après chaque point.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Erreur : Fichier introuvable à '{file_path}'")
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        for tag_to_decompose in soup(['script', 'style', 'noscript', 'meta', 'link', 'form', 'nav', 'aside', 'header', 'footer', 'canvas', 'svg', 'iframe']):
            tag_to_decompose.decompose()

        top_level_block_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'div', 'blockquote', 'pre', 'article', 'section', 'main']

        raw_output_lines = []

        if soup.body:
            for element in soup.body.children:
                if isinstance(element, NavigableString) and element.strip():
                    cleaned_text = re.sub(r'\s+', ' ', str(element)).strip()
                    if cleaned_text:
                        raw_output_lines.append(cleaned_text)
                elif element.name in top_level_block_tags:
                    text_content = ""
                    if element.name == 'math':
                        annotation = element.find('annotation', encoding='application/x-tex')
                        if annotation and annotation.string:
                            text_content = f"[FORMULE LaTeX: {annotation.string.strip()}]"
                        else:
                            text_content = f"[FORMULE MathML: {element.get_text(separator=' ', strip=True)}]"
                    elif element.name in ['span', 'div'] and ('math-inline' in element.get('class', []) or 'math-display' in element.get('class', [])):
                        latex_source = element.get('data-latex') or element.get('data-mathml')
                        if latex_source:
                            text_content = f"[FORMULE SOURCE: {latex_source.strip()}]"
                        else:
                            text_content = f"[FORMULE TEXTE: {element.get_text(separator=' ', strip=True)}]"
                    else:
                        text_content = _get_text_with_inline_spacing(element)

                    if text_content:
                        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                            raw_output_lines.append(f"### {text_content.upper()} ###")
                        elif element.name == 'li':
                            raw_output_lines.append(f"- {text_content}")
                        else:
                            raw_output_lines.append(text_content)

        # --- Déduplication finale des lignes ---
        final_processed_lines = []
        seen_lines_hash = set()

        for line in raw_output_lines:
            clean_for_hash = re.sub(r'[^\w\s]', '', line).lower().strip()
            clean_for_hash = re.sub(r'\d+', '', clean_for_hash)

            if not clean_for_hash:
                continue

            if clean_for_hash in seen_lines_hash:
                continue

            seen_lines_hash.add(clean_for_hash)
            final_processed_lines.append(line)

        # --- NOUVEAU : Insérer un saut de ligne après chaque point ---
        text_before_line_breaks = "\n\n".join(final_processed_lines) # Joindre d'abord les blocs
        
        # Remplacer chaque point suivi d'un espace (ou non) par un point et un saut de ligne
        # Assurez-vous que le point n'est pas déjà suivi d'un saut de ligne ou d'un autre point.
        # Regex: \.  (le point)
        #        (?![.\n]) (lookahead négatif: ne pas être suivi par un point ou un saut de ligne)
        final_text = re.sub(r'\.(?![.\n])', '.\n', text_before_line_breaks)
        
        # Nettoyage final des sauts de ligne multiples excessifs
        final_text = re.sub(r'\n\n+', '\n\n', final_text)
        final_text = final_text.strip() # S'assurer qu'il n'y a pas d'espace en début/fin

        # Ajouter le titre de la page au début du texte
        page_title_tag = soup.find('title')
        page_title = page_title_tag.string.strip() if page_title_tag and page_title_tag.string else "Titre non trouvé"
        if page_title and (not final_text or not final_text.lower().startswith(f"titre de la page : {page_title.lower()}")):
            final_text = f"Titre de la page : {page_title}\n\n" + final_text

        return final_text

    except Exception as e:
        print(f"Une erreur inattendue est survenue lors de l'extraction ou du formatage de '{file_path}': {e}")
        return f"Échec de l'extraction ou erreur d'affichage pour le fichier : {os.path.basename(file_path)}\nErreur: {e}"

# --- Interface Utilisateur CustomTkinter (inchangée, sauf le nom du titre) ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Extracteur HTML Pro (Par Ligne)")
        self.geometry("1000x750")
        self.resizable(True, True)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Extracteur HTML Pro",
                                         font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.open_file_button = ctk.CTkButton(self.sidebar_frame, text="Ouvrir Fichier HTML",
                                              command=self.open_file_dialog, height=40, font=ctk.CTkFont(size=14, weight="bold"))
        self.open_file_button.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Mode d'Apparence:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                               values=["Light", "Dark", "System"],
                                                               command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        self.text_display = ctk.CTkTextbox(self, wrap="word",
                                         font=("Arial", 13),
                                         activate_scrollbars=True,
                                         corner_radius=10,
                                         border_width=2,
                                         border_color="gray",
                                         padx=15, pady=15)
        self.text_display.grid(row=0, column=1, padx=(10, 20), pady=(20, 20), sticky="nsew")
        self.text_display.insert("0.0", "Sélectionnez un fichier HTML pour en extraire et formater le texte.")
        self.text_display.configure(state="disabled")

    def open_file_dialog(self):
        file_path = tk.filedialog.askopenfilename(
            initialdir=BASE_PATH,
            filetypes=[("Fichiers HTML", "*.html *.htm"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            self.current_file_path = file_path
            self.extract_and_display(file_path)

    def extract_and_display(self, file_path):
        try:
            extracted_text = extract_and_format_clean_text(file_path)
            self.text_display.configure(state="normal")
            self.text_display.delete("0.0", "end")
            self.text_display.insert("0.0", extracted_text)
            self.text_display.configure(state="disabled")
            self.title(f"Texte Extrait Nettoyé - {os.path.basename(file_path)}")
        except Exception as e:
            error_message = f"Une erreur s'est produite lors de l'affichage ou du traitement du fichier : {os.path.basename(file_path)}\nErreur: {e}"
            self.text_display.configure(state="normal")
            self.text_display.delete("0.0", "end")
            self.text_display.insert("0.0", error_message)
            self.text_display.configure(state="disabled")
            self.title("Erreur d'Affichage")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    dummy_file_name = "dot_separated_example_page.html"
    dummy_file_path = os.path.join(BASE_PATH, dummy_file_name)

    if not os.path.exists(dummy_file_path):
        try:
            with open(dummy_file_path, 'w', encoding='utf-8') as f:
                f.write("""
                <!DOCTYPE html>
                <html lang="fr">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Page Test Point-Par-Ligne</title>
                </head>
                <body>
                    <h1><span>Ceci</span><span>est</span><span>un</span><span>titre</span>important. Ceci est une phrase.</h1>
                    <p>Un paragraphe avec <strong>du texte en gras</strong> et <em>en italique</em>. Suivi d'un <a href="#">lien</a>. Une autre phrase ici.</p>
                    <div>
                        Texte direct dans un div.<span>Un</span><span>mot</span><span>en</span><span>plus</span>.
                    </div>
                    <p>Ceci est la première phrase. Deuxième phrase. Troisième phrase.</p>
                    <p>Un autre paragraphe unique.</p>
                    <h2>Sous-titre. Une phrase de sous-titre.</h2>
                    <ul>
                        <li><p>Item de liste 1.</p> Ceci est un detail.</li>
                        <li>Item de liste 2. Avec un point.</li>
                        <li><span class="math-inline">`f(x)=<span>x</span>^2`</span>. Une formule.</li>
                    </ul>
                    <p>Final paragraph. Un point final.</p>
                    <p>Encore une ligne.</p>
                    <div>Un dernier <span style="color:red;">texte</span> simple. Point.</div>
                </body>
                </html>
                """)
            print(f"Fichier HTML factice '{dummy_file_name}' créé dans '{BASE_PATH}'.")
        except Exception as e:
            print(f"Impossible de créer le fichier factice dans '{BASE_PATH}': {e}")
            print("Veuillez vérifier les permissions ou créer le dossier manuellement.")
    else:
        print(f"Le fichier factice '{dummy_file_name}' existe déjà dans '{BASE_PATH}'.")

    app = App()
    app.mainloop()