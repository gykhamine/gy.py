objects_python = {
    "String": {
        "methods": {
            "charAt()": ("Retourne le caractère à une position donnée.", "s = 'Hello'; print(s[1]) # 'e'"),
            "concat()": ("Concatène deux ou plusieurs chaînes.", "s1 = 'Hello'; s2 = ' World'; print(s1 + s2) # 'Hello World'"),
            "includes()": ("Vérifie si une chaîne contient une autre chaîne.", "s = 'Hello'; print('ell' in s) # True"),
            "indexOf()": ("Retourne la première position où une chaîne se trouve.", "s = 'Hello'; print(s.find('l')) # 2"),
            "replace()": ("Remplace une partie de la chaîne par une autre.", "s = 'Hello'; print(s.replace('l', 'L', 1)) # 'HeLlo' (remplace la première occurence)"),
            "slice()": ("Extrait une portion d'une chaîne.", "s = 'Hello World'; print(s[0:5]) # 'Hello'"),
            "split()": ("Divise une chaîne en une liste en fonction d'un séparateur.", "s = 'apple,banana,grape'; print(s.split(',')) # ['apple', 'banana', 'grape']"),
            "toLowerCase()": ("Convertit tous les caractères en minuscules.", "s = 'HELLO'; print(s.lower()) # 'hello'"),
            "toUpperCase()": ("Convertit tous les caractères en majuscules.", "s = 'hello'; print(s.upper()) # 'HELLO'"),
            "trim()": ("Supprime les espaces au début et à la fin de la chaîne.", "s = '  Hello  '; print(s.strip()) # 'Hello'"),
            "startsWith()": ("Vérifie si une chaîne commence par un certain texte.", "s = 'Hello'; print(s.startswith('He')) # True"),
            "endsWith()": ("Vérifie si une chaîne se termine par un certain texte.", "s = 'Hello'; print(s.endswith('lo')) # True"),
            "repeat()": ("Répète une chaîne de caractères plusieurs fois.", "s = 'Hi'; print(s * 3) # 'HiHiHi'"),
            "charCodeAt()": ("Retourne le code de caractère Unicode à une position donnée.", "s = 'Hello'; print(ord(s[1])) # 101"),
            "lastIndexOf()": ("Retourne la dernière position où un élément se trouve.", "s = 'Hello Hello'; print(s.rfind('Hello')) # 6"),
        },
        "description": "Les **chaînes de caractères** en Python sont des séquences immuables de caractères."
    },
    "List": { # L'équivalent Python de "Array" en JS
        "methods": {
            "push()": ("Ajoute un ou plusieurs éléments à la fin d'une liste.", "arr = [1, 2]; arr.append(3); print(arr) # [1, 2, 3]"),
            "pop()": ("Supprime le dernier élément d'une liste.", "arr = [1, 2, 3]; arr.pop(); print(arr) # [1, 2]"),
            "shift()": ("Supprime le premier élément d'une liste (implémentation via slice).", "arr = [1, 2, 3]; arr = arr[1:]; print(arr) # [2, 3]"),
            "unshift()": ("Ajoute un ou plusieurs éléments au début d'une liste (implémentation via slice et concaténation).", "arr = [2, 3]; arr = [1] + arr; print(arr) # [1, 2, 3]"),
            "map()": ("Crée une nouvelle liste avec les résultats de l'application d'une fonction sur chaque élément.", "arr = [1, 2, 3]; result = list(map(lambda x: x * 2, arr)); print(result) # [2, 4, 6]"),
            "filter()": ("Crée une nouvelle liste avec tous les éléments qui passent un test.", "arr = [1, 2, 3, 4]; result = list(filter(lambda x: x % 2 == 0, arr)); print(result) # [2, 4]"),
            "reduce()": ("Applique une fonction sur un accumulateur et chaque élément d'une liste pour la réduire à une seule valeur (via boucle).", "arr = [1, 2, 3]; sum_val = 0; for val in arr: sum_val += val; print(sum_val) # 6"),
            "forEach()": ("Exécute une fonction sur chaque élément d'une liste (via boucle `for`).", "arr = [1, 2, 3]; for x in arr: print(x) # 1\\n2\\n3"),
            "concat()": ("Fusionne deux ou plusieurs listes.", "arr1 = [1, 2]; arr2 = [3, 4]; print(arr1 + arr2) # [1, 2, 3, 4]"),
            "join()": ("Fusionne tous les éléments d'une liste en une seule chaîne.", "arr = ['1', '2', '3']; print('-'.join(arr)) # '1-2-3'"),
            "indexOf()": ("Retourne la première position où un élément se trouve.", "arr = [1, 2, 3]; print(arr.index(2)) # 1"),
            "find()": ("Retourne le premier élément trouvé qui passe un test (via boucle `for`).", "arr = [1, 2, 3]; found = None; for x in arr: if x > 2: found = x; break; print(found) # 3"),
            "sort()": ("Trie les éléments d'une liste.", "arr = [3, 1, 2]; arr.sort(); print(arr) # [1, 2, 3]"),
            "reverse()": ("Inverse l'ordre des éléments d'une liste.", "arr = [1, 2, 3]; arr.reverse(); print(arr) # [3, 2, 1]"),
            "slice()": ("Extrait une portion d'une liste.", "arr = [1, 2, 3, 4]; print(arr[1:3]) # [2, 3]"),
            "splice()": ("Modifie une liste en ajoutant ou supprimant des éléments (via slice et assignation).", "arr = [1, 2, 3]; arr[1:2] = [4]; print(arr) # [1, 4, 3]"),
            "some()": ("Teste si au moins un élément de la liste passe un test (via `any()`).", "arr = [1, 2, 3]; print(any(x > 2 for x in arr)) # True"),
            "every()": ("Teste si tous les éléments de la liste passent un test (via `all()`).", "arr = [1, 2, 3]; print(all(x > 0 for x in arr)) # True"),
            "findIndex()": ("Retourne l'index du premier élément trouvé qui passe un test (via boucle `for` avec `enumerate`).", "arr = [1, 2, 3]; index = -1; for i, x in enumerate(arr): if x > 2: index = i; break; print(index) # 2"),
            "fill()": ("Remplit tous les éléments d'une liste avec une valeur statique (via multiplication ou list comprehension).", "arr = [0] * 3; print(arr) # [0, 0, 0]")
        },
        "description": "Le type **List** est une structure de données mutable en Python qui peut contenir des éléments de différents types."
    },
    "Tuple": {
        "methods": {
            "concat()": ("Fusionne deux ou plusieurs tuples.", "t1 = (1, 2); t2 = (3, 4); print(t1 + t2) # (1, 2, 3, 4)"),
            "slice()": ("Extrait une portion d'un tuple.", "t = (1, 2, 3, 4); print(t[1:3]) # (2, 3)"),
            "indexOf()": ("Retourne la première position où un élément se trouve.", "t = (1, 2, 3); print(t.index(2)) # 1"),
            "count()": ("Retourne le nombre d'occurrences d'une valeur.", "t = (1, 2, 2, 3); print(t.count(2)) # 2"),
            "len()": ("Retourne la longueur (nombre d'éléments) du tuple.", "t = (1, 2, 3); print(len(t)) # 3")
        },
        "description": "Le type **Tuple** est une séquence immuable d'éléments, souvent utilisée pour des collections de taille fixe."
    },
    "Set": {
        "methods": {
            "add()": ("Ajoute un élément à l'ensemble.", "s = {1, 2}; s.add(3); print(s) # {1, 2, 3}"),
            "remove()": ("Supprime un élément de l'ensemble (lève une erreur si l'élément n'existe pas).", "s = {1, 2, 3}; s.remove(3); print(s) # {1, 2}"),
            "discard()": ("Supprime un élément de l'ensemble (ne fait rien si l'élément n'existe pas).", "s = {1, 2, 3}; s.discard(4); print(s) # {1, 2, 3}"),
            "pop()": ("Supprime et retourne un élément arbitraire de l'ensemble.", "s = {1, 2, 3}; elem = s.pop(); print(s) # {1, 2} (exemple)"),
            "clear()": ("Supprime tous les éléments de l'ensemble.", "s = {1, 2, 3}; s.clear(); print(s) # set()"),
            "union()": ("Retourne un nouvel ensemble contenant tous les éléments de tous les ensembles.", "s1 = {1, 2}; s2 = {2, 3}; print(s1.union(s2)) # {1, 2, 3}"),
            "intersection()": ("Retourne un nouvel ensemble contenant les éléments communs.", "s1 = {1, 2}; s2 = {2, 3}; print(s1.intersection(s2)) # {2}"),
            "difference()": ("Retourne un nouvel ensemble avec les éléments présents dans le premier ensemble mais pas dans le second.", "s1 = {1, 2, 3}; s2 = {3, 4}; print(s1.difference(s2)) # {1, 2}"),
            "symmetric_difference()": ("Retourne un nouvel ensemble avec les éléments qui sont dans l'un des ensembles, mais pas dans les deux.", "s1 = {1, 2, 3}; s2 = {3, 4, 5}; print(s1.symmetric_difference(s2)) # {1, 2, 4, 5}"),
            "issubset()": ("Vérifie si un ensemble est un sous-ensemble d'un autre.", "s1 = {1, 2}; s2 = {1, 2, 3}; print(s1.issubset(s2)) # True"),
            "issuperset()": ("Vérifie si un ensemble est un sur-ensemble d'un autre.", "s1 = {1, 2, 3}; s2 = {1, 2}; print(s1.issuperset(s2)) # True"),
            "isdisjoint()": ("Vérifie si deux ensembles n'ont aucun élément en commun.", "s1 = {1, 2}; s2 = {3, 4}; print(s1.isdisjoint(s2)) # True"),
            "len()": ("Retourne le nombre d'éléments dans l'ensemble.", "s = {1, 2, 3}; print(len(s)) # 3"),
            "in": ("Vérifie si un élément est présent dans l'ensemble.", "s = {1, 2, 3}; print(2 in s) # True")
        },
        "description": "Le type **Set** est une collection non ordonnée d'éléments uniques et mutables."
    },
    "Boolean": { # L'équivalent Python de "Boolean"
        "methods": {
            "bool()": ("Convertit une valeur en booléen.", "print(bool(0)) # False; print(bool('hello')) # True"),
            "and": ("Opérateur logique AND.", "print(True and False) # False"),
            "or": ("Opérateur logique OR.", "print(True or False) # True"),
            "not": ("Opérateur logique NOT.", "print(not True) # False"),
            "isinstance()": ("Vérifie si une valeur est de type booléen.", "print(isinstance(True, bool)) # True")
        },
        "description": "Le type **Boolean** représente les valeurs de vérité : `True` ou `False`."
    },
    "Integer": { # Pour les nombres entiers
        "methods": {
            "int()": ("Convertit une valeur en entier.", "print(int('123')) # 123; print(int(3.14)) # 3"),
            "abs()": ("Retourne la valeur absolue d'un entier.", "print(abs(-5)) # 5"),
            "pow()": ("Retourne la base élevée à la puissance de l'exposant.", "print(pow(2, 3)) # 8"),
            "divmod()": ("Retourne le quotient et le reste de la division.", "print(divmod(10, 3)) # (3, 1)"),
            "bit_length()": ("Retourne le nombre de bits nécessaires pour représenter l'entier en binaire.", "n = 42; print(n.bit_length()) # 6 (0b101010)"),
            "as_integer_ratio()": ("Retourne une paire d'entiers représentant le ratio de l'entier et 1.", "n = 5; print(n.as_integer_ratio()) # (5, 1)"),
            "from_bytes()": ("Retourne l'entier représenté par un tableau d'octets.", "print(int.from_bytes(b'\\x00\\x01', byteorder='big')) # 1"),
            "to_bytes()": ("Retourne un tableau d'octets représentant l'entier.", "n = 1; print(n.to_bytes(2, byteorder='big')) # b'\\x00\\x01'"),
            "__add__ (opérateur +)": ("Additionne deux entiers.", "print(5 + 3) # 8"),
            "__sub__ (opérateur -)": ("Soustrait deux entiers.", "print(5 - 3) # 2"),
            "__mul__ (opérateur *)": ("Multiplie deux entiers.", "print(5 * 3) # 15"),
            "__truediv__ (opérateur /)": ("Divise deux entiers (retourne un flottant).", "print(5 / 2) # 2.5"),
            "__floordiv__ (opérateur //)": ("Division entière.", "print(5 // 2) # 2"),
            "__mod__ (opérateur %)": ("Retourne le reste de la division.", "print(5 % 2) # 1"),
            "__pow__ (opérateur **)": ("Élève à la puissance.", "print(2 ** 3) # 8")
        },
        "description": "Le type **Integer** représente les nombres entiers (positifs, négatifs, zéro) en Python avec une précision arbitraire."
    },
    "Float": { # Pour les nombres à virgule flottante
        "methods": {
            "float()": ("Convertit une valeur en nombre à virgule flottante.", "print(float('3.14')) # 3.14"),
            "abs()": ("Retourne la valeur absolue d'un flottant.", "print(abs(-5.5)) # 5.5"),
            "round()": ("Arrondit un flottant à l'entier le plus proche (ou au nombre de décimales spécifié).", "print(round(3.14)) # 3; print(round(3.14159, 2)) # 3.14"),
            "is_integer()": ("Vérifie si le flottant a une valeur entière.", "f = 5.0; print(f.is_integer()) # True"),
            "as_integer_ratio()": ("Retourne une paire d'entiers dont le ratio est égal au flottant.", "f = 0.5; print(f.as_integer_ratio()) # (1, 2)"),
            "hex()": ("Retourne une représentation hexadécimale du flottant.", "f = 3.5; print(f.hex()) # '0x1.c000000000000p+1'"),
            "fromhex()": ("Construit un flottant à partir d'une chaîne hexadécimale.", "print(float.fromhex('0x1.c000000000000p+1')) # 3.5"),
            "__add__ (opérateur +)": ("Additionne deux flottants.", "print(5.5 + 3.2) # 8.7"),
            "__sub__ (opérateur -)": ("Soustrait deux flottants.", "print(5.5 - 3.2) # 2.3"),
            "__mul__ (opérateur *)": ("Multiplie deux flottants.", "print(5.5 * 2.0) # 11.0"),
            "__truediv__ (opérateur /)": ("Divise deux flottants.", "print(5.0 / 2.0) # 2.5"),
            "__floordiv__ (opérateur //)": ("Division entière (retourne un flottant).", "print(5.0 // 2.0) # 2.0"),
            "__mod__ (opérateur %)": ("Retourne le reste de la division.", "print(5.0 % 2.0) # 1.0"),
            "__pow__ (opérateur **)": ("Élève à la puissance.", "print(2.0 ** 3.0) # 8.0"),
            "MAX_VALUE": ("Représente la valeur maximale qu'un flottant peut prendre.", "import sys; print(sys.float_info.max) # 1.7976931348623157e+308"),
            "MIN_VALUE": ("Représente la valeur minimale qu'un flottant peut prendre.", "import sys; print(sys.float_info.min) # 2.2250738585072014e-308"),
            "EPSILON": ("Représente la plus petite différence entre 1 et le plus petit flottant > 1.", "import sys; print(sys.float_info.epsilon) # 2.220446049250313e-16"),
            "NaN": ("Représente la valeur Not-a-Number.", "print(float('nan')) # nan"),
            "NEGATIVE_INFINITY": ("Représente la valeur négative infinie.", "print(float('-inf')) # -inf"),
            "POSITIVE_INFINITY": ("Représente la valeur positive infinie.", "print(float('inf')) # inf")
        },
        "description": "Le type **Float** représente les nombres décimaux en Python."
    },
    "Binary Data": { # Ajout de la section pour les données binaires
        "methods": {
            "bin() (sur int)": ("Convertit un entier en sa représentation binaire (chaîne).", "nombre = 10; print(bin(nombre)) # '0b1010'"),
            "int(binaire_str, 2)": ("Convertit une chaîne binaire en entier.", "chaine_binaire = '0b1010'; print(int(chaine_binaire, 2)) # 10"),
            "& (opérateur AND bit à bit)": ("Effectue un ET logique bit à bit entre entiers.", "print(5 & 3) # 1 (0b101 & 0b011 = 0b001)"),
            "| (opérateur OR bit à bit)": ("Effectue un OU logique bit à bit entre entiers.", "print(5 | 3) # 7 (0b101 | 0b011 = 0b111)"),
            "^ (opérateur XOR bit à bit)": ("Effectue un OU exclusif bit à bit entre entiers.", "print(5 ^ 3) # 6 (0b101 ^ 0b011 = 0b110)"),
            "~ (opérateur NOT bit à bit)": ("Inverse tous les bits (complément à un) d'un entier.", "print(~5) # -6"),
            "<< (opérateur décalage à gauche)": ("Décale les bits d'un entier vers la gauche.", "print(5 << 1) # 10"),
            ">> (opérateur décalage à droite)": ("Décale les bits d'un entier vers la droite.", "print(5 >> 1) # 2"),
            "bytes() (création)": ("Crée une séquence d'octets immuable.", "binaire = bytes([72, 101, 108]); print(binaire) # b'Hel'"),
            "bytearray() (création)": ("Crée une séquence d'octets mutable.", "mutable_binaire = bytearray(b'abc'); mutable_binaire[0] = 97; print(mutable_binaire) # bytearray(b'abc')"),
            "b'...' (littéral bytes)": ("Crée une séquence d'octets à partir d'un littéral de chaîne.", "litt_bytes = b'hello'; print(litt_bytes) # b'hello'"),
            ".decode() (sur bytes)": ("Convertit une séquence d'octets en chaîne (avec encodage).", "octets = b'salut'; print(octets.decode('utf-8')) # 'salut'"),
            ".encode() (sur str)": ("Convertit une chaîne en séquence d'octets (avec encodage).", "chaine = 'salut'; print(chaine.encode('utf-8')) # b'salut'")
        },
        "description": "En Python, les données binaires sont représentées par des **nombres entiers** (pour les opérations bit à bit et conversions) et des types **bytes** ou **bytearray** (pour les séquences d'octets brutes)."
    }
}