import customtkinter as ctk
import os
import subprocess
import json # Bien que non utilisé pour charger les leçons ici, utile si on les externalise.

class PHP8LearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Apprentissage PHP 8 Avancé avec CTk")
        self.geometry("1100x750") # Taille ajustée pour plus de contenu

        # Configurer la grille principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Barre latérale de navigation ---
        self.sidebar_frame = ctk.CTkScrollableFrame(self, width=200, corner_radius=0) # Ajout d'un scrollbar
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(0, weight=1) # Permettre au contenu de s'étendre

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Apprentissage PHP 8", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Boutons de navigation
        self.sidebar_buttons = {}
        lessons = [
            "Introduction", "Variables et Types", "Opérateurs", "Structures de Contrôle",
            "Fonctions", "POO",
            "--- Nouveautés PHP 8.0 ---", # Séparateur visuel
            "Match Expression", "Attributs", "Types d'Union 2.0",
            "Constructeur Property Promotion", "Nullsafe Operator",
            "Expressions Throw", "Weak Maps",
            "null, false, true comme Types", "Nouvelles Fonctions String",
            "JIT Compiler (Concept)",
            "--- Nouveautés PHP 8.1 ---", # Séparateur visuel
            "Enums", "Propriétés en Lecture Seule"
        ]
        
        # Positionnement des boutons avec un index qui continue malgré les séparateurs
        button_row_index = 1 
        for lesson in lessons:
            if lesson.startswith("---"):
                separator = ctk.CTkLabel(self.sidebar_frame, text=lesson.strip('- ').replace('Nouveautés ', ''), 
                                         font=ctk.CTkFont(size=14, weight="bold"), text_color="gray")
                separator.grid(row=button_row_index, column=0, padx=20, pady=(15, 5), sticky="ew")
            else:
                button = ctk.CTkButton(self.sidebar_frame, text=lesson, command=lambda l=lesson: self.display_lesson(l))
                button.grid(row=button_row_index, column=0, padx=20, pady=5, sticky="ew")
                self.sidebar_buttons[lesson] = button
            button_row_index += 1

        # --- Zone de contenu principale ---
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content_frame.grid_rowconfigure(1, weight=1) # Le textbox de leçon prend plus de place
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        self.lesson_title_label = ctk.CTkLabel(self.main_content_frame, text="", font=ctk.CTkFont(size=24, weight="bold"))
        self.lesson_title_label.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

        self.lesson_text = ctk.CTkTextbox(self.main_content_frame, wrap="word", activate_scrollbars=True, height=250)
        self.lesson_text.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.lesson_text.configure(state="disabled") 

        # --- Zone d'exécution de code ---
        self.code_execution_frame = ctk.CTkFrame(self, corner_radius=0)
        self.code_execution_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.code_execution_frame.grid_columnconfigure(0, weight=1)
        self.code_execution_frame.grid_rowconfigure(1, weight=1) # Le textbox de code prend plus de place

        self.code_label = ctk.CTkLabel(self.code_execution_frame, text="Exécuter du code PHP :", font=ctk.CTkFont(size=16, weight="bold"))
        self.code_label.grid(row=0, column=0, padx=20, pady=5, sticky="nw")

        self.code_input = ctk.CTkTextbox(self.code_execution_frame, height=180, wrap="word") # Hauteur ajustée
        self.code_input.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        self.execute_button = ctk.CTkButton(self.code_execution_frame, text="Exécuter PHP", command=self.execute_php_code)
        self.execute_button.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.output_label = ctk.CTkLabel(self.code_execution_frame, text="Sortie :")
        self.output_label.grid(row=3, column=0, padx=20, pady=5, sticky="nw")

        self.code_output = ctk.CTkTextbox(self.code_execution_frame, height=120, wrap="word") # Hauteur ajustée
        self.code_output.grid(row=4, column=0, padx=20, pady=5, sticky="nsew")
        self.code_output.configure(state="disabled")

        # Charger les données des leçons
        self.load_lesson_data()
        self.display_lesson("Introduction") # Afficher la leçon d'introduction au démarrage

    def load_lesson_data(self):
        # Pour une application réelle, vous pourriez charger ceci depuis un fichier JSON
        # ou une base de données. Ici, nous l'avons en dur pour la simplicité.
        self.lessons = {
            "Introduction": {
                "title": "Introduction à PHP 8",
                "content": """
Bienvenue dans le guide d'apprentissage de **PHP 8** !

PHP 8 est une version majeure du langage PHP, sortie en novembre 2020. Elle apporte de nombreuses améliorations de performance et de nouvelles fonctionnalités qui rendent le code plus propre, plus sûr et plus rapide.

Parmi les nouveautés marquantes, on trouve :
* **Match Expression** : Une alternative plus expressive et sûre au `switch` classique.
* **Attributs (Attributes)** : Un moyen d'ajouter des métadonnées déclaratives.
* **Types d'union 2.0** : Permet de déclarer qu'une variable peut être de plusieurs types différents.
* **JIT (Just In Time Compiler)** : Amélioration significative des performances pour certains types de charges de travail.
* **Constructeur Property Promotion** : Syntaxe raccourcie pour les constructeurs.
* **Nullsafe Operator** : Gère élégamment les chaînes d'appels.
* **Expressions `throw`** : Utilisation de `throw` comme une expression.

PHP 8.1, sorti en novembre 2021, a introduit d'autres fonctionnalités comme les **Enums** et les **propriétés en lecture seule**.
                """,
                "code_example": "<?php\nphpinfo();\n?>"
            },
            "Variables et Types": {
                "title": "Variables et Types de Données",
                "content": """
En PHP, une variable commence par le signe dollar (`$`). PHP est un langage à typage dynamique, ce qui signifie que vous n'avez pas besoin de déclarer le type d'une variable explicitement. Cependant, PHP 7 et 8 encouragent fortement l'utilisation des déclarations de type pour un code plus robuste.

Exemples de types de données scalaires :
* **String** : chaîne de caractères (ex: "Bonjour")
* **Integer** : nombres entiers (ex: 123)
* **Float** : nombres décimaux (ex: 10.5)
* **Boolean** : vrai ou faux (true/false)

Autres types :
* **Array** : collection de valeurs
* **Object** : instance d'une classe
* **Null** : variable sans valeur
* **Resource** : ressource externe (ex: connexion à une base de données)

PHP 8 améliore la gestion des types avec les types d'union et la possibilité de typer avec `null`, `false`, `true`.
                """,
                "code_example": """<?php
$nom: string = "Alice"; // Déclaration de type (PHP 7.4+)
$age: int = 30;
$prix: float = 19.99;
$estActif: bool = true;

echo "Nom : " . $nom . "\\n";
echo "Âge : " . $age . "\\n";
echo "Prix : " . $prix . "\\n";
echo "Actif : " . ($estActif ? "Oui" : "Non") . "\\n";

// Les types d'union (PHP 8)
function displayValue(int|string $value): void {
    echo "La valeur est : " . $value . "\\n";
}
displayValue(123);
displayValue("Bonjour");
?>"""
            },
            "Opérateurs": {
                "title": "Opérateurs PHP",
                "content": """
Les opérateurs sont utilisés pour effectuer des opérations sur les variables et les valeurs.

Catégories d'opérateurs :
* **Arithmétiques** : `+`, `-`, `*`, `/`, `%` (modulo), `**` (exponentiation)
* **Assignation** : `=`, `+=`, `-=`, `*=` etc.
* **Comparaison** : `==`, `===` (identité), `!=`, `!==`, `<`, `>`, `<=`, `>=`
* **Logiques** : `and`, `or`, `xor`, `!`, `&&`, `||`
* **Incrémentation/Décrémentation** : `++`, `--`
* **String** : `.` (concaténation), `.` (assignation de concaténation)
* **Opérateur Null Coalescing (??)** : Introduit en PHP 7, retourne la première opérande si elle existe et n'est pas `NULL`, sinon la seconde.
* **Opérateur Nullsafe (?->)** : Nouvelle en PHP 8. Permet d'éviter les erreurs sur les objets `null` dans les chaînes d'appels.
                """,
                "code_example": """<?php
$a = 10;
$b = 3;

echo "Addition: " . ($a + $b) . "\\n";
echo "Modulo: " . ($a % $b) . "\\n";

$c = null;
$d = "Valeur par défaut";
echo "Null Coalescing: " . ($c ?? $d) . "\\n";

$e = "Hello";
$e .= " World";
echo "Concaténation: " . $e . "\\n";

// Exemple de l'opérateur Nullsafe (voir leçon dédiée)
class User { public ?Address $address = null; }
class Address { public ?string $street = null; }

$user = new User();
// Avant PHP 8: if ($user && $user->address) { $street = $user->address->street; }
$street = $user->address?->street; // PHP 8 Nullsafe Operator
echo "Rue (Nullsafe): " . ($street ?? "Non défini") . "\\n";
?>"""
            },
            "Structures de Contrôle": {
                "title": "Structures de Contrôle",
                "content": """
Les structures de contrôle permettent de diriger le flux d'exécution du programme.

* **Conditions** : `if`, `else`, `elseif`, `switch`
* **Boucles** : `for`, `while`, `do-while`, `foreach`

L'opérateur `match` (PHP 8) est une nouvelle structure de contrôle conditionnelle, plus stricte et expressive que `switch`.
                """,
                "code_example": """<?php
$age = 20;

if ($age >= 18) {
    echo "Majeur.\\n";
} else {
    echo "Mineur.\\n";
}

for ($i = 0; $i < 3; $i++) {
    echo "Boucle for: " . $i . "\\n";
}

$fruits = ["Pomme", "Banane", "Orange"];
foreach ($fruits as $fruit) {
    echo "Fruit: " . $fruit . "\\n";
}

$jour = "Lundi";
switch ($jour) {
    case "Lundi":
        echo "C'est le début de la semaine.\\n";
        break;
    case "Dimanche":
        echo "C'est le week-end.\\n";
        break;
    default:
        echo "Jour inconnu.\\n";
}
?>"""
            },
            "Fonctions": {
                "title": "Fonctions en PHP",
                "content": """
Les fonctions sont des blocs de code réutilisables. Elles peuvent prendre des arguments et retourner une valeur.

PHP 7 a introduit les déclarations de type scalaire et les types de retour, qui sont encore plus importants en PHP 8 pour un code robuste.
Les fonctions fléchées (introduites en PHP 7.4) offrent une syntaxe concise pour les fonctions anonymes simples.
                """,
                "code_example": """<?php
function saluer(string $nom): string {
    return "Bonjour, " . $nom . " !\\n";
}

echo saluer("Sophie");

// Fonction avec arguments nommés (PHP 8)
function createUser(string $name, int $age, string $city): string {
    return "Utilisateur: $name, Age: $age, Ville: $city.\\n";
}
echo createUser(age: 25, city: "Paris", name: "Marc"); // Ordre des arguments non important avec les noms

$addition = fn(int $a, int $b): int => $a + $b; // Fonction fléchée
echo "Somme : " . $addition(5, 7) . "\\n";
?>"""
            },
            "POO": {
                "title": "Programmation Orientée Objet (POO)",
                "content": """
La POO est un paradigme de programmation basé sur le concept d'objets.

Concepts clés :
* **Classes** : Plans pour créer des objets.
* **Objets** : Instances d'une classe.
* **Propriétés** : Variables associées à une classe/objet.
* **Méthodes** : Fonctions associées à une classe/objet.
* **Visibilité** : `public`, `protected`, `private`.
* **Héritage** : Une classe peut hériter des propriétés et méthodes d'une autre (`extends`).
* **Interfaces** : Contrats que les classes doivent respecter (`implements`).
* **Classes abstraites** : Classes qui ne peuvent pas être instanciées directement.

PHP 8 continue d'améliorer la POO avec des fonctionnalités comme la promotion des propriétés de constructeur et les propriétés en lecture seule (PHP 8.1).
                """,
                "code_example": """<?php
class Chien {
    public string $nom;
    public string $race;

    public function __construct(string $nom, string $race) {
        $this->nom = $nom;
        $this->race = $race;
    }

    public function aboyer(): string {
        return $this->nom . " aboie !\\n";
    }
}

$monChien = new Chien("Rex", "Berger Allemand");
echo $monChien->aboyer();
echo "Mon chien s'appelle " . $monChien->nom . ".\\n";

// Exemple d'héritage
class Caniche extends Chien {
    public function __construct(string $nom) {
        parent::__construct($nom, "Caniche");
    }
    public function faireLeBeau(): string {
        return $this->nom . " fait le beau.\\n";
    }
}

$monCaniche = new Caniche("Filou");
echo $monCaniche->aboyer();
echo $monCaniche->faireLeBeau();
?>"""
            },
            "Match Expression": {
                "title": "Match Expression (PHP 8.0)",
                "content": """
L'opérateur `match` est une nouvelle expression en PHP 8.0, plus puissante et sûre que l'instruction `switch`.

Caractéristiques clés :
* **Expression** : Elle **retourne une valeur**, ce qui permet de l'assigner directement à une variable.
* **Comparaison stricte** : Utilise `===` (identité) au lieu de `==`. Cela évite les comportements inattendus dus à la conversion de type.
* **Pas de "fall-through"** : Pas besoin de `break;`. Chaque branche est exécutée indépendamment.
* **Peut gérer plusieurs valeurs** avec une virgule pour une même branche.
* **Doit être exhaustif** : Tous les cas possibles doivent être couverts, ou un cas `default` doit être inclus pour éviter une `UnhandledMatchError`.
                """,
                "code_example": """<?php
$statut = 400;

$message = match ($statut) {
    200 => "OK",
    300, 301 => "Redirection",
    400, 401, 403, 404 => "Erreur client",
    500 => "Erreur serveur",
    default => "Statut inconnu" // Obligatoire si tous les cas ne sont pas énumérés
};

echo "Message de statut : " . $message . "\\n";

$fruit = "banane";
$couleur = match ($fruit) {
    "pomme" => "rouge",
    "banane" => "jaune",
    "orange" => "orange",
    default => "inconnue"
};
echo "La couleur de la " . $fruit . " est " . $couleur . ".\\n";
?>"""
            },
            "Attributs": {
                "title": "Attributs (PHP 8.0)",
                "content": """
Les **Attributs**, introduits en PHP 8.0, permettent d'ajouter des **métadonnées déclaratives** aux classes, propriétés, méthodes, fonctions et paramètres. Ils sont définis en utilisant la syntaxe `#[...]`.

Ils offrent un moyen structuré et natif d'ajouter des informations au code sans affecter sa logique d'exécution. Ces métadonnées peuvent ensuite être lues au moment de l'exécution via la **réflexion**. Cela est très utile pour les frameworks (par exemple, pour la configuration de routes, la validation, la sérialisation, etc.) et les outils d'analyse de code.

Avant les attributs, les développeurs utilisaient souvent des commentaires de DocBlock pour des usages similaires, mais les attributs sont parsés par le langage lui-même, les rendant plus robustes et vérifiables.
                """,
                "code_example": """<?php
use Attribute; // Nécessaire pour définir un attribut

#[Attribute(Attribute::TARGET_METHOD)] // Cet attribut peut être appliqué uniquement aux méthodes
class Route {
    public function __construct(public string $path, public array $methods = ['GET']) {}
}

class ApiController {
    #[Route("/users", methods: ["GET", "POST"])]
    public function listUsers() {
        echo "Afficher la liste des utilisateurs.\\n";
    }

    #[Route("/users/{id}", methods: ["GET"])]
    public function getUser(int $id) {
        echo "Afficher l'utilisateur avec l'ID: " . $id . ".\\n";
    }
}

// Comment un framework pourrait utiliser les attributs:
$reflectionClass = new ReflectionClass(ApiController::class);
foreach ($reflectionClass->getMethods() as $method) {
    foreach ($method->getAttributes(Route::class) as $attribute) {
        $route = $attribute->newInstance(); // Instancie l'objet Route
        echo "Route trouvée: " . $route->path . " (Méthode: " . implode(', ', $route->methods) . ") pour " . $method->getName() . ".\\n";
    }
}
?>"""
            },
            "Types d'Union 2.0": {
                "title": "Types d'Union 2.0 (PHP 8.0)",
                "content": """
Les **Types d'Union** (ou Union Types) permettent de déclarer qu'une variable ou un paramètre peut accepter **plusieurs types différents**. En PHP 8.0, la syntaxe `TypeA|TypeB` est utilisée pour combiner les types.

Cela offre une plus grande flexibilité par rapport aux versions précédentes de PHP où une variable pouvait être soit d'un type, soit `null` (avec `?Type`). Avec les types d'union, vous pouvez spécifier que la variable peut être un `int`, un `float`, ou un `string`, par exemple.

Ils aident à rendre le code plus expressif et à éviter les erreurs de type sans avoir recours à des vérifications manuelles complexes.
                """,
                "code_example": """<?php
// Un paramètre peut être un entier ou une chaîne
function printId(int|string $id): void {
    echo "ID: " . $id . " (Type: " . get_debug_type($id) . ")\\n";
}

printId(123);
printId("abc-456");
// printId(true); // Produirait une TypeError si décommenté (bool n'est pas int|string)

// Type de retour qui peut être int, float, ou null
function calculateResult(int $value): int|float|null {
    if ($value < 0) {
        return null;
    } elseif ($value % 2 == 0) {
        return $value * 2; // int
    } else {
        return $value / 3; // float
    }
}

echo "Résultat 10: " . calculateResult(10) . "\\n";
echo "Résultat 7: " . calculateResult(7) . "\\n";
echo "Résultat -5: " . (calculateResult(-5) ?? "N/A") . "\\n";

// Types d'union avec des classes
class Foo {}
class Bar {}

function processObject(Foo|Bar $obj): void {
    if ($obj instanceof Foo) {
        echo "Ceci est un objet Foo.\\n";
    } elseif ($obj instanceof Bar) {
        echo "Ceci est un objet Bar.\\n";
    }
}

processObject(new Foo());
processObject(new Bar());
?>"""
            },
            "Constructeur Property Promotion": {
                "title": "Constructeur Property Promotion (PHP 8.0)",
                "content": """
Le **Constructeur Property Promotion** (ou Promotion des Propriétés du Constructeur), introduit en PHP 8.0, est une amélioration syntaxique majeure pour les classes. Elle permet de **définir et d'initialiser les propriétés d'une classe directement dans les arguments du constructeur**.

Avant PHP 8, il fallait déclarer la propriété, puis la réassigner dans le constructeur. Avec cette fonctionnalité, le code devient beaucoup plus concis et lisible, réduisant ainsi le "boilerplate code".

Syntaxe : Ajoutez la visibilité (`public`, `protected`, `private`) directement devant les arguments du constructeur.
                """,
                "code_example": """<?php
// Avant PHP 8:
class UserLegacy {
    public string $name;
    public int $age;

    public function __construct(string $name, int $age) {
        $this->name = $name;
        $this->age = $age;
    }
}

$userLegacy = new UserLegacy("Alice", 30);
echo "User Legacy: " . $userLegacy->name . ", " . $userLegacy->age . " ans.\\n";

// Avec Constructeur Property Promotion (PHP 8.0):
class UserPHP8 {
    public function __construct(
        public string $name,
        public int $age,
        private string $email // Peut aussi être private/protected
    ) {}

    public function getEmail(): string {
        return $this->email;
    }
}

$userPhp8 = new UserPHP8("Bob", 25, "bob@example.com");
echo "User PHP 8: " . $userPhp8->name . ", " . $userPhp8->age . " ans, Email: " . $userPhp8->getEmail() . ".\\n";
?>"""
            },
            "Nullsafe Operator": {
                "title": "Nullsafe Operator (?->) (PHP 8.0)",
                "content": """
L'**Opérateur Nullsafe** (`?->`), introduit en PHP 8.0, est un ajout très pratique pour gérer les situations où vous devez accéder à des propriétés ou appeler des méthodes sur des objets qui pourraient être `null`.

Avant PHP 8, il fallait souvent enchaîner des vérifications `if` ou utiliser l'opérateur ternaire pour éviter une `TypeError` si un objet de la chaîne était `null`. L'opérateur nullsafe court-circuite l'exécution de la chaîne si l'élément précédent est `null`, et retourne `null` à la place.

C'est une amélioration significative de la lisibilité du code, réduisant le besoin de multiples vérifications.
                """,
                "code_example": """<?php
class User {
    public ?Address $address = null; // ?Address indique que address peut être null
}

class Address {
    public ?string $street = null;
    public ?City $city = null;
}

class City {
    public ?string $name = null;
    public ?string $zipCode = null;
}

$user1 = new User();
$user1->address = new Address();
$user1->address->street = "123 Main St";
$user1->address->city = new City();
$user1->address->city->name = "Anville";

$user2 = new User(); // $user2->address est null par défaut

echo "--- Utilisation de l'opérateur Nullsafe ---\\n";
$street1 = $user1->address?->street;
$cityName1 = $user1->address?->city?->name;
echo "Rue User 1: " . ($street1 ?? "Non défini") . "\\n";
echo "Ville User 1: " . ($cityName1 ?? "Non défini") . "\\n";

$street2 = $user2->address?->street; // Retourne null car $user2->address est null
$cityName2 = $user2->address?->city?->name; // Retourne null car $user2->address est null
echo "Rue User 2: " . ($street2 ?? "Non défini") . "\\n";
echo "Ville User 2: " . ($cityName2 ?? "Non défini") . "\\n";

echo "\\n--- Comparaison avant PHP 8 (code plus verbeux) ---\\n";
$street_legacy = null;
if ($user1->address !== null) {
    $street_legacy = $user1->address->street;
}
echo "Rue User 1 (Legacy): " . ($street_legacy ?? "Non défini") . "\\n";

$cityName_legacy = null;
if ($user2->address !== null && $user2->address->city !== null) {
    $cityName_legacy = $user2->address->city->name;
}
echo "Ville User 2 (Legacy): " . ($cityName_legacy ?? "Non défini") . "\\n";
?>"""
            },
            "Expressions Throw": {
                "title": "Expressions `throw` (PHP 8.0)",
                "content": """
En PHP 8.0, l'instruction `throw` est devenue une **expression**. Cela signifie que vous pouvez utiliser `throw` dans des contextes où seules des expressions sont normalement autorisées, comme :

* Dans les fonctions fléchées (`fn`).
* Dans l'opérateur ternaire (`condition ? A : throw B`).
* Dans l'opérateur de coalescence nulle (`??`).
* Dans les arguments de fonction ou les propriétés de constructeur avec promotion.

Cette fonctionnalité rend le code plus concis et permet de placer la logique de validation ou d'erreur directement là où elle est nécessaire, sans avoir besoin d'une instruction `if` ou d'un bloc `try-catch` distinct pour des cas simples.
                """,
                "code_example": """<?php
// Exemple dans une fonction fléchée
$calculateDivision = fn(int $a, int $b): float =>
    $b === 0 ? throw new InvalidArgumentException("Division par zéro impossible.") : $a / $b;

try {
    echo "10 / 2 = " . $calculateDivision(10, 2) . "\\n";
    echo "5 / 0 = " . $calculateDivision(5, 0) . "\\n"; // Cette ligne va lancer une exception
} catch (InvalidArgumentException $e) {
    echo "Erreur: " . $e->getMessage() . "\\n";
}

echo "\\n";

// Exemple avec l'opérateur de coalescence nulle (??)
$userName = $_GET['user'] ?? throw new Exception("Paramètre 'user' manquant.");

try {
    // Simuler le paramètre manquant
    echo "Nom d'utilisateur: " . $userName . "\\n"; 
} catch (Exception $e) {
    echo "Erreur lors de la récupération du nom d'utilisateur: " . $e->getMessage() . "\\n";
}

// Exemple dans une propriété de constructeur promue (PHP 8.0)
class Product {
    public function __construct(
        public int $id,
        public string $name = throw new InvalidArgumentException("Le nom du produit est requis.")
    ) {}
}

try {
    $p1 = new Product(1, "Laptop");
    echo "Produit créé: " . $p1->name . "\\n";
    $p2 = new Product(2); // Lance l'exception car le nom est manquant
} catch (InvalidArgumentException $e) {
    echo "Erreur lors de la création du produit: " . $e->getMessage() . "\\n";
}
?>"""
            },
            "Weak Maps": {
                "title": "Weak Maps (PHP 8.0)",
                "content": """
Les **Weak Maps** (cartes faibles), introduites en PHP 8.0, sont un type de collection qui contient des références "faibles" à des objets en tant que clés.

La particularité d'une `WeakMap` est que si un objet utilisé comme clé n'est plus référencé ailleurs dans votre programme (c'est-à-dire, qu'il est sur le point d'être collecté par le ramasse-miettes - garbage collector), l'entrée correspondante dans la `WeakMap` est automatiquement supprimée.

Cela est particulièrement utile pour les **caches d'objets** ou pour associer des données supplémentaires à des objets sans empêcher ces objets d'être libérés de la mémoire lorsque plus personne n'en a besoin. Les `WeakMap` sont couramment utilisées pour la mise en cache de données calculées à partir d'objets, ou pour des gestionnaires d'événements liés à la durée de vie d'un objet.
                """,
                "code_example": """<?php
class CacheableObject {
    public string $id;
    public function __construct(string $id) {
        $this->id = $id;
        echo "Objet " . $this->id . " créé.\\n";
    }
    public function __destruct() {
        echo "Objet " . $this->id . " détruit.\\n";
    }
}

$map = new WeakMap();

// Créons un objet et ajoutons-le à la WeakMap
$obj1 = new CacheableObject("A");
$map[$obj1] = "Données pour objet A";

echo "Dans la WeakMap (après ajout A): " . (isset($map[$obj1]) ? "Oui" : "Non") . "\\n";

// Créons un autre objet, sans le stocker dans une variable forte
$map[new CacheableObject("B")] = "Données pour objet B";

// L'objet "B" n'a pas de référence forte et sera probablement collecté immédiatement
// (le __destruct s'exécutera après la fin du script ou si la mémoire est faible)

echo "Dans la WeakMap (après ajout B sans ref forte): " . (isset($map[new CacheableObject("B_temp")]) ? "Oui" : "Non") . " (N'existe plus si pas de ref forte)\\n";

echo "--- Libération de la référence forte pour l'objet A ---\\n";
unset($obj1); // La seule référence forte à $obj1 est maintenant supprimée

// L'objet "A" est maintenant éligible à la collecte, et son entrée dans la WeakMap sera supprimée
// Note: Le destructeur peut ne pas être appelé immédiatement, dépend du GC de PHP.
// Cependant, l'entrée dans la WeakMap est *logiquement* supprimée.

// Pour vérifier, on ne peut pas interroger l'objet qui n'existe plus, mais on sait que l'entrée est partie.
// Un moyen indirect serait de parcourir la map (pas de foreach direct sur WeakMap en PHP 8.0 pour les clés)
// ou de tenter d'accéder à une clé qui aurait dû exister.

echo "Tenter d'accéder à l'objet A dans WeakMap (après unset): " . (isset($map[$obj1]) ? "Oui" : "Non") . " (Devrait être Non)\\n";

// Pour démontrer l'effet:
$obj3 = new CacheableObject("C");
$map[$obj3] = "Données pour C";
echo "Avant fin du script, objet C dans map: " . (isset($map[$obj3]) ? "Oui" : "Non") . "\\n";

echo "Fin du script.\\n";
?>"""
            },
            "null, false, true comme Types": {
                "title": "`null`, `false`, `true` en tant que Types Autonomes (PHP 8.0)",
                "content": """
En PHP 8.0, `null`, `false` et `true` peuvent désormais être utilisés comme **types autonomes** dans les déclarations de type. Cela signifie que vous pouvez explicitement déclarer qu'une fonction ou une propriété attend ou retourne spécifiquement l'une de ces valeurs.

* `null` comme type : utile si une fonction est spécifiquement conçue pour retourner `null` dans certains cas (par exemple, pour indiquer l'absence de résultat).
* `false` comme type : pour les fonctions qui retournent spécifiquement `false` en cas d'échec (souvent des fonctions de bas niveau).
* `true` comme type : plus rare, mais peut être utilisé pour indiquer un succès sans autre valeur pertinente.

Ces types peuvent également être combinés avec des types d'union.
                """,
                "code_example": """<?php
// Une fonction qui retourne null si un élément n'est pas trouvé
function findItem(array $haystack, string $needle): ?string { // ?string est équivalent à string|null
    return in_array($needle, $haystack) ? $needle : null;
}

$items = ["apple", "banana", "orange"];
echo "Recherche 'apple': " . (findItem($items, "apple") ?? "Non trouvé") . "\\n";
echo "Recherche 'grape': " . (findItem($items, "grape") ?? "Non trouvé") . "\\n";

// Une fonction qui retourne false en cas d'erreur de validation (souvent des API plus anciennes)
function validateLegacy(string $input): bool { // Retourne false en cas d'échec, true sinon
    if (empty($input)) {
        return false;
    }
    return true;
}

if (validateLegacy("abc")) {
    echo "'abc' est valide (par true).\\n";
}
if (!validateLegacy("")) {
    echo "'' n'est pas valide (par false).\\n";
}

// Exemple avec un type d'union (string|bool)
function processStatus(string|bool $status): string {
    if (is_string($status)) {
        return "Statut chaîne: " . $status;
    } elseif ($status === true) {
        return "Statut: VRAI";
    } else { // $status === false
        return "Statut: FAUX";
    }
}

echo processStatus("actif") . "\\n";
echo processStatus(true) . "\\n";
echo processStatus(false) . "\\n";
?>"""
            },
            "Nouvelles Fonctions String": {
                "title": "Nouvelles Fonctions de Chaîne (PHP 8.0)",
                "content": """
PHP 8.0 introduit trois nouvelles fonctions de chaîne très utiles pour des opérations courantes :

* `str_contains(haystack, needle)` : Vérifie si une chaîne (`haystack`) **contient** une sous-chaîne (`needle`).
* `str_starts_with(haystack, needle)` : Vérifie si une chaîne (`haystack`) **commence par** une sous-chaîne (`needle`).
* `str_ends_with(haystack, needle)` : Vérifie si une chaîne (`haystack`) **se termine par** une sous-chaîne (`needle`).

Ces fonctions sont plus intuitives et lisibles que les solutions précédentes basées sur `strpos` (qui retournait `false` ou 0, source potentielle de bugs si 0 était confondu avec `false`). Elles simplifient le code et le rendent moins sujet aux erreurs.
                """,
                "code_example": """<?php
$texte = "Bonjour le monde ! Ceci est un exemple.";

// str_contains
echo "Contient 'monde' : " . (str_contains($texte, "monde") ? "Oui" : "Non") . "\\n"; // Oui
echo "Contient 'PHP' : " . (str_contains($texte, "PHP") ? "Oui" : "Non") . "\\n";     // Non
echo "Contient 'exemple' : " . (str_contains($texte, "exemple") ? "Oui" : "Non") . "\\n"; // Oui

echo "\\n";

// str_starts_with
echo "Commence par 'Bonjour' : " . (str_starts_with($texte, "Bonjour") ? "Oui" : "Non") . "\\n"; // Oui
echo "Commence par 'Salut' : " . (str_starts_with($texte, "Salut") ? "Oui" : "Non") . "\\n";     // Non

echo "\\n";

// str_ends_with
echo "Se termine par 'exemple.' : " . (str_ends_with($texte, "exemple.") ? "Oui" : "Non") . "\\n"; // Oui
echo "Se termine par '!' : " . (str_ends_with($texte, "!") ? "Oui" : "Non") . "\\n";         // Non (car il y a un point ensuite)
echo "Se termine par 'exemple' : " . (str_ends_with($texte, "exemple") ? "Oui" : "Non") . "\\n";   // Non (manque le point)

// Ancien moyen (moins lisible et potentiellement dangereux avec 0)
$pos = strpos($texte, "monde");
echo "Ancien contains 'monde': " . ($pos !== false ? "Oui (pos: $pos)" : "Non") . "\\n";
?>"""
            },
            "JIT Compiler (Concept)": {
                "title": "JIT (Just In Time) Compiler (PHP 8.0)",
                "content": """
Le **JIT (Just In Time) Compiler** est l'une des améliorations de performance les plus significatives introduites dans PHP 8.0.

**Comment PHP fonctionne habituellement (avant JIT) :**
Traditionnellement, PHP est un langage interprété. Le code source PHP est converti en **opcodes** (instructions de bas niveau) par l'interpréteur Zend Engine. Ces opcodes sont ensuite exécutés. Pour améliorer les performances, l'extension **OPcache** met en cache ces opcodes compilés en mémoire, évitant ainsi la recompilation à chaque requête.

**Le rôle du JIT :**
Le JIT va un pas plus loin. Au lieu d'exécuter directement les opcodes, le JIT peut **compiler les sections de code les plus fréquemment exécutées** (les "hot paths") en **code machine natif** directement au moment de l'exécution. Ce code machine natif peut alors s'exécuter beaucoup plus rapidement que les opcodes.

**Impact et Cas d'Utilisation :**
* **Amélioration de la performance CPU intensive :** Le JIT est particulièrement bénéfique pour les applications qui effectuent des calculs intensifs, du traitement de données complexe, des boucles serrées, ou de l'apprentissage automatique, où le code passe beaucoup de temps à s'exécuter plutôt qu'à attendre des I/O (entrées/sorties, comme des requêtes de base de données).
* **Moins d'impact sur le web traditionnel :** Pour les applications web typiques (CMS, e-commerce) qui passent la majeure partie de leur temps à attendre les requêtes de base de données ou les I/O, l'impact du JIT est moins spectaculaire que pour les charges de travail CPU intensives, car le goulot d'étranglement n'est pas le traitement du code PHP lui-même.
* **Configuration :** Le JIT est désactivé par défaut. Il doit être activé et configuré dans le fichier `php.ini` (par exemple, `opcache.jit=1255`).

En résumé, le JIT rend PHP plus compétitif pour les usages au-delà du simple développement web, ouvrant la porte à des applications plus gourmandes en calcul.
                """,
                "code_example": """<?php
// Le JIT est une optimisation de l'exécution au niveau de l'interpréteur,
// pas une fonctionnalité de langage qui se manifeste directement dans le code PHP.
// Cet exemple montre un code CPU-intensif qui pourrait bénéficier du JIT.

function fibonacci(int $n): int {
    if ($n <= 1) {
        return $n;
    }
    return fibonacci($n - 1) + fibonacci($n - 2);
}

$start = microtime(true);
$result = fibonacci(35); // Un nombre suffisamment grand pour être significatif
$end = microtime(true);

echo "Calcul de Fibonacci de 35: " . $result . "\\n";
echo "Temps d'exécution: " . round(($end - $start) * 1000, 2) . " ms\\n";

// Pour réellement voir l'impact du JIT, vous devriez :
// 1. Exécuter ce code avec JIT désactivé (`opcache.jit=0` ou commenté).
// 2. Exécuter ce code avec JIT activé (`opcache.jit=1255` ou autre valeur).
// 3. Comparer les temps d'exécution. Les différences seront plus nettes sur des calculs plus longs.

// Pour vérifier si OPcache et JIT sont activés :
// echo phpinfo(); // Recherchez 'opcache.enable' et 'opcache.jit'
?>"""
            },
            "Enums": {
                "title": "Enums (PHP 8.1)",
                "content": """
Les **Enums** (énumérations) ont été introduites dans PHP 8.1. Elles permettent de définir un ensemble fini, sûr et nommé de cas possibles. C'est une amélioration significative par rapport aux solutions précédentes (constantes de classe, chaînes "magiques", etc.), qui étaient sujettes aux fautes de frappe et moins lisibles.

Il existe deux types d'Enums :
1.  **Pure Enums (ou Standard Enums)** : Simplement une liste de cas sans valeur scalaire associée.
2.  **Backed Enums** : Chaque cas a une valeur scalaire associée (`string` ou `int`), ce qui permet de les sérialiser ou de les stocker facilement.

Les Enums améliorent la lisibilité, la sécurité de type et la prévisibilité du code, notamment lorsqu'elles sont utilisées avec `match` expressions.
                """,
                "code_example": """<?php
// 1. Pure Enum (PHP 8.1)
enum StatutCommande
{
    case EN_ATTENTE;
    case EN_COURS;
    case LIVREE;
    case ANNULEE;

    // Les Enums peuvent aussi avoir des méthodes
    public function description(): string {
        return match($this) {
            self::EN_ATTENTE => "Votre commande est en attente de traitement.",
            self::EN_COURS => "Votre commande est en cours de livraison.",
            self::LIVREE => "Votre commande a été livrée.",
            self::ANNULEE => "Votre commande a été annulée."
        };
    }
}

function processOrder(StatutCommande $statut): void {
    echo $statut->description() . "\\n";
}

echo "--- Pure Enum ---\\n";
processOrder(StatutCommande::EN_ATTENTE);
processOrder(StatutCommande::LIVREE);
// echo StatutCommande::EN_ATTENTE; // Erreur: Cannot convert enum case to string
echo "Nom du statut: " . StatutCommande::EN_ATTENTE->name . "\\n"; // Accès au nom du cas

echo "\\n";

// 2. Backed Enum (PHP 8.1) - avec des valeurs string
enum Role: string {
    case ADMIN = 'admin';
    case USER = 'user';
    case GUEST = 'guest';

    public function label(): string {
        return match($this) {
            self::ADMIN => "Administrateur Système",
            self::USER => "Utilisateur Standard",
            self::GUEST => "Invité du Site"
        };
    }
}

function displayUserRole(Role $role): void {
    echo "Le rôle est : " . $role->label() . " (Valeur: " . $role->value . ")\\n";
}

echo "--- Backed Enum (string) ---\\n";
displayUserRole(Role::ADMIN);
displayUserRole(Role::USER);

// Créer une Enum à partir d'une valeur (si c'est une Backed Enum)
$roleFromValue = Role::tryFrom("guest"); // tryFrom retourne null si la valeur n'existe pas
if ($roleFromValue) {
    echo "Rôle créé à partir de 'guest': " . $roleFromValue->label() . "\\n";
}

// 3. Backed Enum (int) - avec des valeurs int
enum HttpCode: int {
    case OK = 200;
    case NOT_FOUND = 404;
    case SERVER_ERROR = 500;
}

echo "\\n--- Backed Enum (int) ---\\n";
echo "Code HTTP pour OK: " . HttpCode::OK->value . "\\n";
?>"""
            },
            "Propriétés en Lecture Seule": {
                "title": "Propriétés en Lecture Seule (PHP 8.1)",
                "content": """
Les **Propriétés en Lecture Seule** (`readonly`), introduites en PHP 8.1, permettent de déclarer des propriétés de classe qui ne peuvent être initialisées **qu'une seule fois**. Après leur initialisation (généralement dans le constructeur), leur valeur ne peut plus être modifiée.

Ceci est très utile pour créer des objets immuables (dont l'état ne change pas après leur création), ce qui peut simplifier la logique, améliorer la prévisibilité du code et rendre les objets plus faciles à tester et à manipuler, en particulier dans des contextes concurrents ou complexes.

**Règles clés :**
* Elles doivent être typées.
* Elles ne peuvent être initialisées qu'une seule fois (dans la déclaration ou dans le constructeur).
* Elles ne peuvent pas avoir de valeur par défaut si elles sont promues dans le constructeur.
* Elles ne peuvent pas être des propriétés `static`.
* Elles ne peuvent pas être `unset()` une fois initialisées.
                """,
                "code_example": """<?php
class Point {
    public function __construct(
        public readonly int $x, // Propriété en lecture seule
        public readonly int $y
    ) {}
}

$p = new Point(10, 20);
echo "Point: x=" . $p->x . ", y=" . $p->y . "\\n";

// Tenter de modifier une propriété readonly après initialisation entraînera une erreur:
try {
    // $p->x = 30; // Fatal error: Readonly property Point::$x cannot be modified
} catch (Error $e) {
    echo "Erreur (attendu): " . $e->getMessage() . "\\n";
}

// Exemple avec une classe plus complexe
class ImmutableUser {
    public function __construct(
        public readonly int $id,
        public readonly string $name,
        public readonly string $email
    ) {}

    // Méthode pour créer une nouvelle instance avec des données modifiées (immutabilité)
    public function withEmail(string $newEmail): self {
        return new self($this->id, $this->name, $newEmail);
    }
}

$user1 = new ImmutableUser(1, "Alice", "alice@example.com");
echo "User 1: " . $user1->name . " (" . $user1->email . ")\\n";

// Si on veut "modifier" l'email, on crée un nouvel objet
$user2 = $user1->withEmail("alice.new@example.com");
echo "User 2 (nouvel objet): " . $user2->name . " (" . $user2->email . ")\\n";
echo "User 1 (original inchangé): " . $user1->name . " (" . $user1->email . ")\\n";
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

            self.code_output.configure(state="normal")
            self.code_output.delete("1.0", "end")
            self.code_output.configure(state="disabled")

    def execute_php_code(self):
        php_code = self.code_input.get("1.0", "end").strip()

        # Vérifier si PHP est installé et dans le PATH
        try:
            subprocess.run(["php", "-v"], capture_output=True, check=True)
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
        temp_file_path = "temp_code.php"
        try:
            with open(temp_file_path, "w", encoding="utf-8") as f:
                f.write(php_code)

            # Exécuter le fichier PHP avec l'interpréteur PHP
            # Il est recommandé de spécifier le chemin complet de l'exécutable PHP si non dans le PATH
            # Par exemple: ["C:\\xampp\\php\\php.exe", temp_file_path]
            # Ou: ["/usr/bin/php", temp_file_path]
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