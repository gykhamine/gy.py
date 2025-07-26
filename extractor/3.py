import cv2
import numpy as np # NumPy est implicitement utilisé par OpenCV pour les images

# --- 1. Chemin de l'image ---
# Remplacez 'votre_image.jpg' par le nom de votre fichier image.
# Assurez-vous que le fichier est dans le même dossier que votre script Python,
# ou donnez le chemin complet vers le fichier (ex: 'C:/Users/Moi/Images/photo.png').
chemin_image = '32.png' # <<<<<< CHANGEZ CE CHEMIN >>>>>>

# --- 2. Lire l'image ---
# cv2.imread() charge l'image dans un tableau NumPy.
# Par défaut, OpenCV lit les images couleur en format BGR (Bleu, Vert, Rouge).
image = cv2.imread(chemin_image)

# --- 3. Vérifier si l'image a été chargée correctement ---
# Si le chemin est incorrect ou si le fichier est corrompu, imread() retourne None.
if image is None:
    print(f"Erreur : Impossible de lire l'image '{chemin_image}'.")
    print("Vérifiez le chemin du fichier et assurez-vous qu'il existe.")
    # On peut créer une image noire de démonstration pour continuer sans erreur
    # (utile pour les tests si vous n'avez pas de fichier image sous la main)
    image = np.zeros((300, 500, 3), dtype=np.uint8) # Crée une image noire 300x500 pixels
    cv2.putText(image, "Image non trouvee !", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(image, "Demo : Image noire", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
else:
    print(f"Image '{chemin_image}' lue avec succès.")
    print(f"Forme de l'image (hauteur, largeur, canaux) : {image.shape}")
    print(f"Type de données des pixels : {image.dtype}")


# --- 4. Afficher l'image (optionnel mais utile pour vérifier) ---
cv2.imshow('Image Chargee', image)

# --- 5. Attendre une touche et fermer la fenêtre ---
# cv2.waitKey(0) attend que vous appuyiez sur n'importe quelle touche pour fermer la fenêtre.
# Sans cette ligne, la fenêtre s'ouvrirait et se fermerait instantanément.
print("\nAppuyez sur n'importe quelle touche dans la fenêtre 'Image Chargee' pour la fermer...")
cv2.waitKey(0)
cv2.destroyAllWindows() # Ferme toutes les fenêtres d'OpenCV
print("Fenêtre fermée. Fin du programme.")