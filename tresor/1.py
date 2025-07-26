import numpy as np

# --- 1. Cr�ation de tableaux (Arrays) ---

# Cr�er un tableau 1D (vecteur)
arr1d = np.array([1, 2, 3, 4, 5])
print("1D Array:", arr1d)
print("Type d'�l�ments:", arr1d.dtype)
print("Forme (Shape):", arr1d.shape) # (5,) signifie 5 �l�ments, 1 dimension
print("-" * 20)

# Cr�er un tableau 2D (matrice)
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("2D Array:\n", arr2d)
print("Forme (Shape):", arr2d.shape) # (3, 3) signifie 3 lignes, 3 colonnes
print("-" * 20)

# Cr�er un tableau rempli de z�ros
zeros_arr = np.zeros((2, 4)) # 2 lignes, 4 colonnes
print("Zeros Array:\n", zeros_arr)
print("-" * 20)

# Cr�er un tableau rempli de uns
ones_arr = np.ones((3, 3))
print("Ones Array:\n", ones_arr)
print("-" * 20)

# Cr�er un tableau avec une s�quence de nombres (similaire � range())
seq_arr = np.arange(0, 10, 2) # Commence � 0, va jusqu'� (mais n'inclut pas) 10, par pas de 2
print("Sequence Array:", seq_arr)
print("-" * 20)

# Cr�er un tableau avec des nombres espac�s lin�airement
linspace_arr = np.linspace(0, 10, 5) # 5 nombres entre 0 et 10 (inclus)
print("Linspace Array:", linspace_arr)
print("-" * 20)

# --- 2. Op�rations arithm�tiques ---

a = np.array([10, 20, 30, 40])
b = np.array([1, 2, 3, 4])

# Addition �l�ment par �l�ment
print("a + b:", a + b)

# Soustraction �l�ment par �l�ment
print("a - b:", a - b)

# Multiplication �l�ment par �l�ment
print("a * b:", a * b)

# Division �l�ment par �l�ment
print("a / b:", a / b)

# Op�ration scalaire (appliqu�e � chaque �l�ment)
print("a + 5:", a + 5)
print("-" * 20)

# --- 3. Indexation et Slicing (d�coupage) ---

mat = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Acc�der � un �l�ment (ligne, colonne)
print("Element (0, 0):", mat[0, 0]) # Premier �l�ment (1)
print("Element (1, 2):", mat[1, 2]) # �l�ment � la deuxi�me ligne, troisi�me colonne (6)
print("-" * 20)

# Acc�der � une ligne enti�re
print("Premi�re ligne:", mat[0, :]) # ou mat[0]
print("-" * 20)

# Acc�der � une colonne enti�re
print("Deuxi�me colonne:", mat[:, 1])
print("-" * 20)

# Slicing (sous-matrice)
sub_mat = mat[0:2, 1:3] # Lignes 0 et 1, colonnes 1 et 2
print("Sous-matrice:\n", sub_mat)
print("-" * 20)

# --- 4. Manipulation de la forme (Reshaping) ---

original_arr = np.arange(12) # [ 0  1  2  3  4  5  6  7  8  9 10 11]
print("Original Array:", original_arr)

# Changer la forme en 3x4 (3 lignes, 4 colonnes)
reshaped_arr = original_arr.reshape(3, 4)
print("Reshaped to 3x4:\n", reshaped_arr)

# Changer la forme en 4x3 (4 lignes, 3 colonnes)
reshaped_arr_2 = original_arr.reshape(4, 3)
print("Reshaped to 4x3:\n", reshaped_arr_2)

# -1 permet � NumPy de calculer la dimension manquante
reshaped_arr_3 = original_arr.reshape(2, -1) # 2 lignes, NumPy calcule la colonne (6)
print("Reshaped to 2 rows (-1 col):\n", reshaped_arr_3)
print("-" * 20)

# --- 5. Fonctions agr�g�es (Agr�gations) ---

rand_arr = np.array([[1, 2, 3], [4, 5, 6]])

print("Somme de tous les �l�ments:", rand_arr.sum())
print("Minimum:", rand_arr.min())
print("Maximum:", rand_arr.max())
print("Moyenne:", rand_arr.mean())
print("�cart-type:", rand_arr.std())

# Somme par colonne (axis=0)
print("Somme par colonne:", rand_arr.sum(axis=0)) # [5 7 9]

# Somme par ligne (axis=1)
print("Somme par ligne:", rand_arr.sum(axis=1)) # [ 6 15]
print("-" * 20)

# --- 6. Alg�bre Lin�aire ---

mat1 = np.array([[1, 2], [3, 4]])
mat2 = np.array([[5, 6], [7, 8]])

# Produit matriciel (dot product)
dot_product = np.dot(mat1, mat2)
print("Produit matriciel:\n", dot_product)

# Transpos�e d'une matrice
transposed_mat1 = mat1.T
print("Transpos�e de mat1:\n", transposed_mat1)
print("-" * 20)