import customtkinter as ctk
import os
import subprocess
import json # Utilisé pour la structure des leçons, même si elles sont en dur pour l'exemple

class PHP8LearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tutoriel PHP 8 Interactif")
        self.geometry("1200x800") # Taille ajustée pour plus de contenu et de confort

        # Configurer la grille principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Barre latérale de navigation (scrollable) ---
        self.sidebar_frame = ctk.CTkScrollableFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        # self.sidebar_frame.grid_rowconfigure(0, weight=1) # Pas besoin si les boutons sont packés ou gridés séquentiellement

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Tutoriel PHP 8", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Boutons de navigation
        self.sidebar_buttons = {}
        # Les leçons sont regroupées par sections pour une meilleure organisation
        lesson_sections = {
            "Introduction": ["Accueil et PHP 8"],
            "Fondamentaux de PHP": ["Variables et Types", "Opérateurs", "Structures de Contrôle", "Fonctions", "POO - Bases"],
            "Nouveautés PHP 8.0": [
                "Match Expression", "Attributs", "Types d'Union 2.0",
                "Constructeur Property Promotion", "Nullsafe Operator",
                "Expressions Throw", "Weak Maps",
                "null, false, true comme Types", "Nouvelles Fonctions String",
                "JIT Compiler (Concept)"
            ],
            "Nouveautés PHP 8.1+": [
                "Enums", "Propriétés en Lecture Seule",
                "Final en Constantes de Classe (PHP 8.1)",
                "Nouvelle fonction array_is_list (PHP 8.1)",
                "Intersection Types (PHP 8.1)"
            ],
            "Pour aller plus loin": ["Gestion des Erreurs et Exceptions", "Débogage et Outils"]
        }
        
        button_row_index = 1 
        for section_title, lessons_list in lesson_sections.items():
            # Ajouter un séparateur ou un titre de section
            if section_title != "Introduction": # Pas de séparateur avant la première section
                separator = ctk.CTkLabel(self.sidebar_frame, text="--- " + section_title + " ---", 
                                         font=ctk.CTkFont(size=14, weight="bold"), text_color="gray")
                separator.grid(row=button_row_index, column=0, padx=10, pady=(15, 5), sticky="ew")
                button_row_index += 1

            for lesson_name in lessons_list:
                button = ctk.CTkButton(self.sidebar_frame, text=lesson_name, command=lambda l=lesson_name: self.display_lesson(l))
                button.grid(row=button_row_index, column=0, padx=20, pady=5, sticky="ew")
                self.sidebar_buttons[lesson_name] = button
                button_row_index += 1

        # --- Zone de contenu principale ---
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content_frame.grid_rowconfigure(1, weight=1) # Le textbox de leçon prend plus de place
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        self.lesson_title_label = ctk.CTkLabel(self.main_content_frame, text="", font=ctk.CTkFont(size=26, weight="bold"))
        self.lesson_title_label.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

        self.lesson_text = ctk.CTkTextbox(self.main_content_frame, wrap="word", activate_scrollbars=True, height=280)
        self.lesson_text.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.lesson_text.configure(state="disabled") 

        # --- Zone d'exécution de code ---
        self.code_execution_frame = ctk.CTkFrame(self, corner_radius=0)
        self.code_execution_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.code_execution_frame.grid_columnconfigure(0, weight=1)
        self.code_execution_frame.grid_rowconfigure(1, weight=1) # Le textbox de code prend plus de place

        self.code_label = ctk.CTkLabel(self.code_execution_frame, text="Exécuteur de Code PHP :", font=ctk.CTkFont(size=18, weight="bold"))
        self.code_label.grid(row=0, column=0, padx=20, pady=5, sticky="nw")

        self.code_input = ctk.CTkTextbox(self.code_execution_frame, height=200, wrap="word", font=ctk.CTkFont(family="Consolas", size=14))
        self.code_input.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        self.execute_button = ctk.CTkButton(self.code_execution_frame, text="Exécuter PHP", command=self.execute_php_code, font=ctk.CTkFont(size=16, weight="bold"))
        self.execute_button.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.output_label = ctk.CTkLabel(self.code_execution_frame, text="Sortie :", font=ctk.CTkFont(size=16, weight="bold"))
        self.output_label.grid(row=3, column=0, padx=20, pady=5, sticky="nw")

        self.code_output = ctk.CTkTextbox(self.code_execution_frame, height=150, wrap="word", font=ctk.CTkFont(family="Consolas", size=14))
        self.code_output.grid(row=4, column=0, padx=20, pady=5, sticky="nsew")
        self.code_output.configure(state="disabled")

        # Charger les données des leçons
        self.load_lesson_data()
        self.display_lesson("Accueil et PHP 8") # Afficher la leçon d'introduction au démarrage

    def load_lesson_data(self):
        # Pour une application réelle, on chargerait ceci depuis des fichiers .md ou .json
        # Ici, en dur pour la simplicité de l'exemple.
        self.lessons = {
            "Accueil et PHP 8": {
                "title": "Bienvenue dans le Tutoriel PHP 8 !",
                "content": """
Bonjour et bienvenue dans ce tutoriel interactif dédié à PHP 8 !

**Qu'est-ce que PHP ?**
PHP (Hypertext Preprocessor) est un langage de script côté serveur largement utilisé pour le développement web. Il permet de créer des pages web dynamiques, des applications web complexes et des API. C'est la base de nombreux CMS populaires comme WordPress, Joomla ou Drupal.

**Pourquoi PHP 8 ?**
PHP 8 est une version majeure qui a introduit des améliorations significatives en termes de **performance** et de **nouvelles fonctionnalités** qui rendent le code plus moderne, plus sûr et plus expressif. Apprendre PHP 8, c'est se doter des outils les plus récents pour un développement web efficace.

**Comment utiliser ce tutoriel ?**
* Utilisez la **barre latérale** à gauche pour naviguer entre les différentes leçons.
* Chaque leçon contient une **explication du concept** et un **exemple de code PHP**.
* Le **cadre "Exécuteur de Code PHP"** à droite vous permet de :
    * Voir le code de l'exemple.
    * **Modifier le code** à votre guise.
    * Cliquer sur "Exécuter PHP" pour voir le résultat.
    * C'est l'occasion d'expérimenter et de comprendre par la pratique !

Prêt à commencer ? Choisissez une leçon dans le menu de gauche !
                """,
                "code_example": "<?php\n// Bienvenue dans le monde de PHP 8!\n\necho 'Bonjour depuis PHP ' . PHP_VERSION . '!\\n';\n\n// Exercice : Changez le message ci-dessus et exécutez le code.\n?>"
            },
            "Variables et Types": {
                "title": "Variables et Types de Données en PHP",
                "content": """
En PHP, les **variables** commencent par le signe dollar (`$`). PHP est un langage à **typage dynamique**, ce qui signifie que vous n'avez pas besoin de déclarer explicitement le type d'une variable (le type est déterminé à l'exécution). Cependant, PHP 7 et 8 encouragent fortement les **déclarations de type** pour les paramètres de fonction, les valeurs de retour et les propriétés de classe, afin de rendre le code plus robuste et prévisible.

**Types de données scalaires (simples) :**
* **`string`** : Chaînes de caractères (ex: `"Bonjour"`, `'monde'`).
* **`int`** : Nombres entiers (ex: `123`, `-45`).
* **`float`** : Nombres décimaux (ex: `10.5`, `3.14`).
* **`bool`** : Valeurs booléennes (`true` ou `false`).

**Autres types importants :**
* **`array`** : Collections ordonnées ou associatives de valeurs.
* **`object`** : Instances de classes.
* **`null`** : Représente l'absence de valeur.
* **`resource`** : Référence à une ressource externe (ex: connexion à une base de données, fichier ouvert).

**Exercice :** Créez différentes variables avec différents types et affichez-les.
                """,
                "code_example": """<?php
// Déclaration et assignation de variables
$nom = "Alice"; // string
$age = 30; // int
$prix = 19.99; // float
$estActif = true; // bool

echo "Nom : " . $nom . "\\n";
echo "Âge : " . $age . "\\n";
echo "Prix : " . $prix . "\\n";
echo "Actif : " . ($estActif ? "Oui" : "No") . "\\n"; // Utilisation de l'opérateur ternaire

// Déclarations de type (PHP 7+)
function afficherInfo(string $nom, int $age): void {
    echo "L'utilisateur $nom a $age ans.\\n";
}
afficherInfo("Bob", 25);

// Exercice : Essayez de passer un nombre décimal à `afficherInfo` pour voir l'erreur.
// afficherInfo(12.5, 20); // Fatal error: Uncaught TypeError
?>"""
            },
            "Opérateurs": {
                "title": "Les Opérateurs en PHP",
                "content": """
Les **opérateurs** sont des symboles spéciaux qui effectuent des opérations sur des valeurs et des variables.

**Catégories principales :**
* **Arithmétiques** : `+`, `-`, `*`, `/`, `%` (modulo), `**` (exponentiation).
* **Assignation** : `=`, `+=`, `-=`, `*=` etc. (combine une opération et une assignation).
* **Comparaison** : `==` (égalité), `===` (identité - égalité de valeur ET de type), `!=`, `!==`, `<`, `>`, `<=`, `>=`.
* **Logiques** : `and`, `or`, `xor`, `!`, `&&` (ET), `||` (OU).
* **Incrémentation/Décrémentation** : `++` (incrémente de 1), `--` (décrémente de 1).
* **String** : `.` (concaténation), `.` (assignation de concaténation).
* **Null Coalescing Operator (`??`)** : (PHP 7) Retourne la première opérande si elle existe et n'est pas `NULL`, sinon la seconde.
* **Nullsafe Operator (`?->`)** : (PHP 8) Appelle une méthode ou accède à une propriété uniquement si l'objet n'est pas `NULL`.

**Exercice :** Créez des exemples pour chaque type d'opérateur et observez les résultats.
                """,
                "code_example": """<?php
$a = 10;
$b = 3;

echo "--- Opérateurs Arithmétiques ---\\n";
echo "Addition: " . ($a + $b) . "\\n"; // 13
echo "Modulo: " . ($a % $b) . "\\n";   // 1 (reste de la division)
echo "Puissance: " . ($a ** $b) . "\\n"; // 10^3 = 1000

echo "\\n--- Opérateurs d'Assignation ---\\n";
$c = 5;
$c += 2; // $c = $c + 2;
echo "c après += : " . $c . "\\n"; // 7

echo "\\n--- Opérateurs de Comparaison ---\\n";
$x = "5";
$y = 5;
echo "x == y : " . (int)($x == $y) . "\\n";   // 1 (true) - égalité de valeur
echo "x === y : " . (int)($x === $y) . "\\n"; // 0 (false) - pas égalité de type

echo "\\n--- Opérateur Null Coalescing (PHP 7) ---\\n";
$username = $_GET['user'] ?? "Invité"; // Si $_GET['user'] est NULL ou non défini, utilise "Invité"
echo "Utilisateur : " . $username . "\\n"; // Ici, Invité car $_GET n'est pas défini

// Exercice : Essayez de simuler une valeur pour $_GET['user'] et exécutez.
// $_GET['user'] = "Jean";
// echo "Utilisateur (avec GET) : " . ($_GET['user'] ?? "Invité") . "\\n";
?>"""
            },
            "Structures de Contrôle": {
                "title": "Structures de Contrôle du Flux",
                "content": """
Les **structures de contrôle** vous permettent de diriger le flux d'exécution de votre programme en fonction de conditions ou pour répéter des actions.

**Conditions :**
* **`if`, `else`, `elseif`** : Exécutent des blocs de code sous certaines conditions.
* **`switch`** : Permet de choisir parmi de nombreuses alternatives basées sur une seule valeur.
* **`match` expression (PHP 8)** : Une alternative plus moderne et sûre au `switch`.

**Boucles :**
* **`for`** : Pour les boucles avec un nombre connu d'itérations.
* **`while`** : Pour les boucles qui s'exécutent tant qu'une condition est vraie.
* **`do-while`** : Similaire à `while`, mais le bloc de code est exécuté au moins une fois.
* **`foreach`** : Pour parcourir facilement les éléments d'un tableau (array) ou d'un objet.

**Exercice :** Modifiez les conditions et les boucles pour voir comment le comportement du code change.
                """,
                "code_example": """<?php
$heure = 14;

echo "--- Conditions (if/else) ---\\n";
if ($heure < 12) {
    echo "Bonjour (matin) !\\n";
} elseif ($heure < 18) {
    echo "Bon après-midi !\\n";
} else {
    echo "Bonsoir !\\n";
}

$jour = "Mercredi";
echo "\\n--- Conditions (switch) ---\\n";
switch ($jour) {
    case "Lundi":
    case "Mardi":
        echo "C'est le début de la semaine de travail.\\n";
        break;
    case "Mercredi":
        echo "Milieu de semaine.\\n";
        break;
    default:
        echo "Jour de la semaine inconnu ou week-end.\\n";
        break;
}

echo "\\n--- Boucle for ---\\n";
for ($i = 0; $i < 3; $i++) {
    echo "Compteur for : " . $i . "\\n";
}

echo "\\n--- Boucle foreach avec tableau ---\\n";
$fruits = ["Pomme", "Banane", "Orange"];
foreach ($fruits as $fruit) {
    echo "J'aime les " . $fruit . ".\\n";
}

// Exercice : Ajoutez un nouveau fruit au tableau et exécutez.
?>"""
            },
            "Fonctions": {
                "title": "Définir et Utiliser des Fonctions",
                "content": """
Les **fonctions** sont des blocs de code réutilisables qui exécutent une tâche spécifique. Elles permettent d'organiser votre code, de le rendre plus modulaire et facile à maintenir.

**Concepts clés :**
* **Définition :** Utilisez le mot-clé `function` suivi du nom de la fonction, des parenthèses pour les arguments, et d'accolades pour le corps de la fonction.
* **Arguments (Paramètres) :** Les valeurs passées à une fonction. PHP 7+ permet les **déclarations de type** pour les arguments.
* **Valeur de retour :** Une fonction peut retourner une valeur en utilisant le mot-clé `return`. PHP 7+ permet aussi la **déclaration de type de retour**.
* **Arguments nommés (PHP 8)** : Vous pouvez passer des arguments à une fonction en spécifiant leur nom, ce qui améliore la lisibilité et l'ordre n'est plus important.
* **Fonctions fléchées (`fn`) (PHP 7.4+)** : Une syntaxe concise pour les fonctions anonymes simples.

**Exercice :** Créez votre propre fonction qui prend des arguments et retourne une valeur.
                """,
                "code_example": """<?php
// Fonction simple
function saluer(string $nom): string {
    return "Bonjour, " . $nom . " !\\n";
}
echo saluer("Emma");

// Fonction avec plusieurs arguments et type de retour
function additionner(int $num1, int $num2): int {
    return $num1 + $num2;
}
echo "5 + 7 = " . additionner(5, 7) . "\\n";

// Arguments nommés (PHP 8)
function creerUtilisateur(string $nom, int $age, string $ville): string {
    return "Utilisateur : $nom, Âge : $age, Ville : $ville.\\n";
}
echo creerUtilisateur(age: 30, ville: "Paris", nom: "Dupont"); // Ordre différent grâce aux noms

// Fonction fléchée (PHP 7.4+)
$multiplier = fn(int $a, int $b): int => $a * $b;
echo "3 * 4 = " . $multiplier(3, 4) . "\\n";

// Exercice : Créez une fonction qui calcule la surface d'un rectangle.
// function calculerSurfaceRectangle(float $longueur, float $largeur): float {
//     // Votre code ici
// }
// echo "Surface : " . calculerSurfaceRectangle(10.5, 5) . "\\n";
?>"""
            },
            "POO - Bases": {
                "title": "Programmation Orientée Objet (POO) - Bases",
                "content": """
La **Programmation Orientée Objet (POO)** est un paradigme de programmation basé sur le concept d'objets, qui peuvent contenir des données (propriétés) et du code (méthodes). La POO vise à modéliser le monde réel de manière plus intuitive et à rendre le code plus modulaire, réutilisable et facile à maintenir.

**Concepts fondamentaux :**
* **Classe** : Un plan ou un modèle pour créer des objets. Elle définit les propriétés et les méthodes que les objets de ce type auront.
* **Objet** : Une instance concrète d'une classe. Chaque objet a son propre ensemble de valeurs pour les propriétés définies par sa classe.
* **Propriétés** : Les variables qui appartiennent à une classe ou un objet. Elles décrivent l'état de l'objet.
* **Méthodes** : Les fonctions qui appartiennent à une classe ou un objet. Elles définissent le comportement de l'objet.
* **Constructeur (`__construct`)** : Une méthode spéciale appelée automatiquement lors de la création d'un nouvel objet. Elle est utilisée pour initialiser les propriétés de l'objet.
* **Visibilité** :
    * `public` : Accessible de partout.
    * `protected` : Accessible à l'intérieur de la classe et de ses classes descendantes.
    * `private` : Accessible uniquement à l'intérieur de la classe elle-même.

**Exercice :** Créez une classe `Voiture` avec des propriétés comme `marque`, `modèle`, `couleur` et des méthodes comme `demarrer()` et `rouler()`.
                """,
                "code_example": """<?php
class Chien {
    // Propriétés de la classe
    public string $nom;
    public string $race;
    private int $age; // Propriété privée

    // Constructeur : appelé lors de la création d'un objet
    public function __construct(string $nom, string $race, int $age) {
        $this->nom = $nom;
        $this->race = $race;
        $this->age = $age;
        echo "Un nouveau chien " . $this->nom . " est né !\\n";
    }

    // Méthode publique
    public function aboyer(): string {
        return $this->nom . " de race " . $this->race . " aboie : Wouaf !\\n";
    }

    // Méthode pour accéder à la propriété privée
    public function getAge(): int {
        return $this->age;
    }
}

// Création d'un objet (instance de la classe Chien)
$monChien = new Chien("Rex", "Berger Allemand", 5);

// Accéder aux propriétés et appeler les méthodes
echo $monChien->aboyer();
echo $monChien->nom . " a " . $monChien->getAge() . " ans.\\n";

$autreChien = new Chien("Fido", "Labrador", 3);
echo $autreChien->aboyer();

// Exercice : Tentez d'accéder directement à $monChien->age et voyez l'erreur.
// echo $monChien->age; // Fatal error: Uncaught Error: Cannot access private property
?>"""
            },
            "Match Expression": {
                "title": "Match Expression (PHP 8.0)",
                "content": """
L'opérateur **`match`** a été introduit en PHP 8.0 comme une alternative plus puissante, sécurisée et expressive à l'instruction `switch` traditionnelle.

**Avantages clés de `match` par rapport à `switch` :**
* **Est une expression :** `match` retourne une valeur, ce qui signifie que vous pouvez l'assigner directement à une variable ou l'utiliser dans d'autres expressions. Le `switch` est une instruction et ne retourne rien.
* **Comparaison stricte (`===`) :** `match` utilise la comparaison stricte par défaut, ce qui évite les comportements inattendus dus à la conversion de type implicite (`==`) du `switch`.
* **Pas de "fall-through" :** Chaque branche du `match` est exécutée indépendamment. Il n'est pas nécessaire d'utiliser `break;` pour éviter le "fall-through" (où le code continue à s'exécuter dans la branche suivante), ce qui rend le code moins sujet aux erreurs.
* **Peut gérer plusieurs valeurs :** Vous pouvez spécifier plusieurs valeurs pour une même branche en les séparant par des virgules.
* **Doit être exhaustif :** Tous les cas possibles doivent être couverts. Si une valeur ne correspond à aucune branche et qu'il n'y a pas de `default` clause, une `UnhandledMatchError` est levée.

`match` rend le code plus propre et plus facile à lire pour les logiques de branchement complexes.

**Exercice :** Remplacez un `switch` simple par une `match` expression.
                """,
                "code_example": """<?php
$statutHttp = 400;

// Utilisation de la Match Expression (PHP 8.0)
$message = match ($statutHttp) {
    200 => "OK",
    301 => "Redirection permanente",
    400, 401, 403, 404 => "Erreur client", // Plusieurs valeurs pour une branche
    500 => "Erreur serveur interne",
    default => "Statut inconnu" // Obligatoire si tous les cas ne sont pas couverts
};

echo "Le statut HTTP " . $statutHttp . " signifie : " . $message . "\\n";

echo "\\n";

$jourSemaine = "Dimanche";
$typeJour = match ($jourSemaine) {
    "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi" => "Jour de travail",
    "Samedi", "Dimanche" => "Jour de repos",
    default => throw new InvalidArgumentException("Jour invalide") // throw comme expression
};

echo "$jourSemaine est un : " . $typeJour . "\\n";

// Exercice : Changez la valeur de $statutHttp à 200, 301, ou une autre valeur.
// Exercice : Supprimez la ligne `default => ...` et mettez $statutHttp à une valeur non gérée pour voir l'erreur.
?>"""
            },
            "Attributs": {
                "title": "Attributs (PHP 8.0)",
                "content": """
Les **Attributs**, introduits en PHP 8.0, sont une fonctionnalité majeure qui permet d'ajouter des **métadonnées déclaratives** directement dans le code. Ils sont l'équivalent des "annotations" dans d'autres langages (comme Java ou C#).

**Qu'est-ce qu'une métadonnée ?**
C'est une "donnée sur la donnée". Par exemple, un attribut peut indiquer qu'une méthode est une "route" pour un framework web, qu'une propriété doit être validée d'une certaine manière, ou qu'une classe est "dépréciée".

**Syntaxe :**
Les attributs sont définis en utilisant la syntaxe `#[...]` juste au-dessus de l'élément auquel ils s'appliquent (classe, propriété, méthode, fonction, paramètre).

**Avantages :**
* **Amélioration de la lisibilité :** Les configurations et métadonnées sont colocalisées avec le code qu'elles décrivent.
* **Code plus propre :** Réduit le besoin de fichiers de configuration XML/YAML externes ou de commentaires DocBlock surchargés.
* **Facilite l'introspection :** Les attributs peuvent être lus au moment de l'exécution via l'API de **réflexion** de PHP, ce qui permet aux frameworks et aux outils de prendre des décisions basées sur ces métadonnées.

**Exercice :** Créez vos propres attributs et essayez de les lire via la réflexion.
                """,
                "code_example": """<?php
use Attribute; // Nécessaire pour définir un attribut

// Définition d'un attribut simple
#[Attribute(Attribute::TARGET_METHOD)] // Cet attribut ne peut être appliqué qu'aux méthodes
class LogMethodCall {
    public function __construct(public string $message = "Méthode appelée.") {}
}

// Définition d'un attribut pour la validation de propriété
#[Attribute(Attribute::TARGET_PROPERTY)]
class Validate {
    public function __construct(public int $min, public int $max) {}
}

class UserService {
    #[LogMethodCall("Tentative de récupération d'utilisateur.")]
    public function getUserById(int $id): string {
        // Logique de récupération de l'utilisateur
        return "Utilisateur ID: " . $id;
    }

    #[LogMethodCall()] // Utilisation avec le message par défaut
    public function saveUser(string $name): string {
        return "Utilisateur '" . $name . "' enregistré.";
    }

    #[Validate(min: 1, max: 100)]
    public int $score = 50;
}

echo "--- Utilisation des attributs (manuellement, par un framework) ---\\n";

// Exemple de lecture des attributs via la réflexion (comme le ferait un framework)
$service = new UserService();
$reflectionClass = new ReflectionClass($service);

foreach ($reflectionClass->getMethods() as $method) {
    foreach ($method->getAttributes(LogMethodCall::class) as $attribute) {
        $logAttr = $attribute->newInstance(); // Instancie l'objet LogMethodCall
        echo "LOG: " . $logAttr->message . " sur la méthode " . $method->getName() . "\\n";
    }
}

foreach ($reflectionClass->getProperties() as $property) {
    foreach ($property->getAttributes(Validate::class) as $attribute) {
        $validateAttr = $attribute->newInstance();
        echo "VALIDATE: Propriété '" . $property->getName() . "' doit être entre " . $validateAttr->min . " et " . $validateAttr->max . ".\\n";
        // On pourrait ajouter une logique de validation ici
    }
}

echo "\\n--- Exécution des méthodes ---\\n";
echo $service->getUserById(7) . "\\n";
echo $service->saveUser("Julie") . "\\n";

// Exercice : Ajoutez un autre attribut (ex: #[Deprecated]) et essayez de le lire.
?>"""
            },
            "Types d'Union 2.0": {
                "title": "Types d'Union 2.0 (PHP 8.0)",
                "content": """
Les **Types d'Union** (ou Union Types), introduits en PHP 8.0, permettent de déclarer qu'une variable, un paramètre de fonction, ou une valeur de retour peut accepter **plusieurs types différents**. C'est une amélioration significative pour exprimer des intentions de code plus précises.

**Syntaxe :**
Utilisez le caractère `|` (pipe) pour séparer les types possibles. Par exemple, `int|string` signifie que la variable peut être un entier OU une chaîne.

**Avantages :**
* **Flexibilité typée :** Permet une flexibilité là où c'est nécessaire, tout en conservant les avantages du typage statique (meilleure lisibilité, détection d'erreurs plus précoce, meilleures suggestions d'IDE).
* **Moins de code "boilerplate" :** Réduit le besoin de vérifications manuelles de type (`is_int()`, `is_string()`, etc.) à l'intérieur des fonctions.
* **Clarté accrue :** Il est immédiatement clair quels types sont attendus ou peuvent être retournés.

**Points à noter :**
* Vous ne pouvez pas inclure `void` dans un type d'union (car `void` signifie "rien n'est retourné").
* `null` peut être inclus explicitement (`int|string|null`) ou implicitement avec le `?` préfixe (`?int` est équivalent à `int|null`).

**Exercice :** Créez une fonction qui accepte un type d'union et testez-la avec différentes valeurs.
                """,
                "code_example": """<?php
// Exemple de paramètre avec type d'union
function afficherIdentifiant(int|string $id): void {
    echo "L'identifiant est : " . $id . " (Type : " . get_debug_type($id) . ")\\n";
}

afficherIdentifiant(123);       // Fonctionne avec un int
afficherIdentifiant("ABC-789"); // Fonctionne avec une string
// afficherIdentifiant(true); // Fatal error: Uncaught TypeError (bool n'est pas int|string)

echo "\\n";

// Exemple de type de retour avec type d'union
function obtenirValeur(int $choix): int|string|float|null {
    return match ($choix) {
        1 => 100,            // int
        2 => "Hello World",  // string
        3 => 3.14,           // float
        default => null      // null
    };
}

echo "Choix 1 : " . (obtenirValeur(1) ?? "N/A") . "\\n";
echo "Choix 2 : " . (obtenirValeur(2) ?? "N/A") . "\\n";
echo "Choix 3 : " . (obtenirValeur(3) ?? "N/A") . "\\n";
echo "Choix 4 (inconnu) : " . (obtenirValeur(4) ?? "N/A") . "\\n";

echo "\\n";

// Exemple avec les types d'union et les propriétés de classe
class Element {
    public int|string $value;

    public function __construct(int|string $value) {
        $this->value = $value;
    }
}

$elem1 = new Element(42);
$elem2 = new Element("PHP is great!");

echo "Élément 1 : " . $elem1->value . "\\n";
echo "Élément 2 : " . $elem2->value . "\\n";

// Exercice : Modifiez `obtenirValeur` pour inclure un type `bool` et testez.
?>"""
            },
            "Constructeur Property Promotion": {
                "title": "Constructeur Property Promotion (PHP 8.0)",
                "content": """
La **Promotion des Propriétés du Constructeur** (ou Constructor Property Promotion), introduite en PHP 8.0, est une amélioration syntaxique majeure pour les classes. Elle permet de **définir la visibilité et le type des propriétés d'une classe directement dans les arguments du constructeur**.

**Avant PHP 8.0 :**
Il fallait déclarer la propriété, puis la réassigner dans le constructeur, ce qui entraînait beaucoup de code répétitif (boilerplate).

**Avec PHP 8.0 et la promotion des propriétés :**
Le code devient beaucoup plus concis et lisible. PHP se charge automatiquement de créer la propriété de classe avec la visibilité et le type spécifiés, et de lui assigner la valeur de l'argument correspondant.

**Avantages :**
* **Code concis :** Réduit considérablement la quantité de code répétitif pour les propriétés des classes.
* **Lisibilité :** Il est clair en un coup d'œil quelles propriétés sont définies par le constructeur.
* **Maintenance facilitée :** Moins de code, moins de risques d'erreurs et plus facile à modifier.

**Remarque :** Les propriétés promues peuvent avoir n'importe quelle visibilité (`public`, `protected`, `private`). Elles doivent toujours être typées.

**Exercice :** Transformez une classe simple avec un constructeur classique en utilisant la promotion des propriétés.
                """,
                "code_example": """<?php
// Ancien style (avant PHP 8.0)
class UtilisateurAncien {
    public string $nom;
    public int $age;
    private string $email;

    public function __construct(string $nom, int $age, string $email) {
        $this->nom = $nom;
        $this->age = $age;
        $this->email = $email;
    }

    public function getEmail(): string {
        return $this->email;
    }
}

$u1 = new UtilisateurAncien("Alice", 30, "alice@ancien.com");
echo "Ancien style : " . $u1->nom . ", " . $u1->age . " ans, " . $u1->getEmail() . "\\n";

echo "\\n";

// Nouveau style (PHP 8.0) avec Constructeur Property Promotion
class UtilisateurNouveau {
    // Les propriétés sont déclarées directement dans les arguments du constructeur
    public function __construct(
        public string $nom,         // Propriété publique 'nom'
        public int $age,           // Propriété publique 'age'
        private string $email,      // Propriété privée 'email'
        protected string $role = "guest" // Peut avoir une valeur par défaut
    ) {
        // Le corps du constructeur peut être vide ou contenir une logique supplémentaire
        echo "Nouvel utilisateur '" . $this->nom . "' créé.\\n";
    }

    public function getEmail(): string {
        return $this->email;
    }

    public function getRole(): string {
        return $this->role;
    }
}

$u2 = new UtilisateurNouveau("Bob", 25, "bob@nouveau.com");
echo "Nouveau style : " . $u2->nom . ", " . $u2->age . " ans, " . $u2->getEmail() . ", Rôle : " . $u2->getRole() . "\\n";

$u3 = new UtilisateurNouveau("Charlie", 40, "charlie@nouveau.com", "admin");
echo "Nouveau style (avec rôle) : " . $u3->nom . ", " . $u3->age . " ans, " . $u3->getEmail() . ", Rôle : " . $u3->getRole() . "\\n";

// Exercice : Ajoutez une nouvelle propriété 'adresse' à la classe `UtilisateurNouveau` en utilisant la promotion.
?>"""
            },
            "Nullsafe Operator": {
                "title": "Nullsafe Operator (?->) (PHP 8.0)",
                "content": """
L'**Opérateur Nullsafe** (`?->`), introduit en PHP 8.0, est un petit mais très puissant ajout syntaxique qui simplifie la gestion des objets potentiellement `null` dans les chaînes d'appels de méthodes ou d'accès aux propriétés.

**Problématique avant PHP 8.0 :**
Lorsque vous aviez une chaîne d'appels (par exemple, `$utilisateur->adresse->ville->nom`), si l'un des objets intermédiaires (`adresse` ou `ville`) était `null`, PHP déclenchait une `TypeError` (avant PHP 7) ou une `Fatal error` (avec PHP 7). Pour éviter cela, il fallait ajouter des vérifications `if` ou utiliser l'opérateur ternaire, ce qui rendait le code verbeux.

**Fonctionnement de l'Opérateur Nullsafe :**
* Si l'opérande à gauche de `?->` est `NULL`, toute la chaîne d'appels suivante est court-circuitée.
* L'expression entière (par exemple, `$utilisateur->adresse?->ville`) retournera alors `NULL` au lieu de lever une erreur.

**Avantages :**
* **Code concis et lisible :** Élimine le besoin de nombreuses vérifications `if (null !== $obj)` imbriquées.
* **Robustesse :** Prévient les erreurs fatales lorsque des objets peuvent être absents.
* **Simplicité :** Rend le code plus propre et plus facile à comprendre.

**Exercice :** Expérimentez avec des objets qui peuvent être `null` et observez la différence avec et sans l'opérateur Nullsafe.
                """,
                "code_example": """<?php
class User {
    public ?Address $address = null; // ?Address indique que 'address' peut être null
}

class Address {
    public ?string $street = null;
    public ?City $city = null;
}

class City {
    public ?string $name = null;
    public ?string $zipCode = null;
}

// Scénario 1 : L'utilisateur a une adresse et une ville
$user1 = new User();
$user1->address = new Address();
$user1->address->street = "123 Main St";
$user1->address->city = new City();
$user1->address->city->name = "VilleLumineuse";
$user1->address->city->zipCode = "75001";

// Scénario 2 : L'utilisateur n'a pas d'adresse
$user2 = new User();

// Scénario 3 : L'utilisateur a une adresse, mais pas de ville
$user3 = new User();
$user3->address = new Address();
$user3->address->street = "456 Side Ave";

echo "--- Récupération d'informations avec l'opérateur Nullsafe (?->) ---\\n";

// User 1 : Toutes les informations sont présentes
$street1 = $user1->address?->street;
$cityName1 = $user1->address?->city?->name;
$zipCode1 = $user1->address?->city?->zipCode;
echo "User 1 (rue) : " . ($street1 ?? "N/A") . "\\n";
echo "User 1 (ville) : " . ($cityName1 ?? "N/A") . "\\n";
echo "User 1 (code postal) : " . ($zipCode1 ?? "N/A") . "\\n";

echo "\\n";

// User 2 : Pas d'adresse, donc toute la chaîne devient null
$street2 = $user2->address?->street;
$cityName2 = $user2->address?->city?->name;
echo "User 2 (rue) : " . ($street2 ?? "N/A") . "\\n"; // Retourne N/A
echo "User 2 (ville) : " . ($cityName2 ?? "N/A") . "\\n"; // Retourne N/A

echo "\\n";

// User 3 : A une adresse, mais pas de ville
$street3 = $user3->address?->street;
$cityName3 = $user3->address?->city?->name; // $user3->address->city est null
echo "User 3 (rue) : " . ($street3 ?? "N/A") . "\\n";
echo "User 3 (ville) : " . ($cityName3 ?? "N/A") . "\\n"; // Retourne N/A

echo "\\n--- Comparaison avec l'ancien style (plus verbeux) ---\\n";
$oldStreet = null;
if ($user1->address !== null) {
    $oldStreet = $user1->address->street;
}
echo "User 1 (rue, ancien) : " . ($oldStreet ?? "N/A") . "\\n";

$oldCityName = null;
if ($user2->address !== null && $user2->address->city !== null) {
    $oldCityName = $user2->address->city->name;
}
echo "User 2 (ville, ancien) : " . ($oldCityName ?? "N/A") . "\\n";

// Exercice : Ajoutez une propriété `country` à la classe `City` et essayez de l'accéder avec `?->`.
?>"""
            },
            "Expressions Throw": {
                "title": "Expressions `throw` (PHP 8.0)",
                "content": """
En PHP 8.0, l'instruction `throw` est devenue une **expression**. Cela signifie que vous pouvez l'utiliser dans n'importe quel contexte où une expression est attendue, comme :

* Dans les fonctions fléchées (`fn`).
* Dans l'opérateur ternaire (`condition ? vrai : throw Exception`).
* Dans l'opérateur de coalescence nulle (`??`).
* Dans les arguments de fonction ou les propriétés de constructeur avec promotion.
* Dans les branches d'une `match` expression.

**Avantages :**
* **Code plus concis :** Permet d'intégrer la logique de levée d'exception directement dans des expressions, évitant ainsi des blocs `if` ou `try-catch` plus verbeux pour des cas simples.
* **Lisibilité :** La cause de l'erreur est visible là où la condition d'erreur se produit.

Ceci est particulièrement utile pour les validations rapides ou les situations où une valeur par défaut devrait déclencher une erreur si elle n'est pas définie.

**Exercice :** Modifiez une fonction pour utiliser `throw` comme une expression.
                """,
                "code_example": """<?php
// Exemple 1 : Utilisation dans une fonction fléchée
$getPositiveNumber = fn(int $num): int =>
    $num < 0 ? throw new InvalidArgumentException("Le nombre doit être positif.") : $num;

try {
    echo "Nombre positif : " . $getPositiveNumber(10) . "\\n";
    echo "Nombre négatif (va lever une exception) : " . $getPositiveNumber(-5) . "\\n";
} catch (InvalidArgumentException $e) {
    echo "Capture d'erreur : " . $e->getMessage() . "\\n";
}

echo "\\n";

// Exemple 2 : Utilisation avec l'opérateur de coalescence nulle (??)
// Simulez une variable non définie pour déclencher l'exception
// $userId = $_GET['user_id'] ?? throw new Exception("Paramètre 'user_id' manquant.");

try {
    // Supposons que $_GET['user_id'] n'est pas défini pour cet exemple
    $userId = null; // Simule l'absence du paramètre
    $idToProcess = $userId ?? throw new Exception("ID utilisateur est obligatoire.");
    echo "Traitement de l'utilisateur avec ID : " . $idToProcess . "\\n";
} catch (Exception $e) {
    echo "Erreur : " . $e->getMessage() . "\\n";
}

echo "\\n";

// Exemple 3 : Utilisation dans une propriété de constructeur promue (PHP 8.0)
class Product {
    public function __construct(
        public readonly int $id,
        public readonly string $name = throw new InvalidArgumentException("Le nom du produit est requis lors de la création.")
    ) {}
}

try {
    $p1 = new Product(1, "Smartphone");
    echo "Produit créé : " . $p1->name . "\\n";
    $p2 = new Product(2); // Ceci va déclencher l'exception
} catch (InvalidArgumentException $e) {
    echo "Erreur lors de la création du produit : " . $e->getMessage() . "\\n";
}

// Exercice : Intégrez une expression `throw` dans une `match` expression.
?>"""
            },
            "Weak Maps": {
                "title": "Weak Maps (PHP 8.0)",
                "content": """
Les **Weak Maps** (`WeakMap`), introduites en PHP 8.0, sont un type de collection où les clés sont des **références faibles** à des objets.

**Qu'est-ce qu'une référence faible ?**
Normalement, lorsque vous stockez un objet dans un tableau ou une collection, vous créez une "référence forte" à cet objet. Tant qu'il existe au moins une référence forte, l'objet reste en mémoire et n'est pas collecté par le ramasse-miettes (Garbage Collector - GC) de PHP.

Avec une `WeakMap`, si un objet utilisé comme clé n'est plus référencé par aucune autre "référence forte" dans votre programme, l'entrée correspondante dans la `WeakMap` est **automatiquement supprimée**. Le ramasse-miettes peut alors libérer la mémoire de cet objet.

**Cas d'utilisation typiques :**
* **Caches d'objets :** Pour stocker des données calculées ou des états supplémentaires associés à des objets, sans empêcher ces objets d'être libérés de la mémoire lorsqu'ils ne sont plus nécessaires ailleurs.
* **Métadonnées contextuelles :** Associer des informations supplémentaires à des objets tiers (que vous ne pouvez pas modifier) qui doivent exister tant que l'objet lui-même est en vie.
* **Gestionnaires d'événements :** Attacher des gestionnaires d'événements à des objets sans créer de fuites de mémoire.

`WeakMap` est différente de `SplObjectStorage` qui, elle, maintient des références fortes par défaut.

**Exercice :** Observez comment les objets sont "nettoyés" de la `WeakMap` lorsque leurs références fortes sont supprimées.
                """,
                "code_example": """<?php
class CacheableData {
    public string $id;
    public function __construct(string $id) {
        $this->id = $id;
        echo "Objet CacheableData '" . $this->id . "' créé.\\n";
    }
    public function __destruct() {
        echo "Objet CacheableData '" . $this->id . "' détruit.\\n"; // Sera appelé par le GC
    }
}

echo "--- Démonstration de WeakMap ---\\n";

$weakMap = new WeakMap();

// Créons un objet avec une référence forte
$objA = new CacheableData("A");
$weakMap[$objA] = "Données pour l'objet A";

echo "Objet A est-il dans la WeakMap ? " . (isset($weakMap[$objA]) ? "Oui" : "Non") . "\\n";

echo "\\n--- Création d'un objet sans référence forte externe ---\\n";
// L'objet créé ici n'est référencé que par la WeakMap.
// Il sera éligible au ramasse-miettes et son entrée dans la WeakMap sera supprimée.
$weakMap[new CacheableData("B")] = "Données pour l'objet B (sans ref forte)";
// Note : Le destructeur de B peut ne pas s'exécuter immédiatement ici,
// car le GC de PHP fonctionne périodiquement ou lorsque la mémoire est basse.
// Cependant, son entrée dans la WeakMap est logiquement supprimée dès qu'il est candidat.

echo "Objet B créé sans ref forte : (son entrée ne devrait pas persister longtemps si on le recrée)\\n";
// Cette vérification ne fonctionne pas directement car new CacheableData("B_test") est un NOUVEL objet.
// echo "Objet B est-il dans la WeakMap ? " . (isset($weakMap[new CacheableData("B_test")]) ? "Oui" : "Non") . "\\n";


echo "\\n--- Suppression de la référence forte pour l'objet A ---\\n";
unset($objA); // La seule référence forte à $objA est supprimée

// L'objet $objA est maintenant éligible à la collecte, et son entrée dans $weakMap sera supprimée.
// Pour vérifier, on ne peut pas interroger l'objet qui n'existe plus,
// mais le principe est que l'entrée est partie.
// Note : La destruction réelle et la suppression de la map dépendent du cycle du GC.

// Le fait que le __destruct de A soit appelé indique qu'il a été collecté.
// Vous pourriez avoir besoin d'exécuter ce script plusieurs fois ou dans un contexte plus long
// pour voir clairement le __destruct de B s'activer, mais le comportement de la WeakMap est sûr.

echo "\\nFin de la démonstration de WeakMap.\\n";
?>"""
            },
            "null, false, true comme Types": {
                "title": "`null`, `false`, `true` en tant que Types Autonomes (PHP 8.0)",
                "content": """
En PHP 8.0, les valeurs littérales `null`, `false` et `true` peuvent être utilisées comme **types autonomes** dans les déclarations de type. Cela signifie que vous pouvez explicitement déclarer qu'une fonction, une propriété ou un paramètre attend ou retourne spécifiquement l'une de ces valeurs booléennes ou `null`.

**Utilité :**
* **Précision accrue :** Pour les cas où une fonction est spécifiquement conçue pour retourner exactement `null`, `true` ou `false` (et non d'autres valeurs).
* **Amélioration des types d'union :** Ces types peuvent être combinés avec d'autres types d'union pour une flexibilité granulaire.

**Exemples :**
* `function foo(): null` : La fonction doit retourner `null`.
* `function bar(): false` : La fonction doit retourner `false`.
* `function baz(): true` : La fonction doit retourner `true`.

**Remarque :** L'utilisation de `?Type` (ex: `?string`) est un raccourci pour `string|null`. Ainsi, `?int` est identique à `int|null`.

**Exercice :** Créez des fonctions qui retournent spécifiquement `null`, `false` ou `true`.
                """,
                "code_example": """<?php
// Fonction qui retourne spécifiquement null
function trouverPremierPair(array $nombres): ?int { // ?int est équivalent à int|null
    foreach ($nombres as $n) {
        if ($n % 2 === 0) {
            return $n;
        }
    }
    return null; // Retourne explicitement null si aucun pair n'est trouvé
}

echo "Premier pair dans [1, 3, 5] : " . (trouverPremierPair([1, 3, 5]) ?? "Aucun") . "\\n";
echo "Premier pair dans [1, 2, 3] : " . (trouverPremierPair([1, 2, 3]) ?? "Aucun") . "\\n";

echo "\\n";

// Fonction qui retourne spécifiquement false en cas d'échec (pattern ancien ou spécifique)
function validerChaine(string $chaine): bool {
    if (strlen($chaine) < 5) {
        return false; // Échec de la validation
    }
    return true; // Succès de la validation
}

if (validerChaine("hello")) {
    echo "'hello' est valide.\\n";
}
if (!validerChaine("hi")) {
    echo "'hi' est invalide.\\n";
}

echo "\\n";

// Fonction avec un type d'union incluant true et false
function getAccessStatus(int $level): string|true|false {
    return match ($level) {
        1 => true,         // Accès complet
        2 => "limited",    // Accès limité
        default => false   // Pas d'accès
    };
}

$status1 = getAccessStatus(1);
$status2 = getAccessStatus(2);
$status3 = getAccessStatus(99);

echo "Statut niveau 1 : " . (is_bool($status1) ? ($status1 ? "Vrai" : "Faux") : $status1) . "\\n";
echo "Statut niveau 2 : " . (is_bool($status2) ? ($status2 ? "Vrai" : "Faux") : $status2) . "\\n";
echo "Statut niveau 3 : " . (is_bool($status3) ? ($status3 ? "Vrai" : "Faux") : $status3) . "\\n";

// Exercice : Créez une fonction qui accepte un type `true|false` comme paramètre.
?>"""
            },
            "Nouvelles Fonctions String": {
                "title": "Nouvelles Fonctions de Chaîne (PHP 8.0)",
                "content": """
PHP 8.0 a introduit trois fonctions de chaîne très pratiques qui améliorent la lisibilité et la sécurité du code en remplaçant des idiomes plus anciens et moins clairs :

* **`str_contains(string $haystack, string $needle): bool`**
    * Vérifie si une chaîne (`$haystack`) **contient** une sous-chaîne (`$needle`).
    * Retourne `true` si la sous-chaîne est trouvée, `false` sinon.
    * **Avantage :** Plus clair et moins sujet aux erreurs que `strpos($haystack, $needle) !== false`.

* **`str_starts_with(string $haystack, string $needle): bool`**
    * Vérifie si une chaîne (`$haystack`) **commence par** une sous-chaîne (`$needle`).
    * Retourne `true` si la chaîne commence par la sous-chaîne, `false` sinon.

* **`str_ends_with(string $haystack, string $needle): bool`**
    * Vérifie si une chaîne (`$haystack`) **se termine par** une sous-chaîne (`$needle`).
    * Retourne `true` si la chaîne se termine par la sous-chaîne, `false` sinon.

Ces fonctions sont sensibles à la casse. Pour une comparaison insensible à la casse, vous devrez convertir les chaînes en minuscules (`strtolower()`) avant d'utiliser ces fonctions.

**Exercice :** Utilisez ces fonctions pour vérifier différentes conditions sur des chaînes de caractères.
                """,
                "code_example": """<?php
$phrase = "Le langage PHP est puissant et moderne.";

echo "--- str_contains() ---\\n";
echo "La phrase contient 'PHP' : " . (str_contains($phrase, "PHP") ? "Oui" : "Non") . "\\n"; // Oui
echo "La phrase contient 'Java' : " . (str_contains($phrase, "Java") ? "Oui" : "Non") . "\\n"; // Non
echo "La phrase contient 'moderne.' : " . (str_contains($phrase, "moderne.") ? "Oui" : "Non") . "\\n"; // Oui

echo "\\n--- str_starts_with() ---\\n";
echo "La phrase commence par 'Le langage' : " . (str_starts_with($phrase, "Le langage") ? "Oui" : "Non") . "\\n"; // Oui
echo "La phrase commence par 'php' (casse) : " . (str_starts_with($phrase, "php") ? "Oui" : "Non") . "\\n"; // Non (sensible à la casse)
echo "La phrase commence par 'Le' : " . (str_starts_with($phrase, "Le") ? "Oui" : "Non") . "\\n"; // Oui

echo "\\n--- str_ends_with() ---\\n";
echo "La phrase se termine par 'moderne.' : " . (str_ends_with($phrase, "moderne.") ? "Oui" : "Non") . "\\n"; // Oui
echo "La phrase se termine par 'moderne' (sans point) : " . (str_ends_with($phrase, "moderne") ? "Oui" : "Non") . "\\n"; // Non
echo "La phrase se termine par 'ornement.' : " . (str_ends_with($phrase, "ornement.") ? "Oui" : "Non") . "\\n"; // Non

echo "\\n--- Comparaison (ancien vs nouveau) ---\\n";
// Ancien moyen de vérifier si une chaîne contient une sous-chaîne
$hasPhpOld = strpos($phrase, "PHP") !== false;
echo "Ancien méthode 'PHP' : " . ($hasPhpOld ? "Oui" : "Non") . "\\n";

// Exercice : Vérifiez si la phrase commence par "Le langage" de manière insensible à la casse.
// (Indice : strtolower())
?>"""
            },
            "JIT Compiler (Concept)": {
                "title": "JIT (Just In Time) Compiler (PHP 8.0) - Concept",
                "content": """
Le **JIT (Just In Time) Compiler** est l'une des améliorations de performance les plus significatives introduites dans PHP 8.0. C'est une fonctionnalité sous le capot du moteur Zend qui n'affecte pas la syntaxe de votre code PHP, mais qui peut grandement influencer sa vitesse d'exécution.

**Comment PHP fonctionne traditionnellement (avant JIT) ?**
1.  **Parsing :** Le code source PHP est analysé.
2.  **Compilation en opcodes :** Le code est transformé en un format de bytecode appelé "opcodes" par le moteur Zend.
3.  **Exécution des opcodes :** Les opcodes sont exécutés par une machine virtuelle.
4.  **OPcache :** Pour accélérer, l'extension OPcache (obligatoire en production) met en cache ces opcodes compilés en mémoire, évitant ainsi la recompilation à chaque requête.

**Le rôle du JIT :**
Le JIT va un pas plus loin. Il peut identifier les **parties de votre code les plus fréquemment exécutées** (les "hot paths") et les compiler en **code machine natif** juste avant leur exécution. Ce code machine est directement compréhensible par le processeur, ce qui le rend beaucoup plus rapide que l'exécution des opcodes interprétés.

**Impact et cas d'utilisation :**
* **Applications CPU-intensives :** Le JIT est particulièrement bénéfique pour les applications qui effectuent des calculs lourds, des transformations de données complexes, des algorithmes gourmands en CPU, ou des tâches d'apprentissage automatique.
* **Applications web traditionnelles :** Pour les sites web classiques (CMS, e-commerce) qui passent la majeure partie de leur temps à attendre les E/S (entrées/sorties, comme les requêtes de base de données ou réseau), l'impact du JIT est généralement moins spectaculaire. Cependant, il peut toujours apporter des gains marginaux.
* **Configuration :** Le JIT est désactivé par défaut. Il doit être activé et configuré dans le fichier `php.ini` (par exemple, `opcache.jit=1255`).

En résumé, le JIT rend PHP plus compétitif pour les usages au-delà du développement web pur, ouvrant la porte à des applications plus gourmandes en calcul.

**Exercice :** Le code d'exemple montre une fonction de Fibonacci récursive. Exécutez-le pour voir un exemple de code CPU-intensif. Notez que l'impact du JIT ne sera visible qu'en modifiant votre configuration PHP réelle et en mesurant les performances.
                """,
                "code_example": """<?php
// Le JIT est une optimisation de l'exécution au niveau de l'interpréteur,
// pas une fonctionnalité de langage qui se manifeste directement dans le code PHP.
// Cet exemple montre un code CPU-intensif qui pourrait potentiellement bénéficier du JIT.

function fibonacci(int $n): int {
    if ($n <= 1) {
        return $n;
    }
    return fibonacci($n - 1) + fibonacci($n - 2);
}

echo "--- Calculs CPU-intensifs (pour le JIT) ---\\n";

$start = microtime(true);
$result = fibonacci(35); // Un nombre suffisamment grand pour être significatif
$end = microtime(true);

echo "Calcul de Fibonacci de 35 : " . $result . "\\n";
echo "Temps d'exécution : " . round(($end - $start) * 1000, 2) . " ms\\n";

// Pour réellement observer l'effet du JIT, vous devriez :
// 1. Activer et configurer le JIT dans votre php.ini (opcache.jit=1255 par exemple).
// 2. Exécuter ce script plusieurs fois pour que le JIT identifie la fonction fibonacci comme "hot".
// 3. Comparer les temps d'exécution avec le JIT activé et désactivé.

// Informations sur OPcache et JIT (si phpinfo est activé sur votre CLI)
// phpinfo(); // Recherchez 'opcache.enable' et 'opcache.jit'
?>"""
            },
            "Enums": {
                "title": "Enums (PHP 8.1)",
                "content": """
Les **Enums** (énumérations), introduites dans PHP 8.1, sont un ajout très attendu. Elles permettent de définir un ensemble fini, sûr et nommé de cas possibles pour une valeur. C'est une amélioration majeure par rapport aux pratiques antérieures qui utilisaient des constantes de classe, des chaînes de caractères "magiques" ou des entiers, toutes sujettes aux erreurs.

**Avantages :**
* **Sécurité de type :** Vous ne pouvez assigner qu'une des valeurs prédéfinies de l'Enum.
* **Lisibilité :** Le code est beaucoup plus clair et auto-documenté.
* **IntelliSense/Autocomplétion :** Les IDE peuvent facilement suggérer les cas possibles, réduisant les fautes de frappe.
* **Intégration avec `match` :** Les Enums fonctionnent parfaitement avec les `match` expressions pour une logique conditionnelle élégante et exhaustive.

**Types d'Enums :**
1.  **Pure Enums (ou Standard Enums) :** Une simple liste de cas sans valeur scalaire associée.
    ```php
    enum Statut {
        case Brouillon;
        case Publié;
        case Archivé;
    }
    ```
2.  **Backed Enums :** Chaque cas a une valeur scalaire associée (`string` ou `int`). C'est utile si vous devez sérialiser l'Enum (par exemple, la stocker en base de données).
    ```php
    enum Role: string { // 'string' indique que la valeur associée est une chaîne
        case Admin = 'admin';
        case User = 'user';
    }
    ```

**Méthodes d'Enums :**
Les Enums peuvent avoir des méthodes, ce qui permet d'ajouter de la logique métier directement liée aux cas de l'Enum.
`Enum::from(value)` : Crée un cas d'Enum à partir de sa valeur. Lève une `ValueError` si la valeur n'existe pas.
`Enum::tryFrom(value)` : Similaire à `from()`, mais retourne `null` si la valeur n'existe pas.

**Exercice :** Créez une `Backed Enum` pour des statuts de commande et utilisez-la avec une `match` expression.
                """,
                "code_example": """<?php
// Exemple 1 : Pure Enum (Standard Enum)
enum StatutDocument
{
    case BROUILLON;
    case EN_REVUE;
    case PUBLIE;
    case ARCHIVE;

    // Les Enums peuvent avoir des méthodes !
    public function estFinal(): bool {
        return match($this) {
            self::PUBLIE, self::ARCHIVE => true,
            default => false
        };
    }
}

function afficherStatut(StatutDocument $statut): void {
    echo "Document est " . $statut->name; // .name donne le nom du cas (BROUILLON, EN_REVUE etc.)
    if ($statut->estFinal()) {
        echo " et il est dans un état final.";
    }
    echo "\\n";
}

echo "--- Pure Enum (PHP 8.1) ---\\n";
afficherStatut(StatutDocument::BROUILLON);
afficherStatut(StatutDocument::PUBLIE);
echo "Statut ARCHIVE est final ? " . (StatutDocument::ARCHIVE->estFinal() ? "Oui" : "Non") . "\\n";

echo "\\n";

// Exemple 2 : Backed Enum (avec valeur string)
enum NiveauAcces: string {
    case GUEST = 'guest';
    case MEMBER = 'member';
    case MODERATOR = 'moderator';
    case ADMIN = 'admin';

    // Méthode pour obtenir un libellé plus convivial
    public function getLabel(): string {
        return match($this) {
            self::GUEST => "Visiteur",
            self::MEMBER => "Membre enregistré",
            self::MODERATOR => "Modérateur du site",
            self::ADMIN => "Administrateur complet"
        };
    }
}

function verifierAcces(NiveauAcces $niveau): void {
    echo "Niveau d'accès : " . $niveau->getLabel() . " (Valeur : " . $niveau->value . ")\\n";
}

echo "--- Backed Enum (PHP 8.1) ---\\n";
verifierAcces(NiveauAcces::MEMBER);
verifierAcces(NiveauAcces::ADMIN);

// Conversion de valeur en Enum (pour les Backed Enums)
$inputRole = "moderator";
$role = NiveauAcces::tryFrom($inputRole); // tryFrom retourne null si la valeur n'existe pas
if ($role) {
    echo "Rôle à partir de l'entrée '" . $inputRole . "' : " . $role->getLabel() . "\\n";
} else {
    echo "Rôle '" . $inputRole . "' inconnu.\\n";
}

$invalidRole = "super_admin";
$role = NiveauAcces::tryFrom($invalidRole);
if (!$role) {
    echo "Rôle '" . $invalidRole . "' est invalide (tryFrom retourne null).\\n";
}

// Exercice : Créez une Backed Enum `CouleurFeuTricolore` avec des valeurs int (0, 1, 2) et des méthodes.
?>"""
            },
            "Propriétés en Lecture Seule": {
                "title": "Propriétés en Lecture Seule (`readonly`) (PHP 8.1)",
                "content": """
Les **Propriétés en Lecture Seule** (`readonly`), introduites en PHP 8.1, sont un moyen de déclarer des propriétés de classe qui ne peuvent être initialisées **qu'une seule fois**. Après leur initialisation (généralement dans le constructeur), leur valeur ne peut plus être modifiée.

**Pourquoi l'immutabilité ?**
L'**immutabilité** (le fait qu'un objet ne puisse pas changer d'état après sa création) est un concept important en programmation. Elle rend le code :
* **Plus prévisible :** Vous savez que l'état de l'objet ne changera pas de manière inattendue.
* **Plus sûr :** Réduit les bugs liés aux modifications d'état inattendues, surtout dans les systèmes concurrents.
* **Plus facile à tester :** Les objets immuables ont un état fixe, ce qui simplifie les tests unitaires.

**Règles clés des propriétés `readonly` :**
* Elles doivent être **typées** (elles ne peuvent pas être `mixed` si elles sont promues, mais peuvent être `mixed` si elles sont juste déclarées).
* Elles ne peuvent être initialisées qu'une seule fois : soit lors de la déclaration, soit (plus communément) dans le **constructeur** de la classe.
* Elles ne peuvent pas avoir de valeur par défaut directement si elles sont promues via le constructeur.
* Elles ne peuvent pas être des propriétés `static`.
* Vous ne pouvez pas les `unset()` une fois initialisées.

**Exercice :** Créez une classe avec des propriétés `readonly` et essayez de les modifier après la construction pour voir l'erreur.
                """,
                "code_example": """<?php
// Exemple simple de propriété en lecture seule
class Coordonnees {
    public function __construct(
        public readonly int $x, // Propriété 'x' est en lecture seule
        public readonly int $y  // Propriété 'y' est en lecture seule
    ) {}
}

$point = new Coordonnees(10, 20);
echo "Point : x=" . $point->x . ", y=" . $point->y . "\\n";

// Tenter de modifier une propriété readonly après initialisation lève une erreur:
try {
    // $point->x = 30; // Ceci déclencherait une Fatal error: Readonly property Coordonnees::$x cannot be modified
    echo "Tenter de modifier x (commenté) : Tentative bloquée.\\n";
} catch (Error $e) {
    echo "Erreur capturée (attendu) : " . $e->getMessage() . "\\n";
}

echo "\\n";

// Exemple avec une classe d'objet de valeur (Value Object)
class ProductDetails {
    public function __construct(
        public readonly string $sku, // SKU du produit, ne doit pas changer
        public readonly string $name,
        public readonly float $price
    ) {
        if ($price <= 0) {
            throw new InvalidArgumentException("Le prix doit être positif.");
        }
    }

    // Méthode pour créer une nouvelle instance avec un prix modifié (approche immuable)
    public function withNewPrice(float $newPrice): self {
        return new self($this->sku, $this->name, $newPrice);
    }
}

try {
    $productA = new ProductDetails("SKU001", "Laptop", 1200.50);
    echo "Produit A : " . $productA->name . ", Prix : " . $productA->price . "\\n";

    // Modifier le prix en créant un nouvel objet
    $productB = $productA->withNewPrice(1250.00);
    echo "Produit B (nouvel objet) : " . $productB->name . ", Nouveau Prix : " . $productB->price . "\\n";
    echo "Produit A (original inchangé) : " . $productA->name . ", Prix original : " . $productA->price . "\\n";

    // $productA->price = 1300; // Fatal error!
    // $productC = new ProductDetails("SKU003", "Invalid Product", -50); // Lève une InvalidArgumentException
} catch (InvalidArgumentException $e) {
    echo "Erreur : " . $e->getMessage() . "\\n";
}

// Exercice : Créez une classe `Adresse` avec des propriétés `readonly` pour `rue`, `ville`, `codePostal`.
?>"""
            },
            "Final en Constantes de Classe (PHP 8.1)": {
                "title": "Final en Constantes de Classe (PHP 8.1)",
                "content": """
En PHP 8.1, il est désormais possible de marquer les **constantes de classe** avec le mot-clé `final`.

**Que signifie `final` ?**
Lorsqu'une méthode ou une classe est déclarée `final`, elle ne peut pas être redéfinie (écrasée) par les classes descendantes. Appliquer `final` à une constante de classe a un effet similaire : **la valeur de cette constante ne peut pas être modifiée dans les classes qui héritent.**

**Avantages :**
* **Garantie d'immutabilité :** Assure que certaines valeurs fondamentales d'une classe (souvent des configurations ou des identifiants uniques) ne seront jamais altérées par des sous-classes, garantissant ainsi un comportement prévisible.
* **Robustesse du code :** Prévient les modifications accidentelles ou mal intentionnées de constantes critiques.
* **Clarté :** Indique clairement aux développeurs que la valeur de cette constante est fixe et ne doit pas être modifiée dans les héritiers.

Ceci est particulièrement utile pour les constantes qui définissent des valeurs critiques pour la logique d'une librairie ou d'un framework, comme des identifiants d'API, des statuts fixes, etc.

**Exercice :** Créez une classe parente avec une constante `final` et une classe enfant qui tente de la modifier.
                """,
                "code_example": """<?php
class Config {
    // Cette constante ne pourra pas être redéfinie dans les classes enfants
    public const final string VERSION = "1.0.0";
    public const string APP_NAME = "My Application";
}

class NewConfig extends Config {
    // Fatal error: Cannot override final class constant Config::VERSION
    // public const string VERSION = "2.0.0"; // Décommentez pour voir l'erreur !

    // Ceci est autorisé car APP_NAME n'est pas final
    public const string APP_NAME = "My New Application";
}

echo "Version de Config : " . Config::VERSION . "\\n";
echo "Nom de l'App (Config) : " . Config::APP_NAME . "\\n";
echo "Nom de l'App (NewConfig) : " . NewConfig::APP_NAME . "\\n";

echo "\\n";

class ApiClient {
    public const final string API_URL = "https://api.example.com/v1";
    public const int TIMEOUT = 10;
}

class SpecificApiClient extends ApiClient {
    // public const final string API_URL = "https://api.another.com/v2"; // Fatal error si décommenté

    // TIMEOUT peut être modifié car non final
    public const int TIMEOUT = 20;
}

echo "API URL (Client) : " . ApiClient::API_URL . "\\n";
echo "API Timeout (Client) : " . ApiClient::TIMEOUT . "s\\n";
echo "API Timeout (Specific Client) : " . SpecificApiClient::TIMEOUT . "s\\n";

// Exercice : Créez une hiérarchie de classes avec une constante `final` et une autre non `final`,
// et observez les comportements.
?>"""
            },
            "Nouvelle fonction array_is_list (PHP 8.1)": {
                "title": "Nouvelle fonction `array_is_list` (PHP 8.1)",
                "content": """
La fonction **`array_is_list(array $array): bool`**, introduite en PHP 8.1, est un ajout très utile pour déterminer si un tableau est une **liste au sens strict**.

**Qu'est-ce qu'une "liste" en PHP ?**
En PHP, un tableau peut être :
* Un **tableau associatif** (avec des clés de chaîne ou des clés numériques non séquentielles, ex: `['a' => 1, 'b' => 2]`).
* Une **liste** (avec des clés numériques séquentielles, commençant à 0, sans aucun "trou" entre les clés, ex: `[0 => 'a', 1 => 'b', 2 => 'c']` ou simplement `['a', 'b', 'c']`).

`array_is_list()` retourne `true` si le tableau est une liste stricte, et `false` sinon.

**Critères pour qu'un tableau soit une "liste" :**
1.  Les clés du tableau sont des entiers.
2.  Les clés commencent à `0`.
3.  Les clés sont séquentielles (0, 1, 2, ... `count($array) - 1`).

**Avantages :**
* **Clarté du code :** Permet de distinguer facilement les tableaux associatifs des listes, ce qui est crucial pour le traitement des données (par exemple, lors de la sérialisation/désérialisation JSON).
* **Robustesse :** Aide à éviter les erreurs lorsque votre logique attend spécifiquement une liste et non un tableau associatif.

**Exercice :** Testez différents types de tableaux avec `array_is_list()` et observez le comportement.
                """,
                "code_example": """<?php
echo "--- Démonstration de array_is_list() (PHP 8.1) ---\\n";

// 1. Un tableau est une liste s'il a des clés numériques séquentielles commençant par 0
$list1 = ["apple", "banana", "orange"]; // Clés implicites: 0, 1, 2
echo "['apple', 'banana', 'orange'] est une liste : " . (array_is_list($list1) ? "Oui" : "Non") . "\\n"; // Oui

$list2 = [0 => "red", 1 => "green", 2 => "blue"]; // Clés explicites et séquentielles
echo "[0 => 'red', 1 => 'green', 2 => 'blue'] est une liste : " . (array_is_list($list2) ? "Oui" : "Non") . "\\n"; // Oui

echo "\\n";

// 2. Un tableau n'est PAS une liste si les clés ne sont pas séquentielles ou ne commencent pas par 0
$associativeArray = ["name" => "Alice", "age" => 30]; // Clés string
echo "['name' => 'Alice', 'age' => 30] est une liste : " . (array_is_list($associativeArray) ? "Oui" : "Non") . "\\n"; // Non

$sparseArray = [0 => "a", 2 => "c", 1 => "b"]; // Clés numériques, mais non séquentielles (trou à l'index 1 au début)
echo "[0 => 'a', 2 => 'c', 1 => 'b'] est une liste : " . (array_is_list($sparseArray) ? "Oui" : "Non") . "\\n"; // Non (PHP lit l'ordre d'insertion pour déterminer la séquence logique)
                                                                                                                // Correction: l'ordre des éléments n'a pas d'importance, l'ordre des CLÉS sì.
                                                                                                                // array_is_list vérifie si les clés sont 0, 1, 2, ..., N-1, peu importe l'ordre de déclaration.
                                                                                                                // Dans cet exemple, le fait qu'il manque le 1 rend ce tableau non-liste.

$startIndexNotZero = [1 => "first", 2 => "second"]; // Ne commence pas par 0
echo "[1 => 'first', 2 => 'second'] est une liste : " . (array_is_list($startIndexNotZero) ? "Oui" : "Non") . "\\n"; // Non

echo "\\n";

// 3. Cas particuliers
$emptyArray = []; // Un tableau vide est considéré comme une liste
echo "[] (tableau vide) est une liste : " . (array_is_list($emptyArray) ? "Oui" : "Non") . "\\n"; // Oui

$singleElementAssoc = ["a" => 1];
echo "['a' => 1] est une liste : " . (array_is_list($singleElementAssoc) ? "Oui" : "Non") . "\\n"; // Non

$singleElementList = [0 => 1];
echo "[0 => 1] est une liste : " . (array_is_list($singleElementList) ? "Oui" : "Non") . "\\n"; // Oui

// Exercice : Créez un tableau avec des clés numériques mais non séquentielles.
// $myArray = [0 => 'un', 3 => 'trois'];
// echo "Votre tableau est une liste : " . (array_is_list($myArray) ? "Oui" : "Non") . "\\n";
?>"""
            },
            "Intersection Types (PHP 8.1)": {
                "title": "Intersection Types (PHP 8.1)",
                "content": """
Les **Intersection Types** (`TypeA&TypeB`), introduits en PHP 8.1, sont un concept de typage avancé qui complète les Types d'Union. Alors que les Types d'Union (`TypeA|TypeB`) signifient "soit TypeA, soit TypeB", les Types d'Intersection signifient **"doit être à la fois TypeA ET TypeB"**.

**Comment ça marche ?**
Pour qu'une valeur satisfasse un type d'intersection `A&B`, elle doit être une instance d'une classe qui implémente ou hérite de **tous les types spécifiés** dans l'intersection. Typiquement, cela est utilisé avec des **interfaces**.

**Cas d'utilisation courants :**
* **Objets polymorphiques :** Lorsque vous attendez un objet qui non seulement est d'un certain type, mais implémente également une ou plusieurs interfaces spécifiques.
* **Contrats multiples :** Garantir qu'un objet fournit plusieurs fonctionnalités définies par différentes interfaces.
* **Validation plus stricte :** Force les développeurs à fournir des objets qui adhèrent à des comportements combinés.

**Important :** Les types d'intersection ne peuvent être utilisés qu'avec des interfaces ou des classes, pas avec des types scalaires comme `int` ou `string`.

**Exercice :** Créez une classe qui implémente deux interfaces et utilisez un type d'intersection pour son paramètre.
                """,
                "code_example": """<?php
// Définition de deux interfaces
interface Cacheable {
    public function getKey(): string;
    public function toCacheArray(): array;
}

interface Loggable {
    public function toLogString(): string;
}

// Une classe qui implémente les deux interfaces
class UserData implements Cacheable, Loggable {
    public function __construct(
        public readonly int $id,
        public readonly string $name,
        public readonly string $email
    ) {}

    public function getKey(): string {
        return "user_" . $this->id;
    }

    public function toCacheArray(): array {
        return ['id' => $this->id, 'name' => $this->name, 'email' => $this->email];
    }

    public function toLogString(): string {
        return "User(ID: {$this->id}, Name: {$this->name}, Email: {$this->email})";
    }
}

// Fonction qui accepte un type d'intersection : doit être Cacheable ET Loggable
function processObject(Cacheable&Loggable $obj): void {
    echo "Clé de cache : " . $obj->getKey() . "\\n";
    echo "Données pour log : " . $obj->toLogString() . "\\n";
    echo "Données pour cache : " . json_encode($obj->toCacheArray()) . "\\n";
}

echo "--- Utilisation des Intersection Types (PHP 8.1) ---\\n";

$user = new UserData(1, "Alice", "alice@example.com");
processObject($user);

echo "\\n";

// Exemple de classe qui n'implémente qu'une des interfaces
class SimpleCache implements Cacheable {
    public function getKey(): string { return "simple_key"; }
    public function toCacheArray(): array { return ['data' => 'simple']; }
}

$simple = new SimpleCache();
try {
    // processObject($simple); // Fatal error: Uncaught TypeError: Argument #1 ($obj) must be of type Cacheable&Loggable, SimpleCache given
    echo "Tentative de passer SimpleCache (commentée) : aurait causé une erreur de type.\\n";
} catch (TypeError $e) {
    echo "Erreur capturée (attendu) : " . $e->getMessage() . "\\n";
}

// Exercice : Créez deux interfaces `Renderable` et `Clickable` et une classe qui les implémente toutes les deux.
// Utilisez ensuite un type d'intersection pour un paramètre de fonction.
?>"""
            },
            "Gestion des Erreurs et Exceptions": {
                "title": "Gestion des Erreurs et Exceptions",
                "content": """
La **gestion des erreurs et des exceptions** est cruciale pour créer des applications PHP robustes et fiables. Elle permet de réagir élégamment aux problèmes inattendus et d'empêcher votre application de planter.

**Les Erreurs (Errors) :**
En PHP, les erreurs sont des problèmes non catchables qui indiquent généralement des problèmes de syntaxe, des ressources manquantes ou des situations irrécupérables. Avant PHP 7, beaucoup de ces erreurs étaient des "Fatal Errors" qui arrêtaient le script. Depuis PHP 7, la plupart d'entre elles sont devenues des `Throwable` (Exceptions ou Erreurs) et peuvent être interceptées.

**Les Exceptions (`Exception`) :**
Les exceptions sont des objets qui représentent des conditions exceptionnelles (mais gérables) qui interrompent le flux normal du programme.
* Elles sont lancées (`throw`) lorsqu'une condition anormale se produit.
* Elles sont interceptées (`catch`) dans un bloc `try-catch` pour gérer le problème.
* Vous pouvez créer vos propres classes d'exception personnalisées en étendant `Exception`.

**Bloc `try-catch-finally` :**
* **`try`** : Contient le code qui pourrait potentiellement lancer une exception.
* **`catch`** : Intercepte une exception d'un type spécifique (ou de n'importe quel type si `catch (Throwable $e)` est utilisé) et contient le code de gestion de l'erreur.
* **`finally`** : (PHP 5.5+) Le bloc de code dans `finally` est **toujours exécuté**, que l'exception ait été levée et gérée, ou non. C'est idéal pour le nettoyage (fermer des fichiers, des connexions de base de données).

**Les `Throwable` (PHP 7+) :**
`Throwable` est l'interface racine pour tous les objets qui peuvent être lancés via `throw`. Elle est implémentée par la classe `Exception` et la classe `Error` (qui représente les erreurs internes de PHP). Cela permet de capturer à la fois les exceptions classiques et les erreurs du moteur PHP.

**Exercice :** Provoquez une division par zéro et une exception personnalisée, puis gérez-les.
                """,
                "code_example": """<?php
// Exemple 1 : Gestion simple d'une exception
function diviser(float $a, float $b): float {
    if ($b === 0.0) {
        throw new InvalidArgumentException("Division par zéro impossible !");
    }
    return $a / $b;
}

echo "--- Gestion des Exceptions ---\\n";
try {
    echo "10 / 2 = " . diviser(10, 2) . "\\n";
    echo "5 / 0 = " . diviser(5, 0) . "\\n"; // Cette ligne va lancer une exception
    echo "Cette ligne ne sera pas exécutée.\\n";
} catch (InvalidArgumentException $e) {
    echo "ERREUR : " . $e->getMessage() . " (dans " . $e->getFile() . " à la ligne " . $e->getLine() . ")\\n";
} finally {
    echo "Le bloc 'finally' est toujours exécuté, quelle que soit l'issue du try/catch.\\n";
}

echo "\\n";

// Exemple 2 : Création d'une exception personnalisée
class MonExceptionPersonnalisee extends Exception {
    public function __construct(string $message = "", int $code = 0, Throwable $previous = null) {
        parent::__construct($message, $code, $previous);
        // Vous pouvez ajouter une logique de logging ici si nécessaire
        error_log("Une MonExceptionPersonnalisee a été levée : " . $message);
    }

    public function messagePourUtilisateur(): string {
        return "Désolé, une erreur interne est survenue : " . $this->getMessage();
    }
}

function traiterCommande(int $quantite): string {
    if ($quantite <= 0) {
        throw new MonExceptionPersonnalisee("La quantité doit être supérieure à zéro.");
    }
    return "Commande de " . $quantite . " articles traitée.\\n";
}

try {
    echo traiterCommande(5);
    echo traiterCommande(0); // Lève notre exception personnalisée
} catch (MonExceptionPersonnalisee $e) {
    echo "ERREUR PERSONNALISÉE : " . $e->messagePourUtilisateur() . "\\n";
} catch (Throwable $e) { // Capturer toute autre erreur/exception inattendue (PHP 7+)
    echo "Une erreur inattendue de type " . get_class($e) . " est survenue : " . $e->getMessage() . "\\n";
}

// Exercice : Simulez une connexion à une base de données et lancez une exception si la connexion échoue.
?>"""
            },
            "Débogage et Outils": {
                "title": "Débogage et Outils en PHP",
                "content": """
Le **débogage** est une compétence essentielle pour tout développeur. Il s'agit du processus de détection et de correction des bugs (erreurs) dans le code. PHP offre plusieurs outils et approches pour faciliter ce processus.

**1. `echo`, `print_r()`, `var_dump()` :**
Ces fonctions sont les outils les plus basiques pour inspecter les valeurs des variables, les tableaux et les objets à différents points de votre code.
* `echo` : Affiche des chaînes simples.
* `print_r()` : Affiche les informations sur les variables dans un format lisible par l'homme (particulièrement utile pour les tableaux).
* `var_dump()` : Affiche des informations structurées sur une ou plusieurs expressions, y compris leur type et leur valeur. C'est l'outil de débogage le plus puissant pour inspecter les données.

**2. Journalisation (Logging) :**
Utiliser des fonctions comme `error_log()` ou des bibliothèques de journalisation (comme Monolog) pour écrire des messages et des informations d'erreur dans des fichiers journaux. C'est indispensable pour les applications en production où vous ne pouvez pas utiliser d'outils interactifs.

**3. XDebug : Le débogueur professionnel :**
**XDebug** est l'outil de débogage le plus puissant pour PHP. Il s'agit d'une extension PHP qui permet :
* De définir des **points d'arrêt (breakpoints)** dans votre code.
* De **parcourir le code pas à pas** (step-by-step).
* D'inspecter le **contenu de toutes les variables** à chaque étape.
* D'analyser la **pile d'appels (call stack)**.
* De générer des **profils de performance** et des rapports de couverture de code.

Pour utiliser XDebug, vous avez besoin :
* De l'extension XDebug installée et configurée dans votre `php.ini`.
* D'un IDE supportant XDebug (comme VS Code avec l'extension PHP Debug, PhpStorm, ou NetBeans).

**4. Outils de développement des navigateurs :**
Pour le développement web, les outils de développement intégrés à votre navigateur (Developer Tools de Chrome, Firefox, Edge) sont essentiels pour déboguer le code HTML, CSS et JavaScript côté client, ainsi que pour inspecter les requêtes réseau vers votre serveur PHP.

**Exercice :** Utilisez `var_dump()` et `print_r()` sur différents types de données pour voir leurs sorties.
                """,
                "code_example": """<?php
echo "--- Outils de Débogage Basiques ---\\n";

$name = "Alice";
$age = 30;
$city = "Paris";

echo "Affichage avec echo :\\n";
echo "Nom: $name, Âge: $age\\n";

echo "\\n";

$dataArray = [
    "user" => [
        "id" => 1,
        "name" => "Bob",
        "email" => "bob@example.com",
        "roles" => ["admin", "editor"]
    ],
    "status" => "active",
    "last_login" => null
];

echo "Affichage avec print_r() :\\n";
print_r($dataArray); // Utile pour les tableaux, mais sans les types

echo "\\n";

echo "Affichage avec var_dump() :\\n";
var_dump($dataArray, $name, $age); // Le plus détaillé, montre types et valeurs

echo "\\n";

// Exemple d'utilisation de error_log()
// error_log("Ceci est un message de log à " . date('Y-m-d H:i:s'));
// error_log("Données de l'utilisateur: " . json_encode($dataArray));
echo "Des messages de log peuvent être envoyés au journal des erreurs du serveur.\\n";

// Exercice : Modifiez le tableau `$dataArray` et observez la sortie de `var_dump()`.
?>"""
            }
            # Ajoutez plus de leçons ici
        }

    def display_lesson(self, lesson_name):
        lesson_data = self.lessons.get(lesson_name)
        if lesson_data:
            self.lesson_title_label.configure(text=lesson_data["title"])

            self.lesson_text.configure(state="normal")
            self.lesson_text.delete("1.0", "end")
            self.lesson_text.insert("1.0", lesson_data["content"])
            self.lesson_text.configure(state="disabled")

            # Afficher l'exemple de code dans la zone d'exécution
            self.code_input.delete("1.0", "end")
            self.code_input.insert("1.0", lesson_data.get("code_example", "<?php\n// Pas d'exemple de code pour cette leçon.\n?>"))

            # Effacer la sortie précédente
            self.code_output.configure(state="normal")
            self.code_output.delete("1.0", "end")
            self.code_output.configure(state="disabled")

    def execute_php_code(self):
        php_code = self.code_input.get("1.0", "end").strip()

        # Vérifier si PHP est installé et dans le PATH
        try:
            # Tente d'exécuter 'php -v' pour s'assurer que PHP est accessible
            subprocess.run(["php", "-v"], capture_output=True, check=True, text=True, encoding="utf-8")
        except FileNotFoundError:
            self.code_output.configure(state="normal")
            self.code_output.delete("1.0", "end")
            self.code_output.insert("1.0", "Erreur: L'interpréteur PHP est introuvable.\nAssurez-vous que 'php' est dans votre PATH ou spécifiez le chemin complet (ex: C:\\xampp\\php\\php.exe).")
            self.code_output.configure(state="disabled")
            return
        except subprocess.CalledProcessError as e:
            self.code_output.configure(state="normal")
            self.code_output.delete("1.0", "end")
            self.code_output.insert("1.0", f"Erreur lors de la vérification de PHP : {e.stderr}")
            self.code_output.configure(state="disabled")
            return

        # Écrire le code dans un fichier temporaire
        temp_file_path = "temp_php_script.php" # Nom de fichier plus explicite
        try:
            with open(temp_file_path, "w", encoding="utf-8") as f:
                f.write(php_code)

            # Exécuter le fichier PHP avec l'interpréteur PHP
            process = subprocess.run(["php", temp_file_path], capture_output=True, text=True, encoding="utf-8", check=False)

            self.code_output.configure(state="normal")
            self.code_output.delete("1.0", "end")
            self.code_output.insert("1.0", process.stdout)
            if process.stderr:
                self.code_output.insert("end", "\n\n--- Erreur (stderr) ---\n" + process.stderr)
            self.code_output.configure(state="disabled")

        except Exception as e:
            self.code_output.configure(state="normal")
            self.code_output.delete("1.0", "end")
            self.code_output.insert("1.0", f"Une erreur inattendue est survenue : {e}")
            self.code_output.configure(state="disabled")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path) # Nettoyer le fichier temporaire

if __name__ == "__main__":
    # Définir le thème et la couleur de l'interface
    ctk.set_appearance_mode("System")  # Modes: "System" (par défaut), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Thèmes: "blue" (par défaut), "dark-blue", "green"

    app = PHP8LearningApp()
    app.mainloop()