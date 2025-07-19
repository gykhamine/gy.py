import qrcode
from PIL import Image

# Texte ou URL à encoder
data = "https://gykhamine.github.io/YP/1.html"

# Génération du QR code
qr = qrcode.make(data)


# Sauvegarde dans un fichier image
qr.save("qrcode2.png")