import customtkinter as ctk

class JavaScriptExplainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Explorateur JavaScript Avancé avec CTk")
        self.geometry("1000x700")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navigation_frame = ctk.CTkScrollableFrame(self, corner_radius=0, width=200)
        self.navigation_frame.grid(row=0, column=0, sticky="nswe", padx=(10, 0), pady=10)
        self.navigation_frame.grid_rowconfigure(99, weight=1)

        self.content_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.buttons = {}
        self.current_concept_frame = None

        self.create_navigation_buttons()
        self.show_concept("introduction")

    def create_navigation_buttons(self):
        concepts = {
            "introduction": "Introduction",
            "variables": "Variables",
            "fonctions": "Fonctions",
            "conditions": "Conditions",
            "boucles": "Boucles",
            "objets": "Objets",
            "tableaux": "Tableaux",
            "dom": "Le DOM",
            "evenements": "Événements",
            "asynchrone": "Asynchrone",
            "manip_avancee": "Manip. Avancée",
            "erreurs": "Gestion des Erreurs",
            "modules": "Modules (ESM)",
            "closures": "Closures",
            "this_keyword": "Le mot-clé 'this'",
            "heritage_prototypal": "Héritage Prototypal",
            "prog_fonctionnelle": "Prog. Fonctionnelle",
            "decorateurs_mixins": "Décorateurs & Mixins",
            "web_apis": "Web APIs (Fetch, LocalStorage)",
            "strict_mode": "Strict Mode",
            "currying_partial": "Currying & Partial App.",
            "set_map": "Set & Map"
        }

        nav_title = ctk.CTkLabel(self.navigation_frame, text="Concepts JS",
                                 font=ctk.CTkFont(size=22, weight="bold"))
        nav_title.pack(pady=(10, 20), padx=20)


        for i, (key, text) in enumerate(concepts.items()):
            button = ctk.CTkButton(self.navigation_frame, text=text,
                                   command=lambda k=key: self.show_concept(k),
                                   height=40)
            button.pack(pady=5, padx=10, fill="x")
            self.buttons[key] = button

    def show_concept(self, concept_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.content_frame._parent_canvas.yview_moveto(0)

        concept_display_functions = {
            "introduction": self.display_introduction,
            "variables": self.display_variables,
            "fonctions": self.display_fonctions,
            "conditions": self.display_conditions,
            "boucles": self.display_boucles,
            "objets": self.display_objets,
            "tableaux": self.display_tableaux,
            "dom": self.display_dom,
            "evenements": self.display_evenements,
            "asynchrone": self.display_asynchronous,
            "manip_avancee": self.display_advanced_manipulation,
            "erreurs": self.display_error_handling,
            "modules": self.display_modules,
            "closures": self.display_closures,
            "this_keyword": self.display_this_keyword,
            "heritage_prototypal": self.display_heritage_prototypal,
            "prog_fonctionnelle": self.display_prog_fonctionnelle,
            "decorateurs_mixins": self.display_decorateurs_mixins,
            "web_apis": self.display_web_apis,
            "strict_mode": self.display_strict_mode,
            "currying_partial": self.display_currying_partial,
            "set_map": self.display_set_map
        }

        if concept_name in concept_display_functions:
            concept_display_functions[concept_name]()
        else:
            self.add_concept_section("Concept Non Trouvé", "Cette section est en cours de développement ou n'existe pas.")


    def add_concept_section(self, title, description, code_example=None):
        title_label = ctk.CTkLabel(self.content_frame, text=title,
                                   font=ctk.CTkFont(size=22, weight="bold"),
                                   wraplength=750, justify="left")
        title_label.pack(pady=(15, 8), anchor="w", padx=20)

        desc_label = ctk.CTkLabel(self.content_frame, text=description,
                                  wraplength=750, justify="left",
                                  font=ctk.CTkFont(size=14))
        desc_label.pack(pady=(0, 15), anchor="w", padx=20)

        if code_example:
            code_title = ctk.CTkLabel(self.content_frame, text="Exemple de Code:",
                                      font=ctk.CTkFont(size=16, weight="bold"))
            code_title.pack(pady=(10, 5), anchor="w", padx=20)

            code_frame = ctk.CTkFrame(self.content_frame, fg_color="#2b2b2b", corner_radius=8, border_width=1, border_color="#555555")
            code_frame.pack(fill="x", padx=20, pady=5, ipadx=5, ipady=5)
            code_label = ctk.CTkLabel(code_frame, text=code_example,
                                      font=ctk.CTkFont("Consolas", size=13),
                                      text_color="#9FE85A",
                                      justify="left")
            code_label.pack(fill="both", expand=True, padx=10, pady=10, anchor="w")

    # --- Fonctions d'affichage des concepts (enrichies) ---

    def display_introduction(self):
        self.add_concept_section(
            "Introduction à JavaScript : Le Langage du Web Interactif",
            "**JavaScript (JS)** est un **langage de programmation de script léger et dynamique**, principalement connu comme le langage de programmation des pages web. C'est le seul langage de programmation qui s'exécute nativement dans **tous les navigateurs web majeurs**, le rendant indispensable pour donner vie à l'interface utilisateur. Au-delà du navigateur, grâce à des environnements comme **Node.js**, JavaScript est devenu un langage **full-stack**, utilisé pour le développement de serveurs, d'applications mobiles (avec React Native) et même d'applications de bureau (avec Electron).",
            """
// Un simple script JavaScript dans le navigateur
console.log("Bonjour le monde !"); // Affiche un message dans la console du navigateur

// Interagir avec le HTML (DOM Manipulation)
// document.getElementById("monBouton").addEventListener("click", function() {
//     alert("Bouton cliqué !");
// });

// JavaScript côté serveur (Node.js)
// const http = require('http');
// http.createServer((req, res) => {
//     res.writeHead(200, {'Content-Type': 'text/plain'});
//     res.end('Hello Node.js !\\n');
// }).listen(3000);
// console.log('Serveur Node.js démarré sur le port 3000');
            """
        )
        self.add_concept_section(
            "Pourquoi JavaScript est-il si Populaire et Important ?",
            "1.  **Omniprésence :** Il est partout où il y a un navigateur web, et son écosystème s'étend au-delà.\n2.  **Facilité d'apprentissage :** Sa syntaxe est relativement simple pour les débutants.\n3.  **Écosystème vaste :** Des frameworks et bibliothèques puissants comme **React**, **Angular**, **Vue.js** pour le frontend, et **Express.js** pour le backend, accélèrent considérablement le développement.\n4.  **Communauté immense :** Une communauté active signifie des tonnes de ressources, de tutoriels et de support.\n5.  **Polyvalence :** La capacité à travailler à la fois côté client et côté serveur avec un seul langage (full-stack) est un avantage majeur."
        )

    def display_variables(self):
        self.add_concept_section(
            "Variables en JavaScript : Stockage et Portée des Données",
            "Les variables sont des conteneurs nommés utilisés pour stocker des valeurs. JavaScript est un **langage à typage dynamique**, ce qui signifie que vous n'avez pas besoin de spécifier le type de données d'une variable lors de sa déclaration ; le type est déterminé au moment de l'exécution et peut changer. Il existe trois mots-clés principaux pour déclarer des variables, chacun avec des règles de **portée (scope)** et de **mutabilité** distinctes.",
            """
// 1. 'var' (avant ES6) : Portée fonctionnelle et Hoisting
// 'var' est associé au hoisting (déplacement des déclarations en haut de leur portée),
// ce qui peut entraîner des comportements inattendus et des bugs si mal compris.
var maVariableVar = "Je suis globale";
if (true) {
    var maVariableVar = "Je suis réassignée"; // Redéclaration possible, écrasant la précédente
    console.log(maVariableVar); // Je suis réassignée
}
console.log(maVariableVar); // Je suis réassignée (la portée est la fonction entière, pas le bloc if)

// 2. 'let' (ES6+) : Portée par bloc et pas de redéclaration
// 'let' est la façon recommandée de déclarer des variables qui seront réassignées.
let maVariableLet = 10;
if (true) {
    let maVariableLet = 20; // Ceci est une nouvelle variable locale au bloc 'if'
    console.log(maVariableLet); // 20
}
console.log(maVariableLet); // 10 (la variable externe n'a pas été affectée)

// 3. 'const' (ES6+) : Portée par bloc et valeur constante (non réassignable)
// 'const' est idéal pour les valeurs qui ne changeront jamais.
const maConstante = "Valeur Initiale";
// maConstante = "Nouvelle Valeur"; // Erreur : Assignment to constant variable.

const monObjet = { a: 1 };
monObjet.a = 2; // OK : on modifie la propriété de l'objet, pas la référence de l'objet lui-même.
console.log(monObjet); // { a: 2 }
// const monObjet = { b: 3 }; // Erreur : Identifiant 'monObjet' a déjà été déclaré.
            """
        )
        self.add_concept_section(
            "Types de Données Primitifs et Objets",
            "JavaScript gère différents types de données. Comprendre la distinction entre **types primitifs (immuables)** et **types objets (mutables)** est fondamental pour éviter des surprises.",
            """
// Types Primitifs (copiés par valeur)
let nombre = 123;         // number (nombres entiers et flottants)
let chaine = "Salut !";   // string (texte)
let bool = true;          // boolean (true ou false)
let undef = undefined;    // undefined (variable déclarée mais sans valeur attribuée)
let nul = null;           // null (absence intentionnelle de valeur, un 'bug' historique fait que typeof null est 'object')
let symbole = Symbol('id'); // symbol (identificateurs uniques, ES6+)
let bigInt = 10n;         // bigint (pour des nombres entiers très grands, ES2020+)

let a = 10;
let b = a;
b = 20;
console.log(a); // 10 (la valeur de 'a' n'est pas affectée)

// Types Objets / Non-Primitifs (copiés par référence)
let obj1 = { nom: "Alice" }; // object (objets littéraux)
let arr1 = [1, 2, 3];        // object (les tableaux sont un type d'objet)
let func1 = function() {};   // function (les fonctions sont aussi des objets)

let c = obj1;
c.nom = "Bob";
console.log(obj1.nom); // Bob (la référence a été copiée, donc les deux pointent vers le même objet)
            """
        )

    def display_fonctions(self):
        self.add_concept_section(
            "Fonctions : Les Bâtisseurs de Code Réutilisable et Organisé",
            "Les **fonctions** sont des blocs de code conçus pour effectuer une tâche spécifique. Elles sont le moyen fondamental d'organiser et de réutiliser le code en JavaScript. Les fonctions peuvent accepter des **arguments (paramètres d'entrée)** et **retourner une valeur**. Elles sont des 'citoyens de première classe' en JS, ce qui signifie qu'elles peuvent être traitées comme n'importe quelle autre valeur : stockées dans des variables, passées en arguments, ou retournées par d'autres fonctions.",
            """
// 1. Déclaration de fonction (Function Declaration)
// C'est la façon la plus courante de définir une fonction. Elles sont 'hoistées'.
function saluer(nom) {
    return `Bonjour, ${nom} ! Comment vas-tu ?`;
}
console.log(saluer("Marc")); // Bonjour, Marc ! Comment vas-tu ?

// 2. Expression de fonction (Function Expression)
// La fonction est assignée à une variable. Elle n'est pas 'hoistée' de la même manière.
const addition = function(a, b) {
    return a + b;
};
console.log(addition(10, 5)); // 15

// 3. Fonctions Fléchées (Arrow Functions) - ES6+
// Une syntaxe plus concise, surtout utile pour les fonctions anonymes et les callbacks.
// Elles ont un comportement différent pour le mot-clé 'this'.
const soustraction = (x, y) => x - y; // Retour implicite si une seule expression
console.log(soustraction(20, 7)); // 13

const direMessage = () => { // Bloc de code avec retour explicite
    console.log("Ceci est un message d'une fonction fléchée.");
};
direMessage();

// Une fonction fléchée avec un seul paramètre n'a pas besoin de parenthèses autour du paramètre
const carre = n => n * n;
console.log(carre(9)); // 81

// 4. Paramètres par Défaut (ES6+)
// Permet de définir une valeur par défaut pour un paramètre si aucun argument n'est fourni.
function saluerAvecDefaut(nom = "visiteur") {
    return `Bienvenue, ${nom} !`;
}
console.log(saluerAvecDefaut());      // Bienvenue, visiteur !
console.log(saluerAvecDefaut("Anna")); // Bienvenue, Anna !
            """
        )
        self.add_concept_section(
            "Portée (Scope) et Hoisting des Fonctions",
            "Les fonctions créent leur propre portée lexicale (locale). Les variables déclarées à l'intérieur d'une fonction sont locales à cette fonction et ne sont pas accessibles de l'extérieur. Le **hoisting** est le comportement de JavaScript qui 'déplace' les déclarations (pas les initialisations) de variables et de fonctions au début de leur portée. Les déclarations de fonctions sont entièrement hoistées, tandis que les expressions de fonctions ne le sont pas (seule la variable est hoistée, pas l'assignation de la fonction).",
            """
// Exemple de Hoisting
direBonjour(); // Fonctionne, car la déclaration de fonction est hoistée
function direBonjour() {
    console.log("Salut !");
}

// erreurDireBonjour(); // Erreur : erreurDireBonjour n'est pas une fonction (car c'est une expression)
const erreurDireBonjour = function() {
    console.log("Ceci ne fonctionnera pas avant la définition.");
};
erreurDireBonjour(); // Fonctionne ici
            """
        )

    def display_conditions(self):
        self.add_concept_section(
            "Structures Conditionnelles : La Prise de Décision dans votre Code",
            "Les **structures conditionnelles** permettent à votre programme d'exécuter différents blocs de code en fonction de l'évaluation de conditions (expressions booléennes). C'est le fondement de la logique et de la capacité d'un programme à s'adapter à diverses situations.",
            """
let age = 19;

// 1. `if`, `else if`, `else` : La structure conditionnelle la plus courante
if (age < 13) {
    console.log("Vous êtes un enfant.");
} else if (age < 18) {
    console.log("Vous êtes un adolescent.");
} else if (age < 65) {
    console.log("Vous êtes un adulte.");
} else {
    console.log("Vous êtes un senior.");
}

// 2. Opérateur Ternaire (`condition ? valeurSiVrai : valeurSiFaux`)
// Une forme concise pour les conditions simples qui retournent une valeur.
let statut = (age >= 18) ? "Majeur" : "Mineur";
console.log(`Statut : ${statut}`); // Statut : Majeur

let prix = 100;
let remise = (prix > 50) ? 0.10 : 0; // 10% de remise si prix > 50
let prixFinal = prix * (1 - remise);
console.log(`Prix final avec remise : ${prixFinal}`); // 90
            """
        )
        self.add_concept_section(
            "`switch` Statement : Choisir parmi Plusieurs Options Fixes",
            "Le `switch` est une alternative aux longues chaînes de `if...else if` lorsque vous avez une seule expression à comparer à plusieurs valeurs possibles. Il est souvent plus lisible pour ce type de scénario.",
            """
let jourDeSemaine = 3; // 1=Lundi, 2=Mardi, etc.
let nomDuJour;

switch (jourDeSemaine) {
    case 1:
        nomDuJour = "Lundi";
        break; // Important : arrête l'exécution après ce 'case'
    case 2:
        nomDuJour = "Mardi";
        break;
    case 3:
        nomDuJour = "Mercredi";
        break;
    case 4:
        nomDuJour = "Jeudi";
        break;
    case 5:
        nomDuJour = "Vendredi";
        break;
    default: // Exécuté si aucune des correspondances précédentes n'est trouvée
        nomDuJour = "Weekend ou jour invalide";
}
console.log(`Aujourd'hui, c'est ${nomDuJour}.`); // Aujourd'hui, c'est Mercredi.

// Groupement de 'case' (pas de 'break')
let fruit = "pomme";
switch (fruit) {
    case "pomme":
    case "banane":
        console.log("Ceci est un fruit commun.");
        break;
    case "mangue":
        console.log("Ceci est un fruit tropical.");
        break;
    default:
        console.log("Fruit inconnu.");
}
            """
        )

    def display_boucles(self):
        self.add_concept_section(
            "Boucles : Automatiser les Tâches Répétitives",
            "Les **boucles** sont des structures de contrôle qui permettent d'exécuter un bloc de code plusieurs fois. Elles sont essentielles pour automatiser les tâches, itérer sur des collections de données (tableaux, objets) et répéter des actions jusqu'à ce qu'une condition spécifique soit remplie ou qu'une collection soit épuisée.",
            """
// 1. `for` Loop : Idéale lorsque le nombre d'itérations est connu
// Syntaxe: for (initialisation; condition; incrémentation/décrémentation)
for (let i = 0; i < 5; i++) {
    console.log(`Itération 'for' numéro : ${i}`); // Affiche 0, 1, 2, 3, 4
}

// 2. `while` Loop : Continue tant qu'une condition est vraie
// Idéale lorsque le nombre d'itérations est inconnu à l'avance.
let compteurWhile = 0;
while (compteurWhile < 3) {
    console.log(`Itération 'while' numéro : ${compteurWhile}`);
    compteurWhile++; // N'oubliez pas d'incrémenter pour éviter une boucle infinie !
}
// Affiche 0, 1, 2

// 3. `do...while` Loop : Exécute le bloc au moins une fois, puis vérifie la condition
// La condition est évaluée après la première exécution.
let x = 0;
do {
    console.log(`Itération 'do-while' numéro : ${x}`);
    x++;
} while (x < 1); // Affiche 0 (s'exécute une fois même si x n'était pas < 1 au départ)
            """
        )
        self.add_concept_section(
            "Boucles pour Itérer sur des Collections (Tableaux et Objets)",
            "JavaScript offre des boucles spécialisées pour travailler avec des tableaux et des objets, rendant le code plus concis et expressif.",
            """
const couleurs = ["rouge", "vert", "bleu", "jaune"];
const utilisateur = { nom: "Léa", age: 25, ville: "Nice" };

// 4. `for...of` Loop (ES6+) : Itère sur les VALEURS d'un itérable (Tableaux, String, Map, Set)
// C'est la boucle préférée pour les tableaux.
for (const couleur of couleurs) {
    console.log(`Couleur : ${couleur}`);
}
// Affiche: "rouge", "vert", "bleu", "jaune"

// 5. `forEach` Method (pour les Tableaux) : Exécute une fonction de rappel pour chaque élément
// Ne peut pas être interrompue avec 'break' ou 'continue'.
couleurs.forEach(function(couleur, index) {
    console.log(`L'élément à l'index ${index} est : ${couleur}`);
});

// 6. `for...in` Loop : Itère sur les PROPRIÉTÉS/CLÉS d'un objet (et indices de tableaux)
// Moins recommandé pour les tableaux car il itère sur les clés/indices en tant que chaînes.
for (const cle in utilisateur) {
    console.log(`${cle}: ${utilisateur[cle]}`);
}
// Affiche:
// nom: Léa
// age: 25
// ville: Nice

// Précautions avec `for...in` :
// Il peut aussi itérer sur des propriétés héritées de la chaîne de prototype.
// Il est souvent préférable de l'utiliser avec `hasOwnProperty` pour éviter les propriétés héritées.
for (const cle in utilisateur) {
    if (Object.prototype.hasOwnProperty.call(utilisateur, cle)) {
        console.log(`${cle}: ${utilisateur[cle]}`);
    }
}
            """
        )

    def display_objets(self):
        self.add_concept_section(
            "Objets en JavaScript : La Base de Toute Structure Complexe",
            "Les **objets** sont des collections de paires **clé-valeur** (ou nom-valeur). Ils sont le type de données fondamental le plus important en JavaScript pour représenter des entités complexes et regrouper des données et des fonctionnalités associées. Presque tout en JavaScript est un objet ou se comporte comme un objet.",
            """
// 1. Création d'un objet littéral (la méthode la plus courante)
const personne = {
    nom: "Dupont",
    prenom: "Sophie",
    age: 30,
    estEtudiant: false,
    adresse: { // Un objet peut contenir d'autres objets
        rue: "10 Rue de la Paix",
        ville: "Paris",
        codePostal: "75001"
    },
    interets: ["lecture", "randonnée", "programmation"], // Un tableau
    saluer: function() { // Une méthode (fonction attachée à l'objet)
        return `Bonjour, je m'appelle ${this.prenom} ${this.nom}.`;
    },
    // Syntaxe de méthode raccourcie (ES6+)
    presenter() {
        console.log(`J'ai ${this.age} ans et j'habite à ${this.adresse.ville}.`);
    }
};

// Accéder aux propriétés d'un objet
console.log(personne.nom);         // Dupont (notation pointée)
console.log(personne['age']);      // 30 (notation crochets, utile si la clé est dynamique ou contient des espaces/caractères spéciaux)
console.log(personne.adresse.ville); // Paris

// Modifier les propriétés
personne.age = 31;
console.log(personne.age); // 31

// Ajouter de nouvelles propriétés
personne.email = "sophie.dupont@example.com";
console.log(personne.email);

// Appeler une méthode
console.log(personne.saluer()); // Bonjour, je m'appelle Sophie Dupont.
personne.presenter();           // J'ai 31 ans et j'habite à Paris.

// Supprimer une propriété
delete personne.estEtudiant;
console.log(personne.estEtudiant); // undefined
            """
        )
        self.add_concept_section(
            "Constructeurs, Classes et Prototypes : Créer des Objets Structurés",
            "Pour créer plusieurs objets du même type, JavaScript utilise des **fonctions constructeurs** ou des **classes (ES6+)**. En coulisses, ces mécanismes reposent sur l'**héritage prototypal**.",
            """
// 2. Fonction Constructeur (approche 'avant ES6')
function Livre(titre, auteur, annee) {
    this.titre = titre;
    this.auteur = auteur;
    this.annee = annee;
    this.getInfos = function() {
        return `${this.titre} par ${this.auteur} (${this.annee})`;
    };
}
const livre1 = new Livre("Le Petit Prince", "Antoine de Saint-Exupéry", 1943);
const livre2 = new Livre("1984", "George Orwell", 1949);
console.log(livre1.getInfos());
console.log(livre2.getInfos());

// Les méthodes devraient être sur le prototype pour l'efficacité mémoire
function LivreOpti(titre, auteur) {
    this.titre = titre;
    this.auteur = auteur;
}
LivreOpti.prototype.getInfos = function() { // Ajout de la méthode au prototype
    return `${this.titre} par ${this.auteur}`;
};
const livre3 = new LivreOpti("Dune", "Frank Herbert");
console.log(livre3.getInfos());

// 3. Classes (ES6+) : Syntaxe plus moderne et 'syntaxic sugar' pour les prototypes
class Voiture {
    constructor(marque, modele, annee) {
        this.marque = marque;
        this.modele = modele;
        this.annee = annee;
    }
    afficherDetails() {
        return `Voiture: ${this.marque} ${this.modele} (${this.annee})`;
    }
}
const maVoiture = new Voiture("Renault", "Clio", 2022);
console.log(maVoiture.afficherDetails());

// Héritage de Classes (`extends` et `super`)
class Camion extends Voiture {
    constructor(marque, modele, annee, capacite) {
        super(marque, modele, annee); // Appelle le constructeur de la classe parent (Voiture)
        this.capacite = capacite;
    }
    afficherDetails() {
        // Surcharge la méthode parentale
        return `${super.afficherDetails()} avec ${this.capacite} tonnes de capacité.`;
    }
}
const monCamion = new Camion("Volvo", "FH16", 2023, 40);
console.log(monCamion.afficherDetails());
            """
        )

    def display_tableaux(self):
        self.add_concept_section(
            "Tableaux (Arrays) : Gérer des Collections de Données Ordonnées",
            "Les **tableaux** en JavaScript sont des objets spéciaux qui vous permettent de stocker des **collections ordonnées d'éléments**. Ces éléments peuvent être de n'importe quel type de données (nombres, chaînes, objets, autres tableaux, etc.), et même un mélange de types. Les éléments d'un tableau sont accessibles par leur **index numérique**, qui commence toujours à **0**.",
            """
// 1. Création d'un tableau
const fruits = ["pomme", "banane", "cerise", "mangue"]; // Tableau littéral (le plus courant)
const nombres = new Array(1, 2, 3);                 // Utilisation du constructeur Array (moins courant)
const vide = [];                                    // Tableau vide

console.log(fruits); // ["pomme", "banane", "cerise", "mangue"]
console.log(fruits.length); // 4 (nombre d'éléments)

// 2. Accéder aux éléments
console.log(fruits[0]); // "pomme" (premier élément)
console.log(fruits[2]); // "cerise"
console.log(fruits[fruits.length - 1]); // "mangue" (dernier élément)

// 3. Modifier un élément
fruits[1] = "kiwi";
console.log(fruits); // ["pomme", "kiwi", "cerise", "mangue"]

// 4. Ajouter des éléments
fruits.push("orange"); // Ajoute 'orange' à la fin du tableau
console.log(fruits); // ["pomme", "kiwi", "cerise", "mangue", "orange"]

fruits.unshift("ananas"); // Ajoute 'ananas' au début du tableau
console.log(fruits); // ["ananas", "pomme", "kiwi", "cerise", "mangue", "orange"]

// 5. Supprimer des éléments
const dernierFruit = fruits.pop(); // Supprime et retourne le dernier élément ("orange")
console.log(fruits);       // ["ananas", "pomme", "kiwi", "cerise", "mangue"]
console.log(dernierFruit); // "orange"

const premierFruit = fruits.shift(); // Supprime et retourne le premier élément ("ananas")
console.log(fruits);         // ["pomme", "kiwi", "cerise", "mangue"]
console.log(premierFruit);   // "ananas"

// `splice()` : Méthode puissante pour ajouter/supprimer à n'importe quel index
// `array.splice(startIndex, deleteCount, item1, item2, ...)`
fruits.splice(1, 1, "raisin", "figue"); // À l'index 1, supprime 1 élément, ajoute "raisin", "figue"
console.log(fruits); // ["pomme", "raisin", "figue", "cerise", "mangue"]
            """
        )
        self.add_concept_section(
            "Méthodes d'Itération et de Transformation des Tableaux (FP)",
            "Les tableaux disposent de nombreuses méthodes intégrées qui simplifient les opérations courantes d'itération, de recherche et de transformation, en s'appuyant souvent sur des principes de programmation fonctionnelle (retournent de nouveaux tableaux sans modifier l'original).",
            """
const produits = [
    { id: 1, nom: "Ordinateur", prix: 1200 },
    { id: 2, nom: "Souris", prix: 25 },
    { id: 3, nom: "Clavier", prix: 75 }
];

// 6. `forEach()` : Exécute une fonction pour chaque élément (pas de retour)
produits.forEach(produit => console.log(`Nom: ${produit.nom}, Prix: ${produit.prix}`));

// 7. `map()` : Crée un NOUVEAU tableau en appliquant une fonction à chaque élément
const nomsProduits = produits.map(produit => produit.nom);
console.log(nomsProduits); // ["Ordinateur", "Souris", "Clavier"]

// 8. `filter()` : Crée un NOUVEAU tableau avec les éléments qui passent une condition
const produitsChers = produits.filter(produit => produit.prix > 50);
console.log(produitsChers); // [{ id: 1, nom: "Ordinateur", prix: 1200 }, { id: 3, nom: "Clavier", prix: 75 }]

// 9. `reduce()` : Réduit le tableau à une seule valeur
const prixTotal = produits.reduce((accumulateur, produit) => accumulateur + produit.prix, 0); // 0 est la valeur initiale
console.log(prixTotal); // 1300

// 10. `find()` : Retourne le PREMIER élément qui satisfait la condition, ou undefined
const souris = produits.find(produit => produit.nom === "Souris");
console.log(souris); // { id: 2, nom: "Souris", prix: 25 }

// 11. `findIndex()` : Retourne l'INDEX du premier élément qui satisfait la condition, ou -1
const indexClavier = produits.findIndex(produit => produit.nom === "Clavier");
console.log(indexClavier); // 2

// 12. `some()` / `every()` : Vérifient si AU MOINS UN / TOUS les éléments satisfont une condition
const aDesProduitsChers = produits.some(produit => produit.prix > 1000); // true
const tousLesProduitsSontChers = produits.every(produit => produit.prix > 1000); // false
console.log(aDesProduitsChers, tousLesProduitsSontChers);
            """
        )

    def display_dom(self):
        self.add_concept_section(
            "Le DOM (Document Object Model) : L'Interface de Votre Page Web",
            "Le **DOM** est une **interface de programmation pour les documents HTML et XML**. Il représente la structure d'une page web comme une arborescence de nœuds, où chaque nœud est un objet représentant une partie du document (un élément, un attribut, un texte, etc.). JavaScript interagit avec le DOM pour **lire, modifier, ajouter ou supprimer** le contenu, la structure et le style des pages web, rendant les pages dynamiques et interactives.",
            """
"""
        )
        self.add_concept_section(
            "Sélectionner des Éléments : Trouver sa Cible dans le DOM",
            "Avant de pouvoir manipuler un élément HTML, vous devez d'abord le **sélectionner** (le trouver) dans l'arborescence DOM. JavaScript offre plusieurs méthodes pour cela.",
            """
// 1. `document.getElementById('id')` : Sélectionne un seul élément par son ID unique
const mainTitle = document.getElementById('mainTitle');
console.log(mainTitle.textContent); // "Bienvenue"

// 2. `document.getElementsByClassName('class')` : Sélectionne tous les éléments par leur classe
// Retourne une HTMLCollection (qui ressemble à un tableau, mais n'est pas un Array réel)
const introTexts = document.getElementsByClassName('intro-text');
console.log(introTexts[0].textContent); // "Ceci est un paragraphe introductif."

// 3. `document.getElementsByTagName('tagname')` : Sélectionne tous les éléments par leur nom de balise
const paragraphs = document.getElementsByTagName('p');
console.log(paragraphs.length); // 2 (dans l'exemple HTML ci-dessus)

// 4. `document.querySelector('CSS_selector')` : Sélectionne le PREMIER élément correspondant à un sélecteur CSS
const firstParagraph = document.querySelector('.intro-text');
console.log(firstParagraph.textContent);

const anyElementWithId = document.querySelector('#mainTitle'); // Peut aussi utiliser l'ID
console.log(anyElementWithId.textContent);

// 5. `document.querySelectorAll('CSS_selector')` : Sélectionne TOUS les éléments correspondant à un sélecteur CSS
// Retourne une NodeList (qui peut être itérée avec forEach, mais n'est pas un Array réel)
const allParagraphs = document.querySelectorAll('p');
allParagraphs.forEach(p => console.log(p.textContent));

const allHighlightElements = document.querySelectorAll('.highlight, #content'); // S'applique à plusieurs sélecteurs
console.log(`Nombre d'éléments en surbrillance ou dans la div 'content': ${allHighlightElements.length}`);
            """
        )
        self.add_concept_section(
            "Manipuler le Contenu, les Attributs et les Styles",
            "Une fois un élément sélectionné, vous pouvez le modifier de diverses manières.",
            """
const title = document.getElementById('mainTitle');
const myButton = document.getElementById('myButton');

// 1. Modifier le Contenu Textuel ou HTML
title.textContent = "Bienvenue sur ma Page Awesome !"; // Modifie le texte pur
// title.innerHTML = "<em>Nouveau</em> Titre <span style='color: orange;'>Dynamique</span>"; // Modifie le HTML interne (attention aux risques XSS)

// 2. Modifier les Attributs
myButton.setAttribute('disabled', 'true'); // Ajoute l'attribut 'disabled'
// myButton.removeAttribute('disabled'); // Supprime l'attribut
// console.log(myButton.getAttribute('id')); // myButton
// console.log(myButton.hasAttribute('disabled')); // true

// 3. Modifier les Styles CSS (inline)
title.style.color = "blue";
title.style.fontSize = "36px";
title.style.backgroundColor = "#e0e0e0"; // Nom de propriété en camelCase pour CSS-hyphenated

// 4. Manipuler les Classes CSS (préférable pour le style)
title.classList.add('new-style');       // Ajoute une classe
// title.classList.remove('old-style');    // Supprime une classe
// title.classList.toggle('active');       // Ajoute/supprime la classe selon sa présence
// console.log(title.classList.contains('highlight')); // true
            """
        )
        self.add_concept_section(
            "Créer, Ajouter et Supprimer des Éléments Dynamiquement",
            "JavaScript permet de construire ou de déconstruire la structure HTML de votre page sans recharger la page.",
            """
const contentDiv = document.getElementById('content');

// 1. Créer un nouvel élément
const newParagraph = document.createElement('p');
newParagraph.textContent = "Ce paragraphe a été ajouté dynamiquement.";
newParagraph.style.fontStyle = "italic";

// 2. Ajouter un élément au DOM
contentDiv.appendChild(newParagraph); // Ajoute à la fin de 'contentDiv'

// Créer et ajouter un élément avec un attribut et du texte
const newLink = document.createElement('a');
newLink.href = "https://developer.mozilla.org/fr/docs/Web/API/Document_Object_Model";
newLink.textContent = "Apprenez-en plus sur le DOM";
newLink.target = "_blank"; // Ouvre dans un nouvel onglet
contentDiv.appendChild(newLink);

// 3. Supprimer un élément
// myButton.remove(); // Supprime le bouton (méthode moderne)
// contentDiv.removeChild(newParagraph); // Méthode plus ancienne (besoin du parent)
            """
        )

    def display_evenements(self):
        self.add_concept_section(
            "Événements en JavaScript : Rendre vos Pages Interactives et Réactives",
            "Les **événements** sont des actions ou des occurrences qui se produisent dans le système (par exemple, un clic de souris, un chargement de page, une touche de clavier pressée, la soumission d'un formulaire, une image qui charge). JavaScript vous permet de 'réagir' à ces événements en exécutant des fonctions spécifiques appelées **gestionnaires d'événements (event handlers)** ou **callbacks d'événements**.",
            """
// Supposons ces éléments HTML pour les exemples :
/*
<button id="myBtn">Clique-moi !</button>
<input type="text" id="myInput" placeholder="Tapez ici...">
<div id="myDiv" style="width:100px; height:100px; background-color: lightblue;"></div>
<form id="myForm">
    <input type="text" name="data">
    <button type="submit">Envoyer</button>
</form>
*/

const myButton = document.getElementById('myBtn');
const myInput = document.getElementById('myInput');
const myDiv = document.getElementById('myDiv');
const myForm = document.getElementById('myForm');

// 1. `addEventListener()` : La méthode préférée pour attacher des événements
// Syntaxe: element.addEventListener(typeEvenement, fonctionDeRappel, [options]);

// Événement de Clic
myButton.addEventListener('click', function() {
    alert("Le bouton a été cliqué !");
    console.log("Clic détecté sur le bouton.");
});

// Événements de Souris (Mouse Events)
myDiv.addEventListener('mouseover', function() {
    myDiv.style.backgroundColor = 'darkblue';
    myDiv.textContent = 'SURVOLÉ';
});
myDiv.addEventListener('mouseout', function() {
    myDiv.style.backgroundColor = 'lightblue';
    myDiv.textContent = '';
});

// Événements de Clavier (Keyboard Events)
myInput.addEventListener('keydown', function(event) { // 'event' objet contient des infos sur l'événement
    console.log(`Touche pressée : ${event.key}, Code : ${event.keyCode}`);
    if (event.key === 'Enter') {
        alert(`Vous avez tapé Enter ! Votre texte : ${myInput.value}`);
    }
});

// Événements de Formulaire (Form Events)
myForm.addEventListener('submit', function(event) {
    event.preventDefault(); // TRÈS IMPORTANT : Empêche le comportement par défaut (rechargement de la page)
    const formData = new FormData(myForm); // Récupère les données du formulaire
    const textValue = formData.get('data');
    console.log("Formulaire soumis. Valeur tapée :", textValue);
    alert("Formulaire soumis !");
});

// 2. Supprimer un écouteur d'événement (`removeEventListener()`)
// Nécessite une référence à la même fonction de rappel.
function handleClickOnce() {
    alert("Cliqué une seule fois !");
    myButton.removeEventListener('click', handleClickOnce);
}
// myButton.addEventListener('click', handleClickOnce); // Décommenter pour tester
            """
        )
        self.add_concept_section(
            "L'Objet `Event` et la Propagation des Événements",
            "Lorsqu'un événement se produit, un **objet `Event`** est automatiquement créé et passé comme premier argument à votre fonction de rappel. Cet objet contient toutes les informations pertinentes sur l'événement (type, cible, coordonnées, touche pressée, etc.).",
            """
/* Propagation des Événements (Event Bubbling & Capturing) */
// Lorsque un événement se produit sur un élément, il 'bulle' (bubbling) vers le haut
// de l'arborescence DOM jusqu'au document. Vous pouvez aussi le 'capturer' (capturing)
// lors de sa descente depuis le document.

// HTML : <div id="parent"><button id="child">Clique</button></div>

// const parentDiv = document.getElementById('parent');
// const childButton = document.getElementById('child');

// parentDiv.addEventListener('click', function() {
//     console.log("Clic sur le div parent");
// });

// childButton.addEventListener('click', function(event) {
//     console.log("Clic sur le bouton enfant");
//     // event.stopPropagation(); // Empêche l'événement de remonter au parent
// });

// // Par défaut, 'bubbling' se produit : "Clic sur le bouton enfant", puis "Clic sur le div parent"
// // Si stopPropagation() est activé : "Clic sur le bouton enfant" seulement.
            """
        )

    def display_asynchronous(self):
        self.add_concept_section(
            "Programmation Asynchrone : Gérer l'Imprévisibilité du Temps",
            "JavaScript est **single-threaded**, ce qui signifie qu'il exécute une seule tâche à la fois. Si une opération prend beaucoup de temps (comme une requête réseau ou un calcul complexe), elle bloquerait tout le reste du programme. La **programmation asynchrone** est le mécanisme qui permet à JavaScript d'exécuter des opérations longues sans bloquer le thread principal, en différant leur exécution à plus tard. Les concepts clés pour gérer cela sont les **Callbacks**, les **Promesses** et la syntaxe **Async/Await** (le plus moderne).",
            """
console.log("1. Début du script.");

// 1. Callbacks : La méthode historique
// Une fonction passée en argument à une autre fonction pour être exécutée plus tard.
// Peut mener au 'callback hell' (imbrication profonde)
setTimeout(() => { // setTimeout est une fonction asynchrone native du navigateur/Node.js
    console.log("3. Opération asynchrone terminée après 2 secondes (via callback).");
}, 2000);

console.log("2. Le script continue son exécution immédiate.");

/* Résultat dans la console:
1. Début du script.
2. Le script continue son exécution immédiate.
(après 2 secondes) 3. Opération asynchrone terminée après 2 secondes (via callback).
*/
            """
        )
        self.add_concept_section(
            "Les Promesses (Promises) : Une Meilleure Gestion des Opérations Futures",
            "Les **Promesses** (introduites avec ES6) sont un objet qui représente l'achèvement (ou l'échec) éventuel d'une opération asynchrone et sa valeur résultante. Elles sont une amélioration majeure par rapport aux callbacks pour gérer la complexité des flux asynchrones, offrant une meilleure lisibilité et une gestion d'erreur plus robuste.",
            """
// Création d'une promesse
const recupererDonnees = new Promise((resolve, reject) => {
    // Simule une opération de longue durée (ex: appel API)
    const estConnecte = true; // Changez à 'false' pour voir l'erreur

    setTimeout(() => {
        if (estConnecte) {
            resolve("Utilisateur Alice récupéré !"); // La promesse est RÉSOLUE avec cette valeur
        } else {
            reject("Échec de la connexion réseau."); // La promesse est REJETÉE avec cette erreur
        }
    }, 1500);
});

// Utilisation d'une promesse
recupererDonnees
    .then(message => { // '.then()' est appelé si la promesse est résolue
        console.log("Succès de la promesse :", message);
        return "Traitement suivant..."; // Les then peuvent chaîner
    })
    .then(messageSuivant => {
        console.log(messageSuivant);
    })
    .catch(erreur => { // '.catch()' est appelé si la promesse est rejetée
        console.error("Erreur de la promesse :", erreur);
    })
    .finally(() => { // '.finally()' est toujours appelé, que la promesse réussisse ou échoue
        console.log("La promesse est terminée.");
    });

console.log("Requête de données envoyée..."); // S'affiche immédiatement
            """
        )
        self.add_concept_section(
            "`async`/`await` : L'Asynchrone comme du Synchrone",
            "Introduits en ES2017, les mots-clés **`async`** et **`await`** sont le moyen le plus propre et le plus moderne d'écrire du code asynchrone. Ils sont bâtis sur les Promesses et vous permettent d'écrire du code asynchrone qui ressemble et se lit comme du code synchrone, améliorant considérablement la lisibilité et la maintenabilité.",
            """
// Une fonction 'async' retourne toujours une promesse.
async function obtenirInfosUtilisateur(id) {
    try {
        console.log(`Début de la récupération pour l'utilisateur ${id}...`);
        // `await` met en pause l'exécution de la fonction `async` jusqu'à ce que la promesse soit résolue.
        // C'est comme attendre la fin d'une opération bloquante, mais sans bloquer le thread principal.
        const reponse = await new Promise(res => setTimeout(() => res(`Infos pour l'utilisateur ${id}`), 2000));

        const autreDonnee = await new Promise(res => setTimeout(() => res(`Autre donnée pour ${id}`), 1000));

        console.log(reponse);
        console.log(autreDonnee);
        return { reponse, autreDonnee };
    } catch (erreur) {
        // La gestion des erreurs avec try...catch fonctionne directement avec await
        console.error("Une erreur est survenue :", erreur);
        throw erreur; // Relancer l'erreur si nécessaire
    }
}

// Appel de la fonction async
obtenirInfosUtilisateur(123)
    .then(data => console.log("Opération complète :", data))
    .catch(err => console.error("Gestion d'erreur externe :", err));

console.log("Appel de fonction asynchrone lancé !"); // S'affiche immédiatement
            """
        )

    def display_advanced_manipulation(self):
        self.add_concept_section(
            "Destructuration (Destructuring Assignment) : Extraire les Données Facilement",
            "La **destructuration** est une syntaxe puissante (introduite en ES6) qui permet d'extraire des valeurs directement à partir de tableaux ou des propriétés à partir d'objets, et de les assigner à de nouvelles variables de manière concise et lisible. Elle simplifie grandement l'accès et l'utilisation des données structurées.",
            """
// 1. Destructuration d'Objet
const utilisateur = {
    nom: "Alice",
    age: 28,
    email: "alice@example.com",
    adresse: {
        ville: "Lyon",
        pays: "France"
    }
};

// Extraction de propriétés dans des variables avec les mêmes noms
const { nom, age } = utilisateur;
console.log(nom); // Alice
console.log(age); // 28

// Renommer les variables lors de la destructuration
const { nom: nomComplet, email: adresseMail } = utilisateur;
console.log(nomComplet);  // Alice
console.log(adresseMail); // alice@example.com

// Valeurs par défaut en cas de propriété manquante
const { telephone = "N/A", age: ageUtilisateur } = utilisateur;
console.log(telephone);     // N/A
console.log(ageUtilisateur); // 28

// Destructuration imbriquée (pour les objets dans les objets)
const { adresse: { ville, pays } } = utilisateur;
console.log(ville); // Lyon
console.log(pays);  // France

// 2. Destructuration de Tableau
const couleurs = ["rouge", "vert", "bleu", "jaune"];

// Extraction d'éléments par position
const [premiereCouleur, deuxiemeCouleur] = couleurs;
console.log(premiereCouleur); // rouge
console.log(deuxiemeCouleur); // vert

// Ignorer des éléments
const [, , troisiemeCouleur] = couleurs; // Saute les deux premiers
console.log(troisiemeCouleur); // bleu

// Utilisation avec le reste des éléments (Rest operator)
const [chef, ...equipe] = ["Jean", "Marie", "Pierre", "Sophie"];
console.log(chef);   // Jean
console.log(equipe); // ["Marie", "Pierre", "Sophie"]
            """
        )
        self.add_concept_section(
            "Opérateur Spread (`...`) : Étendre et Combiner",
            "L'**opérateur spread** (`...`) est utilisé pour étendre un itérable (comme un tableau, une chaîne de caractères) ou un objet littéral dans un endroit où zéro ou plusieurs arguments (pour les appels de fonction), ou éléments (pour les tableaux littéraux), ou paires clé-valeur (pour les objets littéraux) sont attendus. Il est très utile pour copier, combiner ou décomposer des structures de données.",
            """
// 1. Étendre des tableaux (pour les combiner ou copier)
const arr1 = [1, 2];
const arr2 = [3, 4];
const combine = [...arr1, ...arr2, 5]; // Crée un nouveau tableau
console.log(combine); // [1, 2, 3, 4, 5]

const copieArr = [...arr1]; // Création d'une copie superficielle (nouvelle référence)
console.log(copieArr); // [1, 2]
console.log(copieArr === arr1); // false

// 2. Étendre des objets (pour les fusionner ou copier)
const objBase = { a: 1, b: 2 };
const objExtensions = { c: 3, d: 4 };
const objFusionne = { ...objBase, ...objExtensions, e: 5 }; // Fusionne les propriétés
console.log(objFusionne); // { a: 1, b: 2, c: 3, d: 4, e: 5 }

// Surcharge de propriétés (la dernière propriété gagne)
const objAvecSurcharge = { ...objBase, b: 99 };
console.log(objAvecSurcharge); // { a: 1, b: 99 }

// 3. Passer des arguments à une fonction
function additionnerTroisNombres(a, b, c) {
    return a + b + c;
}
const nombresPourFonction = [10, 20, 30];
console.log(additionnerTroisNombres(...nombresPourFonction)); // 60
            """
        )
        self.add_concept_section(
            "Opérateur Rest (`...`) : Regrouper les Éléments Restants",
            "L'**opérateur rest** (qui utilise la même syntaxe `...` que l'opérateur spread, mais dans un contexte différent) est utilisé pour collecter un nombre indéfini d'arguments d'une fonction dans un tableau, ou pour collecter les propriétés restantes d'un objet lors de la destructuration. Il regroupe les éléments 'restants' dans un nouveau tableau ou objet.",
            """
// 1. Dans les paramètres d'une fonction (collecte tous les arguments restants)
function afficherDetails(prenom, nom, ...autresInfos) {
    console.log(`Prénom: ${prenom}`);
    console.log(`Nom: ${nom}`);
    console.log(`Autres infos:`, autresInfos); // Un tableau
}
afficherDetails("Léa", "Martin", 30, "Développeuse", "Paris");
/*
Prénom: Léa
Nom: Martin
Autres infos: [30, "Développeuse", "Paris"]
*/

// 2. Dans la destructuration d'objet (collecte les propriétés restantes dans un nouvel objet)
const produit = {
    id: 101,
    nom: "Smartphone",
    prix: 500,
    categorie: "Électronique",
    stock: 150
};

const { id, nom, ...detailsComplementaires } = produit;
console.log(id);                      // 101
console.log(nom);                     // Smartphone
console.log(detailsComplementaires);  // { prix: 500, categorie: "Électronique", stock: 150 }

// 3. Dans la destructuration de tableau (collecte les éléments restants dans un nouveau tableau)
const [premier, deuxieme, ...leReste] = [1, 2, 3, 4, 5, 6];
console.log(premier); // 1
console.log(deuxieme); // 2
console.log(leReste);  // [3, 4, 5, 6]
            """
        )

    def display_error_handling(self):
        self.add_concept_section(
            "Gestion des Erreurs : Rendre votre Code Robuste et Prévisible",
            "La **gestion des erreurs** est une pratique essentielle en programmation pour anticiper et réagir aux problèmes qui peuvent survenir pendant l'exécution d'un script. En JavaScript, le mécanisme principal est le bloc **`try...catch`**, complété par l'instruction **`throw`** et le bloc optionnel **`finally`**. Une bonne gestion des erreurs empêche votre application de planter et fournit des informations utiles pour le débogage ou pour l'utilisateur.",
            """
// 1. Le bloc `try...catch`
// `try`: Contient le code qui pourrait générer une erreur.
// `catch(error)`: S'exécute si une erreur est lancée dans le bloc `try`. L'objet 'error' contient les détails.
// `finally`: (Optionnel) S'exécute toujours, que l'erreur se produise ou non, après `try` et `catch`.

try {
    console.log("Début du bloc try.");
    // Simule une erreur (par exemple, appel à une fonction non définie)
    let resultat = maFonctionInexistante();
    console.log(resultat); // Cette ligne ne sera pas atteinte si une erreur se produit avant
} catch (err) {
    console.error("ERREUR DÉTECTÉE :", err.name);      // Le nom de l'erreur (ex: ReferenceError)
    console.error("Message :", err.message); // Le message de l'erreur (ex: maFonctionInexistante is not defined)
    // console.error("Pile d'appels (stack) :", err.stack); // Trace de l'erreur
} finally {
    console.log("Le bloc 'finally' est toujours exécuté.");
}

console.log("Le script continue son exécution après le bloc try...catch.");
            """
        )
        self.add_concept_section(
            "Lancer des Erreurs Manuellement (`throw`)",
            "L'instruction **`throw`** vous permet de créer et de lancer vos propres erreurs personnalisées ou de relancer une erreur existante. C'est utile pour indiquer qu'une condition anormale s'est produite et que le code ne peut pas continuer son exécution normale.",
            """
function diviser(a, b) {
    if (b === 0) {
        // Lancer une erreur de type 'Error' avec un message descriptif
        throw new Error("Erreur de division : Le diviseur ne peut pas être zéro.");
    }
    if (typeof a !== 'number' || typeof b !== 'number') {
        throw new TypeError("Erreur de type : Les arguments doivent être des nombres.");
    }
    return a / b;
}

try {
    console.log("Résultat de 10 / 2 :", diviser(10, 2)); // 5
    // console.log("Résultat de 10 / 0 :", diviser(10, 0)); // Ceci va lancer une erreur
    console.log("Résultat de 'abc' / 2 :", diviser("abc", 2)); // Ceci va lancer une erreur de type
} catch (erreur) {
    // On peut vérifier le type de l'erreur
    if (erreur instanceof TypeError) {
        console.warn("Attention ! Erreur de type :", erreur.message);
    } else if (erreur instanceof Error) {
        console.error("Erreur générale :", erreur.message);
    } else {
        console.error("Une erreur inattendue est survenue :", erreur);
    }
}
            """
        )
        self.add_concept_section(
            "Gestion des Erreurs avec les Promesses et Async/Await",
            "En programmation asynchrone, les erreurs qui se produisent dans une promesse sont gérées avec la méthode **`.catch()`**. Avec `async`/`await`, le bloc `try...catch` peut être utilisé de manière synchrone pour capturer les erreurs des opérations `await`.",
            """
// Gestion d'erreur avec `.catch()` pour les Promesses
new Promise((resolve, reject) => {
    // Simule une opération échouée
    setTimeout(() => reject(new Error("Données de l'API introuvables")), 1500);
})
.then(data => console.log(data))
.catch(error => console.error("Problème API (via .catch) :", error.message));

// Gestion d'erreur avec `try...catch` dans une fonction `async`
async function chargerUtilisateur(id) {
    try {
        const response = await new Promise((res, rej) => {
            // Simule une erreur réseau
            setTimeout(() => rej("Erreur réseau sur l'utilisateur " + id), 1000);
        });
        console.log("Utilisateur chargé :", response);
    } catch (e) {
        console.error("Échec du chargement de l'utilisateur (via async/await try/catch) :", e);
    }
}
chargerUtilisateur(456);
            """
        )

    def display_modules(self):
        self.add_concept_section(
            "Modules (ES Modules) : Organiser, Réutiliser et Isoler votre Code",
            "Les **modules JavaScript (ES Modules ou ESM)**, introduits avec ES6 (ECMAScript 2015), sont le système standard et le plus moderne pour organiser votre code en unités réutilisables et bien définies. Chaque fichier JavaScript est considéré comme son propre module. Les modules permettent d'exporter des éléments (fonctions, variables, classes) pour qu'ils soient accessibles à d'autres modules et d'importer des éléments d'autres modules. Cela favorise une meilleure organisation, la prévention des conflits de noms et l'optimisation du code.",
            """
// --- Fichier : `utils/math.js` ---
// Exportation nommée : Utilisez `export` devant les déclarations.
export const PI = 3.14159;

export function addition(a, b) {
    return a + b;
}

export function soustraction(a, b) {
    return a - b;
}

// Exportation par défaut : Une seule exportation par défaut par module, facile à importer.
// Utilisée pour la "chose" principale que le module fournit.
export default class Calculateur {
    multiplier(a, b) {
        return a * b;
    }
}

// --- Fichier : `app.js` ---
// Importation nommée : Les noms doivent correspondre aux noms exportés.
import { PI, addition } from './utils/math.js';

// Importation par défaut : Peut être importée avec n'importe quel nom.
import MonCalculateur from './utils/math.js'; // 'MonCalculateur' est le nom choisi ici

// Importation de tout dans un objet (namespace import)
import * as MathOperations from './utils/math.js';

console.log(PI);             // 3.14159
console.log(addition(10, 5)); // 15

const calc = new MonCalculateur();
console.log(calc.multiplier(4, 3)); // 12

console.log(MathOperations.soustraction(10, 2)); // 8 (via l'objet MathOperations)

// Exemples d'utilisation dans HTML (type="module") :
// <script type="module" src="app.js"></script>
            """
        )
        self.add_concept_section(
            "Avantages Cruciaux des Modules",
            "1.  **Isolation de la Portée :** Chaque module a sa propre portée. Les variables, fonctions ou classes déclarées dans un module ne sont pas accessibles globalement à moins d'être explicitement exportées. Cela élimine les conflits de noms (pollution de l'espace global).\n2.  **Clarté des Dépendances :** Il est immédiatement clair quels sont les dépendances d'un module grâce aux déclarations `import`.\n3.  **Réutilisabilité :** Le code est plus facile à réutiliser dans différentes parties de votre application ou dans d'autres projets.\n4.  **Chargement Asynchrone :** Les modules sont chargés de manière asynchrone par défaut (dans les navigateurs), améliorant les performances.\n5.  **Tree Shaking :** Les outils de bundling peuvent analyser les dépendances des modules et supprimer le code non utilisé (dead code), réduisant la taille finale de votre application."
        )

    def display_closures(self):
        self.add_concept_section(
            "Closures (Fermetures) : Quand les Fonctions se Souviennent",
            "Une **closure** (ou fermeture en français) est un concept fondamental en JavaScript et un aspect puissant des fonctions. Une closure est une **fonction qui 'se souvient' et peut accéder à son environnement lexical (la portée dans laquelle elle a été déclarée) même après que cet environnement ait été fermé.** En d'autres termes, une fonction inner (interne) garde une référence aux variables de la fonction outer (externe) même si la fonction externe a terminé son exécution.",
            """
// Exemple Classique de Closure : Un Compteur
function creerCompteur() {
    let count = 0; // Cette variable 'count' fait partie de l'environnement lexical

    // La fonction `incrementer` est une closure
    // Elle "capture" la variable `count` de sa portée parente (`creerCompteur`)
    return function incrementer() {
        count++; // Accède et modifie 'count'
        console.log(`Compteur actuel : ${count}`);
    };
}

const compteur1 = creerCompteur(); // Appelle creerCompteur, qui retourne la fonction incrementer
compteur1(); // Compteur actuel : 1
compteur1(); // Compteur actuel : 2

const compteur2 = creerCompteur(); // Crée une NOUVELLE closure, avec son propre 'count'
compteur2(); // Compteur actuel : 1 (pour compteur2)
compteur1(); // Compteur actuel : 3 (compteur1 continue sur son propre 'count')

// Les deux compteurs maintiennent un état indépendant grâce aux closures.
            """
        )
        self.add_concept_section(
            "Mécanisme des Closures et Cas d'Utilisation",
            "**Comment ça marche ?** Quand `creerCompteur()` est appelée, elle crée une variable `count` et une fonction `incrementer`. Au lieu de détruire `count` après que `creerCompteur()` ait fini (comme le ferait une portée normale), JavaScript conserve l'environnement lexical de `creerCompteur()` en mémoire parce que la fonction `incrementer` y fait référence. C'est cette persistance de la portée qui constitue la closure.\n\n**Cas d'utilisation courants :**\n1.  **Encapsulation de données (Variables Privées) :** Pour créer des variables qui ne sont pas directement accessibles de l'extérieur, mais peuvent être manipulées via des méthodes publiques.\n2.  **Fonctions usines / Fabriques de fonctions :** Des fonctions qui génèrent d'autres fonctions avec un comportement pré-configuré.\n3.  **Callbacks :** Souvent, les fonctions de rappel dans les opérations asynchrones (timers, requêtes API) sont des closures qui ont besoin d'accéder à des variables de leur environnement d'origine.\n4.  **Currying et Partial Application :** Comme vu dans une autre section, ces techniques s'appuient fortement sur les closures."
        )

    def display_this_keyword(self):
        self.add_concept_section(
            "Le mot-clé `this` : Le Contexte d'Exécution Mystérieux",
            "Le mot-clé **`this`** en JavaScript est l'une des sources de confusion les plus fréquentes pour les développeurs. Sa valeur **n'est pas déterminée par l'endroit où la fonction est déclarée, mais par la manière dont la fonction est appelée (le contexte d'exécution)**. Comprendre `this` est crucial pour la programmation orientée objet en JavaScript et pour interagir correctement avec le DOM.",
            """
// 1. Contexte Global (hors de toute fonction)
console.log(this === window); // Dans un navigateur: true (this fait référence à l'objet global window)
// En mode strict ou dans un module (par défaut en ES Modules), 'this' global est `undefined`.

// 2. Appel de Fonction Simple (Function Invocation)
function montrerThisSimple() {
    console.log(this);
}
montrerThisSimple(); // Dans un navigateur (mode non strict) : window
                   // En mode strict ou dans un module : undefined

// 3. Méthode d'Objet (Method Invocation)
// Quand une fonction est appelée comme une méthode d'un objet, 'this' fait référence à cet objet.
const utilisateur = {
    nom: "Charles",
    saluer: function() {
        console.log(`Bonjour, je suis ${this.nom}.`); // 'this' fait référence à 'utilisateur'
    }
};
utilisateur.saluer(); // Bonjour, je suis Charles.

// 4. Contexte du Constructeur (Constructor Invocation)
// Quand une fonction est appelée avec le mot-clé `new`, elle agit comme un constructeur,
// et 'this' fait référence à la nouvelle instance de l'objet créée.
function Personne(nom) {
    this.nom = nom; // 'this' est la nouvelle instance créée (ex: p1)
    console.log(`Nouvelle personne créée : ${this.nom}`);
}
const p1 = new Personne("Diane"); // Nouvelle personne créée : Diane
console.log(p1.nom); // Diane

// 5. Fonctions Fléchées (Arrow Functions) : 'this' Lexical
// Les fonctions fléchées n'ont PAS leur propre `this`. Elles héritent la valeur de `this`
// du contexte lexical (la portée) où elles ont été définies. C'est une différence majeure.
const voiture = {
    marque: "Toyota",
    vitesse: 0,
    accelerer: function() {
        console.log(`Méthode normale: this.marque est ${this.marque}`); // 'this' est 'voiture'
        // setTimeout est une fonction globale, son callback perdrait le 'this' si ce n'était pas une fléchée.
        setTimeout(() => { // Cette fonction fléchée garde le 'this' de 'accelerer' (qui est 'voiture')
            this.vitesse += 10;
            console.log(`Après 1s, la vitesse de ${this.marque} est ${this.vitesse} km/h.`);
        }, 1000);
    }
};
voiture.accelerer();
            """
        )
        self.add_concept_section(
            "Contrôler la Valeur de `this` : `call()`, `apply()`, `bind()`",
            "Ces trois méthodes sont des fonctions prototypiques des fonctions qui permettent de définir explicitement la valeur de `this` lors de l'appel d'une fonction.",
            """
const objA = { valeur: 10 };
const objB = { valeur: 20 };

function afficherValeur() {
    console.log(this.valeur);
}

// `call(thisArg, arg1, arg2, ...)` : Appelle la fonction immédiatement avec `thisArg` et arguments individuels.
afficherValeur.call(objA); // 10

// `apply(thisArg, [argsArray])` : Appelle la fonction immédiatement avec `thisArg` et arguments sous forme de tableau.
afficherValeur.apply(objB); // 20

// `bind(thisArg)` : Retourne une NOUVELLE fonction avec `this` lié de manière permanente à `thisArg`.
const fonctionLieeA_objA = afficherValeur.bind(objA);
fonctionLieeA_objA(); // 10 (même si appelée sans contexte direct)

// Le `bind` est très utile pour les callbacks où le contexte de `this` pourrait être perdu.
// Exemple typique dans React ou d'autres frameworks quand on passe des méthodes en props.
            """
        )

    def display_heritage_prototypal(self):
        self.add_concept_section(
            "Héritage Prototypal : Le Véritable Modèle d'Héritage de JavaScript",
            "Contrairement à la plupart des langages de programmation orientés objet (comme Java ou C++) qui utilisent un modèle d'héritage basé sur les classes, JavaScript adopte un modèle d'**héritage prototypal**. Cela signifie que les objets héritent directement d'autres objets (appelés leurs **prototypes**) plutôt que de classes. Chaque objet en JavaScript a un prototype, et une propriété ou une méthode qui n'est pas trouvée directement sur l'objet est recherchée sur son prototype, et ainsi de suite le long de la **chaîne de prototype**.",
            """
// 1. Tous les Objets ont un Prototype
const obj = {};
// obj.__proto__ est Object.prototype
console.log(obj.__proto__ === Object.prototype); // true

// Object.prototype est le prototype de base de tous les objets.
// C'est pourquoi tous les objets ont des méthodes comme toString(), hasOwnProperty(), etc.

// 2. La Chaîne de Prototype
const animal = {
    manger: function() {
        console.log(`${this.nom} mange.`);
    },
    estVivant: true
};

const chien = {
    nom: "Rex",
    aboyer: function() {
        console.log(`${this.nom} aboie !`);
    }
};

// Lier 'chien' au prototype 'animal'
// C'est une façon directe de manipuler la chaîne de prototype.
Object.setPrototypeOf(chien, animal);

console.log(chien.nom);         // Rex (propriété propre à chien)
chien.aboyer();                 // Rex aboie ! (méthode propre à chien)
console.log(chien.estVivant);   // true (hérité de 'animal' via la chaîne de prototype)
chien.manger();                 // Rex mange. (hérité de 'animal')

console.log(chien.__proto__ === animal); // true
console.log(animal.__proto__ === Object.prototype); // true
console.log(Object.prototype.__proto__); // null (fin de la chaîne)

// Lorsque vous accédez à 'chien.manger()', JS cherche 'manger' sur 'chien'.
// Ne le trouvant pas, il remonte à 'chien.__proto__' (qui est 'animal'), et le trouve là.
            """
        )
        self.add_concept_section(
            "Créer des Objets avec des Prototypes Spécifiques et la Vue 'Classique'",
            "Il existe plusieurs façons de créer des objets et de manipuler leurs prototypes. Les **classes ES6+** sont un 'sucre syntaxique' qui rend l'héritage prototypal plus familier pour ceux qui viennent de langages basés sur les classes.",
            """
// 3. `Object.create()` : Créer un nouvel objet avec un prototype spécifique
const chatPrototype = {
    miauler() {
        console.log(`${this.nom} miaule.`);
    },
    ronronner: true
};

const felix = Object.create(chatPrototype); // Crée un objet vide avec `chatPrototype` comme prototype
felix.nom = "Felix"; // Ajoute une propriété propre à felix
console.log(felix.nom);        // Felix
console.log(felix.ronronner);  // true (hérité)
felix.miauler();               // Felix miaule.

// 4. Les Classes ES6+ et l'Héritage Prototypal
// Les classes en JavaScript sont des fonctions spéciales et sont toujours basées sur les prototypes.
// La syntaxe `class` et `extends` simplifie la manipulation des prototypes en arrière-plan.
class Forme {
    constructor(nom) {
        this.nom = nom;
    }
    presenter() {
        console.log(`Je suis une ${this.nom}.`);
    }
}

class Cercle extends Forme { // 'Cercle.prototype' hérite de 'Forme.prototype'
    constructor(nom, rayon) {
        super(nom); // Appelle le constructeur de Forme
        this.rayon = rayon;
    }
    calculerAire() {
        return Math.PI * this.rayon * this.rayon;
    }
}

const monCercle = new Cercle("cercle", 5);
monCercle.presenter();       // Je suis une cercle. (méthode héritée)
console.log(monCercle.calculerAire()); // 78.53... (méthode propre)

console.log(Cercle.prototype.__proto__ === Forme.prototype); // true
console.log(Object.getPrototypeOf(monCercle) === Cercle.prototype); // true
            """
        )

    def display_prog_fonctionnelle(self):
        self.add_concept_section(
            "Programmation Fonctionnelle (FP) : Un Style de Programmation Épuré",
            "La **programmation fonctionnelle (FP)** est un paradigme de programmation qui met l'accent sur l'utilisation de **fonctions pures** et sur l'**immuabilité des données**. En JavaScript, avec son support des fonctions en tant que 'citoyens de première classe', la FP est un style puissant pour écrire du code plus lisible, plus maintenable, et plus facile à tester. Elle se concentre sur 'ce qu'il faut faire' plutôt que 'comment le faire'.",
            """
// Principes clés de la FP :
// 1. Fonctions Pures :
//    - Ne produisent pas d'effets de bord (ne modifient pas l'état externe ou les arguments).
//    - Retournent toujours la même sortie pour les mêmes entrées.
function pureAdd(a, b) {
    return a + b; // Pure
}

let total = 0;
function impureAdd(a, b) {
    total = a + b; // Impure (modifie une variable externe)
    return total;
}

// 2. Immuabilité :
//    - Ne pas modifier les données existantes.
//    - Créer de nouvelles copies des données avec les modifications.
const originalArray = [1, 2, 3];
// const modifiedArray = originalArray.push(4); // Mauvaise pratique en FP (modifie l'original)
const newArray = [...originalArray, 4]; // Bonne pratique en FP (nouvel array)
console.log(originalArray); // [1, 2, 3]
console.log(newArray);      // [1, 2, 3, 4]
            """
        )
        self.add_concept_section(
            "Méthodes de Tableaux Fonctionnelles : `map`, `filter`, `reduce`",
            "Ces trois méthodes sont les piliers de la manipulation de données en style fonctionnel en JavaScript. Elles transforment des tableaux en créant de nouveaux tableaux sans modifier l'original (immuabilité).",
            """
const utilisateurs = [
    { id: 1, nom: "Alice", age: 30, actif: true },
    { id: 2, nom: "Bob", age: 24, actif: false },
    { id: 3, nom: "Charlie", age: 35, actif: true },
    { id: 4, nom: "Diane", age: 24, actif: true }
];

// 1. `map()` : Transformer chaque élément
// Crée un NOUVEAU tableau en appliquant une fonction de transformation à chaque élément.
const nomsUtilisateurs = utilisateurs.map(user => user.nom);
console.log("Noms:", nomsUtilisateurs); // ["Alice", "Bob", "Charlie", "Diane"]

const utilisateursAvecAgeDouble = utilisateurs.map(user => ({
    ...user, // Copie toutes les propriétés existantes (opérateur spread)
    age: user.age * 2 // Modifie l'âge
}));
console.log("Utilisateurs avec âge doublé:", utilisateursAvecAgeDouble);

// 2. `filter()` : Filtrer des éléments
// Crée un NOUVEAU tableau contenant uniquement les éléments qui passent une condition spécifiée.
const utilisateursActifs = utilisateurs.filter(user => user.actif);
console.log("Actifs:", utilisateursActifs); // [Alice, Charlie, Diane]

const utilisateursDe24Ans = utilisateurs.filter(user => user.age === 24);
console.log("24 ans:", utilisateursDe24Ans); // [Bob, Diane]

// 3. `reduce()` : Réduire un tableau à une seule valeur
// Exécute une fonction de 'réducteur' sur chaque élément du tableau,
// aboutissant à une seule valeur de sortie (somme, objet, chaîne, etc.).
const totalAges = utilisateurs.reduce((acc, user) => acc + user.age, 0); // 0 est l'accumulateur initial
console.log("Total des âges:", totalAges); // 113 (30+24+35+24)

const nomsParId = utilisateurs.reduce((acc, user) => {
    acc[user.id] = user.nom;
    return acc;
}, {}); // {} est l'accumulateur initial (un objet vide)
console.log("Noms par ID:", nomsParId); // { '1': 'Alice', '2': 'Bob', '3': 'Charlie', '4': 'Diane' }
            """
        )

    def display_decorateurs_mixins(self):
        self.add_concept_section(
            "Décorateurs et Mixins : Étendre les Fonctionnalités par Composition",
            "Les **décorateurs** et les **mixins** sont des patterns de conception qui permettent d'ajouter des fonctionnalités à des objets ou des classes existants sans modifier leur structure de base ou recourir à l'héritage classique (qui peut entraîner des hiérarchies complexes). Ils favorisent la **composition** plutôt que l'héritage, ce qui rend le code plus flexible et réutilisable.",
            """
// --- 1. Mixins (Composition d'Objets) ---
// Un mixin est un objet qui contient des méthodes que d'autres objets ou classes peuvent 'emprunter'
// ou 'copier' pour étendre leurs propres fonctionnalités. C'est une forme de réutilisation de code.

const peutCourir = {
    courir() {
        console.log(`${this.nom} court !`);
    }
};

const peutSauter = {
    sauter() {
        console.log(`${this.nom} saute !`);
    }
};

// Créer une classe de base
class Hero {
    constructor(nom) {
        this.nom = nom;
    }
    presenter() {
        console.log(`Je suis ${this.nom}.`);
    }
}

// Appliquer les mixins à la classe Hero (ou à son prototype)
// `Object.assign()` copie les propriétés d'un ou plusieurs objets sources vers un objet cible.
Object.assign(Hero.prototype, peutCourir, peutSauter);

const superHero = new Hero("Flash");
superHero.presenter();
superHero.courir(); // Flash court ! (méthode du mixin)
superHero.sauter(); // Flash saute ! (méthode du mixin)

const autreHero = new Hero("Superman");
autreHero.sauter(); // Superman saute !

// Avantage : Éviter le "diamant de l'héritage" et permettre à un objet d'avoir plusieurs "capacités".
            """
        )
        self.add_concept_section(
            "Décorateurs (Fonctionnels et ES7+)",
            "Un **décorateur** est une fonction qui prend une autre fonction ou une classe (ou une propriété/méthode) et en retourne une nouvelle, augmentée de fonctionnalités supplémentaires, sans modifier l'original directement. Il 'décore' ou 'enveloppe' l'entité originale.",
            """
// --- 2. Décorateur Fonctionnel (JS Vanilla - Pattern d'Enveloppement) ---
// Une fonction qui prend une fonction en entrée et retourne une nouvelle fonction
function logExecution(originalFunction) {
    return function(...args) { // Retourne une nouvelle fonction (une closure)
        console.log(`Avant exécution de ${originalFunction.name} avec arguments:`, args);
        const result = originalFunction(...args); // Exécute la fonction originale
        console.log(`Après exécution de ${originalFunction.name}, résultat:`, result);
        return result;
    };
}

function calculerProduit(a, b) {
    return a * b;
}

// "Décorer" la fonction `calculerProduit`
const calculerProduitLogge = logExecution(calculerProduit);
calculerProduitLogge(7, 8);
/* Affiche :
Avant exécution de calculerProduit avec arguments: [7, 8]
Après exécution de calculerProduit, résultat: 56
*/

// --- Décorateurs avec la syntaxe `@` (Proposition ES7+ / Babel / TypeScript) ---
// La syntaxe `@decoratorName` est une proposition de fonctionnalité JavaScript
// qui est déjà largement utilisée avec des transpileurs comme Babel ou dans TypeScript.
// C'est du sucre syntaxique pour le pattern d'enveloppement ci-dessus.

/* Exemple conceptuel (nécessite un transpileur):
// function logClass(targetClass) {
//     return class extends targetClass {
//         constructor(...args) {
//             console.log(`Création d'une instance de ${targetClass.name}`);
//             super(...args);
//         }
//     };
// }

// @logClass
// class Person {
//     constructor(name) {
//         this.name = name;
//     }
// }

// const p = new Person("Alice"); // Affichera "Création d'une instance de Person"
*/
            """
        )
        self.add_concept_section(
            "Résumé : Composition vs Héritage",
            "Les mixins et les décorateurs sont des techniques puissantes qui mettent en œuvre le principe de **composition préférée à l'héritage**. Ils permettent de construire des objets avec des comportements modulaires et de manière plus flexible que les hiérarchies d'héritage rigides, réduisant le couplage et augmentant la réutilisabilité du code."
        )

    def display_web_apis(self):
        self.add_concept_section(
            "Web APIs : L'Interaction de JavaScript avec le Navigateur et au-delà",
            "Les **Web APIs** (Application Programming Interfaces) ne font pas partie du langage JavaScript lui-même, mais sont des **interfaces fournies par l'environnement du navigateur** (ou Node.js pour des APIs côté serveur). Elles permettent à JavaScript d'interagir avec des fonctionnalités du navigateur (comme le DOM, le réseau, le stockage local, la géolocalisation) ou des services externes. Sans les Web APIs, JavaScript ne serait qu'un langage de script isolé ; avec elles, il devient le moteur interactif des applications web.",
            """
// Toutes les opérations ci-dessous s'exécutent dans l'environnement d'un navigateur web.

// 1. `Fetch API` : Effectuer des Requêtes Réseau (le remplaçant moderne de XMLHttpRequest)
// Permet de faire des requêtes HTTP (GET, POST, etc.) vers des serveurs distants.
// Retourne une Promesse, ce qui la rend très agréable à utiliser avec async/await.

// Exemple : Récupérer des données d'une API publique (simulée)
async function getProduits() {
    try {
        console.log("Tentative de récupération des produits...");
        const response = await fetch('https://api.example.com/products'); // Remplacez par une vraie URL
        // Vérifier si la réponse est OK (statut HTTP 200-299)
        if (!response.ok) {
            throw new Error(`Erreur HTTP! Statut: ${response.status}`);
        }
        const data = await response.json(); // Parsez la réponse JSON en objet JavaScript
        console.log("Produits récupérés :", data);
        return data;
    } catch (error) {
        console.error("Échec de la récupération des produits :", error);
        // Vous pouvez gérer l'erreur, par exemple, afficher un message à l'utilisateur
        return [];
    }
}
// getProduits(); // Décommenter pour simuler l'appel API
            """
        )
        self.add_concept_section(
            "Web Storage API : `localStorage` et `sessionStorage`",
            "Ces APIs fournissent un moyen de stocker des paires clé-valeur de manière persistante (ou semi-persistante) dans le navigateur côté client. Utile pour les préférences utilisateur, les jetons d'authentification ou les données temporaires.",
            """
// 2. `localStorage` : Stockage persistant (les données restent même après la fermeture du navigateur)
localStorage.setItem('nomUtilisateur', 'Lea Dubois'); // Stocker une chaîne de caractères
localStorage.setItem('derniereVisite', new Date().toISOString());

const userPrefs = { theme: 'dark', notifications: true };
// Les objets doivent être convertis en chaîne JSON avant d'être stockés
localStorage.setItem('preferences', JSON.stringify(userPrefs));

// Récupérer des données
const nom = localStorage.getItem('nomUtilisateur');
console.log(`Nom de l'utilisateur stocké : ${nom}`);

const prefsString = localStorage.getItem('preferences');
const prefsObj = JSON.parse(prefsString); // Reconvertir la chaîne JSON en objet
console.log(`Préférence de thème : ${prefsObj.theme}`);

// Supprimer des données
// localStorage.removeItem('nomUtilisateur'); // Supprime une clé spécifique
// localStorage.clear(); // Supprime toutes les données du localStorage pour le domaine actuel

// 3. `sessionStorage` : Stockage de session (les données sont effacées à la fermeture de l'onglet/navigateur)
sessionStorage.setItem('tempData', 'Données temporaires de session');
const tempData = sessionStorage.getItem('tempData');
console.log(`Données de session : ${tempData}`);
            """
        )
        self.add_concept_section(
            "Autres Web APIs Essentielles",
            "De nombreuses autres APIs enrichissent les capacités de JavaScript dans le navigateur :\n* **DOM API :** (Déjà couverte) Manipulation du HTML et du CSS.\n* **Event API :** (Déjà couverte) Gestion des interactions utilisateur et du système.\n* **Geolocation API :** Accéder à la position géographique de l'utilisateur.\n* **Canvas API :** Dessiner des graphiques, des jeux et des animations en 2D et 3D.\n* **Web Audio API :** Traiter et synthétiser l'audio dans le navigateur.\n* **History API :** Manipuler l'historique du navigateur pour créer des Single Page Applications (SPA) avec des URLs propres.\n* **Drag and Drop API :** Permet d'implémenter des fonctionnalités de glisser-déposer.\n* **Web Workers API :** Exécuter des scripts complexes en arrière-plan sans bloquer l'interface utilisateur (permet le multi-threading).\n* **Service Workers API :** Un proxy entre le navigateur et le réseau, permettant des expériences hors ligne, des notifications push et des mises à jour en arrière-plan (essentiel pour les Progressive Web Apps - PWA)."
        )

    def display_strict_mode(self):
        self.add_concept_section(
            "Strict Mode (`'use strict'`) : Écrire du Code JavaScript plus Sûr et Robuste",
            "Le **mode strict** (`'use strict'`) est une fonctionnalité opt-in introduite en ECMAScript 5 (ES5) qui permet d'écrire du code JavaScript d'une manière plus restreinte et plus sûre. Il 'détecte' et 'corrige' certaines erreurs qui seraient silencieusement ignorées en mode non-strict, rendant le code plus fiable et plus facile à déboguer. Il empêche également l'utilisation de certaines syntaxes considérées comme problématiques ou réservées pour de futures versions.",
            """
// Pour activer le mode strict pour tout un script :
// Placez la directive en haut de votre fichier JavaScript.
// 'use strict';

// Pour activer le mode strict pour une fonction spécifique :
function executerEnModeStrict() {
    'use strict';
    // Le code à l'intérieur de cette fonction sera en mode strict.
    // Le code à l'extérieur de cette fonction (dans le même fichier) ne le sera pas.
    console.log("Cette fonction s'exécute en mode strict.");
}
executerEnModeStrict();

// Exemples de comportements qui entraînent des erreurs en mode strict (mais pas en mode non-strict) :

// 1. Variables non déclarées :
// (function() {
//     'use strict';
//     uneNouvelleVariable = "Bonjour"; // ERREUR : uneNouvelleVariable is not defined
// })();

// 2. Supprimer des propriétés non configurables (ou des variables non-déclenchables) :
// (function() {
//     'use strict';
//     // delete Object.prototype; // ERREUR
//     // const x = 10;
//     // delete x; // ERREUR
// })();

// 3. Dupliquer les noms de paramètres de fonction :
// (function() {
//     'use strict';
//     // function maFonction(a, b, a) { // ERREUR : Duplicate parameter name not allowed in strict mode
//     //     console.log(a, b);
//     // }
//     // maFonction(1, 2, 3);
// })();

// 4. Utilisation de `this` global dans les appels de fonction simples :
// En mode strict, `this` dans un appel de fonction simple (non-méthode) est `undefined`.
// En mode non-strict, il serait l'objet global (`window` dans un navigateur).
// (function() {
//     'use strict';
//     function montrerThis() {
//         console.log(this); // undefined
//     }
//     montrerThis();
// })();

// 5. Interdiction de `with` statement (considéré comme problématique pour l'optimisation)
// (function() {
//     'use strict';
//     // with (Math) { // ERREUR : Strict mode does not allow 'with' statements
//     //     console.log(PI);
//     // }
// })();
            """
        )
        self.add_concept_section(
            "Avantages de l'Utilisation du Strict Mode",
            "1.  **Détection Précoce des Erreurs :** Transforme les erreurs silencieuses en erreurs explicites, ce qui facilite le débogage.\n2.  **Code plus Robuste :** Empêche certaines pratiques de codage 'dangereuses' ou non optimales.\n3.  **Amélioration des Performances :** En supprimant certaines ambiguïtés, le moteur JavaScript peut mieux optimiser votre code.\n4.  **Préparation pour l'Avenir :** Interdit certaines syntaxes qui pourraient être réservées pour de futures versions d'ECMAScript, assurant une meilleure compatibilité future.\n\n**Recommandation :** Il est fortement recommandé d'utiliser le mode strict dans tous les nouveaux projets JavaScript modernes. La plupart des frameworks et outils de build (comme Babel) l'activent par défaut pour vous."
        )

    def display_currying_partial(self):
        self.add_concept_section(
            "Currying et Partial Application : Transformer les Fonctions pour Plus de Flexibilité",
            "Le **currying** et la **partial application** sont deux techniques de programmation fonctionnelle qui permettent de transformer des fonctions. Elles aident à créer des fonctions plus flexibles, réutilisables et composables, en permettant à une fonction de recevoir ses arguments en plusieurs étapes.",
            """
// --- 1. Currying (Curryfication) ---
// Le currying est la transformation d'une fonction qui prend plusieurs arguments
// en une série de fonctions qui prennent chacune un seul argument, et qui retournent
// à chaque fois une nouvelle fonction attendant le prochain argument, jusqu'à ce que tous les arguments soient fournis.

// Fonction normale :
function additionnerTroisNombres(a, b, c) {
    return a + b + c;
}
console.log(additionnerTroisNombres(1, 2, 3)); // 6

// Version 'Curried' de la fonction :
function curriedAddition(a) {
    return function(b) { // Retourne une fonction qui prend 'b'
        return function(c) { // Retourne une fonction qui prend 'c'
            return a + b + c; // Utilise 'a', 'b' et 'c' (closure)
        };
    };
}

// Utilisation de la fonction curried :
console.log(curriedAddition(1)(2)(3)); // 6 (chaque appel retourne une fonction)

// Avantages du Currying :
// - Création de fonctions spécialisées ("pré-configurées").
const addFive = curriedAddition(5); // Fonction qui attend 'b', 'c' et ajoute 5.
const addFiveAndTen = addFive(10);  // Fonction qui attend 'c' et ajoute 15.
console.log(addFiveAndTen(20));     // 35 (5 + 10 + 20)
console.log(curriedAddition(10)(20)(30)); // 60
            """
        )
        self.add_concept_section(
            "Partial Application (Application Partielle)",
            "La **partial application** (ou application partielle) est un processus qui consiste à prendre une fonction qui accepte plusieurs arguments et à en retourner une nouvelle fonction avec certains de ces arguments déjà 'remplis' (fixés). La nouvelle fonction attendra les arguments restants. Contrairement au currying, la partial application ne réduit pas nécessairement le nombre d'arguments à un seul à chaque étape.",
            """
// Fonction normale :
function envoyerEmail(destinataire, sujet, corpsDuMessage) {
    console.log(`Envoi à: ${destinataire}`);
    console.log(`Sujet: ${sujet}`);
    console.log(`Message: ${corpsDuMessage}`);
    console.log('---');
}

// Utilisation de `Function.prototype.bind()` pour l'application partielle
// `bind(thisArg, arg1, arg2, ...)` : crée une nouvelle fonction dont `this` est lié
// et dont les arguments initiaux sont pré-fixés.
const envoyerEmailDeSupport = envoyerEmail.bind(null, "support@example.com"); // `null` car `this` n'est pas pertinent

envoyerEmailDeSupport("Problème de compte", "Mon compte ne fonctionne pas.");
// Équivaut à: envoyerEmail("support@example.com", "Problème de compte", "Mon compte ne fonctionne pas.");

const envoyerEmailPromo = envoyerEmail.bind(null, "marketing@example.com", "Nouvelle Promotion !");
envoyerEmailPromo("Découvrez nos offres spéciales !");
// Équivaut à: envoyerEmail("marketing@example.com", "Nouvelle Promotion !", "Découvrez nos offres spéciales !");

// Avantages : Réutiliser des fonctions avec des configurations communes.
// Vous pouvez également implémenter la partial application manuellement avec des closures.
function partial(fn, ...fixedArgs) {
    return function(...remainingArgs) {
        return fn(...fixedArgs, ...remainingArgs);
    };
}

const envoyerEmailVentes = partial(envoyerEmail, "ventes@example.com");
envoyerEmailVentes("Question", "Je suis intéressé par vos produits.");
            """
        )
        self.add_concept_section(
            "Currying vs Partial Application : Les Subtilités",
            "La distinction est subtile mais importante :\n* Le **currying** transforme une fonction `f(a, b, c)` en `f(a)(b)(c)`. Il s'agit d'une séquence de fonctions unaires (qui prennent un seul argument) qui s'enchaînent.\n* La **partial application** transforme une fonction `f(a, b, c)` en une nouvelle fonction `g(b, c)` (si `a` est pré-fixé). La nouvelle fonction peut toujours attendre plusieurs arguments restants. Elle ne se soucie pas de la réduction à un argument par appel.",
            "En pratique, les deux techniques sont utilisées pour améliorer la composabilité et la réutilisation du code, particulièrement dans un style de programmation fonctionnelle."
        )

    def display_set_map(self):
        self.add_concept_section(
            "Set et Map : Des Structures de Données Modernes et Optimisées",
            "En plus des objets littéraux (`{}`) et des tableaux (`[]`), JavaScript (depuis ES6) offre deux nouvelles structures de données puissantes : **`Set`** et **`Map`**. Elles fournissent des fonctionnalités spécifiques et sont souvent plus performantes et plus sémantiques que les objets ou tableaux traditionnels pour certains cas d'utilisation.",
            """
// --- 1. `Set` : Une Collection d'Éléments Uniques ---
// Un `Set` est une collection d'éléments où chaque élément ne peut apparaître qu'une seule fois.
// Il ne stocke pas de paires clé-valeur, mais juste une liste de valeurs.

const monSet = new Set();

// Ajouter des éléments : `add()`
monSet.add(10);
monSet.add("Hello");
monSet.add({ nom: "Alice" }); // Les objets sont considérés comme uniques même si leur contenu est similaire
monSet.add(10); // Ceci est ignoré, car 10 est déjà présent
monSet.add("Hello"); // Ignoré

console.log("Taille du Set :", monSet.size); // 3

// Vérifier la présence d'un élément : `has()`
console.log("Le Set contient 10 :", monSet.has(10)); // true
console.log("Le Set contient 20 :", monSet.has(20)); // false

// Supprimer un élément : `delete()`
monSet.delete("Hello");
console.log("Après suppression 'Hello', taille :", monSet.size); // 2

// Itérer sur un Set : `forEach()` ou `for...of`
for (const item of monSet) {
    console.log("Élément du Set :", item);
}

// Convertir un tableau avec doublons en un Set (pour filtrer les doublons), puis le reconvertir en tableau
const nombresAvecDoublons = [1, 2, 3, 2, 4, 1, 5];
const nombresUniques = [...new Set(nombresAvecDoublons)]; // Utilise l'opérateur Spread
console.log("Nombres uniques :", nombresUniques); // [1, 2, 3, 4, 5]

// `clear()` : Supprime tous les éléments du Set
// monSet.clear();
// console.log("Après clear, taille :", monSet.size); // 0
            """
        )
        self.add_concept_section(
            "Map : Des Paires Clé-Valeur avec des Clés de N'importe Quel Type",
            "Une **`Map`** est une collection de paires clé-valeur, similaire à un objet littéral, mais avec une différence majeure : **les clés d'une `Map` peuvent être de n'importe quel type de données** (chaînes, nombres, objets, fonctions, `null`, `undefined`, etc.), alors que les clés d'un objet sont limitées aux chaînes de caractères ou Symboles.",
            """
// --- 2. `Map` : Une Collection de Paires Clé-Valeur ---
const maMap = new Map();

// Définir des paires clé-valeur : `set(clé, valeur)`
maMap.set('nom', 'Bob');
maMap.set(1, 'numéro un'); // Une clé peut être un nombre
maMap.set({}, 'objet comme clé'); // Une clé peut être un objet (chaque objet est unique)
maMap.set(function() {}, 'fonction comme clé'); // Une clé peut être une fonction

console.log("Taille de la Map :", maMap.size); // 4

// Récupérer une valeur par sa clé : `get(clé)`
console.log("Valeur pour 'nom' :", maMap.get('nom')); // Bob
console.log("Valeur pour 1 :", maMap.get(1));       // numéro un

// Vérifier si une clé existe : `has(clé)`
console.log("La Map a la clé 'nom' :", maMap.has('nom')); // true
console.log("La Map a la clé 'age' :", maMap.has('age')); // false

// Supprimer une paire clé-valeur : `delete(clé)`
maMap.delete(1);
console.log("Après suppression de la clé 1, taille :", maMap.size); // 3

// Itérer sur une Map : `forEach()` ou `for...of` (retourne [clé, valeur])
for (const [key, value] of maMap) {
    console.log(`Clé: "${key}", Valeur: "${value}"`);
}
// output:
// Clé: "nom", Valeur: "Bob"
// Clé: "[object Object]", Valeur: "objet comme clé" (représentation de l'objet)
// Clé: "function () {}", Valeur: "fonction comme clé" (représentation de la fonction)

// `clear()` : Supprime toutes les paires clé-valeur de la Map
// maMap.clear();
// console.log("Après clear, taille :", maMap.size); // 0
            """
        )
        self.add_concept_section(
            "Quand Utiliser Set et Map ?",
            "**Utilisez `Set` quand :**\n* Vous avez besoin d'une collection d'éléments uniques.\n* Vous voulez rapidement vérifier si un élément existe dans une collection.\n* Vous avez besoin de supprimer des doublons d'un tableau.\n\n**Utilisez `Map` quand :**\n* Vous avez besoin de stocker des paires clé-valeur où les clés peuvent être de n'importe quel type de données (pas seulement des chaînes).\n* Vous avez besoin de maintenir l'ordre d'insertion des éléments (les objets traditionnels ne garantissent pas toujours l'ordre).\n* Vous effectuez fréquemment des ajouts ou des suppressions de paires clé-valeur (les performances de `Map` sont optimisées pour cela)."
        )

# --- Point d'entrée de l'application ---
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = JavaScriptExplainerApp()
    app.mainloop()