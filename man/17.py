import customtkinter as ctk
import tkinter as tk

# Liste complète des objets JavaScript et de leurs méthodes (20 fonctions par objet)
objects_js = {
    "String": {
        "methods": {
            "charAt()": ("Retourne le caractère à une position donnée.", "$str = 'Hello'; echo substr($str, 1, 1); // 'e'"),
            "concat()": ("Concatène deux ou plusieurs chaînes.", "$str1 = 'Hello'; $str2 = ' World'; echo $str1 . $str2; // 'Hello World'"),
            "includes()": ("Vérifie si une chaîne contient une autre chaîne.", "$str = 'Hello'; var_dump(str_contains($str, 'ell')); // true (PHP 8+)"),
            "indexOf()": ("Retourne la première position où une chaîne se trouve.", "$str = 'Hello'; echo strpos($str, 'l'); // 2"),
            "replace()": ("Remplace une partie de la chaîne par une autre.", "$str = 'Hello'; echo str_replace('l', 'L', $str); // 'HeLlo'"),
            "slice()": ("Extraire une portion d'une chaîne.", "$str = 'Hello World'; echo substr($str, 0, 5); // 'Hello'"),
            "split()": ("Divise une chaîne en un tableau en fonction d'un séparateur.", "$str = 'apple,banana,grape'; print_r(explode(',', $str)); // Array ( [0] => apple [1] => banana [2] => grape )"),
            "toLowerCase()": ("Convertit tous les caractères en minuscules.", "$str = 'HELLO'; echo strtolower($str); // 'hello'"),
            "toUpperCase()": ("Convertit tous les caractères en majuscules.", "$str = 'hello'; echo strtoupper($str); // 'HELLO'"),
            "trim()": ("Supprime les espaces au début et à la fin de la chaîne.", "$str = '  Hello  '; echo trim($str); // 'Hello'"),
            "startsWith()": ("Vérifie si une chaîne commence par un certain texte.", "$str = 'Hello'; var_dump(str_starts_with($str, 'He')); // true (PHP 8+)"),
            "endsWith()": ("Vérifie si une chaîne se termine par un certain texte.", "$str = 'Hello'; var_dump(str_ends_with($str, 'lo')); // true (PHP 8+)"),
            "repeat()": ("Répète une chaîne de caractères plusieurs fois.", "$str = 'Hi'; echo str_repeat($str, 3); // 'HiHiHi'"),
            "charCodeAt()": ("Retourne le code de caractère Unicode à une position donnée.", "$str = 'Hello'; echo ord($str[1]); // 101"),
            "localeCompare()": ("Compare deux chaînes de manière locale.", "$str1 = 'apple'; $str2 = 'banana'; echo strcoll($str1, $str2); // -1 (dépend de la locale)"),
            "padStart()": ("Ajoute des caractères au début de la chaîne jusqu'à une longueur spécifiée.", "$str = '5'; echo str_pad($str, 3, '0', STR_PAD_LEFT); // '005'"),
            "padEnd()": ("Ajoute des caractères à la fin de la chaîne jusqu'à une longueur spécifiée.", "$str = '5'; echo str_pad($str, 3, '0', STR_PAD_RIGHT); // '500'"),
            "fromCharCode()": ("Crée une chaîne à partir d'une ou plusieurs valeurs de code de caractère.", "echo chr(72) . chr(101) . chr(108) . chr(108) . chr(111); // 'Hello'"),
            "lastIndexOf()": ("Retourne la dernière position où un élément se trouve.", "$str = 'Hello Hello'; echo strrpos($str, 'Hello'); // 6"),
            "match()": ("Cherche une correspondance entre une chaîne et une expression régulière.", "$str = 'Hello'; preg_match_all('/[a-z]/', $str, $matches); print_r($matches[0]); // Array ( [0] => e [1] => l [2] => l [3] => o )")
        },
        "description": "Le type String représente des chaînes de caractères."
    },
    "Array": {
        "methods": {
            "push()": ("Ajoute un ou plusieurs éléments à la fin d'un tableau.", "$arr = [1, 2]; array_push($arr, 3); print_r($arr); // Array ( [0] => 1 [1] => 2 [2] => 3 )"),
            "pop()": ("Supprime le dernier élément d'un tableau.", "$arr = [1, 2, 3]; array_pop($arr); print_r($arr); // [1, 2]"),
            "shift()": ("Supprime le premier élément d'un tableau.", "$arr = [1, 2, 3]; array_shift($arr); print_r($arr); // [2, 3]"),
            "unshift()": ("Ajoute un ou plusieurs éléments au début d'un tableau.", "$arr = [2, 3]; array_unshift($arr, 1); print_r($arr); // [1, 2, 3]"),
            "map()": ("Crée un nouveau tableau avec les résultats de l'appel d'une fonction sur chaque élément.", "$arr = [1, 2, 3]; $result = array_map(function($x) { return $x * 2; }, $arr); print_r($result); // [2, 4, 6]"),
            "filter()": ("Crée un nouveau tableau avec tous les éléments qui passent un test.", "$arr = [1, 2, 3, 4]; $result = array_filter($arr, function($x) { return $x % 2 === 0; }); print_r($result); // [2, 4]"),
            "reduce()": ("Applique une fonction sur un accumulateur et chaque élément d'un tableau pour le réduire à une seule valeur.", "$arr = [1, 2, 3]; $sum = array_reduce($arr, function($acc, $val) { return $acc + $val; }, 0); echo $sum; // 6"),
            "forEach()": ("Exécute une fonction sur chaque élément d'un tableau. (Utilisez une boucle `foreach`)", "$arr = [1, 2, 3]; foreach ($arr as $x) { echo $x . ' '; } // 1 2 3"),
            "concat()": ("Fusionne deux ou plusieurs tableaux.", "$arr1 = [1, 2]; $arr2 = [3, 4]; print_r(array_merge($arr1, $arr2)); // [1, 2, 3, 4]"),
            "join()": ("Fusionne tous les éléments d'un tableau en une seule chaîne.", "$arr = [1, 2, 3]; echo implode('-', $arr); // '1-2-3'"),
            "indexOf()": ("Retourne la première position où un élément se trouve.", "$arr = [1, 2, 3]; echo array_search(2, $arr); // 1"),
            "find()": ("Retourne le premier élément trouvé qui passe un test (implémentation manuelle).", "$arr = [1, 2, 3]; $found = null; foreach ($arr as $x) { if ($x > 2) { $found = $x; break; } } echo $found; // 3"),
            "sort()": ("Trie les éléments d'un tableau.", "$arr = [3, 1, 2]; sort($arr); print_r($arr); // [1, 2, 3]"),
            "reverse()": ("Inverse l'ordre des éléments d'un tableau.", "$arr = [1, 2, 3]; $reversed_arr = array_reverse($arr); print_r($reversed_arr); // [3, 2, 1]"),
            "slice()": ("Extrait une portion d'un tableau.", "$arr = [1, 2, 3, 4]; print_r(array_slice($arr, 1, 2)); // [2, 3]"),
            "splice()": ("Modifie un tableau en ajoutant ou supprimant des éléments.", "$arr = [1, 2, 3]; array_splice($arr, 1, 1, 4); print_r($arr); // [1, 4, 3]"),
            "some()": ("Teste si au moins un élément du tableau passe un test (implémentation manuelle).", "$arr = [1, 2, 3]; $result = false; foreach ($arr as $x) { if ($x > 2) { $result = true; break; } } var_dump($result); // true"),
            "every()": ("Teste si tous les éléments du tableau passent un test (implémentation manuelle).", "$arr = [1, 2, 3]; $result = true; foreach ($arr as $x) { if (!($x > 0)) { $result = false; break; } } var_dump($result); // true"),
            "findIndex()": ("Retourne l'index du premier élément trouvé qui passe un test (implémentation manuelle).", "$arr = [1, 2, 3]; $index = -1; foreach ($arr as $key => $x) { if ($x > 2) { $index = $key; break; } } echo $index; // 2"),
            "fill()": ("Remplit un tableau avec une valeur statique.", "$arr = array_fill(0, 3, 0); print_r($arr); // [0, 0, 0]")
        },
        "description": "Le type Array est une structure de données qui contient plusieurs valeurs. En PHP, ce sont des tableaux."
    },
    "Math": {
        "methods": {
            "abs()": ("Retourne la valeur absolue d'un nombre.", "echo abs(-5); // 5"),
            "ceil()": ("Retourne le plus petit entier supérieur ou égal à un nombre.", "echo ceil(4.3); // 5"),
            "floor()": ("Retourne le plus grand entier inférieur ou égal à un nombre.", "echo floor(4.7); // 4"),
            "round()": ("Arrondit un nombre à l'entier le plus proche.", "echo round(4.5); // 5"),
            "max()": ("Retourne le plus grand nombre parmi les arguments.", "echo max(1, 2, 3); // 3"),
            "min()": ("Retourne le plus petit nombre parmi les arguments.", "echo min(1, 2, 3); // 1"),
            "random()": ("Retourne un nombre aléatoire entre 0 et 1 (simulé).", "echo mt_rand() / mt_getrandmax(); // 0.37423345920612966 (exemple)"),
            "pow()": ("Retourne la base élevée à la puissance de l'exposant.", "echo pow(2, 3); // 8"),
            "sqrt()": ("Retourne la racine carrée d'un nombre.", "echo sqrt(16); // 4"),
            "sin()": ("Retourne le sinus d'un angle en radians.", "echo sin(M_PI / 2); // 1"),
            "cos()": ("Retourne le cosinus d'un angle en radians.", "echo cos(M_PI); // -1"),
            "tan()": ("Retourne la tangente d'un angle en radians.", "echo tan(M_PI / 4); // 1"),
            "log()": ("Retourne le logarithme naturel (base e) d'un nombre.", "echo log(10); // 2.302585092994046"),
            "exp()": ("Retourne e élevé à la puissance de x.", "echo exp(1); // 2.718281828459045"),
            "PI": ("La constante pi.", "echo M_PI; // 3.141592653589793"),
            "E": ("La constante e.", "echo M_E; // 2.718281828459045"),
            "atan()": ("Retourne l'arc tangente d'un nombre.", "echo atan(1); // 0.7853981633974483")
        },
        "description": "Les fonctions mathématiques en PHP sont généralement des fonctions globales."
    },
    "Date": {
        "methods": {
            "getDate()": ("Retourne le jour du mois pour une date donnée.", "$date = new DateTime(); echo $date->format('j'); // 25"),
            "getDay()": ("Retourne le jour de la semaine pour une date donnée.", "$date = new DateTime(); echo $date->format('w'); // 2 (mardi, 0 pour dimanche)"),
            "getFullYear()": ("Retourne l'année complète d'une date.", "$date = new DateTime(); echo $date->format('Y'); // 2025"),
            "getHours()": ("Retourne l'heure d'une date.", "$date = new DateTime(); echo $date->format('H'); // 14"),
            "getMinutes()": ("Retourne les minutes d'une date.", "$date = new DateTime(); echo $date->format('i'); // 30"),
            "getSeconds()": ("Retourne les secondes d'une date.", "$date = new DateTime(); echo $date->format('s'); // 45"),
            "getMilliseconds()": ("Retourne les millisecondes d'une date (non directement disponible en PHP DateTime).", "$date = new DateTime(); echo $date->format('v'); // 123 (PHP 7.0+)"),
            "getTime()": ("Retourne le nombre de secondes écoulées depuis le 1er janvier 1970.", "$date = new DateTime(); echo $date->getTimestamp(); // 1640995200"),
            "setDate()": ("Définit le jour du mois pour une date donnée.", "$date = new DateTime(); $date->setDate($date->format('Y'), $date->format('m'), 15); echo $date->format('j'); // 15"),
            "setFullYear()": ("Définit l'année d'une date.", "$date = new DateTime(); $date->setDate(2025, $date->format('m'), $date->format('d')); echo $date->format('Y'); // 2025"),
            "setHours()": ("Définit l'heure d'une date.", "$date = new DateTime(); $date->setTime(10, $date->format('i'), $date->format('s')); echo $date->format('H'); // 10"),
            "setMinutes()": ("Définit les minutes d'une date.", "$date = new DateTime(); $date->setTime($date->format('H'), 45, $date->format('s')); echo $date->format('i'); // 45"),
            "setSeconds()": ("Définit les secondes d'une date.", "$date = new DateTime(); $date->setTime($date->format('H'), $date->format('i'), 30); echo $date->format('s'); // 30"),
            "toISOString()": ("Retourne une chaîne représentant la date au format ISO.", "$date = new DateTime(); echo $date->format(DateTime::ISO8601); // '2025-07-25T12:30:45+0000'"),
            "toLocaleDateString()": ("Retourne la date sous forme de chaîne au format local.", "$date = new DateTime(); echo $date->format('d/m/Y'); // '25/07/2025'"),
            "toLocaleString()": ("Retourne la date et l'heure au format local.", "$date = new DateTime(); echo $date->format('d/m/Y, H:i:s'); // '25/07/2025, 12:30:45'"),
            "toUTCString()": ("Retourne la date sous forme de chaîne en format UTC.", "$date = new DateTime(); $date->setTimezone(new DateTimeZone('UTC')); echo $date->format('D, d M Y H:i:s T'); // 'Fri, 25 Jul 2025 12:30:45 GMT'")
        },
        "description": "L'objet DateTime en PHP permet de manipuler les dates et les heures."
    },
    "Number": {
        "methods": {
            "toString()": ("Retourne une chaîne représentant le nombre.", "$num = 123; echo (string)$num; // '123'"),
            "toFixed()": ("Formate un nombre en une chaîne avec un nombre fixe de décimales.", "$num = 3.14159; echo number_format($num, 2); // '3.14'"),
            "toPrecision()": ("Formate un nombre en une chaîne avec une précision spécifiée (simulé).", "$num = 12345.6789; echo sprintf('%.4G', $num); // '1.235E+4' (proche, mais pas identique)"),
            "isInteger()": ("Vérifie si une valeur est un entier.", "var_dump(is_int(4)); // true"),
            "isNaN()": ("Vérifie si une valeur est NaN (Not-a-Number).", "var_dump(is_nan(acos(8))); // true"),
            "parseFloat()": ("Analyse une chaîne et retourne un nombre à virgule flottante.", "$str = '3.14'; echo floatval($str); // 3.14"),
            "parseInt()": ("Analyse une chaîne et retourne un entier.", "$str = '10px'; echo intval($str); // 10"),
            "MAX_VALUE": ("Retourne la valeur maximale qu'un nombre peut prendre.", "echo PHP_FLOAT_MAX; // 1.7976931348623157E+308"),
            "MIN_VALUE": ("Retourne la valeur minimale qu'un nombre peut prendre.", "echo PHP_FLOAT_MIN; // 2.2250738585072E-308"),
            "EPSILON": ("Retourne la différence entre 1 et le plus petit nombre supérieur à 1.", "echo PHP_FLOAT_EPSILON; // 2.220446049250313E-16"),
            "NaN": ("Représente la valeur spéciale Not-a-Number.", "echo NAN; // NAN"),
            "NEGATIVE_INFINITY": ("Représente la valeur négative infinie.", "echo -INF; // -INF"),
            "POSITIVE_INFINITY": ("Représente la valeur positive infinie.", "echo INF; // INF")
        },
        "description": "Le type Number représente les valeurs numériques en PHP."
    },
    "DOM": {
        "methods": {
            "getElementById()": ("Retourne l'élément avec l'ID spécifié (côté serveur, nécessite un parseur DOM).", "$doc = new DOMDocument(); $doc->loadHTML('<html><body><div id=\"myId\"></div></body></html>'); $element = $doc->getElementById('myId');"),
            "createElement()": ("Crée un nouvel élément HTML (côté serveur, avec DOMDocument).", "$doc = new DOMDocument(); $div = $doc->createElement('div');"),
            "appendChild()": ("Ajoute un élément à la fin de la liste des enfants d'un autre élément (côté serveur, avec DOMDocument).", "$parentElement->appendChild($childElement);"),
            "removeChild()": ("Supprime un enfant de l'élément spécifié (côté serveur, avec DOMDocument).", "$parentElement->removeChild($childElement);"),
            "setAttribute()": ("Modifie un attribut d'un élément (côté serveur, avec DOMElement).", "$element->setAttribute('class', 'newClass');"),
            "getAttribute()": ("Retourne la valeur de l'attribut spécifié d'un élément (côté serveur, avec DOMElement).", "$value = $element->getAttribute('class');"),
            "innerHTML": ("Retourne ou définit le contenu HTML d'un élément (côté serveur, avec DOMElement).", "$element->nodeValue = '<p>Hello World</p>'; // Pour du texte, pour du HTML, utiliser un fragment de document."),
            "style": ("Retourne ou définit le style CSS d'un élément (côté serveur, manipulation de l'attribut 'style').", "$element->setAttribute('style', 'color: red;');"),
            "getElementsByTagName()": ("Retourne tous les éléments avec un nom de balise spécifié (côté serveur, avec DOMDocument).", "$elements = $doc->getElementsByTagName('div');")
        },
        "description": "L'interaction avec le DOM en PHP se fait généralement via l'extension DOMDocument pour manipuler des documents XML/HTML côté serveur."
    },
    "Location": {
        "methods": {
            "assign()": ("Redirige le navigateur vers une nouvelle URL.", "header('Location: https://www.example.com'); exit;"),
            "reload()": ("Recharge la page actuelle (redirige vers la même URL).", "header('Location: ' . $_SERVER['REQUEST_URI']); exit;"),
            "replace()": ("Remplace la page actuelle par une nouvelle URL (redirige sans laisser d'entrée dans l'historique du navigateur).", "header('Location: https://www.example.com', true, 303); exit;"),
            "href": ("Retourne l'URL complète de la page.", "echo $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];"),
            "protocol": ("Retourne le protocole de l'URL.", "echo $_SERVER['REQUEST_SCHEME'];"),
            "host": ("Retourne le nom d'hôte et le port de l'URL.", "echo $_SERVER['HTTP_HOST'];"),
            "hostname": ("Retourne le nom d'hôte de l'URL sans le port.", "echo parse_url($_SERVER['HTTP_HOST'], PHP_URL_HOST); // Nécessite un peu plus de parsing"),
            "port": ("Retourne le port de l'URL.", "echo parse_url($_SERVER['HTTP_HOST'], PHP_URL_PORT); // Peut être vide"),
            "pathname": ("Retourne le chemin de l'URL.", "echo parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);"),
            "search": ("Retourne la partie de la requête de l'URL.", "echo parse_url($_SERVER['REQUEST_URI'], PHP_URL_QUERY);")
        },
        "description": "En PHP, les informations de l'URL sont accessibles via la superglobale $_SERVER et les redirections via la fonction header()."
    }
}

def build_listbox(frame, data):
    lb = tk.Listbox(frame, width=40, font=("Consolas", 12))
    for key in data:
        lb.insert(tk.END, key)
    lb.pack(side="left", fill="y", padx=(5, 0), pady=5)
    sb = tk.Scrollbar(frame, orient="vertical", command=lb.yview)
    sb.pack(side="left", fill="y")
    lb.config(yscrollcommand=sb.set)
    return lb

def setup_gui():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = ctk.CTk()
    app.title("Objets et Méthodes JavaScript")

    # Frames
    frame_left = ctk.CTkFrame(app, width=250, height=600)
    frame_right = ctk.CTkFrame(app, width=800, height=600)
    frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
    frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    app.grid_columnconfigure(1, weight=1)

    # Listbox pour les objets JavaScript
    lb_objects = build_listbox(frame_left, objects_js)

    # Zone de texte pour afficher la description et les méthodes
    txt = ctk.CTkTextbox(frame_right, width=800, height=600)
    txt.pack(expand=True, fill="both", padx=5, pady=5)

    def show_desc(event):
        sel = event.widget.get(event.widget.curselection())
        desc = objects_js[sel]["description"]
        methods = objects_js[sel]["methods"]
        
        txt.delete("0.0", tk.END)
        txt.insert(tk.END, f"{sel}:\n{desc}\n\nMéthodes disponibles:\n")
        
        for method, (method_desc, example) in methods.items():
            txt.insert(tk.END, f"- {method}: {method_desc}\nExemple: {example}\n")

    lb_objects.bind("<<ListboxSelect>>", show_desc)

    app.mainloop()

if __name__ == "__main__":
    setup_gui()

