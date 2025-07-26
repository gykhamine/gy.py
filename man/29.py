import customtkinter as ctk

class PHPTutorialApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tutoriel PHP Complet: Sécurité & Interactions Avancées")
        self.geometry("1200x850") # Agrandir encore plus la fenêtre

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Ajouter les onglets pour chaque concept
        self.tab_view.add("Introduction")
        self.tab_view.add("Syntaxe & Balises")
        self.tab_view.add("Variables & Types")
        self.tab_view.add("Opérateurs")
        self.tab_view.add("Structures de Contrôle")
        self.tab_view.add("Fonctions")
        self.tab_view.add("Tableaux (Arrays)")
        self.tab_view.add("Superglobales Web")
        self.tab_view.add("Formulaires (GET/POST)")
        self.tab_view.add("Upload de Fichiers") # Nouveau
        self.tab_view.add("Cookies")          # Nouveau
        self.tab_view.add("Sessions & Tokens") # Nouveau (combiné pour la sécurité)
        self.tab_view.add("Sécurité Web (Basique)") # Nouveau

        # Remplir chaque onglet avec son contenu
        self.setup_introduction_tab()
        self.setup_syntax_tags_tab()
        self.setup_variables_types_tab()
        self.setup_operators_tab()
        self.setup_control_structures_tab()
        self.setup_functions_tab()
        self.setup_arrays_tab()
        self.setup_superglobals_tab()
        self.setup_forms_tab()
        self.setup_file_upload_tab()    # Nouvelle méthode
        self.setup_cookies_tab()        # Nouvelle méthode
        self.setup_sessions_tokens_tab() # Nouvelle méthode
        self.setup_web_security_tab()   # Nouvelle méthode

    def create_content_frame(self, parent_tab, title, explanation, code_example, keywords=None):
        """Helper function to create content for each tab, now including keywords."""
        frame = ctk.CTkScrollableFrame(parent_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(pady=(10, 5))

        explanation_label = ctk.CTkLabel(frame, text=explanation, wraplength=1100, justify="left")
        explanation_label.pack(pady=(0, 10))

        if keywords:
            keywords_label = ctk.CTkLabel(frame, text="Mots-clés importants :", font=ctk.CTkFont(weight="bold"))
            keywords_label.pack(pady=(5, 0), anchor="w")
            for keyword, desc in keywords.items():
                keyword_text = f"- **`{keyword}`** : {desc}"
                keyword_line = ctk.CTkLabel(frame, text=keyword_text, wraplength=1100, justify="left")
                keyword_line.pack(pady=(0, 2), anchor="w")
            keyword_separator = ctk.CTkFrame(frame, height=2, fg_color="gray")
            keyword_separator.pack(fill="x", pady=10)


        code_label_text = "Exemple de code PHP :"
        code_label = ctk.CTkLabel(frame, text=code_label_text, font=ctk.CTkFont(weight="bold"))
        code_label.pack(pady=(5, 0), anchor="w")

        code_text_box = ctk.CTkTextbox(frame, width=1050, height=300, activate_scrollbars=True, wrap="word", font=("Courier New", 12))
        code_text_box.insert("0.0", code_example)
        code_text_box.configure(state="disabled") # Rendre le texte non modifiable
        code_text_box.pack(pady=(0, 10))

    def setup_introduction_tab(self):
        title = "Introduction à PHP"
        explanation = (
            "**PHP** (acronyme récursif pour *PHP: Hypertext Preprocessor*) est un langage de script "
            "côté serveur, conçu spécifiquement pour le développement web. Il est intégré dans le "
            "code HTML et est exécuté sur le serveur, générant du HTML qui est ensuite envoyé au "
            "navigateur du client. PHP est gratuit, open-source et fonctionne sur diverses plateformes "
            "(Linux, Windows, macOS) avec des serveurs web comme Apache ou Nginx."
            "\n\n"
            "Sa popularité vient de sa simplicité d'apprentissage, de sa capacité à interagir avec "
            "une multitude de bases de données et de son vaste écosystème de frameworks (Laravel, Symfony) "
            "et de CMS (WordPress, Drupal)."
        )
        code = (
            "<?php\n"
            "    // Un premier programme PHP\n"
            "    echo \"Bonjour, monde !\"; // Affiche un message dans le navigateur\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Introduction"), title, explanation, code)

    def setup_syntax_tags_tab(self):
        title = "Syntaxe de Base et Balises PHP"
        explanation = (
            "Le code PHP est toujours inclus entre des balises spéciales qui délimitent les sections "
            "de code à interpréter par le serveur. Chaque instruction PHP doit se terminer par un "
            "point-virgule (`;`). Les commentaires sont utilisés pour rendre le code compréhensible "
            "sans affecter son exécution."
        )
        keywords = {
            "<?php ?>": "Les balises standard pour ouvrir et fermer un bloc de code PHP. La balise fermante `?>` peut être omise à la fin d'un fichier PHP pur pour éviter les problèmes d'espaces blancs.",
            ";": "Le point-virgule est le terminateur d'instruction en PHP. Il est obligatoire après chaque instruction.",
            "//": "Commentaire sur une seule ligne. Tout ce qui suit `//` jusqu'à la fin de la ligne est ignoré.",
            "#": "Un autre type de commentaire sur une seule ligne (style shell script).",
            "/* */": "Commentaire sur plusieurs lignes. Tout ce qui se trouve entre `/*` et `*/` est ignoré."
        }
        code = (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head><title>Syntaxe PHP</title></head>\n"
            "<body>\n"
            "    <h1>Exemple de Syntaxe PHP</h1>\n"
            "    <?php\n"
            "        // Ceci est la première instruction PHP\n"
            "        echo \"<p>Bonjour depuis le serveur web !</p>\"; // Affiche un paragraphe HTML\n"
            "        # Une autre ligne de commentaire\n"
            "        /*\n"
            "         Ceci est un commentaire\n"
            "         qui peut s'étendre\n"
            "         sur plusieurs lignes.\n"
            "        */\n"
            "        $nom = \"PHP\"; // Déclaration de variable\n"
            "        echo \"<p>Apprendre \" . $nom . \" est passionnant !</p>\";\n"
            "    ?>\n"
            "    <p>Le contenu HTML peut se mélanger au PHP.</p>\n"
            "</body>\n"
            "</html>"
        )
        self.create_content_frame(self.tab_view.tab("Syntaxe & Balises"), title, explanation, code, keywords)

    def setup_variables_types_tab(self):
        title = "Variables et Types de Données"
        explanation = (
            "Les variables sont des conteneurs pour stocker des informations. En PHP, elles commencent "
            "toujours par un signe dollar (`$`) suivi du nom de la variable. PHP est un langage à "
            "**typage dynamique**, ce qui signifie que vous n'avez pas besoin de spécifier le type "
            "de données lors de la déclaration d'une variable; PHP le détermine automatiquement."
            "\n\n"
            "Les principaux types de données en PHP sont :"
            "\n- **Chaînes de caractères (String)**: Séquence de caractères (texte)."
            "\n- **Entiers (Integer)**: Nombres entiers, positifs ou négatifs."
            "\n- **Décimaux (Float/Double)**: Nombres à virgule flottante."
            "\n- **Booléens (Boolean)**: Vrai (`true`) ou Faux (`false`)."
            "\n- **Tableaux (Array)**: Collection de valeurs."
            "\n- **Objets (Object)**: Instances de classes."
            "\n- **NULL**: Variable sans valeur."
            "\n- **Ressource (Resource)**: Référence à une ressource externe (ex: connexion à une base de données)."
        )
        keywords = {
            "$variable": "Syntaxe pour déclarer et utiliser une variable en PHP.",
            "String": "Type de données pour le texte, défini avec des guillemets simples ou doubles (`'texte'` ou `\"texte\"`).",
            "Integer": "Type de données pour les nombres entiers (ex: `10`, `-5`).",
            "Float": "Type de données pour les nombres décimaux (ex: `3.14`, `0.5`).",
            "Boolean": "Type de données pour les valeurs de vérité (`true` ou `false`).",
            "Array": "Type de données pour les collections de valeurs (voir onglet Tableaux).",
            "null": "Valeur spéciale indiquant qu'une variable n'a pas de valeur."
        }
        code = (
            "<?php\n"
            "    $nom = \"Alice\";       // Chaîne de caractères\n"
            "    $age = 25;            // Entier\n"
            "    $taille = 1.75;       // Décimal (float)\n"
            "    $estEtudiant = true;  // Booléen\n"
            "    $fruits = array(\"pomme\", \"banane\"); // Tableau\n"
            "    $aucuneValeur = null; // NULL\n"
            "\n"
            "    echo \"Nom: \" . $nom . \"<br>\";\n"
            "    echo \"Âge: \" . $age . \"<br>\";\n"
            "    echo \"Taille: \" . $taille . \"m<br>\";\n"
            "    echo \"Est étudiant: \" . ($estEtudiant ? 'Oui' : 'Non') . \"<br>\";\n"
            "    echo \"Aucune valeur est: \" . var_dump($aucuneValeur) . \"<br>\";\n"
            "\n"
            "    $variableDynamique = \"Bonjour\";\n"
            "    echo \"Variable Dynamique (string): \" . $variableDynamique . \"<br>\";\n"
            "    $variableDynamique = 123;\n"
            "    echo \"Variable Dynamique (integer): \" . $variableDynamique . \"<br>\";\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Variables & Types"), title, explanation, code, keywords)

    def setup_operators_tab(self):
        title = "Les Opérateurs"
        explanation = (
            "Les opérateurs sont des symboles qui permettent d'effectuer des opérations sur des "
            "variables et des valeurs. PHP possède une riche collection d'opérateurs."
        )
        keywords = {
            "**Opérateurs Arithmétiques**": "Effectuent des calculs mathématiques.",
            "+": "Addition", "-": "Soustraction", "*": "Multiplication", "/": "Division",
            "%": "Modulo (reste de la division)", "**": "Exposant (PHP 5.6+)",
            "**Opérateurs d'Assignation**": "Utilisés pour assigner des valeurs à des variables.",
            "=": "Assignation simple", "+=": "Addition et assignation", "-=": "Soustraction et assignation",
            ".=": "Concaténation et assignation",
            "**Opérateurs de Comparaison**": "Comparent deux valeurs et renvoient un booléen (true/false).",
            "==": "Égalité (valeur)", "===": "Identité (valeur et type)", "!=": "Différent de (valeur)",
            "<>": "Différent de (valeur, alternative à !=)", "!==": "Non identique (valeur ou type)",
            ">": "Supérieur à", "<": "Inférieur à", ">=": "Supérieur ou égal à", "<=": "Inférieur ou égal à",
            "<=>": "Opérateur de vaisseau spatial (PHP 7+, compare et retourne -1, 0, 1)",
            "**Opérateurs Logiques**": "Combinent des conditions booléennes.",
            "&& (and)": "AND logique (vrai si les deux sont vrais)", "|| (or)": "OR logique (vrai si l'un est vrai)",
            "! (not)": "NOT logique (inverse la valeur booléenne)", "xor": "XOR logique (vrai si l'un ou l'autre est vrai, mais pas les deux)"
        }
        code = (
            "<?php\n"
            "    // Opérateurs Arithmétiques\n"
            "    $a = 15; $b = 4;\n"
            "    echo \"\$a + \$b = \" . ($a + $b) . \"<br>\";\n"
            "    echo \"\$a % \$b = \" . ($a % $b) . \"<br>\";\n"
            "    echo \"\$a ** 2 = \" . ($a ** 2) . \"<br>\";\n"
            "\n"
            "    // Opérateurs d'Assignation\n"
            "    $compteur = 0;\n"
            "    $compteur += 5;\n"
            "    echo \"Compteur: \" . $compteur . \"<br>\";\n"
            "    $message = \"Bonjour \";\n"
            "    $message .= \"le monde\";\n"
            "    echo \"Message: \" . $message . \"<br>\";\n"
            "\n"
            "    // Opérateurs de Comparaison\n"
            "    $num = 20; $texteNum = \"20\";\n"
            "    echo \"20 == '20' (valeur): \" . ($num == $texteNum ? 'Vrai' : 'Faux') . \"<br>\";\n"
            "    echo \"20 === '20' (valeur et type): \" . ($num === $texteNum ? 'Vrai' : 'Faux') . \"<br>\";\n"
            "\n"
            "    // Opérateurs Logiques\n"
            "    $estMajeur = true; $aUnPermis = false;\n"
            "    echo \"Peut conduire (Majeur ET Permis): \" . ($estMajeur && $aUnPermis ? 'Oui' : 'Non') . \"<br>\";\n"
            "    echo \"Peut voter (Majeur OU Permis): \" . ($estMajeur || $aUnPermis ? 'Oui' : 'Non') . \"<br>\";\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Opérateurs"), title, explanation, code, keywords)

    def setup_control_structures_tab(self):
        title = "Structures de Contrôle"
        explanation = (
            "Les structures de contrôle régissent le flux d'exécution de votre code, "
            "permettant de prendre des décisions (conditions) ou de répéter des actions (boucles)."
        )
        keywords = {
            "**Structures Conditionnelles**": "Exécutent du code basé sur des conditions.",
            "if": "Exécute un bloc de code si la condition est vraie.",
            "else": "Exécute un bloc de code si la condition `if` est fausse.",
            "elseif (or else if)": "Teste une condition supplémentaire si la précédente était fausse.",
            "switch": "Alternative à de multiples `if...elseif` lorsque vous testez une seule variable par rapport à plusieurs valeurs possibles.",
            "**Structures de Boucle**": "Exécutent un bloc de code de manière répétée.",
            "for": "Utilisée lorsque le nombre d'itérations est connu d'avance.",
            "while": "Exécute un bloc de code tant qu'une condition reste vraie.",
            "do-while": "Exécute le bloc de code au moins une fois, puis répète tant que la condition est vraie.",
            "foreach": "Spécifiquement conçue pour itérer sur les éléments des tableaux.",
            "**Contrôle de Boucle**": "Modifient le comportement des boucles.",
            "break": "Sort immédiatement de la boucle la plus interne.",
            "continue": "Passe à l'itération suivante de la boucle, ignorant le reste du code dans l'itération actuelle."
        }
        code = (
            "<?php\n"
            "    // Condition if/elseif/else\n"
            "    $note = 14;\n"
            "    if ($note >= 16) {\n"
            "        echo \"Très bien !<br>\";\n"
            "    } elseif ($note >= 10) {\n"
            "        echo \"Assez bien.<br>\";\n"
            "    } else {\n"
            "        echo \"Insuffisant.<br>\";\n"
            "    }\n"
            "\n"
            "    // Switch\n"
            "    $jour = \"Mercredi\";\n"
            "    switch ($jour) {\n"
            "        case \"Lundi\": echo \"Début de semaine.<br>\"; break;\n"
            "        case \"Vendredi\": echo \"C'est presque le week-end !<br>\"; break;\n"
            "        default: echo \"Jour de semaine normal.<br>\";\n"
            "    }\n"
            "\n"
            "    // Boucle for\n"
            "    for ($i = 1; $i <= 3; $i++) {\n"
            "        echo \"Compteur: \" . $i . \"<br>\";\n"
            "    }\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Structures de Contrôle"), title, explanation, code, keywords)

    def setup_functions_tab(self):
        title = "Les Fonctions"
        explanation = (
            "Les fonctions sont des blocs de code réutilisables qui encapsulent une logique "
            "spécifique. Elles sont essentielles pour organiser le code, le rendre modulaire, "
            "plus facile à maintenir et à déboguer, et pour éviter la répétition (principe DRY - Don't Repeat Yourself)."
        )
        keywords = {
            "function": "Mot-clé utilisé pour déclarer une fonction personnalisée.",
            "return": "Utilisé à l'intérieur d'une fonction pour renvoyer une valeur au code appelant. Si `return` n'est pas utilisé, la fonction renvoie `null` par défaut.",
            "paramètre": "Variable listée entre parenthèses dans la définition de la fonction, recevant des valeurs lors de l'appel de la fonction.",
            "argument": "La valeur réelle passée à un paramètre lors de l'appel de la fonction."
        }
        code = (
            "<?php\n"
            "    function saluerSimple() { echo \"Bonjour à tous !<br>\"; }\n"
            "    saluerSimple();\n"
            "\n"
            "    function direBonjourA($nom) { echo \"Bonjour, \" . $nom . \" !<br>\"; }\n"
            "    direBonjourA(\"Marie\");\n"
            "\n"
            "    function calculerSomme($num1, $num2) { return $num1 + $num2; }\n"
            "    $total = calculerSomme(10, 20);\n"
            "    echo \"La somme de 10 et 20 est : \" . $total . \"<br>\";\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Fonctions"), title, explanation, code, keywords)

    def setup_arrays_tab(self):
        title = "Les Tableaux (Arrays)"
        explanation = (
            "Les tableaux sont des structures de données fondamentales en PHP, permettant de "
            "stocker plusieurs valeurs sous une seule variable. Ils sont très flexibles et "
            "peuvent contenir des valeurs de types différents. PHP propose trois types principaux de tableaux :"
            "\n\n"
            "1.  **Tableaux indexés (ou numériques)** : Les éléments sont ordonnés et accédés via un index numérique qui commence à 0 par défaut."
            "\n2.  **Tableaux associatifs** : Les éléments sont stockés dans des paires clé-valeur, où les clés sont des chaînes de caractères nommées."
            "\n3.  **Tableaux multidimensionnels** : Des tableaux qui contiennent un ou plusieurs autres tableaux, permettant de stocker des données complexes."
        )
        keywords = {
            "array()": "Fonction utilisée pour créer un tableau. Syntaxe courte `[]` (PHP 5.4+).",
            "index": "Position numérique d'un élément dans un tableau indexé (commence à 0).",
            "clé (key)": "Nom (chaîne de caractères) utilisé pour accéder à un élément dans un tableau associatif.",
            "valeur (value)": "Donnée stockée à un index ou une clé donnée dans le tableau.",
            "foreach": "Boucle dédiée au parcours des tableaux, très pratique pour itérer sur chaque élément.",
            "implode()": "Joint les éléments d'un tableau en une seule chaîne de caractères.",
            "print_r()": "Affiche des informations lisibles sur une variable (particulièrement utile pour les tableaux)."
        }
        code = (
            "<?php\n"
            "    // Tableau Indexé\n"
            "    $legumes = ['Carotte', 'Pomme de terre', 'Oignon'];\n"
            "    echo \"Le premier légume est : \" . $legumes[0] . \"<br>\";\n"
            "    $legumes[1] = 'Tomate';\n"
            "    echo \"Après modification: \" . implode(', ', $legumes) . \"<br>\";\n"
            "\n"
            "    // Tableau Associatif\n"
            "    $utilisateur = ['prenom' => 'Jean', 'nom' => 'Dupont', 'email' => 'jean.dupont@example.com'];\n"
            "    echo \"Email de Jean : \" . $utilisateur['email'] . \"<br>\";\n"
            "    $utilisateur['age'] = 30;\n"
            "    echo \"<pre>\"; print_r($utilisateur); echo \"</pre>\";\n"
            "\n"
            "    // Parcourir un tableau avec foreach\n"
            "    echo \"<h3>Liste des Légumes :</h3>\";\n"
            "    foreach ($legumes as $legume) { echo \"- \" . $legume . \"<br>\"; }\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Tableaux (Arrays)"), title, explanation, code, keywords)

    def setup_superglobals_tab(self):
        title = "Les Superglobales Web"
        explanation = (
            "Les **superglobales** sont des tableaux associatifs prédéfinis par PHP, toujours "
            "disponibles dans tous les scopes de votre script. Elles contiennent des informations "
            "essentielles sur l'environnement d'exécution, la requête HTTP, les sessions, etc. "
            "Elles sont cruciales pour interagir avec le navigateur et le serveur web."
        )
        keywords = {
            "$_GET": "Tableau associatif contenant toutes les variables passées à un script via les paramètres d'URL (méthode HTTP GET).",
            "$_POST": "Tableau associatif contenant toutes les variables passées à un script via le corps d'une requête HTTP POST (typiquement depuis un formulaire).",
            "$_REQUEST": "Tableau associatif qui contient par défaut le contenu de `$_GET`, `$_POST` et `$_COOKIE`. Utile pour un accès générique, mais moins spécifique.",
            "$_SERVER": "Tableau associatif contenant des informations sur le serveur et l'environnement d'exécution, telles que l'adresse IP du client, la méthode de requête, le chemin du script, etc.",
            "$_SESSION": "Tableau associatif utilisé pour stocker des données de session (informations spécifiques à un utilisateur) entre différentes pages. Nécessite `session_start()` pour être utilisé.",
            "$_COOKIE": "Tableau associatif contenant les données des cookies envoyés par le client au serveur.",
            "$_FILES": "Tableau associatif pour gérer les fichiers téléchargés via un formulaire HTML (voir l'onglet 'Upload de Fichiers').",
            "$_ENV": "Tableau associatif contenant les variables d'environnement.",
            "isset()": "Fonction pour vérifier si une variable est définie et non NULL. Essentiel pour vérifier l'existence des clés dans les superglobales.",
            "empty()": "Fonction pour vérifier si une variable est vide (non définie, NULL, chaîne vide, 0, false, tableau vide)."
        }
        code = (
            "<?php\n"
            "    echo \"<h3>Informations via \$_SERVER :</h3>\";\n"
            "    echo \"Chemin du script : \" . htmlspecialchars($_SERVER['PHP_SELF']) . \"<br>\";\n"
            "    echo \"Méthode de requête : \" . htmlspecialchars($_SERVER['REQUEST_METHOD']) . \"<br>\";\n"
            "\n"
            "    echo \"<h3>Données via \$_GET :</h3>\";\n"
            "    if (isset($_GET['produit'])) {\n"
            "        echo \"Produit demandé : \" . htmlspecialchars($_GET['produit']) . \"<br>\";\n"
            "    } else {\n"
            "        echo \"Aucun produit spécifié dans l'URL (ex: ?produit=Livre).<br>\";\n"
            "    }\n"
            "\n"
            "    echo \"<h3>Données via \$_POST :</h3>\";\n"
            "    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['nom_utilisateur'])) {\n"
            "        echo \"Nom d'utilisateur reçu via POST : \" . htmlspecialchars($_POST['nom_utilisateur']) . \"<br>\";\n"
            "    } else {\n"
            "        echo \"Aucune donnée POST pour 'nom_utilisateur' reçue (voir onglet Formulaires).<br>\";\n"
            "    }\n"
            "\n"
            "    session_start(); // Nécessaire pour utiliser \$_SESSION\n"
            "    echo \"<h3>Données de Session (\$_SESSION) :</h3>\";\n"
            "    if (!isset($_SESSION['vues_page'])) {\n"
            "        $_SESSION['vues_page'] = 0;\n"
            "    }\n"
            "    $_SESSION['vues_page']++;\n"
            "    echo \"Cette page a été vue \" . $_SESSION['vues_page'] . \" fois par votre session.<br>\";\n"
            "    // Pour réinitialiser: session_destroy();\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Superglobales Web"), title, explanation, code, keywords)

    def setup_forms_tab(self):
        title = "Formulaires HTML et Méthodes GET/POST"
        explanation = (
            "Les formulaires HTML sont la principale méthode d'interaction entre l'utilisateur "
            "et une application web. PHP traite les données soumises par ces formulaires. "
            "Les deux méthodes HTTP les plus courantes pour soumettre des formulaires sont `GET` et `POST`."
            "\n\n"
            "**Méthode GET** : Les données du formulaire sont ajoutées à l'URL sous forme de paramètres de "
            "chaîne de requête (`?cle=valeur&autre_cle=autre_valeur`). Elles sont accessibles via `$_GET`."
            "\n- **Avantages**: Facile à mettre en signet, les requêtes peuvent être rejouées."
            "\n- **Inconvénients**: Données visibles dans l'URL (insécurité pour données sensibles), limite de taille (environ 2000 caractères)."
            "\n\n"
            "**Méthode POST** : Les données du formulaire sont envoyées dans le corps de la requête HTTP, "
            "non visibles dans l'URL. Elles sont accessibles via `$_POST`."
            "\n- **Avantages**: Plus sécurisé pour les données sensibles (mots de passe), pas de limite de taille (pour les données de texte), permet l'envoi de fichiers."
            "\n- **Inconvénients**: Impossible de mettre en signet directement la requête, le rechargement peut demander une re-soumission."
            "\n\n"
            "**Sécurité**: Toujours valider et filtrer les données reçues des formulaires avant de les utiliser (par exemple, avec `htmlspecialchars()` pour éviter les attaques XSS et `filter_var()` pour la validation de type)."
        )
        keywords = {
            "<form action=\"...\" method=\"...\">": "Balise HTML pour définir un formulaire. `action` spécifie le script PHP qui traitera les données, `method` spécifie la méthode HTTP (GET ou POST).",
            "<input type=\"text\" name=\"...\" />": "Champ de texte. `name` est la clé dans `$_GET` ou `$_POST`.",
            "<input type=\"submit\" />": "Bouton pour soumettre le formulaire.",
            "method=\"GET\"": "Envoie les données via l'URL.",
            "method=\"POST\"": "Envoie les données via le corps de la requête.",
            "htmlspecialchars()": "Convertit les caractères spéciaux en entités HTML, prévenant les attaques XSS.",
            "filter_var()": "Valide et filtre les données (ex: email, URL)."
        }
        code = (
            "\n"
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head><title>Formulaires GET/POST</title></head>\n"
            "<body>\n"
            "    <h2>Formulaire POST (pour données sensibles ou grandes)</h2>\n"
            "    <form action=\"traitement_form.php\" method=\"POST\">\n"
            "        <label for=\"nom_post\">Nom:</label><br>\n"
            "        <input type=\"text\" id=\"nom_post\" name=\"nom_post\" required><br><br>\n"
            "        <label for=\"mdp_post\">Mot de passe:</label><br>\n"
            "        <input type=\"password\" id=\"mdp_post\" name=\"mdp_post\" required><br><br>\n"
            "        <input type=\"submit\" value=\"Envoyer par POST\">\n"
            "    </form>\n"
            "\n"
            "    <h2>Formulaire GET (pour recherche, filtres)</h2>\n"
            "    <form action=\"traitement_form.php\" method=\"GET\">\n"
            "        <label for=\"search_get\">Recherche:</label><br>\n"
            "        <input type=\"search\" id=\"search_get\" name=\"terme_recherche\"><br><br>\n"
            "        <input type=\"submit\" value=\"Rechercher par GET\">\n"
            "    </form>\n"
            "</body>\n"
            "</html>\n"
            "\n"
            "<?php\n"
            "// Fichier PHP (traitement_form.php)\n"
            "\n"
            "    echo \"<h1>Résultat du Traitement du Formulaire</h1>\";\n"
            "\n"
            "    if ($_SERVER['REQUEST_METHOD'] === 'POST') {\n"
            "        echo \"<h2>Données POST :</h2>\";\n"
            "        if (isset($_POST['nom_post']) && isset($_POST['mdp_post'])) {\n"
            "            $nom = htmlspecialchars($_POST['nom_post']);\n"
            "            $mdp = htmlspecialchars($_POST['mdp_post']); // Attention: ne jamais stocker en clair!\n"
            "            echo \"Nom : \" . $nom . \"<br>\";\n"
            "            echo \"Mot de passe (NON SÉCURISÉ ici) : \" . $mdp . \"<br>\";\n"
            "        } else { echo \"Aucune donnée POST reçue.<br>\"; }\n"
            "    }\n"
            "\n"
            "    if ($_SERVER['REQUEST_METHOD'] === 'GET') {\n"
            "        echo \"<h2>Données GET :</h2>\";\n"
            "        if (isset($_GET['terme_recherche']) && !empty($_GET['terme_recherche'])) {\n"
            "            $terme = htmlspecialchars($_GET['terme_recherche']);\n"
            "            echo \"Vous avez recherché : \\\"\" . $terme . \"\\\".<br>\";\n"
            "        } else { echo \"Aucun terme de recherche spécifié.<br>\"; }\n"
            "    }\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Formulaires (GET/POST)"), title, explanation, code, keywords)

    # --- Nouvelle méthode pour l'Upload de Fichiers ---
    def setup_file_upload_tab(self):
        title = "Upload de Fichiers"
        explanation = (
            "Permettre aux utilisateurs de télécharger des fichiers est une fonctionnalité courante "
            "dans les applications web. PHP gère les fichiers téléchargés via la superglobale "
            "**`$_FILES`**. C'est un processus délicat qui nécessite des validations rigoureuses "
            "pour des raisons de sécurité."
            "\n\n"
            "**Étapes clés pour un upload sécurisé :**\n"
            "1.  **Formulaire HTML**: Assurez-vous que l'attribut `enctype=\"multipart/form-data\"` est défini dans la balise `<form>`. Utilisez `type=\"file\"` pour l'input.\n"
            "2.  **Vérification des erreurs**: `$_FILES['input_name']['error']` indique si une erreur s'est produite pendant l'upload.\n"
            "3.  **Validation du Type**: Vérifiez le type MIME (`$_FILES['input_name']['type']`) et l'extension du fichier. Ne vous fiez JAMAIS uniquement à l'extension fournie par le client.\n"
            "4.  **Validation de la Taille**: `$_FILES['input_name']['size']` vous permet de vérifier la taille du fichier. Définissez des limites dans `php.ini` (`upload_max_filesize`, `post_max_size`).\n"
            "5.  **Déplacement du Fichier**: Utilisez `move_uploaded_file()` pour déplacer le fichier temporaire (`$_FILES['input_name']['tmp_name']`) vers son emplacement final sécurisé sur le serveur.\n"
            "6.  **Sécurité du Nom de Fichier**: Nettoyez le nom de fichier pour éviter les attaques par traversée de répertoire ou l'injection de code."
        )
        keywords = {
            "$_FILES": "Superglobale utilisée pour accéder aux informations des fichiers téléchargés.",
            "enctype=\"multipart/form-data\"": "Attribut obligatoire dans la balise `<form>` pour permettre l'upload de fichiers.",
            "move_uploaded_file()": "Fonction PHP sécurisée pour déplacer un fichier téléchargé de son emplacement temporaire vers sa destination finale. **Indispensable**.",
            "upload_max_filesize": "Directive dans `php.ini` qui limite la taille maximale d'un fichier téléchargé.",
            "post_max_size": "Directive dans `php.ini` qui limite la taille totale des données d'une requête POST, y compris les fichiers.",
            "mime_content_type()": "Fonction PHP pour obtenir le type MIME réel d'un fichier, plus fiable que le type fourni par le client."
        }
        code = (
            "\n"
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head><title>Upload de Fichier</title></head>\n"
            "<body>\n"
            "    <h2>Télécharger un Fichier</h2>\n"
            "    <form action=\"upload_handler.php\" method=\"POST\" enctype=\"multipart/form-data\">\n"
            "        <label for=\"fichier\">Sélectionner un fichier (Max 2MB):</label><br>\n"
            "        <input type=\"file\" id=\"fichier\" name=\"mon_fichier\" required><br><br>\n"
            "        <input type=\"submit\" value=\"Uploader\">\n"
            "    </form>\n"
            "</body>\n"
            "</html>\n"
            "\n"
            "<?php\n"
            "// Fichier PHP (upload_handler.php)\n"
            "\n"
            "    $targetDir = \"uploads/\"; // Assurez-vous que ce répertoire existe et est inscriptible !\n"
            "    $uploadOk = 1;\n"
            "\n"
            "    if (isset($_FILES[\"mon_fichier\"])) {\n"
            "        $file = $_FILES[\"mon_fichier\"];\n"
            "        $fileName = basename($file[\"name\"]);\n"
            "        $targetFilePath = $targetDir . $fileName;\n"
            "        $fileType = strtolower(pathinfo($targetFilePath, PATHINFO_EXTENSION));\n"
            "\n"
            "        // 1. Vérifier les erreurs d'upload\n"
            "        if ($file['error'] !== UPLOAD_ERR_OK) {\n"
            "            echo \"Erreur d'upload: \" . $file['error'] . \"<br>\";\n"
            "            $uploadOk = 0;\n"
            "        }\n"
            "\n"
            "        // 2. Vérifier la taille du fichier (ici, max 2MB = 2 * 1024 * 1024 octets)\n"
            "        if ($file[\"size\"] > 2097152) {\n"
            "            echo \"Désolé, votre fichier est trop volumineux (max 2MB).<br>\";\n"
            "            $uploadOk = 0;\n"
            "        }\n"
            "\n"
            "        // 3. Autoriser certains formats de fichier (types MIME)\n"
            "        $allowedTypes = array('jpg', 'png', 'jpeg', 'gif', 'pdf');\n"
            "        if (!in_array($fileType, $allowedTypes)) {\n"
            "            echo \"Désolé, seuls les fichiers JPG, JPEG, PNG, GIF & PDF sont autorisés.<br>\";\n"
            "            $uploadOk = 0;\n"
            "        }\n"
            "\n"
            "        // 4. Vérifier si $uploadOk est à 0 par une erreur\n"
            "        if ($uploadOk == 0) {\n"
            "            echo \"Votre fichier n'a pas été téléchargé.<br>\";\n"
            "        } else {\n"
            "            // 5. Déplacer le fichier téléchargé\n"
            "            if (move_uploaded_file($file[\"tmp_name\"], $targetFilePath)) {\n"
            "                echo \"Le fichier \" . htmlspecialchars(basename($file[\"name\"])) . \" a été téléchargé avec succès.<br>\";\n"
            "                echo \"Chemin : \" . $targetFilePath . \"<br>\";\n"
            "            } else {\n"
            "                echo \"Désolé, une erreur s'est produite lors du téléchargement de votre fichier.<br>\";\n"
            "            }\n"
            "        }\n"
            "    } else {\n"
            "        echo \"Aucun fichier n'a été envoyé.<br>\";\n"
            "    }\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Upload de Fichiers"), title, explanation, code, keywords)

    # --- Nouvelle méthode pour les Cookies ---
    def setup_cookies_tab(self):
        title = "Les Cookies"
        explanation = (
            "Les **cookies** sont de petits fichiers texte stockés par le serveur web sur l'ordinateur "
            "du client via le navigateur. Ils sont utilisés pour **persister des informations** "
            "entre différentes requêtes HTTP, car HTTP est un protocole sans état. "
            "Les cookies sont couramment utilisés pour la personnalisation de sites, "
            "la mémorisation des informations de connexion, le suivi des utilisateurs, etc."
            "\n\n"
            "**Points clés :**\n"
            "1.  **Création**: Un cookie est créé sur le serveur avec `setcookie()` et envoyé au navigateur via les en-têtes HTTP.\n"
            "2.  **Accès**: En PHP, les cookies envoyés par le client sont accessibles via la superglobale **`$_COOKIE`**.\n"
            "3.  **Durée de vie**: Les cookies ont une durée de vie. Sans expiration, ils sont détruits à la fermeture du navigateur (cookies de session). Avec une expiration, ils persistent.\n"
            "4.  **Sécurité**: Les cookies peuvent être interceptés. Utilisez les options `secure` et `httponly` pour renforcer leur sécurité.\n"
            "5.  **RGPD/Vie privée**: Dans de nombreuses régions, le consentement de l'utilisateur est requis pour l'utilisation de certains cookies."
        )
        keywords = {
            "setcookie()": "Fonction PHP pour définir un cookie. Doit être appelée AVANT toute sortie HTML.",
            "$_COOKIE": "Superglobale PHP qui contient les données des cookies envoyées par le navigateur.",
            "name": "Nom du cookie.",
            "value": "Valeur du cookie.",
            "expire": "Timestamp Unix indiquant quand le cookie expire (ex: `time() + 3600` pour 1 heure).",
            "path": "Chemin sur le serveur où le cookie sera disponible (ex: `/` pour tout le site).",
            "domain": "Domaine pour lequel le cookie est valable.",
            "secure": "Si `true`, le cookie ne sera envoyé qu'avec une connexion HTTPS.",
            "httponly": "Si `true`, le cookie ne sera accessible que via HTTP(S) et pas par JavaScript (protection contre les attaques XSS)."
        }
        code = (
            "<?php\n"
            "// Fichier PHP (gestion_cookies.php)\n"
            "\n"
            "    // --- Création / Définition d'un cookie ---\n"
            "    // Définir un cookie qui expire dans 1 heure\n"
            "    // setcookie('nom_utilisateur', 'Alice', time() + 3600, '/');\n"
            "    // setcookie('derniere_visite', date('Y-m-d H:i:s'), time() + (86400 * 30), '/'); // 30 jours\n"
            "\n"
            "    // Pour tester, décommentez les lignes ci-dessus, actualisez, puis commentez-les pour lire.\n"
            "    // Assurez-vous que setcookie() est appelée AVANT TOUT output HTML.\n"
            "\n"
            "    // --- Lecture des cookies ---\n"
            "    echo \"<h2>Gestion des Cookies</h2>\";\n"
            "    if (isset($_COOKIE['nom_utilisateur'])) {\n"
            "        echo \"Bonjour, \" . htmlspecialchars($_COOKIE['nom_utilisateur']) . \" !<br>\";\n"
            "    } else {\n"
            "        echo \"Cookie 'nom_utilisateur' non trouvé.<br>\";\n"
            "        echo \"Pour le créer, décommentez la ligne `setcookie('nom_utilisateur', 'Alice', ...)` dans le code et actualisez la page.<br>\";\n"
            "    }\n"
            "\n"
            "    if (isset($_COOKIE['derniere_visite'])) {\n"
            "        echo \"Votre dernière visite était le : \" . htmlspecialchars($_COOKIE['derniere_visite']) . \"<br>\";\n"
            "    }\n"
            "\n"
            "    // --- Suppression d'un cookie ---\n"
            "    // Pour supprimer un cookie, définissez sa date d'expiration dans le passé.\n"
            "    // setcookie('nom_utilisateur', '', time() - 3600, '/'); // Supprime le cookie 'nom_utilisateur'\n"
            "    // echo \"<br>Cookie 'nom_utilisateur' supprimé (si la ligne de suppression est active).<br>\";\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Cookies"), title, explanation, code, keywords)

    # --- Nouvelle méthode pour les Sessions et Tokens ---
    def setup_sessions_tokens_tab(self):
        title = "Sessions & Tokens de Sécurité"
        explanation = (
            "Les **sessions PHP** sont un mécanisme puissant pour stocker des informations "
            "utilisateur sur le serveur et les rendre disponibles à travers plusieurs pages. "
            "Contrairement aux cookies (stockés côté client), les données de session sont "
            "stockées côté serveur, et seul un identifiant de session (généralement dans un cookie) "
            "est envoyé au client. Cela rend les sessions plus sécurisées pour les données sensibles."
            "\n\n"
            "**Comment ça marche :**\n"
            "1.  **Démarrage**: `session_start()` doit être appelée au début de chaque script PHP où vous souhaitez utiliser les sessions.\n"
            "2.  **Stockage**: Les données sont stockées dans la superglobale **`$_SESSION`**.\n"
            "3.  **Identifiant de session**: PHP génère un identifiant unique (PHPSESSID) qui est souvent stocké dans un cookie sur le client.\n"
            "4.  **Destruction**: `session_destroy()` supprime toutes les données de session du serveur."
            "\n\n"
            "**Tokens de Sécurité (CSRF, JWT)** : Les sessions sont souvent utilisées conjointement avec des tokens pour renforcer la sécurité."
            "\n- **Tokens CSRF (Cross-Site Request Forgery)** : Petites valeurs secrètes et uniques générées côté serveur et incluses dans les formulaires HTML. Elles protègent contre les attaques où un attaquant tente de faire exécuter à un utilisateur authentifié une action non désirée."
            "\n- **Tokens JWT (JSON Web Tokens)** : Utilisés pour l'authentification et l'autorisation dans les API et microservices. Ils sont auto-contenus et signés cryptographiquement, permettant de vérifier l'intégrité et l'authenticité des informations."
        )
        keywords = {
            "session_start()": "Fonction essentielle pour démarrer une session. Doit être appelée au tout début du script.",
            "$_SESSION": "Superglobale pour stocker et récupérer les données de session.",
            "session_destroy()": "Détruit toutes les données enregistrées dans la session actuelle.",
            "session_unset()": "Libère toutes les variables de session actuellement enregistrées.",
            "session_id()": "Récupère ou définit l'ID de session actuel.",
            "CSRF Token": "Jeton de sécurité généré côté serveur et inclus dans les formulaires pour prévenir les attaques CSRF.",
            "JWT (JSON Web Token)": "Standard ouvert et compact pour créer des jetons d'accès qui transmettent des informations de manière sécurisée entre parties."
        }
        code = (
            "<?php\n"
            "// Fichier PHP (gestion_sessions.php)\n"
            "    session_start(); // Toujours au début du script !\n"
            "\n"
            "    echo \"<h2>Gestion des Sessions</h2>\";\n"
            "\n"
            "    // Incrémenter un compteur de vues dans la session\n"
            "    if (!isset($_SESSION['compteur_vues'])) {\n"
            "        $_SESSION['compteur_vues'] = 0;\n"
            "    }\n"
            "    $_SESSION['compteur_vues']++;\n"
            "    echo \"Vous avez visité cette page \" . $_SESSION['compteur_vues'] . \" fois pendant cette session.<br>\";\n"
            "\n"
            "    // Stocker un nom d'utilisateur après connexion simulée\n"
            "    if (isset($_POST['login_submit'])) {\n"
            "        $_SESSION['utilisateur_connecte'] = htmlspecialchars($_POST['username']);\n"
            "        echo \"<p>Bienvenue, \" . $_SESSION['utilisateur_connecte'] . \" ! Vous êtes maintenant connecté.</p>\";\n"
            "    }\n"
            "\n"
            "    if (isset($_SESSION['utilisateur_connecte'])) {\n"
            "        echo \"<p>Utilisateur connecté : \" . $_SESSION['utilisateur_connecte'] . \"</p>\";\n"
            "        echo '<form method=\"POST\"><input type=\"submit\" name=\"logout_submit\" value=\"Déconnexion\"></form>';\n"
            "    } else {\n"
            "        echo \"<p>Vous n'êtes pas connecté.</p>\";\n"
            "        echo '<form method=\"POST\">\n' .\n"
            "             '    <label for=\"username\">Nom d\'utilisateur:</label><br>\n' .\n"
            "             '    <input type=\"text\" id=\"username\" name=\"username\" required><br><br>\n' .\n"
            "             '    <input type=\"submit\" name=\"login_submit\" value=\"Connexion\">\n' .\n"
            "             '</form>';\n"
            "    }\n"
            "\n"
            "    // Gérer la déconnexion\n"
            "    if (isset($_POST['logout_submit'])) {\n"
            "        session_unset();     // Supprime toutes les variables de session\n"
            "        session_destroy();   // Détruit la session elle-même\n"
            "        echo \"<p>Vous avez été déconnecté.</p>\";\n"
            "        // Rediriger pour effacer les données POST après déconnexion\n"
            "        header('Location: ' . $_SERVER['PHP_SELF']);\n"
            "        exit();\n"
            "    }\n"
            "\n"
            "    // --- Génération et validation d'un Token CSRF (Exemple Simplifié) ---\n"
            "    echo \"<h3>Exemple de CSRF Token :</h3>\";\n"
            "    if (!isset($_SESSION['csrf_token'])) {\n"
            "        $_SESSION['csrf_token'] = bin2hex(random_bytes(32)); // Génère un token aléatoire et sécurisé\n"
            "    }\n"
            "    $csrfToken = $_SESSION['csrf_token'];\n"
            "\n"
            "    // Formulaire avec CSRF token\n"
            "    echo '<form action=\"gestion_sessions.php\" method=\"POST\">\n' .\n"
            "         '    <input type=\"hidden\" name=\"csrf_token\" value=\"' . $csrfToken . '\">\n' .\n"
            "         '    <label for=\"action_field\">Action protégée:</label><br>\n' .\n"
            "         '    <input type=\"text\" id=\"action_field\" name=\"action_data\">\n' .\n"
            "         '    <input type=\"submit\" name=\"perform_action\" value=\"Effectuer Action (avec token)\">\n' .\n"
            "         '</form>';\n"
            "\n"
            "    if (isset($_POST['perform_action'])) {\n"
            "        if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== $_SESSION['csrf_token']) {\n"
            "            echo \"<p style='color: red;'>Erreur de sécurité: Token CSRF invalide !</p>\";\n"
            "        } else {\n"
            "            echo \"<p style='color: green;'>Action \" . htmlspecialchars($_POST['action_data']) . \" effectuée avec succès (token valide).</p>\";\n"
            "            // Régénérer le token après usage pour plus de sécurité\n"
            "            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));\n"
            "        }\n"
            "    }\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Sessions & Tokens"), title, explanation, code, keywords)

    # --- Nouvelle méthode pour la Sécurité Web ---
    def setup_web_security_tab(self):
        title = "Sécurité Web Fondamentale"
        explanation = (
            "La sécurité est primordiale dans le développement web. Ignorer les bonnes pratiques "
            "expose votre application à de nombreuses vulnérabilités. Voici les menaces courantes "
            "et les stratégies de défense de base."
            "\n\n"
            "**Menaces Courantes et Défenses :**\n"
            "1.  **Injection SQL (SQL Injection)**:\n"
            "    * **Description**: Un attaquant insère du code SQL malveillant dans les entrées utilisateur pour manipuler la base de données.\n"
            "    * **Défense**: Utilisez des requêtes préparées (Prepared Statements) avec des paramètres liés (`bindParam()`, `bindValue()`) via PDO ou MySQLi. Ne concaténez jamais directement les entrées utilisateur dans des requêtes SQL.\n"
            "2.  **Cross-Site Scripting (XSS)**:\n"
            "    * **Description**: Un attaquant injecte des scripts côté client (JavaScript) dans des pages web visualisées par d'autres utilisateurs. Ces scripts peuvent voler des cookies, dégrader l'interface utilisateur, etc.\n"
            "    * **Défense**: Échappez toujours les sorties de données utilisateur dans le HTML avec `htmlspecialchars()` ou `htmlentities()`. Utilisez `Content-Security-Policy` (CSP).\n"
            "3.  **Cross-Site Request Forgery (CSRF)**:\n"
            "    * **Description**: Un attaquant force un utilisateur authentifié à exécuter des actions non désirées sur une application web via une requête falsifiée.\n"
            "    * **Défense**: Utilisez des **tokens CSRF** (voir onglet Sessions & Tokens) dans les formulaires sensibles. Vérifiez l'en-tête `Referer` (bien que ce ne soit pas une solution complète).\n"
            "4.  **Upload de Fichiers Non Sécurisé**:\n"
            "    * **Description**: Permettre le téléchargement de fichiers malveillants (ex: scripts PHP cachés) qui peuvent être exécutés sur le serveur.\n"
            "    * **Défense**: Validez rigoureusement le type, la taille et le contenu du fichier. Stockez les fichiers téléchargés hors du répertoire racine web si possible. Utilisez `move_uploaded_file()`. Renommez les fichiers.\n"
            "5.  **Exposition d'Informations Sensibles**: \n"
            "    * **Description**: Révéler des informations comme des messages d'erreur détaillés, des chemins de fichiers, des identifiants de base de données.\n"
            "    * **Défense**: Désactivez l'affichage des erreurs en production (`display_errors = Off` dans `php.ini`). Enregistrez les erreurs dans des logs. Ne pas inclure d'informations sensibles directement dans le code versionné."
            "6.  **Gestion des Mots de Passe**: \n"
            "    * **Description**: Stockage des mots de passe en texte clair ou avec un hachage faible.\n"
            "    * **Défense**: Utilisez des fonctions de hachage robustes comme `password_hash()` (avec `PASSWORD_DEFAULT`) et `password_verify()` pour stocker et vérifier les mots de passe. N'utilisez **jamais** MD5 ou SHA1 pour les mots de passe."
        )
        keywords = {
            "SQL Injection": "Vulnérabilité où du code SQL malveillant est injecté dans des requêtes.",
            "Prepared Statements": "Méthode sécurisée pour exécuter des requêtes SQL en séparant le code SQL des données.",
            "XSS (Cross-Site Scripting)": "Vulnérabilité où des scripts malveillants sont injectés côté client.",
            "htmlspecialchars()": "Fonction pour convertir les caractères spéciaux en entités HTML, prévenant le XSS.",
            "CSRF (Cross-Site Request Forgery)": "Vulnérabilité où un attaquant force l'exécution d'actions non désirées.",
            "CSRF Token": "Jeton de sécurité pour prévenir le CSRF.",
            "$_FILES": "Superglobale pour l'upload de fichiers. Doit être utilisée avec prudence.",
            "move_uploaded_file()": "Fonction sécurisée pour déplacer les fichiers téléchargés.",
            "password_hash()": "Fonction PHP pour hacher les mots de passe de manière sécurisée.",
            "password_verify()": "Fonction PHP pour vérifier un mot de passe haché.",
            "display_errors = Off": "Directive `php.ini` à régler en production pour ne pas afficher les erreurs à l'utilisateur."
        }
        code = (
            "<?php\n"
            "// Fichier PHP (security_example.php)\n"
            "    // --- Prévention de l'Injection SQL (via PDO) ---\n"
            "    // NOTE: Ceci nécessite une base de données configurée pour fonctionner réellement.\n"
            "    /*\n"
            "    try {\n"
            "        $pdo = new PDO('mysql:host=localhost;dbname=testdb', 'user', 'password');\n"
            "        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);\n"
            "\n"
            "        $userId = $_GET['id'] ?? 1; // Simulation d'une entrée utilisateur\n"
            "        // Requête Préparée : SÉCURISÉ\n"
            "        $stmt = $pdo->prepare('SELECT * FROM users WHERE id = :id');\n"
            "        $stmt->bindParam(':id', $userId, PDO::PARAM_INT);\n"
            "        $stmt->execute();\n"
            "        $user = $stmt->fetch(PDO::FETCH_ASSOC);\n"
            "        if ($user) {\n"
            "            echo \"Utilisateur trouvé : \" . htmlspecialchars($user['username']) . \"<br>\";\n"
            "        } else { echo \"Utilisateur non trouvé.<br>\"; }\n"
            "\n"
            "        // Mauvaise pratique (Vulnérable à l'Injection SQL) : NE FAITES PAS ÇA !\n"
            "        // $vuln_id = \"1 OR 1=1\";\n"
            "        // $result = $pdo->query(\"SELECT * FROM users WHERE id = \" . $vuln_id);\n"
            "        // echo \"<p style='color:red;'>Recherche vulnérable: \" . $result->rowCount() . \" résultats.</p>\";\n"
            "\n"
            "    } catch (PDOException $e) {\n"
            "        error_log('Erreur de BDD: ' . $e->getMessage()); // Journaliser l'erreur\n"
            "        // echo \"Une erreur de base de données est survenue.\"; // Message générique pour l'utilisateur\n"
            "    }\n"
            "    */\n"
            "\n"
            "    // --- Prévention du XSS ---\n"
            "    echo \"<h3>Prévention du XSS :</h3>\";\n"
            "    $user_input = \"<script>alert('Attaque XSS !');</script><b>Texte gras</b>\";\n"
            "    echo \"Entrée non échappée (dangereux): \" . $user_input . \"<br>\";\n"
            "    echo \"Entrée échappée (sécurisé): \" . htmlspecialchars($user_input) . \"<br>\";\n"
            "\n"
            "    // --- Hachage de Mots de Passe SÉCURISÉ ---\n"
            "    echo \"<h3>Hachage de Mots de Passe :</h3>\";\n"
            "    $motDePasseClair = \"monMotDePasseSecret\";\n"
            "    $motDePasseHashe = password_hash($motDePasseClair, PASSWORD_DEFAULT);\n"
            "    echo \"Mot de passe haché : \" . $motDePasseHashe . \"<br>\";\n"
            "\n"
            "    // Vérification du mot de passe\n"
            "    if (password_verify($motDePasseClair, $motDePasseHashe)) {\n"
            "        echo \"Le mot de passe correspond au hachage.<br>\";\n"
            "    } else {\n"
            "        echo \"Le mot de passe NE correspond PAS au hachage.<br>\";\n"
            "    }\n"
            "\n"
            "    // Exemple de mauvaise pratique (NE FAITES PAS ÇA !)\n"
            "    // $mauvaisHash = md5($motDePasseClair);\n"
            "    // echo \"<p style='color:red;'>Hachage MD5 (NON SÉCURISÉ) : \" . $mauvaisHash . \"</p>\";\n"
            "?>"
        )
        self.create_content_frame(self.tab_view.tab("Sécurité Web (Basique)"), title, explanation, code, keywords)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = PHPTutorialApp()
    app.mainloop()