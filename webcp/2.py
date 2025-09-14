import subprocess
import os

# --- MODIFIEZ CES DEUX LIGNES SEULEMENT ---
SITE_A_TELECHARGER = "https://https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html"  # <--- METTEZ L'URL DU SITE ICI
DOSSIER_DE_SAUVEGARDE = "save"    # <--- METTEZ LE NOM DU DOSSIER ICI
# ------------------------------------------

def telecharger_site_automatiquement():
    """
    Télécharge un site web entier en utilisant 'wget' avec des paramètres prédéfinis.
    """
    url = SITE_A_TELECHARGER
    dossier = DOSSIER_DE_SAUVEGARDE

    if not url.startswith(("http://", "https://")):
        print("❌ Erreur : L'URL doit commencer par http:// ou https://")
        return

    if not os.path.exists(dossier):
        print(f"Création du dossier : {dossier}")
        os.makedirs(dossier)

    commande_wget = [
        "wget",
        "--mirror",          # Télécharge tout le site
        "--page-requisites", # Télécharge images, CSS, JS
        "--convert-links",   # Rend les liens locaux
        "--adjust-extension",# Ajoute .html si besoin
        "--no-parent",       # Reste dans le dossier du site
        "--no-clobber",      # Ne pas écraser les fichiers déjà téléchargés
        "--wait=1",          # Attend 1 seconde entre les requêtes
        "--random-wait",     # Attend un peu plus de manière aléatoire
        f"--directory-prefix={dossier}", # Définit le dossier de sauvegarde
        '--level=30',
        url
    ]

    print(f"Démarrage du téléchargement de {url} vers {dossier}...")
    try:
        subprocess.run(commande_wget, check=True, capture_output=True, text=True)
        print("\n✅ Téléchargement terminé avec succès !")
        print(f"Le site est sauvegardé dans le dossier : {os.path.abspath(dossier)}")
    except FileNotFoundError:
        print("\n❌ Erreur : 'wget' n'est pas trouvé. Assurez-vous qu'il est installé.")
        print("  - Linux/macOS : `sudo apt-get install wget` ou `brew install wget`")
        print("  - Windows : Téléchargez `wget.exe` et mettez-le dans le même dossier que ce script.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur de 'wget' (code : {e.returncode}) :")
        print("--- Sortie de Wget ---")
        print(e.stdout)
        print("--- Erreur de Wget ---")
        print(e.stderr)
    except Exception as e:
        print(f"\n❌ Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    telecharger_site_automatiquement()