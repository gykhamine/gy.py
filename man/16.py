import customtkinter as ctk
import tkinter as tk

# Liste complète des objets JavaScript et de leurs méthodes (20 fonctions par objet)
objects_js = {
    "String": {
        "methods": {
            "charAt()": ("Retourne le caractère à une position donnée.", "let str = 'Hello'; console.log(str.charAt(1)); // 'e'"),
            "concat()": ("Concatène deux ou plusieurs chaînes.", "let str1 = 'Hello'; let str2 = ' World'; console.log(str1.concat(str2)); // 'Hello World'"),
            "includes()": ("Vérifie si une chaîne contient une autre chaîne.", "let str = 'Hello'; console.log(str.includes('ell')); // true"),
            "indexOf()": ("Retourne la première position où une chaîne se trouve.", "let str = 'Hello'; console.log(str.indexOf('l')); // 2"),
            "replace()": ("Remplace une partie de la chaîne par une autre.", "let str = 'Hello'; console.log(str.replace('l', 'L')); // 'HeLlo'"),
            "slice()": ("Extraire une portion d'une chaîne.", "let str = 'Hello World'; console.log(str.slice(0, 5)); // 'Hello'"),
            "split()": ("Divise une chaîne en un tableau en fonction d'un séparateur.", "let str = 'apple,banana,grape'; console.log(str.split(',')); // ['apple', 'banana', 'grape']"),
            "toLowerCase()": ("Convertit tous les caractères en minuscules.", "let str = 'HELLO'; console.log(str.toLowerCase()); // 'hello'"),
            "toUpperCase()": ("Convertit tous les caractères en majuscules.", "let str = 'hello'; console.log(str.toUpperCase()); // 'HELLO'"),
            "trim()": ("Supprime les espaces au début et à la fin de la chaîne.", "let str = '  Hello  '; console.log(str.trim()); // 'Hello'"),
            "startsWith()": ("Vérifie si une chaîne commence par un certain texte.", "let str = 'Hello'; console.log(str.startsWith('He')); // true"),
            "endsWith()": ("Vérifie si une chaîne se termine par un certain texte.", "let str = 'Hello'; console.log(str.endsWith('lo')); // true"),
            "repeat()": ("Répond une chaîne de caractères plusieurs fois.", "let str = 'Hi'; console.log(str.repeat(3)); // 'HiHiHi'"),
            "charCodeAt()": ("Retourne le code de caractère Unicode à une position donnée.", "let str = 'Hello'; console.log(str.charCodeAt(1)); // 101"),
            "localeCompare()": ("Compare deux chaînes de manière locale.", "let str1 = 'apple'; let str2 = 'banana'; console.log(str1.localeCompare(str2)); // -1"),
            "padStart()": ("Ajoute des caractères au début de la chaîne jusqu'à une longueur spécifiée.", "let str = '5'; console.log(str.padStart(3, '0')); // '005'"),
            "padEnd()": ("Ajoute des caractères à la fin de la chaîne jusqu'à une longueur spécifiée.", "let str = '5'; console.log(str.padEnd(3, '0')); // '500'"),
            "fromCharCode()": ("Crée une chaîne à partir d'une ou plusieurs valeurs de code de caractère.", "console.log(String.fromCharCode(72, 101, 108, 108, 111)); // 'Hello'"),
            "lastIndexOf()": ("Retourne la dernière position où un élément se trouve.", "let str = 'Hello Hello'; console.log(str.lastIndexOf('Hello')); // 6"),
            "match()": ("Cherche une correspondance entre une chaîne et une expression régulière.", "let str = 'Hello'; console.log(str.match(/[a-z]/g)); // ['e', 'l', 'l', 'o']")
        },
        "description": "Le type String représente des chaînes de caractères."
    },
    "Array": {
        "methods": {
            "push()": ("Ajoute un ou plusieurs éléments à la fin d'un tableau.", "let arr = [1, 2]; arr.push(3); console.log(arr); // [1, 2, 3]"),
            "pop()": ("Supprime le dernier élément d'un tableau.", "let arr = [1, 2, 3]; arr.pop(); console.log(arr); // [1, 2]"),
            "shift()": ("Supprime le premier élément d'un tableau.", "let arr = [1, 2, 3]; arr.shift(); console.log(arr); // [2, 3]"),
            "unshift()": ("Ajoute un ou plusieurs éléments au début d'un tableau.", "let arr = [2, 3]; arr.unshift(1); console.log(arr); // [1, 2, 3]"),
            "map()": ("Crée un nouveau tableau avec les résultats de l'appel d'une fonction sur chaque élément.", "let arr = [1, 2, 3]; let result = arr.map(x => x * 2); console.log(result); // [2, 4, 6]"),
            "filter()": ("Crée un nouveau tableau avec tous les éléments qui passent un test.", "let arr = [1, 2, 3, 4]; let result = arr.filter(x => x % 2 === 0); console.log(result); // [2, 4]"),
            "reduce()": ("Applique une fonction sur un accumulateur et chaque élément d'un tableau pour le réduire à une seule valeur.", "let arr = [1, 2, 3]; let sum = arr.reduce((acc, val) => acc + val, 0); console.log(sum); // 6"),
            "forEach()": ("Exécute une fonction sur chaque élément d'un tableau.", "let arr = [1, 2, 3]; arr.forEach(x => console.log(x)); // 1 2 3"),
            "concat()": ("Fusionne deux ou plusieurs tableaux.", "let arr1 = [1, 2]; let arr2 = [3, 4]; console.log(arr1.concat(arr2)); // [1, 2, 3, 4]"),
            "join()": ("Fusionne tous les éléments d'un tableau en une seule chaîne.", "let arr = [1, 2, 3]; console.log(arr.join('-')); // '1-2-3'"),
            "indexOf()": ("Retourne la première position où un élément se trouve.", "let arr = [1, 2, 3]; console.log(arr.indexOf(2)); // 1"),
            "find()": ("Retourne le premier élément trouvé qui passe un test.", "let arr = [1, 2, 3]; console.log(arr.find(x => x > 2)); // 3"),
            "sort()": ("Trie les éléments d'un tableau.", "let arr = [3, 1, 2]; arr.sort(); console.log(arr); // [1, 2, 3]"),
            "reverse()": ("Inverse l'ordre des éléments d'un tableau.", "let arr = [1, 2, 3]; arr.reverse(); console.log(arr); // [3, 2, 1]"),
            "slice()": ("Extraire une portion d'un tableau.", "let arr = [1, 2, 3, 4]; console.log(arr.slice(1, 3)); // [2, 3]"),
            "splice()": ("Modifie un tableau en ajoutant ou supprimant des éléments.", "let arr = [1, 2, 3]; arr.splice(1, 1, 4); console.log(arr); // [1, 4, 3]"),
            "some()": ("Teste si au moins un élément du tableau passe un test.", "let arr = [1, 2, 3]; console.log(arr.some(x => x > 2)); // true"),
            "every()": ("Teste si tous les éléments du tableau passent un test.", "let arr = [1, 2, 3]; console.log(arr.every(x => x > 0)); // true"),
            "findIndex()": ("Retourne l'index du premier élément trouvé qui passe un test.", "let arr = [1, 2, 3]; console.log(arr.findIndex(x => x > 2)); // 2"),
            "fill()": ("Remplie tous les éléments d'un tableau avec une valeur statique.", "let arr = [1, 2, 3]; arr.fill(0); console.log(arr); // [0, 0, 0]")
        },
        "description": "Le type Array est une structure de données qui contient plusieurs valeurs."
    },
    "Math": {
        "methods": {
            "abs()": ("Retourne la valeur absolue d'un nombre.", "console.log(Math.abs(-5)); // 5"),
            "ceil()": ("Retourne le plus petit entier supérieur ou égal à un nombre.", "console.log(Math.ceil(4.3)); // 5"),
            "floor()": ("Retourne le plus grand entier inférieur ou égal à un nombre.", "console.log(Math.floor(4.7)); // 4"),
            "round()": ("Arrondit un nombre à l'entier le plus proche.", "console.log(Math.round(4.5)); // 5"),
            "max()": ("Retourne le plus grand nombre parmi les arguments.", "console.log(Math.max(1, 2, 3)); // 3"),
            "min()": ("Retourne le plus petit nombre parmi les arguments.", "console.log(Math.min(1, 2, 3)); // 1"),
            "random()": ("Retourne un nombre aléatoire entre 0 et 1.", "console.log(Math.random()); // 0.37423345920612966"),
            "pow()": ("Retourne la base élevée à la puissance de l'exposant.", "console.log(Math.pow(2, 3)); // 8"),
            "sqrt()": ("Retourne la racine carrée d'un nombre.", "console.log(Math.sqrt(16)); // 4"),
            "sin()": ("Retourne le sinus d'un angle en radians.", "console.log(Math.sin(Math.PI / 2)); // 1"),
            "cos()": ("Retourne le cosinus d'un angle en radians.", "console.log(Math.cos(Math.PI)); // -1"),
            "tan()": ("Retourne la tangente d'un angle en radians.", "console.log(Math.tan(Math.PI / 4)); // 1"),
            "log()": ("Retourne le logarithme en base e d'un nombre.", "console.log(Math.log(10)); // 2.302585092994046"),
            "exp()": ("Retourne e élevé à la puissance de x.", "console.log(Math.exp(1)); // 2.718281828459045"),
            "PI": ("Retourne la constante pi.", "console.log(Math.PI); // 3.141592653589793"),
            "E": ("Retourne la constante e.", "console.log(Math.E); // 2.718281828459045"),
            "atan()": ("Retourne l'arc tangente d'un nombre.", "console.log(Math.atan(1)); // 0.7853981633974483")
        },
        "description": "L'objet Math fournit des méthodes et des constantes pour des calculs mathématiques."
    },
    "Date": {
        "methods": {
            "getDate()": ("Retourne le jour du mois pour une date donnée.", "let date = new Date(); console.log(date.getDate()); // 25"),
            "getDay()": ("Retourne le jour de la semaine pour une date donnée.", "let date = new Date(); console.log(date.getDay()); // 2 (mardi)"),
            "getFullYear()": ("Retourne l'année complète d'une date.", "let date = new Date(); console.log(date.getFullYear()); // 2025"),
            "getHours()": ("Retourne l'heure d'une date.", "let date = new Date(); console.log(date.getHours()); // 14"),
            "getMinutes()": ("Retourne les minutes d'une date.", "let date = new Date(); console.log(date.getMinutes()); // 30"),
            "getSeconds()": ("Retourne les secondes d'une date.", "let date = new Date(); console.log(date.getSeconds()); // 45"),
            "getMilliseconds()": ("Retourne les millisecondes d'une date.", "let date = new Date(); console.log(date.getMilliseconds()); // 123"),
            "getTime()": ("Retourne le nombre de millisecondes écoulées depuis le 1er janvier 1970.", "let date = new Date(); console.log(date.getTime()); // 1640995200000"),
            "setDate()": ("Définit le jour du mois pour une date donnée.", "let date = new Date(); date.setDate(15); console.log(date.getDate()); // 15"),
            "setFullYear()": ("Définit l'année d'une date.", "let date = new Date(); date.setFullYear(2025); console.log(date.getFullYear()); // 2025"),
            "setHours()": ("Définit l'heure d'une date.", "let date = new Date(); date.setHours(10); console.log(date.getHours()); // 10"),
            "setMinutes()": ("Définit les minutes d'une date.", "let date = new Date(); date.setMinutes(45); console.log(date.getMinutes()); // 45"),
            "setSeconds()": ("Définit les secondes d'une date.", "let date = new Date(); date.setSeconds(30); console.log(date.getSeconds()); // 30"),
            "setMilliseconds()": ("Définit les millisecondes d'une date.", "let date = new Date(); date.setMilliseconds(500); console.log(date.getMilliseconds()); // 500"),
            "toISOString()": ("Retourne une chaîne représentant la date au format ISO.", "let date = new Date(); console.log(date.toISOString()); // '2025-07-25T12:30:45.000Z'"),
            "toLocaleDateString()": ("Retourne la date sous forme de chaîne au format local.", "let date = new Date(); console.log(date.toLocaleDateString()); // '25/07/2025'"),
            "toLocaleString()": ("Retourne la date et l'heure au format local.", "let date = new Date(); console.log(date.toLocaleString()); // '25/07/2025, 12:30:45'"),
            "toUTCString()": ("Retourne la date sous forme de chaîne en format UTC.", "let date = new Date(); console.log(date.toUTCString()); // 'Fri, 25 Jul 2025 12:30:45 GMT'")
        },
        "description": "L'objet Date représente une date et une heure."
    },
    "Number": {
        "methods": {
            "toString()": ("Retourne une chaîne représentant le nombre.", "let num = 123; console.log(num.toString()); // '123'"),
            "toFixed()": ("Formate un nombre en une chaîne avec un nombre fixe de décimales.", "let num = 3.14159; console.log(num.toFixed(2)); // '3.14'"),
            "toPrecision()": ("Formate un nombre en une chaîne avec une précision spécifiée.", "let num = 12345.6789; console.log(num.toPrecision(4)); // '12350'"),
            "isInteger()": ("Vérifie si une valeur est un entier.", "console.log(Number.isInteger(4)); // true"),
            "isNaN()": ("Vérifie si une valeur est NaN (Not-a-Number).", "console.log(Number.isNaN(NaN)); // true"),
            "parseFloat()": ("Analyse une chaîne et retourne un nombre à virgule flottante.", "let str = '3.14'; console.log(Number.parseFloat(str)); // 3.14"),
            "parseInt()": ("Analyse une chaîne et retourne un entier.", "let str = '10px'; console.log(Number.parseInt(str)); // 10"),
            "isSafeInteger()": ("Vérifie si un nombre est un entier sécurisé.", "console.log(Number.isSafeInteger(9007199254740992)); // true"),
            "MAX_VALUE": ("Retourne la valeur maximale qu'un nombre peut prendre.", "console.log(Number.MAX_VALUE); // 1.7976931348623157e+308"),
            "MIN_VALUE": ("Retourne la valeur minimale qu'un nombre peut prendre.", "console.log(Number.MIN_VALUE); // 5e-324"),
            "EPSILON": ("Retourne la différence entre 1 et le plus petit nombre supérieur à 1.", "console.log(Number.EPSILON); // 2.220446049250313e-16"),
            "NaN": ("Représente la valeur spéciale Not-a-Number.", "console.log(Number.NaN); // NaN"),
            "NEGATIVE_INFINITY": ("Représente la valeur négative infinie.", "console.log(Number.NEGATIVE_INFINITY); // -Infinity"),
            "POSITIVE_INFINITY": ("Représente la valeur positive infinie.", "console.log(Number.POSITIVE_INFINITY); // Infinity")
        },
        "description": "Le type Number représente les valeurs numériques."
    },
    "DOM": {
        "methods": {
            "getElementById()": ("Retourne l'élément avec l'ID spécifié.", "let element = document.getElementById('myId');"),
            "querySelector()": ("Retourne le premier élément qui correspond au sélecteur CSS.", "let element = document.querySelector('.myClass');"),
            "querySelectorAll()": ("Retourne tous les éléments qui correspondent au sélecteur CSS.", "let elements = document.querySelectorAll('div');"),
            "createElement()": ("Crée un nouvel élément HTML.", "let div = document.createElement('div');"),
            "appendChild()": ("Ajoute un élément à la fin de la liste des enfants d'un autre élément.", "parentElement.appendChild(childElement);"),
            "removeChild()": ("Supprime un enfant de l'élément spécifié.", "parentElement.removeChild(childElement);"),
            "setAttribute()": ("Modifie un attribut d'un élément.", "element.setAttribute('class', 'newClass');"),
            "getAttribute()": ("Retourne la valeur de l'attribut spécifié d'un élément.", "let value = element.getAttribute('class');"),
            "classList.add()": ("Ajoute une ou plusieurs classes à un élément.", "element.classList.add('newClass');"),
            "classList.remove()": ("Supprime une ou plusieurs classes d'un élément.", "element.classList.remove('oldClass');"),
            "addEventListener()": ("Ajoute un écouteur d'événements à un élément.", "element.addEventListener('click', function() { alert('Clicked!'); });"),
            "removeEventListener()": ("Supprime un écouteur d'événements d'un élément.", "element.removeEventListener('click', function() { alert('Clicked!'); });"),
            "innerHTML": ("Retourne ou définit le contenu HTML d'un élément.", "element.innerHTML = '<p>Hello World</p>';"),
            "style": ("Retourne ou définit le style CSS d'un élément.", "element.style.color = 'red';"),
            "focus()": ("Donne le focus à un élément.", "element.focus();"),
            "blur()": ("Supprime le focus d'un élément.", "element.blur();"),
            "getElementsByClassName()": ("Retourne tous les éléments avec une classe spécifiée.", "let elements = document.getElementsByClassName('myClass');"),
            "getElementsByTagName()": ("Retourne tous les éléments avec un nom de balise spécifié.", "let elements = document.getElementsByTagName('div');"),
            "setTimeout()": ("Exécute une fonction après un certain délai.", "setTimeout(function() { alert('Time is up!'); }, 1000);"),
            "setInterval()": ("Exécute une fonction à intervalles réguliers.", "setInterval(function() { alert('Interval passed!'); }, 1000);")
        },
        "description": "L'objet DOM permet d'interagir avec la structure HTML d'une page web."
    },
    "Location": {
        "methods": {
            "assign()": ("Charge une nouvelle URL.", "window.location.assign('https://www.example.com');"),
            "reload()": ("Recharge la page actuelle.", "window.location.reload();"),
            "replace()": ("Remplace la page actuelle par une nouvelle URL.", "window.location.replace('https://www.example.com');"),
            "href": ("Retourne ou définit l'URL de la page.", "console.log(window.location.href);"),
            "protocol": ("Retourne ou définit le protocole de l'URL.", "console.log(window.location.protocol);"),
            "host": ("Retourne ou définit le nom d'hôte de l'URL.", "console.log(window.location.host);"),
            "hostname": ("Retourne ou définit le nom d'hôte de l'URL sans le port.", "console.log(window.location.hostname);"),
            "port": ("Retourne ou définit le port de l'URL.", "console.log(window.location.port);"),
            "pathname": ("Retourne ou définit le chemin de l'URL.", "console.log(window.location.pathname);"),
            "search": ("Retourne ou définit la partie de la requête de l'URL.", "console.log(window.location.search);"),
            "hash": ("Retourne ou définit le fragment de l'URL.", "console.log(window.location.hash);")
        },
        "description": "L'objet Location permet d'interagir avec l'URL de la page."
    },
    "Event": {
        "methods": {
            "preventDefault()": ("Empêche le comportement par défaut d'un événement.", "event.preventDefault();"),
            "stopPropagation()": ("Empêche la propagation d'un événement à l'élément parent.", "event.stopPropagation();"),
            "initEvent()": ("Initialise un événement.", "let event = new Event('click');"),
            "addEventListener()": ("Ajoute un écouteur d'événements à un élément.", "element.addEventListener('click', function() { alert('Clicked!'); });"),
            "removeEventListener()": ("Supprime un écouteur d'événements d'un élément.", "element.removeEventListener('click', function() { alert('Clicked!'); });"),
            "target": ("Retourne l'élément qui a déclenché l'événement.", "console.log(event.target);")
        },
        "description": "L'objet Event est utilisé pour gérer les événements dans le DOM."
    },
    "Screen": {
        "methods": {
            "width": ("Retourne la largeur de l'écran en pixels.", "console.log(screen.width);"),
            "height": ("Retourne la hauteur de l'écran en pixels.", "console.log(screen.height);"),
            "availWidth": ("Retourne la largeur de l'écran disponible (sans la barre de tâches).", "console.log(screen.availWidth);"),
            "availHeight": ("Retourne la hauteur de l'écran disponible (sans la barre de tâches).", "console.log(screen.availHeight);"),
            "colorDepth": ("Retourne la profondeur de couleur de l'écran.", "console.log(screen.colorDepth);"),
            "pixelDepth": ("Retourne la profondeur des pixels de l'écran.", "console.log(screen.pixelDepth);"),
            "orientation": ("Retourne l'orientation de l'écran.", "console.log(screen.orientation.type);"),
        },
        "description": "L'objet Screen fournit des informations sur la taille et les capacités de l'écran."
    },
    "MediaDevices": {
        "methods": {
            "getUserMedia()": ("Accède aux flux multimédia (caméra, microphone).", "navigator.mediaDevices.getUserMedia({ video: True, audio: True })"),
            "enumerateDevices()": ("Liste tous les périphériques multimédia disponibles.", "navigator.mediaDevices.enumerateDevices()"),
            "getSupportedConstraints()": ("Retourne un objet des contraintes prises en charge par l'API.", "console.log(navigator.mediaDevices.getSupportedConstraints());"),
        },
        "description": "L'objet MediaDevices permet de gérer les périphériques multimédia comme la caméra et le microphone."
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
