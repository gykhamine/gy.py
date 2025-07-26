import customtkinter as ctk
import sys # Nécessaire pour sys.stdout.flush() si on avait des inputs console, mais pas ici
import os # Juste pour le chemin du fichier, mais pas réellement utilisé dans l'interface pour l'instant

class CCppSyntaxApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("C/C++ Guide Interactif Ultime")
        self.geometry("1200x850") # Even larger window for more content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar Navigation ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(20, weight=1) # Make space for many buttons

        ctk.CTkLabel(self.sidebar_frame, text="Navigation", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Accueil", command=lambda: self.show_page("home"))
        self.home_button.grid(row=1, column=0, padx=20, pady=10)

        self.data_types_button = ctk.CTkButton(self.sidebar_frame, text="Types de Données C/C++", command=lambda: self.show_page("data_types_c_cpp"))
        self.data_types_button.grid(row=2, column=0, padx=20, pady=10) # Nouvelle position pour le bouton

        self.compilation_button = ctk.CTkButton(self.sidebar_frame, text="Compilation C/C++", command=lambda: self.show_page("compilation_c_cpp"))
        self.compilation_button.grid(row=3, column=0, padx=20, pady=10) # Nouvelle position pour le bouton

        # Les autres boutons décalés vers le bas
        self.basics_c_button = ctk.CTkButton(self.sidebar_frame, text="Les Bases (C)", command=lambda: self.show_page("basics_c"))
        self.basics_c_button.grid(row=4, column=0, padx=20, pady=10)

        self.structs_c_button = ctk.CTkButton(self.sidebar_frame, text="Structures (C)", command=lambda: self.show_page("structs_c"))
        self.structs_c_button.grid(row=5, column=0, padx=20, pady=10)

        self.pointers_memory_button = ctk.CTkButton(self.sidebar_frame, text="Pointeurs & Mémoire", command=lambda: self.show_page("pointers_memory"))
        self.pointers_memory_button.grid(row=6, column=0, padx=20, pady=10)

        self.file_io_button = ctk.CTkButton(self.sidebar_frame, text="Gestion de Fichiers (I/O)", command=lambda: self.show_page("file_io"))
        self.file_io_button.grid(row=7, column=0, padx=20, pady=10)

        self.preprocessor_button = ctk.CTkButton(self.sidebar_frame, text="Préprocesseur C/C++", command=lambda: self.show_page("preprocessor"))
        self.preprocessor_button.grid(row=8, column=0, padx=20, pady=10)

        self.scope_operator_button = ctk.CTkButton(self.sidebar_frame, text="Opérateur ::", command=lambda: self.show_page("scope_operator"))
        self.scope_operator_button.grid(row=9, column=0, padx=20, pady=10)

        self.intro_cpp_button = ctk.CTkButton(self.sidebar_frame, text="Introduction C++", command=lambda: self.show_page("intro_cpp"))
        self.intro_cpp_button.grid(row=10, column=0, padx=20, pady=10)

        self.oop_cpp_button = ctk.CTkButton(self.sidebar_frame, text="POO en C++ (Bases)", command=lambda: self.show_page("oop_cpp"))
        self.oop_cpp_button.grid(row=11, column=0, padx=20, pady=10)

        self.oop_adv_button = ctk.CTkButton(self.sidebar_frame, text="POO en C++ (Avancé)", command=lambda: self.show_page("oop_adv"))
        self.oop_adv_button.grid(row=12, column=0, padx=20, pady=10)

        self.exceptions_button = ctk.CTkButton(self.sidebar_frame, text="Gestion des Exceptions (C++)", command=lambda: self.show_page("exceptions"))
        self.exceptions_button.grid(row=13, column=0, padx=20, pady=10)

        self.templates_stl_button = ctk.CTkButton(self.sidebar_frame, text="Modèles & STL (C++)", command=lambda: self.show_page("templates_stl"))
        self.templates_stl_button.grid(row=14, column=0, padx=20, pady=10)

        self.cpp14_features_button = ctk.CTkButton(self.sidebar_frame, text="C++14 Nouveautés", command=lambda: self.show_page("cpp14_features"))
        self.cpp14_features_button.grid(row=15, column=0, padx=20, pady=10)

        self.concurrency_button = ctk.CTkButton(self.sidebar_frame, text="Concurrence (C++11/14+)", command=lambda: self.show_page("concurrency"))
        self.concurrency_button.grid(row=16, column=0, padx=20, pady=10)

        self.testing_debugging_button = ctk.CTkButton(self.sidebar_frame, text="Tests & Débogage", command=lambda: self.show_page("testing_debugging"))
        self.testing_debugging_button.grid(row=17, column=0, padx=20, pady=10)

        self.best_practices_button = ctk.CTkButton(self.sidebar_frame, text="Bonnes Pratiques", command=lambda: self.show_page("best_practices"))
        self.best_practices_button.grid(row=18, column=0, padx=20, pady=10)

        self.keywords_c_button = ctk.CTkButton(self.sidebar_frame, text="Mots Clés C", command=lambda: self.show_page("keywords_c"))
        self.keywords_c_button.grid(row=19, column=0, padx=20, pady=10)

        self.keywords_cpp_button = ctk.CTkButton(self.sidebar_frame, text="Mots Clés C++", command=lambda: self.show_page("keywords_cpp"))
        self.keywords_cpp_button.grid(row=20, column=0, padx=20, pady=10)


        # --- Main Content Frame ---
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Create pages (frames) for content
        self.pages = {}
        self._create_home_page()
        self._create_data_types_c_cpp_page() # Nouvelle page
        self._create_compilation_c_cpp_page() # Nouvelle page
        self._create_basics_c_page()
        self._create_structs_c_page() # New page for C structs
        self._create_pointers_memory_page()
        self._create_file_io_page()
        self._create_preprocessor_page()
        self._create_scope_operator_page() # New page for :: operator
        self._create_intro_cpp_page()
        self._create_oop_cpp_page()
        self._create_oop_adv_page()
        self._create_exceptions_page()
        self._create_templates_stl_page()
        self._create_cpp14_features_page() # New page for C++14 features
        self._create_concurrency_page()
        self._create_testing_debugging_page()
        self._create_best_practices_page()
        self._create_keywords_c_page()
        self._create_keywords_cpp_page()


        self.show_page("home") # Show home page initially

    def show_page(self, name):
        """Affiche la page demandée et cache les autres."""
        for page in self.pages.values():
            page.pack_forget()
        if name in self.pages:
            self.pages[name].pack(fill="both", expand=True)
        else:
            print(f"Erreur: Page '{name}' non trouvée.")

    def _create_page_template(self, name, title_text, content_text):
        """Crée un template de page avec titre et contenu."""
        frame = ctk.CTkScrollableFrame(self.content_frame, corner_radius=10)
        self.pages[name] = frame

        title_label = ctk.CTkLabel(frame, text=title_text, font=ctk.CTkFont(size=26, weight="bold"))
        title_label.pack(pady=(20, 10), padx=20, anchor="w") # More padding for title

        content_label = ctk.CTkLabel(frame, text=content_text, wraplength=950, justify="left", font=ctk.CTkFont(size=15)) # Slightly larger font and wraplength
        content_label.pack(pady=10, padx=20, fill="both", expand=True)

        return frame

    def _create_home_page(self):
        title = "Bienvenue au Guide Interactif C/C++ Ultime"
        content = """
        Ce guide interactif, construit avec **CustomTkinter**, est conçu pour vous offrir une exploration **claire, structurée et approfondie** des langages C et C++, avec un accent sur les standards modernes jusqu'à C++14.

        Il couvre les bases, les concepts avancés et une référence des mots-clés essentiels, accompagnés d'explications et d'exemples.

        ---

        ### Comment utiliser ce guide :

        Utilisez le **menu de navigation à gauche** pour accéder aux différentes sections :

        * **Accueil**: Cette page d'introduction.
        * **Types de Données C/C++**: Comprenez les types fondamentaux et leur importance en C/C++.
        * **Compilation C/C++**: Explorez le processus de transformation de votre code en exécutable.
        * **Les Bases (C)**: Explorez les fondations du langage C (structure, variables, opérateurs, boucles, fonctions).
        * **Structures (C)**: Comprenez les types de données composites en C.
        * **Pointeurs & Mémoire**: Comprenez la gestion de la mémoire, les pointeurs et l'allocation dynamique en C et C++.
        * **Gestion de Fichiers (I/O)**: Apprenez à lire et écrire des données dans des fichiers.
        * **Préprocesseur C/C++**: Maîtrisez les directives de préprocesseur pour la compilation conditionnelle et les macros.
        * **Opérateur ::**: Découvrez l'opérateur de résolution de portée pour les namespaces et les classes.
        * **Introduction C++**: Découvrez les améliorations de C++ par rapport à C, notamment l'I/O et les espaces de noms.
        * **POO en C++ (Bases)**: Plongez dans les fondations de la Programmation Orientée Objet (POO) avec les classes, objets, héritage et polymorphisme.
        * **POO en C++ (Avancé)**: Explorez des concepts POO plus complexes comme les classes abstraites, les destructeurs virtuels, et les règles de copie/déplacement.
        * **Gestion des Exceptions (C++)**: Apprenez à gérer les erreurs de manière robuste avec les exceptions C++.
        * **Modèles & STL (C++)**: Introduction à la programmation générique et à la Bibliothèque Standard de Modèles.
        * **C++14 Nouveautés**: Découvrez les principales fonctionnalités ajoutées dans le standard C++14.
        * **Concurrence (C++11/14+)**: Découvrez les bases du multithreading pour des applications performantes.
        * **Tests Unitaires & Débogage**: Comprenez l'importance de tester et de déboguer votre code.
        * **Bonnes Pratiques**: Adoptez des conventions de codage pour un code propre et maintenable.
        * **Mots Clés C**: Une liste des mots-clés réservés en C, avec des explications et exemples pour les plus courants.
        * **Mots Clés C++**: Une liste des mots-clés réservés en C++, avec des explications et exemples clés.

        ---

        ### Ressources Supplémentaires :

        Pour une compréhension exhaustive et des détails techniques approfondis, il est fortement recommandé de consulter des ressources externes de référence :

        * **cppreference.com**: Une référence incontournable pour C et C++.
        * **Documentation officielle du standard C++**.
        * **Manuels et tutoriels de programmation C/C++** reconnus.

        Nous espérons que ce guide vous sera utile dans votre parcours d'apprentissage et de maîtrise de C et C++ !
        """
        self._create_page_template("home", title, content)

    # --- NOUVELLES PAGES AJOUTÉES ICI ---
    def _create_data_types_c_cpp_page(self):
        title = "Types de Données Fondamentaux en C/C++"
        content = """
        Contrairement à Python qui est à typage dynamique, en C/C++, les variables doivent
        toujours avoir un **type déclaré**. Ce **typage statique** permet au compilateur de vérifier
        la cohérence et d'optimiser l'utilisation de la mémoire.

        ---

        ### 1. Types Numériques Entiers

        Utilisés pour les nombres entiers sans partie décimale. Leur taille peut varier
        selon l'architecture du système.

        * **`char`**: Généralement 1 octet. Peut stocker un petit entier ou un caractère (ASCII).
            ```c
            char lettre = 'A';
            ```
        * **`short`**: Au moins 2 octets. Pour les petits entiers.
            ```c
            short age = 25;
            ```
        * **`int`**: Taille par défaut pour les entiers, souvent 4 octets. Le plus couramment utilisé.
            ```c
            int nombre = 100;
            ```
        * **`long`**: Au moins 4 octets (souvent 8 octets sur les systèmes modernes 64-bit).
            ```c
            long grande_valeur = 1234567890L;
            ```
        * **`long long`**: Au moins 8 octets. Pour les très grands entiers.
            ```c
            long long tres_grande_valeur = 9876543210987654321LL;
            ```
        **Modificateurs (pour `char`, `short`, `int`, `long`, `long long`):**
        * **`signed`**: Peut stocker des valeurs positives et négatives (par défaut).
        * **`unsigned`**: Peut stocker uniquement des valeurs positives (double la plage positive).
            ```c
            unsigned int compteur = 0;
            ```

        ---

        ### 2. Types Numériques à Virgule Flottante

        Utilisés pour les nombres réels (décimaux).

        * **`float`**: Précision simple, généralement 4 octets.
            ```c
            float temperature = 23.5f;
            ```
        * **`double`**: Double précision, généralement 8 octets. Plus précis et couramment utilisé.
            ```c
            double pi = 3.1415926535;
            ```
        * **`long double`**: Précision étendue, taille variable (souvent 10 ou 16 octets).
            ```c
            long double tres_grand_pi = 3.14159265358979323846L;
            ```

        ---

        ### 3. Type Booléen

        * **`bool` (C++)**: Représente des valeurs de vérité: `true` ou `false`. (En C, on utilise souvent `int` avec 0 pour faux, non-0 pour vrai, ou on inclut `<stdbool.h>` pour `bool`).
            ```cpp
            bool est_actif = true;
            ```

        ---

        ### 4. Types Composites et Pointeur

        * **`void`**: Indique l'absence de type. Utilisé pour les fonctions qui ne retournent rien, ou les pointeurs génériques.
            ```c
            void maFonctionSansRetour(); // Fonction qui ne retourne rien
            ```
        * **Pointeurs (`*`)**: Stockent l'adresse mémoire d'une autre variable. Très puissants mais délicats.
            ```c
            int* ptr_nombre;
            ```
        * **Tableaux (`[]`)**: Collections d'éléments du même type stockés contiguïté en mémoire.
            ```c
            int nombres[5];
            ```
        * **Structures (`struct`) et Classes (`class` en C++)**: Types définis par l'utilisateur pour regrouper des données de types différents.
            ```c
            struct Point { int x; int y; };
            ```
            ```cpp
            class Voiture { std::string marque; int annee; };
            ```

        Ces types sont les briques de base de tout programme C/C++. Le compilateur utilise
        ces informations pour allouer la mémoire et s'assurer que les opérations sont valides.
        """
        self._create_page_template("data_types_c_cpp", title, content)

    def _create_compilation_c_cpp_page(self):
        title = "Le Processus de Compilation en C/C++"
        content = """
        La **compilation** est une étape cruciale en C/C++, transformant votre code source
        en un programme exécutable. Voici les phases principales :

        ---

        ### 1. Préprocesseur (.i ou .ii)

        * **Rôle:** Le préprocesseur est la première étape. Il traite les directives commençant par `#`.
        * **Actions principales:**
            * **`#include`**: Insère le contenu des fichiers d'en-tête (comme `<iostream>`, `stdio.h`, ou vos propres `.h`) directement dans le fichier source.
            * **`#define`**: Remplace les macros (textuellement) avant la compilation.
            * Gère les compilations conditionnelles (`#ifdef`, `#ifndef`, etc.).
        * **Sortie:** Un fichier préprocessé (souvent avec l'extension `.i` pour C, ou `.ii` pour C++), qui est un fichier source 'expansé' sans directives de préprocesseur.
            Exemple de commande (GCC): `gcc -E mon_programme.c -o mon_programme.i`

        ---

        ### 2. Compilation (.s ou .obj/.o)

        * **Rôle:** Le compilateur traduit le code C/C++ préprocessé en code assembleur, puis en code objet.
        * **Actions principales:**
            * **Analyse Lexicale:** Découpe le code en 'tokens' (mots-clés, identifiants, opérateurs).
            * **Analyse Syntaxique:** Vérifie la grammaire du langage et construit un arbre syntaxique.
            * **Analyse Sémantique:** Vérifie la signification du code (vérification des types, déclaration des variables, etc.).
            * **Génération de code intermédiaire et Optimisation:** Le compilateur peut effectuer des optimisations pour rendre le code plus rapide et plus petit.
            * **Génération de code assembleur (.s):** Une étape intermédiaire optionnelle.
            * **Génération de code objet (.obj sur Windows, .o sur Linux/macOS):** Contient le code machine pour votre fichier source, mais pas encore un programme exécutable complet (il manque les fonctions des bibliothèques externes).
        * **Sortie:** Fichiers objet (un par fichier source compilé).
            Exemple de commande (GCC): `gcc -c mon_programme.c -o mon_programme.o`

        ---

        ### 3. Édition de Liens (Linking) (Exécutable)

        * **Rôle:** Le lieur (linker) prend tous les fichiers objet (.o/.obj) et les bibliothèques nécessaires
            (bibliothèques standard, bibliothèques tierces) et les combine pour former un seul fichier exécutable.
        * **Actions principales:**
            * Résout les références aux fonctions et variables définies dans d'autres fichiers objet ou bibliothèques.
            * Crée le fichier exécutable final.
        * **Sortie:** Le programme exécutable (.exe sur Windows, pas d'extension sur Linux/macOS par défaut).
            Exemple de commande (GCC): `gcc mon_programme.o -o mon_programme`
            (Souvent, on compile et lie en une seule commande: `gcc mon_programme.c -o mon_programme`)

        ---

        ### Schéma Récapitulatif :
        `Code Source (.c/.cpp) -> [Préprocesseur] -> Fichier Préprocessé (.i/.ii) ->`
        `[Compilateur] -> Fichier Objet (.o/.obj) -> [Éditeur de Liens] -> Exécutable`

        Cette approche multi-étapes permet une grande flexibilité, une forte optimisation
        et une détection précoce des erreurs, ce qui est essentiel pour les performances
        et la robustesse des applications C/C++.
        """
        self._create_page_template("compilation_c_cpp", title, content)
    # --- FIN DES NOUVELLES PAGES ---

    def _create_basics_c_page(self):
        title = "Les Bases de la Syntaxe C"
        content = """
        Le langage C est la pierre angulaire de nombreux systèmes. Voici ses concepts fondamentaux :

        ---

        ### 1. Structure d'un programme C

        Un programme C typique commence par des **directives de préprocesseur** et inclut la fonction `main()`, le point d'entrée de l'exécution.

        ```c
        #include <stdio.h> // Directive d'inclusion: Importe la bibliothèque d'entrée/sortie standard

        int main() { // La fonction principale: où le programme commence à s'exécuter
            // Votre code C va ici
            printf("Bonjour, Monde !\\n"); // Affiche du texte sur la console
            return 0; // Indique que le programme s'est terminé avec succès (0 = pas d'erreur)
        }
        ```

        ---

        ### 2. Variables et Types de Données

        Les **variables** sont des conteneurs pour stocker des données. Chaque variable doit avoir un **type de données** qui définit la nature des valeurs qu'elle peut contenir.

        * **`int`**: Pour les nombres entiers (ex: `10`, `-500`).
            ```c
            int age = 30;
            ```
        * **`float`**: Pour les nombres à virgule flottante de précision simple (ex: `3.14f`, `-0.5f`). Le `f` à la fin est important.
            ```c
            float prix = 19.99f;
            ```
        * **`double`**: Pour les nombres à virgule flottante de précision double (plus précis que `float`).
            ```c
            double pi = 3.1415926535;
            ```
        * **`char`**: Pour un caractère unique (ex: `'A'`, `'z'`, `'7'`).
            ```c
            char initiale = 'J';
            ```
        * **`void`**: Indique l'absence de type. Utilisé pour les fonctions qui ne retournent rien, ou pour les pointeurs génériques.
            ```c
            void maFonctionSansRetour(); // Fonction qui ne retourne rien
            ```

        ---

        ### 3. Déclaration et Initialisation

        * **Déclaration**: Réserver de la mémoire pour une variable.
        * **Initialisation**: Donner une valeur initiale à cette variable.

        ```c
        int nombre;           // Déclaration: 'nombre' existe, mais sa valeur est indéfinie
        nombre = 10;          // Affectation: 'nombre' reçoit la valeur 10

        float temperature = 25.5; // Déclaration ET initialisation
        ```

        ---

        ### 4. Opérateurs

        Des symboles qui effectuent des opérations sur des variables et des valeurs.

        * **Arithmétiques**: `+`, `-`, `*`, `/`, `%` (modulo - reste de la division).
            ```c
            int a = 10, b = 3;
            int somme = a + b;      // 13
            int reste = a % b;      // 1
            ```
        * **Relationnels**: `==` (égal à), `!=` (différent de), `>`, `<`, `>=`, `<=` (utilisés pour les comparaisons).
            ```c
            if (a == b) { /* ... */ }
            ```
        * **Logiques**: `&&` (ET logique), `||` (OU logique), `!` (NON logique).
            ```c
            if (age > 18 && estEtudiant) { /* ... */ }
            ```
        * **Affectation**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`.
            ```c
            int x = 5;
            x += 3; // Équivalent à x = x + 3; (x devient 8)
            ```
        * **Incrémentation/Décrémentation**: `++`, `--`.
            ```c
            int i = 0;
            i++; // i devient 1
            ```

        ---

        ### 5. Structures de Contrôle

        Contrôlent le flux d'exécution du programme.

        * **`if-else if-else`**: Pour l'exécution conditionnelle.

            ```c
            if (score >= 90) {
                printf("Excellent !\\n");
            } else if (score >= 70) {
                printf("Bien.\\n");
            } else {
                printf("À améliorer.\\n");
            }
            ```

        * **`switch-case`**: Pour des choix multiples basés sur une valeur unique.

            ```c
            char grade = 'B';
            switch (grade) {
                case 'A':
                    printf("Très bien\\n");
                    break; // Important pour sortir du switch
                case 'B':
                    printf("Bien\\n");
                    break;
                case 'C':
                    printf("Passable\\n");
                    break;
                default:
                    printf("Autre grade\\n");
            }
            ```

        * **Boucle `for`**: Pour des itérations avec un nombre connu d'itérations.

            ```c
            for (int i = 0; i < 5; i++) { // Initialisation; Condition; Incrémentation
                printf("Itération %d\\n", i);
            }
            // Affiche: Itération 0, Itération 1, ... Itération 4
            ```

        * **Boucle `while`**: Pour des itérations tant qu'une condition est vraie.

            ```c
            int compteur = 0;
            while (compteur < 3) {
                printf("Compteur: %d\\n", compteur);
                compteur++;
            }
            // Affiche: Compteur: 0, Compteur: 1, Compteur: 2
            ```

        * **Boucle `do-while`**: Exécute le bloc de code au moins une fois, puis vérifie la condition.

            ```c
            int i = 5;
            do {
                printf("Do-While: %d\\n", i);
                i++;
            } while (i < 3); // La condition est fausse, mais s'exécute une fois
            // Affiche: Do-While: 5
            ```

        ---

        ### 6. Fonctions

        Des blocs de code réutilisables qui effectuent une tâche spécifique.

        ```c
        // Déclaration de fonction (prototype): Informe le compilateur de l'existence de la fonction
        int addition(int a, int b);

        int main() {
            int resultat = addition(5, 3); // Appel de la fonction
            printf("Résultat de l'addition: %d\\n", resultat);
            return 0;
        }

        // Définition de fonction: Contient le code réel de la fonction
        int addition(int a, int b) {
            return a + b; // Renvoie la somme de a et b
        }
        ```
        """
        self._create_page_template("basics_c", title, content)

    def _create_structs_c_page(self):
        title = "Structures (`struct`) en C"
        content = """
        En C, une **structure (`struct`)** est un type de données composite qui regroupe plusieurs variables (appelées **membres** ou **champs**) de types différents sous un seul nom. Les structures sont utilisées pour représenter un ensemble cohérent de données.

        ---

        ### 1. Déclaration d'une Structure

        Vous déclarez une structure en utilisant le mot-clé `struct`.

        ```c
        // Déclaration d'une structure pour représenter un point en 2D
        struct Point {
            int x; // Membre pour la coordonnée X
            int y; // Membre pour la coordonnée Y
        }; // N'oubliez pas le point-virgule final !

        // Déclaration d'une structure pour représenter un livre
        struct Livre {
            char titre[50]; // Tableau de caractères pour le titre
            char auteur[50]; // Tableau de caractères pour l'auteur
            int anneePublication;
            float prix;
        };
        ```

        ---

        ### 2. Création et Accès aux Membres d'une Structure

        Pour créer une variable de type structure et accéder à ses membres, vous utilisez l'opérateur point (`.`).

        ```c
        #include <stdio.h>
        #include <string.h> // Pour strcpy

        struct Point {
            int x;
            int y;
        };

        struct Livre {
            char titre[50];
            char auteur[50];
            int anneePublication;
            float prix;
        };

        int main() {
            // Création d'une variable de type struct Point
            struct Point p1;

            // Accès et affectation des valeurs aux membres
            p1.x = 10;
            p1.y = 20;

            printf("Coordonnées de p1 : (%d, %d)\\n", p1.x, p1.y);

            // Création et initialisation directe d'une variable de type struct Livre
            struct Livre livre1 = {"Le Seigneur des Anneaux", "J.R.R. Tolkien", 1954, 25.99f};

            printf("Titre : %s\\n", livre1.titre);
            printf("Auteur : %s\\n", livre1.auteur);
            printf("Année : %d\\n", livre1.anneePublication);
            printf("Prix : %.2f €\\n", livre1.prix);

            // Modifier un membre
            strcpy(livre1.titre, "Le Hobbit"); // Utilisez strcpy pour les tableaux de caractères
            printf("Nouveau titre : %s\\n", livre1.titre);

            return 0;
        }
        ```

        ---

        ### 3. Structures avec `typedef`

        Il est courant d'utiliser `typedef` pour créer un alias (un nouveau nom) pour le type `struct`, ce qui rend la déclaration de variables plus concise.

        ```c
        #include <stdio.h>

        // Déclaration de la structure et création d'un alias de type
        typedef struct {
            float reel;
            float imaginaire;
        } Complexe; // 'Complexe' est maintenant un alias pour le type de structure

        int main() {
            Complexe c1; // Plus besoin de 'struct'
            c1.reel = 3.0;
            c1.imaginaire = 4.5;

            printf("Nombre complexe : %.1f + %.1fi\\n", c1.reel, c1.imaginaire);
            return 0;
        }
        ```

        ---

        ### 4. Structures et Pointeurs

        Lorsqu'un pointeur pointe vers une structure, vous utilisez l'opérateur flèche (`->`) pour accéder à ses membres.

        ```c
        #include <stdio.h>
        #include <stdlib.h> // Pour malloc et free
        #include <string.h> // Pour strcpy

        typedef struct {
            int id;
            char nom[30];
        } Personne;

        int main() {
            // Allocation dynamique d'une structure Personne
            Personne *ptrPersonne = (Personne *) malloc(sizeof(Personne));

            if (ptrPersonne == NULL) {
                fprintf(stderr, "Erreur d'allocation mémoire !\\n");
                return 1;
            }

            // Accès et affectation via le pointeur flèche (->)
            ptrPersonne->id = 101;
            strcpy(ptrPersonne->nom, "Alice Dupont");

            printf("ID : %d, Nom : %s\\n", ptrPersonne->id, ptrPersonne->nom);

            free(ptrPersonne); // Libérer la mémoire allouée
            ptrPersonne = NULL; // Bonne pratique
            return 0;
        }
        ```

        ---

        ### 5. Structures Imbriquées

        Une structure peut contenir d'autres structures comme membres.

        ```c
        #include <stdio.h>

        struct Date {
            int jour;
            int mois;
            int annee;
        };

        struct Evenement {
            char description[100];
            struct Date dateEvt; // Un membre de type struct Date
        };

        int main() {
            struct Evenement monEvt = {"Réunion importante", {25, 7, 2025}}; // Initialisation imbriquée

            printf("Événement : %s\\n", monEvt.description);
            printf("Date : %d/%d/%d\\n", monEvt.dateEvt.jour, monEvt.dateEvt.mois, monEvt.dateEvt.annee);
            return 0;
        }
        ```

        Les structures en C sont un moyen essentiel de regrouper des données hétérogènes et de construire des types de données plus complexes, formant la base de l'organisation des données dans les programmes C.
        """
        self._create_page_template("structs_c", title, content)

    def _create_pointers_memory_page(self):
        title = "Pointeurs et Allocation Mémoire"
        content = """
        Les pointeurs sont une caractéristique puissante de C et C++ pour la manipulation directe de la mémoire.

        ---

        ### 1. Qu'est-ce qu'un Pointeur ?

        Un **pointeur** est une variable qui **stocke l'adresse mémoire** d'une autre variable. Plutôt que de contenir une valeur directe, il "pointe" vers l'emplacement où cette valeur est stockée.

        * **Déclaration:** Utilisez l'opérateur astérisque (`*`).
            ```c
            int *ptr; // Déclare 'ptr' comme un pointeur vers un entier
            float *autrePtr; // Déclare 'autrePtr' comme un pointeur vers un float
            ```

        * **Opérateur d'adresse (`&`):** Retourne l'adresse mémoire d'une variable.
            ```c
            int x = 10;
            ptr = &x; // 'ptr' stocke maintenant l'adresse mémoire de 'x'
            ```

        * **Opérateur de déréférencement (`*`):** Accède à la valeur stockée à l'adresse pointée par un pointeur.
            ```c
            printf("Valeur de x via pointeur: %d\\n", *ptr); // Affiche 10
            *ptr = 20; // Modifie la valeur de 'x' à travers le pointeur (x devient 20)
            printf("Nouvelle valeur de x: %d\\n", x); // Affiche 20
            ```
        * **Pointeurs et Tableaux :** Les noms de tableaux peuvent être traités comme des pointeurs vers leur premier élément.
            ```c
            int arr[] = {10, 20, 30};
            int* p = arr; // p pointe vers arr[0]
            printf("Premier élément via pointeur: %d\\n", *p); // Affiche 10
            printf("Deuxième élément via pointeur: %d\\n", *(p + 1)); // Affiche 20
            ```

        ---

        ### 2. Allocation Mémoire Dynamique (C)

        En C, la mémoire peut être allouée et libérée manuellement pendant l'exécution du programme.

        * **`malloc()`**: Alloue un bloc de mémoire de la taille spécifiée en octets et retourne un pointeur `void*` vers le début du bloc. Doit être casté au type de pointeur désiré.
            ```c
            #include <stdlib.h> // Pour malloc et free

            int *tableau;
            int taille = 5;

            // Alloue de la mémoire pour 5 entiers
            tableau = (int *) malloc(taille * sizeof(int));

            if (tableau == NULL) { // Vérifier si l'allocation a échoué
                printf("Erreur d'allocation mémoire !\\n");
                return 1;
            }

            // Utiliser la mémoire (ex: initialiser)
            for (int i = 0; i < taille; i++) {
                tableau[i] = i * 10;
            }
            printf("Premier élément: %d\\n", tableau[0]); // Affiche 0
            ```

        * **`free()`**: Libère la mémoire précédemment allouée par `malloc`, `calloc` ou `realloc`. C'est **crucial** pour éviter les fuites de mémoire.
            ```c
            free(tableau); // Libère le bloc de mémoire
            tableau = NULL; // Bonne pratique: éviter les pointeurs "pendants"
            ```

        * **`calloc()`**: Similaire à `malloc`, mais alloue de la mémoire pour un tableau d'éléments et initialise tous les bits à zéro.
            ```c
            int *arr_zero = (int *) calloc(5, sizeof(int)); // 5 entiers, tous à 0
            ```

        * **`realloc()`**: Modifie la taille d'un bloc de mémoire alloué précédemment.
            ```c
            // Supposons 'tableau' a déjà été alloué avec malloc
            tableau = (int *) realloc(tableau, 10 * sizeof(int)); // Redimensionne à 10 entiers
            ```

        ---

        ### 3. Allocation Mémoire Dynamique (C++)

        C++ offre des opérateurs plus spécifiques et de type-sûr pour l'allocation dynamique.

        * **`new`**: Alloue de la mémoire pour un objet ou un tableau d'objets et retourne un pointeur du type approprié.
            ```cpp
            #include <iostream>

            int *monInt = new int; // Alloue de la mémoire pour un seul entier
            *monInt = 42;
            std::cout << "Valeur: " << *monInt << std::endl;

            // Allouer un tableau de 3 doubles
            double *dynArray = new double[3];
            dynArray[0] = 1.1;
            dynArray[1] = 2.2;
            dynArray[2] = 3.3;
            std::cout << "Premier élément du tableau: " << dynArray[0] << std::endl;
            ```

        * **`delete`**: Désalloue la mémoire précédemment allouée par `new`.
            ```cpp
            delete monInt; // Libère l'entier unique
            monInt = nullptr; // Bonne pratique C++: utiliser nullptr pour les pointeurs nuls

            delete[] dynArray; // Libère le tableau (notez les crochets!)
            dynArray = nullptr;
            ```

        ---

        ### 4. Dangers des Pointeurs

        * **Fuites de mémoire (Memory Leaks):** Oublier de `free()` ou `delete` la mémoire allouée dynamiquement.
        * **Pointeurs "pendants" (Dangling Pointers):** Un pointeur qui pointe vers une zone mémoire qui a été libérée. L'accès à cette zone peut causer des erreurs ou des crashs.
        * **Accès hors limites (Out-of-bounds Access):** Accéder à la mémoire au-delà des limites allouées pour un tableau.
        * **Null Pointer Dereference:** Tenter de déréférencer un pointeur `NULL` ou `nullptr`.

        La gestion manuelle de la mémoire est puissante mais exige de la rigueur. En C++, les **pointeurs intelligents** (comme `std::unique_ptr`, `std::shared_ptr`) sont fortement recommandés pour automatiser la gestion de la mémoire et éviter ces pièges.
        """
        self._create_page_template("pointers_memory", title, content)

    def _create_file_io_page(self):
        title = "Gestion de Fichiers (File I/O)"
        content = """
        La gestion des fichiers permet à vos programmes d'interagir avec le système de fichiers pour lire et écrire des données.

        ---

        ### 1. Gestion de Fichiers en C (Fonctions Standard)

        Le langage C utilise des pointeurs de type `FILE*` et des fonctions de la bibliothèque `<stdio.h>` pour la gestion des fichiers.

        * **`fopen()`**: Ouvre un fichier. Retourne un pointeur `FILE*` ou `NULL` en cas d'échec.
            * Modes: `"r"` (lecture), `"w"` (écriture, écrase), `"a"` (ajout), `"rb"`, `"wb"`, `"ab"` (modes binaires).
        * **`fclose()`**: Ferme un fichier.
        * **`fprintf()` / `fscanf()`**: Écrit / lit des données formatées.
        * **`fputc()` / `fgetc()`**: Écrit / lit un caractère.
        * **`fputs()` / `fgets()`**: Écrit / lit une chaîne de caractères.
        * **`fwrite()` / `fread()`**: Écrit / lit des blocs de données binaires.

        ```c
        #include <stdio.h>
        #include <stdlib.h> // Pour exit()

        int main() {
            FILE *fichier;
            char texte[] = "Ceci est une ligne de texte.\\n";
            char buffer[100];

            // --- Écriture dans un fichier (mode "w") ---
            fichier = fopen("exemple.txt", "w"); // Ouvre en écriture, écrase si existe
            if (fichier == NULL) {
                perror("Erreur lors de l'ouverture du fichier en écriture");
                return 1;
            }
            fprintf(fichier, "Bonjour, monde fichier !\\n"); // Écrit une ligne formatée
            fputs(texte, fichier); // Écrit une chaîne
            fclose(fichier);
            printf("Fichier 'exemple.txt' créé et écrit.\\n");

            // --- Lecture d'un fichier (mode "r") ---
            fichier = fopen("exemple.txt", "r"); // Ouvre en lecture
            if (fichier == NULL) {
                perror("Erreur lors de l'ouverture du fichier en lecture");
                return 1;
            }
            printf("\\nContenu de 'exemple.txt':\\n");
            while (fgets(buffer, sizeof(buffer), fichier) != NULL) {
                printf("%s", buffer); // Affiche chaque ligne lue
            }
            fclose(fichier);

            // --- Ajout à un fichier (mode "a") ---
            fichier = fopen("exemple.txt", "a"); // Ouvre en ajout
            if (fichier == NULL) {
                perror("Erreur lors de l'ouverture du fichier en ajout");
                return 1;
            }
            fprintf(fichier, "Nouvelle ligne ajoutée.\\n");
            fclose(fichier);
            printf("\\nNouvelle ligne ajoutée à 'exemple.txt'.\\n");

            return 0;
        }
        ```

        ---

        ### 2. Gestion de Fichiers en C++ (`fstream`)

        C++ utilise les classes de la bibliothèque `<fstream>` (`std::ifstream`, `std::ofstream`, `std::fstream`) qui sont intégrées au système de flux C++.

        * **`std::ofstream`**: Pour l'écriture dans des fichiers.
        * **`std::ifstream`**: Pour la lecture de fichiers.
        * **`std::fstream`**: Pour la lecture et l'écriture.

        ```cpp
        #include <iostream>
        #include <fstream> // Pour les classes de fichiers
        #include <string>

        int main() {
            std::string ligne;

            // --- Écriture dans un fichier (std::ofstream) ---
            std::ofstream fichierEcriture("exemple_cpp.txt"); // Ouvre en écriture, écrase par défaut
            if (!fichierEcriture.is_open()) {
                std::cerr << "Erreur: Impossible d'ouvrir le fichier en écriture." << std::endl;
                return 1;
            }
            fichierEcriture << "Bonjour depuis C++ !\\n";
            fichierEcriture << "Ceci est la deuxième ligne.\\n";
            fichierEcriture.close(); // Ferme le fichier
            std::cout << "Fichier 'exemple_cpp.txt' créé et écrit." << std::endl;

            // --- Lecture d'un fichier (std::ifstream) ---
            std::ifstream fichierLecture("exemple_cpp.txt"); // Ouvre en lecture
            if (!fichierLecture.is_open()) {
                std::cerr << "Erreur: Impossible d'ouvrir le fichier en lecture." << std::endl;
                return 1;
            }
            std::cout << "\\nContenu de 'exemple_cpp.txt':" << std::endl;
            while (std::getline(fichierLecture, ligne)) { // Lit ligne par ligne
                std::cout << ligne << std::endl;
            }
            fichierLecture.close();

            // --- Ajout à un fichier (std::ofstream avec mode std::ios::app) ---
            std::ofstream fichierAjout("exemple_cpp.txt", std::ios::app); // Ouvre en ajout
            if (!fichierAjout.is_open()) {
                std::cerr << "Erreur: Impossible d'ouvrir le fichier en ajout." << std::endl;
                return 1;
            }
            fichierAjout << "Ligne ajoutée en C++.\\n";
            fichierAjout.close();
            std::cout << "\\nNouvelle ligne ajoutée à 'exemple_cpp.txt'.\\n";

            return 0;
        }
        ```
        """
        self._create_page_template("file_io", title, content)
    
    def _create_preprocessor_page(self):
        title = "Le Préprocesseur C/C++"
        content = """
        Le **préprocesseur** est la première phase du processus de compilation en C et C++. Il modifie le code source avant même que le compilateur ne commence son travail. Toutes les directives de préprocesseur commencent par le symbole `#`.

        ---

        ### 1. Directives d'inclusion (`#include`)

        Utilisé pour inclure le contenu d'un autre fichier dans le fichier source actuel.

        * **`#include <nom_fichier>`**: Utilisé pour les fichiers d'en-tête standard ou système (qui se trouvent généralement dans des répertoires d'inclusion prédéfinis).
            ```c
            #include <stdio.h>    // Pour les fonctions d'entrée/sortie standard en C
            #include <iostream>   // Pour les flux d'entrée/sortie en C++
            #include <vector>     // Pour le conteneur vector en C++
            ```

        * **`#include "nom_fichier"`**: Utilisé pour les fichiers d'en-tête définis par l'utilisateur (qui se trouvent généralement dans le répertoire du projet ou dans un chemin spécifié).
            ```c
            #include "mon_header.h" // Inclut un fichier d'en-tête personnalisé
            ```
        **Effet:** Le préprocesseur remplace la directive `#include` par le contenu complet du fichier inclus.

        ---

        ### 2. Macros de définition (`#define`)

        Utilisé pour définir des **macros**, qui sont des substitutions textuelles. Elles peuvent être utilisées pour définir des constantes symboliques ou de courtes fonctions "inline".

        * **Constantes symboliques:**
            ```c
            #define PI 3.14159
            #define MAX_SIZE 100

            // Utilisation
            float cercle_aire = PI * rayon * rayon;
            int tableau[MAX_SIZE];
            ```
        * **Macros avec arguments (similaire à des fonctions):** Attention aux effets de bord et à la priorité des opérateurs !
            ```c
            #define ADD(a, b) ((a) + (b)) // Les parenthèses sont cruciales pour éviter les problèmes de priorité

            int x = ADD(5, 3); // Le préprocesseur remplace ceci par ((5) + (3))
            ```
        * **Supprimer une macro (`#undef`):**
            ```c
            #define DEBUG_MODE
            // ... code dépendant de DEBUG_MODE
            #undef DEBUG_MODE // DEBUG_MODE n'est plus défini après cette ligne
            ```

        ---

        ### 3. Compilation Conditionnelle (`#ifdef`, `#ifndef`, `#if`, `#else`, `#elif`, `#endif`)

        Ces directives permettent de compiler ou d'ignorer des blocs de code en fonction de la définition de macros ou de conditions. Utile pour le débogage, les plateformes différentes, ou les versions de fonctionnalités.

        * **`#ifdef MACRO`**: Compile le code suivant si `MACRO` est défini.
        * **`#ifndef MACRO`**: Compile le code suivant si `MACRO` n'est **pas** défini.
        * **`#if condition`**: Compile le code si `condition` est vraie (la condition doit être une expression constante entière).
        * **`#else`**: Bloc de code alternatif.
        * **`#elif condition`**: Combinaison de `else if`.
        * **`#endif`**: Marque la fin d'un bloc conditionnel.

        ```c
        #define DEBUG // Macro de débogage

        #ifdef DEBUG
        #include <assert.h> // Inclut assert.h si DEBUG est défini
        #define LOG(msg) printf("[DEBUG] %s\\n", msg)
        #else
        #define LOG(msg) // Ne fait rien en mode non-débogage
        #endif

        int main() {
            LOG("Démarrage du programme."); // Sera imprimé si DEBUG est défini
            // ...
            #if __cplusplus >= 201103L // Vérifie si le standard C++11 ou plus est utilisé
                // Code spécifique à C++11 et versions ultérieures
            #else
                // Code pour des versions C++ antérieures
            #endif
            return 0;
        }
        ```

        ---

        ### 4. Autres Directives

        * **`#error message`**: Arrête la compilation et affiche un message d'erreur.
        * **`#warning message`**: Affiche un message d'avertissement pendant la compilation.
        * **`#pragma`**: Directives spécifiques au compilateur (peuvent varier).

        Le préprocesseur est un outil puissant pour la modularisation, la configuration et la gestion des versions de votre code C/C++.
        """
        self._create_page_template("preprocessor", title, content)
    
    def _create_scope_operator_page(self):
        title = "L'Opérateur de Résolution de Portée `::` (Scope Resolution Operator)"
        content = """
        L'opérateur de résolution de portée `::` est un concept fondamental en C++ (et a une utilisation très limitée en C pour les structures anonymes, mais est omniprésent en C++). Il permet de spécifier à quel **contexte (portée)** appartient un nom.

        ---

        ### 1. Accéder aux Membres Statiques des Classes

        En C++, `::` est principalement utilisé pour accéder aux membres **statiques** (variables ou fonctions) d'une classe, sans avoir besoin d'un objet de cette classe.

        ```cpp
        #include <iostream>

        class MaClasse {
        public:
            static int compteur; // Membre de donnée statique
            static void saluer() { // Fonction membre statique
                std::cout << "Bonjour depuis la classe !" << std::endl;
            }
        };

        // Initialisation du membre statique (nécessaire en dehors de la classe)
        int MaClasse::compteur = 0; // Utilisation de ::

        int main() {
            MaClasse::saluer();          // Appel de la fonction statique
            MaClasse::compteur = 10;     // Accès à la variable statique
            std::cout << "Compteur de classe: " << MaClasse::compteur << std::endl;
            return 0;
        }
        ```

        ---

        ### 2. Accéder aux Membres d'une Classe depuis l'extérieur (Définition de Méthodes)

        Lorsque vous définissez une fonction membre d'une classe **en dehors de la définition de la classe**, vous devez utiliser l'opérateur `::` pour spécifier à quelle classe cette fonction appartient.

        ```cpp
        #include <iostream>
        #include <string>

        class Personne {
        public:
            std::string nom;
            int age;

            void afficherInfos(); // Déclaration de la fonction membre
        };

        // Définition de la fonction membre en dehors de la classe
        void Personne::afficherInfos() { // Personne:: spécifie que afficherInfos appartient à Personne
            std::cout << "Nom: " << nom << ", Age: " << age << std::endl;
        }

        int main() {
            Personne p;
            p.nom = "Alice";
            p.age = 30;
            p.afficherInfos(); // Appel de la fonction
            return 0;
        }
        ```

        ---

        ### 3. Résolution de Portée de Noms (Namespaces)

        L'opérateur `::` est fondamental pour travailler avec les **espaces de noms (`namespaces`)** en C++. Un espace de noms est un conteneur qui organise des groupes de code logiquement liés pour éviter les conflits de noms.

        * **Accès direct:**
            ```cpp
            #include <iostream>

            namespace MaBibliotheque {
                int valeur = 100;
                void saluer() {
                    std::cout << "Salut de MaBibliotheque!" << std::endl;
                }
            }

            int main() {
                // Accéder aux membres du namespace en utilisant l'opérateur ::
                std::cout << "Valeur: " << MaBibliotheque::valeur << std::endl;
                MaBibliotheque::saluer();

                // std est aussi un namespace !
                std::cout << "Bonjour depuis std::cout !" << std::endl;
                return 0;
            }
            ```
        * **Avec `using namespace` (à utiliser avec prudence):**
            ```cpp
            #include <iostream>
            using namespace MaBibliotheque; // Importe tous les noms de MaBibliotheque dans la portée actuelle

            int main() {
                std::cout << "Valeur: " << valeur << std::endl; // Plus besoin de MaBibliotheque::
                saluer();
                return 0;
            }
            ```

        ---

        ### 4. Accéder à des Membres de Classes de Base Ambigus (Héritage Multiple)

        Dans le cas d'héritage multiple où une classe dérive de plusieurs classes de base ayant des membres avec le même nom, l'opérateur `::` peut être utilisé pour spécifier quel membre de quelle classe de base vous souhaitez utiliser.

        ```cpp
        #include <iostream>

        class BaseA {
        public:
            void print() { std::cout << "Depuis BaseA" << std::endl; }
        };

        class BaseB {
        public:
            void print() { std::cout << "Depuis BaseB" << std::endl; }
        };

        class Derivee : public BaseA, public BaseB {
        public:
            void f() {
                BaseA::print(); // Spécifie d'appeler print() de BaseA
                BaseB::print(); // Spécifie d'appeler print() de BaseB
            }
        };

        int main() {
            Derivee d;
            d.f();
            return 0;
        }
        ```

        ---

        ### 5. Opérateur de Portée Globale

        Lorsque le `::` est utilisé sans nom de classe ou de namespace devant, il fait référence à la **portée globale**. Cela est utile pour accéder à une variable globale qui a été "masquée" (shadowed) par une variable locale du même nom.

        ```cpp
        #include <iostream>

        int global_var = 100; // Variable globale

        int main() {
            int global_var = 50; // Variable locale avec le même nom

            std::cout << "Variable locale: " << global_var << std::endl;         // Affiche 50
            std::cout << "Variable globale: " << ::global_var << std::endl;    // Affiche 100 (accès à la globale)
            return 0;
        }
        ```

        L'opérateur `::` est donc un outil puissant et polyvalent en C++ pour gérer la visibilité et l'accès aux noms dans différents contextes de portée.
        """
        self._create_page_template("scope_operator", title, content)

    def _create_intro_cpp_page(self):
        title = "Introduction au C++ : Évolution du C"
        content = """
        Le **C++** est un langage de programmation **multi-paradigme** (procédural, orienté objet, générique) créé par Bjarne Stroustrup, étendant le langage C. Il offre des fonctionnalités de haut niveau tout en conservant un contrôle de bas niveau sur la mémoire.

        ---

        ### 1. C++ comme "C avec des Classes"

        À l'origine, C++ a été conçu comme une extension du C, en y ajoutant principalement des fonctionnalités de **Programmation Orientée Objet (POO)**. Cela signifie que la plupart du code C valide est également du code C++ valide (avec quelques exceptions mineures).

        ---

        ### 2. Entrées/Sorties avec `iostream` (au lieu de `stdio.h`)

        En C++, l'entrée/sortie est gérée par la bibliothèque `<iostream>` et les objets `std::cout` (pour la sortie) et `std::cin` (pour l'entrée), utilisant les opérateurs de flux `<<` (insertion) et `>>` (extraction). C'est plus type-sûr et extensible que les fonctions `printf`/`scanf` de C.

        ```cpp
        #include <iostream> // Pour std::cout et std::cin
        #include <string>   // Pour std::string

        int main() {
            std::cout << "Entrez votre nom : "; // Affiche un message
            std::string nom;
            std::cin >> nom; // Lit une chaîne de caractères

            int age;
            std::cout << "Entrez votre âge : ";
            std::cin >> age; // Lit un entier

            std::cout << "Bonjour, " << nom << "! Vous avez " << age << " ans." << std::endl;
            // std::endl ajoute un saut de ligne et vide le buffer (flush)

            return 0;
        }
        ```

        ---

        ### 3. Espaces de Noms (`namespaces`)

        Les **espaces de noms** sont une fonctionnalité de C++ (absente en C) qui aide à organiser le code et à éviter les conflits de noms, surtout dans les grands projets ou lors de l'utilisation de bibliothèques tierces.
        La plupart des fonctionnalités de la bibliothèque standard de C++ sont encapsulées dans l'espace de noms `std`.

        ```cpp
        #include <iostream> // Contient std::cout, std::endl
        #include <string>   // Contient std::string

        // Déclaration d'un namespace personnalisé
        namespace MonProjet {
            void direBonjour() {
                std::cout << "Bonjour de MonProjet!" << std::endl;
            }
        }

        int main() {
            // Accès explicite aux éléments du namespace
            std::cout << "Utilisation de std::cout." << std::endl;
            MonProjet::direBonjour();

            // Utilisation de 'using namespace' (peut être pratique pour de petits fichiers)
            // ATTENTION: à éviter dans les fichiers d'en-tête (.h/.hpp)
            using namespace std;
            using namespace MonProjet;
            
            cout << "Utilisation de cout sans std:: prefixe." << endl;
            direBonjour();

            return 0;
        }
        ```

        ---

        ### 4. Références (`&`)

        Les **références** en C++ sont des alias pour des variables existantes. Une fois initialisée, une référence ne peut pas être changée pour faire référence à une autre variable. Elles sont souvent utilisées pour passer des arguments à des fonctions "par référence", évitant la copie et permettant de modifier la variable originale.

        ```cpp
        #include <iostream>

        void modifierValeur(int& ref) { // 'ref' est une référence à un entier
            ref = 100; // Modifie la variable originale passée en argument
        }

        int main() {
            int original = 10;
            int& alias = original; // 'alias' est une référence à 'original'

            std::cout << "Original: " << original << ", Alias: " << alias << std::endl; // 10, 10

            alias = 20; // Modifier 'alias' modifie aussi 'original'
            std::cout << "Original après modification de alias: " << original << std::endl; // 20

            modifierValeur(original); // Passe 'original' par référence
            std::cout << "Original après appel fonction: " << original << std::endl; // 100

            return 0;
        }
        ```

        ---

        ### 5. Surcharge de Fonctions (Function Overloading)

        C++ permet de définir plusieurs fonctions avec le **même nom** tant qu'elles ont des **signatures différentes** (nombre ou types des paramètres). Le compilateur choisit la bonne fonction en fonction des arguments passés.

        ```cpp
        #include <iostream>

        int addition(int a, int b) {
            return a + b;
        }

        double addition(double a, double b) { // Même nom, mais types de paramètres différents
            return a + b;
        }

        std::string addition(std::string s1, std::string s2) { // Même nom, types différents
            return s1 + s2;
        }

        int main() {
            std::cout << "Addition (int): " << addition(5, 3) << std::endl;          // Appelle int addition(int, int)
            std::cout << "Addition (double): " << addition(5.5, 3.2) << std::endl;  // Appelle double addition(double, double)
            std::cout << "Addition (string): " << addition("Hello", "World") << std::endl; // Appelle string addition(string, string)
            return 0;
        }
        ```

        Ces fonctionnalités sont parmi les premières améliorations que C++ apporte par rapport à C, ouvrant la voie à la Programmation Orientée Objet et à d'autres paradigmes.
        """
        self._create_page_template("intro_cpp", title, content)

    def _create_oop_cpp_page(self):
        title = "Programmation Orientée Objet (POO) en C++ : Les Bases"
        content = """
        La **Programmation Orientée Objet (POO)** est un paradigme de programmation qui organise le code autour d'**objets** plutôt que de fonctions et de logique. En C++, la POO repose sur quatre piliers : l'**Encapsulation**, l'**Abstraction**, l'**Héritage** et le **Polymorphisme**.

        ---

        ### 1. Classes et Objets

        * Une **classe** est un plan (blueprint) ou un modèle pour créer des objets. Elle définit les propriétés (variables membres) et les comportements (fonctions membres) que les objets de ce type auront.
        * Un **objet** est une instance concrète d'une classe.

        ```cpp
        #include <iostream>
        #include <string>

        // Déclaration d'une classe 'Chien'
        class Chien {
        public: // Spécificateur d'accès: membres accessibles de l'extérieur
            std::string nom;
            std::string race;
            int age;

            // Fonction membre (méthode)
            void aboyer() {
                std::cout << nom << " aboie : Wouaf wouaf !" << std::endl;
            }

            // Constructeur: fonction spéciale appelée lors de la création d'un objet
            Chien(std::string n, std::string r, int a) {
                nom = n;
                race = r;
                age = a;
                std::cout << nom << " est né !" << std::endl;
            }

            // Destructeur: fonction spéciale appelée lorsque l'objet est détruit
            ~Chien() {
                std::cout << nom << " nous a quittés..." << std::endl;
            }
        };

        int main() {
            // Création d'objets (instances de la classe Chien)
            Chien monChien("Buddy", "Labrador", 3); // Appel du constructeur
            Chien sonChien("Rex", "Berger Allemand", 5);

            // Accès aux membres de l'objet
            std::cout << monChien.nom << " est un " << monChien.race << "." << std::endl;

            // Appel de fonctions membres
            monChien.aboyer();
            sonChien.aboyer();

            // Les destructeurs seront appelés automatiquement à la fin de main()
            return 0;
        }
        ```

        ---

        ### 2. Encapsulation

        L'**encapsulation** est le principe de regrouper les données (variables membres) et les méthodes (fonctions membres) qui opèrent sur ces données en une seule unité (la classe), et de restreindre l'accès direct à certaines de ces données. Ceci est réalisé avec les **spécificateurs d'accès**:

        * **`public`**: Membres accessibles depuis n'importe où.
        * **`private`**: Membres accessibles uniquement depuis l'intérieur de la classe elle-même. C'est le niveau d'accès par défaut pour les membres de classe si rien n'est spécifié.
        * **`protected`**: Membres accessibles depuis l'intérieur de la classe et depuis les classes dérivées (héritées).

        Les données privées sont généralement accédées via des fonctions publiques appelées **accesseurs (getters)** et **mutateurs (setters)**.

        ```cpp
        #include <iostream>
        #include <string>

        class CompteBancaire {
        private:
            std::string titulaire;
            double solde; // Rendu privé pour l'encapsulation

        public:
            CompteBancaire(std::string t, double s) : titulaire(t), solde(s) {}

            // Getter pour le solde
            double getSolde() const { // 'const' indique que la fonction ne modifie pas l'objet
                return solde;
            }

            // Setter pour déposer
            void deposer(double montant) {
                if (montant > 0) {
                    solde += montant;
                    std::cout << "Dépôt de " << montant << " effectué. Nouveau solde: " << solde << std::endl;
                } else {
                    std::cout << "Le montant du dépôt doit être positif." << std::endl;
                }
            }

            // Setter pour retirer
            void retirer(double montant) {
                if (montant > 0 && solde >= montant) {
                    solde -= montant;
                    std::cout << "Retrait de " << montant << " effectué. Nouveau solde: " << solde << std::endl;
                } else {
                    std::cout << "Fonds insuffisants ou montant invalide." << std::endl;
                }
            }
        };

        int main() {
            CompteBancaire monCompte("Jean Dupont", 1000.0);
            // monCompte.solde = 500; // Erreur de compilation: 'solde' est privé

            std::cout << "Solde initial: " << monCompte.getSolde() << std::endl;
            monCompte.deposer(200.0);
            monCompte.retirer(500.0);
            monCompte.retirer(800.0); // Tentative de retrait trop important

            return 0;
        }
        ```

        ---

        ### 3. Héritage

        L'**héritage** permet à une nouvelle classe (classe dérivée ou sous-classe) d'hériter des propriétés et des comportements d'une classe existante (classe de base ou super-classe). Cela favorise la réutilisation du code et établit une relation "est un type de" (Is-A relationship).

        ```cpp
        #include <iostream>
        #include <string>

        // Classe de base
        class Animal {
        public:
            std::string nom;
            int age;

            Animal(std::string n, int a) : nom(n), age(a) {
                std::cout << "Un animal nommé " << nom << " est créé." << std::endl;
            }

            void manger() {
                std::cout << nom << " mange." << std::endl;
            }

            ~Animal() {
                std::cout << "L'animal " << nom << " est détruit." << std::endl;
            }
        };

        // Classe dérivée de Animal
        class Chat : public Animal { // 'public Animal' signifie héritage public
        public:
            std::string couleurPelage;

            // Constructeur de Chat qui appelle le constructeur de la classe de base
            Chat(std::string n, int a, std::string couleur) : Animal(n, a), couleurPelage(couleur) {
                std::cout << "Un chat " << nom << " de couleur " << couleurPelage << " est créé." << std::endl;
            }

            void miauler() {
                std::cout << nom << " miaule: Miaou !" << std::endl;
            }

            // Les fonctions manger() et les membres nom, age sont hérités
        };

        int main() {
            Chat monChat("Whiskers", 2, "Noir");
            monChat.manger();   // Appel de la fonction héritée de Animal
            monChat.miauler();  // Appel de la fonction spécifique à Chat

            std::cout << "Nom du chat: " << monChat.nom << ", Age: " << monChat.age << std::endl;

            return 0;
        }
        ```
        **Types d'héritage:** `public`, `protected`, `private`. L'héritage `public` est le plus courant et maintient les spécificateurs d'accès des membres hérités.

        ---

        ### 4. Polymorphisme (avec fonctions virtuelles)

        Le **polymorphisme** ("plusieurs formes") permet de traiter des objets de classes différentes de manière uniforme via une interface commune. En C++, il est principalement réalisé à l'aide de **fonctions virtuelles** et de pointeurs/références à la classe de base.

        * Une fonction **virtuelle** est une fonction membre déclarée dans la classe de base avec le mot-clé `virtual`. Elle peut être redéfinie dans les classes dérivées.
        * Lorsqu'une fonction virtuelle est appelée via un pointeur ou une référence à la classe de base, la version de la fonction du **type réel de l'objet** est exécutée au moment de l'exécution (liaison dynamique).

        ```cpp
        #include <iostream>
        #include <vector>
        #include <memory> // Pour std::unique_ptr

        class Forme { // Classe de base abstraite (parfois appelée interface si toutes les méthodes sont pures virtuelles)
        public:
            // Fonction virtuelle pure: rend la classe Forme abstraite.
            // Une classe abstraite ne peut pas être instanciée directement.
            virtual void dessiner() = 0; 
            
            // Un destructeur virtuel est crucial pour assurer que le bon destructeur
            // de la classe dérivée est appelé lors de la suppression via un pointeur de base.
            virtual ~Forme() {
                std::cout << "Destructeur de Forme." << std::endl;
            }
        };

        class Cercle : public Forme {
        public:
            void dessiner() override { // 'override' (C++11) est facultatif mais bonne pratique
                std::cout << "Dessiner un cercle." << std::endl;
            }
            ~Cercle() override {
                std::cout << "Destructeur de Cercle." << std::endl;
            }
        };

        class Rectangle : public Forme {
        public:
            void dessiner() override {
                std::cout << "Dessiner un rectangle." << std::endl;
            }
            ~Rectangle() override {
                std::cout << "Destructeur de Rectangle." << std::endl;
            }
        };

        int main() {
            // Utilisation de pointeurs vers la classe de base pour démontrer le polymorphisme
            // std::unique_ptr gère automatiquement la libération mémoire
            std::vector<std::unique_ptr<Forme>> formes;
            formes.push_back(std::make_unique<Cercle>());
            formes.push_back(std::make_unique<Rectangle>());

            for (const auto& forme : formes) {
                forme->dessiner(); // Appelle la version spécifique à l'objet réel (Cercle ou Rectangle)
            }
            // Les destructeurs sont appelés automatiquement lorsque les unique_ptr sont hors de portée

            // Forme f; // Erreur: 'Forme' est une classe abstraite et ne peut pas être instanciée
            
            return 0;
        }
        ```
        Le polymorphisme est un concept clé pour créer des architectures logicielles flexibles et extensibles.
        """
        self._create_page_template("oop_cpp", title, content)
    
    def _create_oop_adv_page(self):
        title = "Programmation Orientée Objet (POO) en C++ : Concepts Avancés"
        content = """
        Après les bases de la POO, C++ offre des mécanismes plus avancés pour la conception orientée objet.

        ---

        ### 1. Classes Abstraites et Fonctions Virtuelles Pures

        Une **classe abstraite** est une classe qui contient au moins une **fonction virtuelle pure**.
        * Une fonction virtuelle pure est déclarée avec `= 0;` à la fin de sa signature (par exemple, `virtual void maFonction() = 0;`).
        * Une classe abstraite **ne peut pas être instanciée directement**.
        * Les classes dérivées d'une classe abstraite **doivent implémenter toutes ses fonctions virtuelles pures**, sinon elles deviennent elles-mêmes abstraites.
        * Les classes abstraites sont souvent utilisées pour définir une **interface** ou un contrat que les classes dérivées doivent respecter.

        ```cpp
        #include <iostream>
        #include <memory> // Pour std::unique_ptr

        class Instrument { // Classe de base abstraite
        public:
            virtual void jouer() = 0; // Fonction virtuelle pure
            virtual ~Instrument() { // Destructeur virtuel recommandé
                std::cout << "Destructeur Instrument." << std::endl;
            }
        };

        class Guitare : public Instrument {
        public:
            void jouer() override { // Implémente la fonction virtuelle pure
                std::cout << "La guitare joue une mélodie." << std::endl;
            }
            ~Guitare() override {
                std::cout << "Destructeur Guitare." << std::endl;
            }
        };

        class Piano : public Instrument {
        public:
            void jouer() override {
                std::cout << "Le piano joue un accord." << std::endl;
            }
            ~Piano() override {
                std::cout << "Destructeur Piano." << std::endl;
            }
        };

        int main() {
            // Instrument i; // ERREUR: Impossible d'instancier une classe abstraite

            std::unique_ptr<Instrument> maGuitare = std::make_unique<Guitare>();
            std::unique_ptr<Instrument> monPiano = std::make_unique<Piano>();

            maGuitare->jouer();
            monPiano->jouer();

            return 0;
        }
        ```

        ---

        ### 2. Destructeurs Virtuels

        Lorsque vous utilisez le **polymorphisme** (pointeurs de classe de base pointant vers des objets de classe dérivée), il est **crucial** que le **destructeur de la classe de base soit virtuel**.
        Si le destructeur de la classe de base n'est pas virtuel et que vous supprimez un objet dérivé via un pointeur de la classe de base, seul le destructeur de la classe de base sera appelé, entraînant des **fuites de mémoire** et un comportement indéfini si la classe dérivée a des ressources à libérer.

        ```cpp
        #include <iostream>
        #include <memory>

        class Base {
        public:
            Base() { std::cout << "Constructeur Base" << std::endl; }
            virtual ~Base() { // Destructeur VIRTUEL
                std::cout << "Destructeur Base" << std::endl;
            }
            void faireQuelqueChose() { std::cout << "Faire quelque chose dans Base." << std::endl; }
        };

        class Derivee : public Base {
        public:
            int* data;
            Derivee() : Base() {
                std::cout << "Constructeur Derivee" << std::endl;
                data = new int[10]; // Alloue de la mémoire
            }
            ~Derivee() override { // Destructeur de la classe Derivee (override est implicite avec virtual)
                std::cout << "Destructeur Derivee" << std::endl;
                delete[] data; // Libère la mémoire
            }
        };

        int main() {
            Base* ptr = new Derivee(); // Un pointeur de Base vers un objet Derivee
            ptr->faireQuelqueChose();
            delete ptr; // Si ~Base() n'était pas virtuel, ~Derivee() ne serait PAS appelé!
            // Avec un destructeur virtuel, le destructeur de Derivee est appelé en premier, puis celui de Base.
            return 0;
        }
        ```
        **Règle d'or:** Si une classe a au moins une fonction virtuelle, son destructeur doit être virtuel.

        ---

        ### 3. Fonctions et Classes Amies (`friend`)

        Les fonctions et classes **amies** (`friend`) permettent à des fonctions ou classes externes d'accéder aux membres **privés** et **protégés** d'une autre classe, brisant l'encapsulation. À utiliser avec parcimonie.

        * **Fonction amie:**
            ```cpp
            #include <iostream>

            class MaClasse {
            private:
                int valeur_privee = 10;
            public:
                // Déclaration de la fonction amie
                friend void afficherValeurPrivee(MaClasse obj);
            };

            // Définition de la fonction amie
            void afficherValeurPrivee(MaClasse obj) {
                std::cout << "Accès à valeur_privee via fonction amie: " << obj.valeur_privee << std::endl;
            }

            int main() {
                MaClasse m;
                afficherValeurPrivee(m);
                return 0;
            }
            ```
        * **Classe amie:**
            ```cpp
            #include <iostream>

            class AutreClasse; // Déclaration anticipée

            class MaClasseAvecAmi {
            private:
                int secret_value = 20;
            public:
                friend class AutreClasse; // Déclaration d'AutreClasse comme classe amie
            };

            class AutreClasse {
            public:
                void revelerSecret(MaClasseAvecAmi obj) {
                    std::cout << "Le secret est: " << obj.secret_value << std::endl;
                }
            };

            int main() {
                MaClasseAvecAmi m;
                AutreClasse a;
                a.revelerSecret(m);
                return 0;
            }
            ```

        ---

        ### 4. Surcharge d'Opérateurs (Operator Overloading)

        C++ permet de redéfinir le comportement des opérateurs (comme `+`, `-`, `*`, `==`, `<<`, `>>`) pour les types définis par l'utilisateur (classes). Cela rend le code plus intuitif et lisible.

        ```cpp
        #include <iostream>

        class Point {
        public:
            int x, y;

            Point(int _x = 0, int _y = 0) : x(_x), y(_y) {}

            // Surcharge de l'opérateur +
            Point operator+(const Point& autre) const {
                return Point(this->x + autre.x, this->y + autre.y);
            }

            // Surcharge de l'opérateur ==
            bool operator==(const Point& autre) const {
                return (this->x == autre.x && this->y == autre.y);
            }

            // Surcharge de l'opérateur d'insertion de flux (pour std::cout)
            friend std::ostream& operator<<(std::ostream& os, const Point& p);
        };

        std::ostream& operator<<(std::ostream& os, const Point& p) {
            os << "(" << p.x << ", " << p.y << ")";
            return os;
        }

        int main() {
            Point p1(10, 20);
            Point p2(5, 15);
            Point p3 = p1 + p2; // Appelle operator+

            std::cout << "P1: " << p1 << std::endl; // Appelle operator<<
            std::cout << "P2: " << p2 << std::endl;
            std::cout << "P1 + P2 = " << p3 << std::endl; // (15, 35)

            if (p1 == p2) { // Appelle operator==
                std::cout << "P1 est égal à P2" << std::endl;
            } else {
                std::cout << "P1 n'est PAS égal à P2" << std::endl;
            }

            return 0;
        }
        ```
        La surcharge d'opérateurs peut améliorer considérablement l'expressivité du code, mais doit être utilisée de manière cohérente et intuitive.

        Ces concepts avancés sont essentiels pour concevoir des systèmes orientés objet robustes et bien structurés en C++.
        """
        self._create_page_template("oop_adv", title, content)

    def _create_exceptions_page(self):
        title = "Gestion des Exceptions (C++)"
        content = """
        La **gestion des exceptions** en C++ est un mécanisme robuste pour gérer les erreurs et les situations anormales de manière propre et organisée, séparant la logique d'erreur de la logique normale du programme.

        ---

        ### 1. Blocs `try`, `catch`, `throw`

        * **`try`**: Un bloc de code où des exceptions *peuvent* être levées (jetées).
        * **`throw`**: Utilisé pour lever une exception. Cela peut être n'importe quel type de données (un entier, une chaîne, un objet d'une classe d'exception).
        * **`catch`**: Un bloc de code qui "attrape" (gère) une exception levée dans le bloc `try` correspondant. Un bloc `catch` spécifie le type d'exception qu'il peut gérer.

        ```cpp
        #include <iostream>
        #include <string>

        double diviser(double numerateur, double denominateur) {
            if (denominateur == 0) {
                // Lever une exception (ici, une chaîne de caractères)
                throw std::string("Erreur: Division par zéro impossible !");
            }
            return numerateur / denominateur;
        }

        int main() {
            try {
                // Code qui pourrait lever une exception
                double resultat1 = diviser(10.0, 2.0);
                std::cout << "Résultat 1: " << resultat1 << std::endl; // Affiche 5.0

                double resultat2 = diviser(5.0, 0.0); // Cette ligne lève une exception
                std::cout << "Résultat 2: " << resultat2 << std::endl; // Cette ligne ne sera PAS exécutée
            }
            catch (const std::string& e) { // Attrape une exception de type std::string
                std::cerr << "Exception attrapée: " << e << std::endl;
            }
            catch (...) { // Attrape n'importe quel autre type d'exception (catch-all)
                std::cerr << "Une exception inconnue a été attrapée." << std::endl;
            }

            std::cout << "Le programme continue après la gestion de l'exception." << std::endl;
            return 0;
        }
        ```

        ---

        ### 2. Classes d'Exceptions Standard (`<stdexcept>`)

        C++ fournit une hiérarchie de classes d'exceptions standard dans l'en-tête `<stdexcept>`. Il est généralement préférable de lever et d'attraper des objets de ces classes ou de classes dérivées, plutôt que des types de base comme `int` ou `std::string`.
        La classe de base pour toutes les exceptions standard est `std::exception`.

        * **`std::runtime_error`**: Pour les erreurs qui ne peuvent être détectées qu'à l'exécution.
        * **`std::logic_error`**: Pour les erreurs logiques dans le programme.
        * **`std::overflow_error`**: Pour les dépassements de capacité.
        * **`std::out_of_range`**: Pour les accès hors limites (ex: vecteurs).
        * etc.

        ```cpp
        #include <iostream>
        #include <stdexcept> // Pour std::runtime_error, std::out_of_range
        #include <vector>

        void accederElement(const std::vector<int>& vec, int index) {
            if (index < 0 || index >= vec.size()) {
                throw std::out_of_range("L'index est hors limites !");
            }
            std::cout << "Valeur à l'index " << index << " : " << vec.at(index) << std::endl;
        }

        int main() {
            std::vector<int> nombres = {10, 20, 30};

            try {
                accederElement(nombres, 0); // OK
                accederElement(nombres, 2); // OK
                accederElement(nombres, 5); // Lève std::out_of_range
            }
            catch (const std::out_of_range& e) { // Attrape une exception spécifique
                std::cerr << "Erreur d'accès : " << e.what() << std::endl; // e.what() donne le message
            }
            catch (const std::exception& e) { // Attrape toute autre exception standard
                std::cerr << "Erreur générique : " << e.what() << std::endl;
            }
            catch (...) { // Attrape toute autre exception non standard
                std::cerr << "Erreur inconnue." << std::endl;
            }

            std::cout << "Fin du programme." << std::endl;
            return 0;
        }
        ```

        ---

        ### 3. Créer ses Propres Classes d'Exceptions

        Pour des erreurs spécifiques à votre application, il est recommandé de créer vos propres classes d'exceptions en dérivant de `std::exception` (ou une de ses sous-classes) et en surchargeant la méthode virtuelle `what()`.

        ```cpp
        #include <iostream>
        #include <stdexcept> // Pour std::exception
        #include <string>

        // Ma classe d'exception personnalisée
        class MaPropreErreur : public std::runtime_error {
        public:
            // Le constructeur de base prend une chaîne pour le message d'erreur
            MaPropreErreur(const std::string& msg) : std::runtime_error(msg) {}

            // Surcharge de what() pour fournir une description
            // const char* what() const noexcept override {
            //     return "MaPropreErreur: " + std::string(std::runtime_error::what()); // Ce n'est pas permis, what() doit retourner const char*
            // }
            // Mieux vaut simplement passer le message au constructeur de la classe de base
        };

        void traitementDonnees(int valeur) {
            if (valeur < 0) {
                throw MaPropreErreur("Valeur négative détectée, impossible de traiter !");
            }
            std::cout << "Traitement de la valeur : " << valeur << std::endl;
        }

        int main() {
            try {
                traitementDonnees(10);
                traitementDonnees(-5); // Lève MaPropreErreur
            }
            catch (const MaPropreErreur& e) {
                std::cerr << "Erreur personnalisée attrapée: " << e.what() << std::endl;
            }
            catch (const std::exception& e) {
                std::cerr << "Erreur standard attrapée: " << e.what() << std::endl;
            }
            return 0;
        }
        ```

        ---

        ### 4. Spécifications `noexcept` (C++11)

        Le mot-clé `noexcept` (C++11) indique au compilateur qu'une fonction ne lèvera **jamais** d'exception. Cela permet au compilateur de faire des optimisations. Si une fonction déclarée `noexcept` lève une exception, le programme se terminera immédiatement (`std::terminate`).

        ```cpp
        #include <iostream>

        void fonction_sans_exception() noexcept {
            std::cout << "Cette fonction est garantie sans exception." << std::endl;
            // throw 1; // Si décommenté, cela provoquerait un appel à std::terminate()
        }

        void fonction_peut_lever_exception() {
            std::cout << "Cette fonction peut lever une exception." << std::endl;
            throw "Oh non, une erreur !";
        }

        int main() {
            try {
                fonction_sans_exception();
                fonction_peut_lever_exception();
            }
            catch (const char* msg) {
                std::cerr << "Erreur: " << msg << std::endl;
            }
            return 0;
        }
        ```

        La gestion des exceptions est une meilleure pratique pour la robustesse des applications C++, rendant le code plus clair et plus facile à maintenir en séparant la logique métier des mécanismes de traitement d'erreur.
        """
        self._create_page_template("exceptions", title, content)

    def _create_templates_stl_page(self):
        title = "Modèles (Templates) et STL (Standard Template Library)"
        content = """
        Les **modèles (templates)** en C++ permettent d'écrire du code générique qui peut fonctionner avec n'importe quel type de données, sans avoir à le réécrire pour chaque type. La **Bibliothèque Standard de Modèles (STL)** est une collection de classes et fonctions génériques qui tirent parti des modèles pour fournir des structures de données et des algorithmes puissants et réutilisables.

        ---

        ### 1. Modèles de Fonctions (Function Templates)

        Un modèle de fonction définit une famille de fonctions. Le compilateur génère automatiquement une version spécifique de la fonction pour chaque type utilisé lors de l'appel.

        ```cpp
        #include <iostream>
        #include <string>

        // Modèle de fonction pour échanger deux valeurs
        template <typename T> // 'T' est un paramètre de type
        void echanger(T& a, T& b) {
            T temp = a;
            a = b;
            b = temp;
        }

        int main() {
            int i1 = 5, i2 = 10;
            std::cout << "Avant échange: i1=" << i1 << ", i2=" << i2 << std::endl;
            echanger(i1, i2); // Le compilateur instancie echanger<int>
            std::cout << "Après échange: i1=" << i1 << ", i2=" << i2 << std::endl;

            double d1 = 3.14, d2 = 2.71;
            std::cout << "Avant échange: d1=" << d1 << ", d2=" << d2 << std::endl;
            echanger(d1, d2); // Le compilateur instancie echanger<double>
            std::cout << "Après échange: d1=" << d1 << ", d2=" << d2 << std::endl;

            std::string s1 = "Bonjour", s2 = "Monde";
            std::cout << "Avant échange: s1='" << s1 << "', s2='" << s2 << "'" << std::endl;
            echanger(s1, s2); // Le compilateur instancie echanger<std::string>
            std::cout << "Après échange: s1='" << s1 << "', s2='" << s2 << "'" << std::endl;

            return 0;
        }
        ```
        Vous pouvez utiliser `class T` ou `typename T` indifféremment pour les paramètres de type de modèle.

        ---

        ### 2. Modèles de Classes (Class Templates)

        Un modèle de classe permet de définir une classe qui peut fonctionner avec différents types de données. Cela est très utilisé pour les structures de données.

        ```cpp
        #include <iostream>
        #include <string>

        // Modèle de classe pour une paire de valeurs
        template <typename T1, typename T2>
        class Paire {
        public:
            T1 premier;
            T2 second;

            Paire(T1 p, T2 s) : premier(p), second(s) {}

            void afficher() const {
                std::cout << "Paire: (" << premier << ", " << second << ")" << std::endl;
            }
        };

        int main() {
            Paire<int, double> p1(10, 3.14); // Instanciation avec int et double
            p1.afficher();

            Paire<std::string, char> p2("Lettre", 'X'); // Instanciation avec string et char
            p2.afficher();

            return 0;
        }
        ```

        ---

        ### 3. La Bibliothèque Standard de Modèles (STL)

        La STL est un ensemble de classes et fonctions génériques prédéfinies, conçues pour être réutilisables et efficaces. Elle se compose de :

        * **Conteneurs:** Objets qui stockent des collections de données (ex: `vector`, `list`, `map`, `set`, `deque`, `queue`, `stack`).
        * **Algorithmes:** Fonctions qui effectuent des opérations sur des conteneurs (ex: `sort`, `find`, `copy`, `transform`).
        * **Itérateurs:** Des objets qui agissent comme des pointeurs pour parcourir les éléments des conteneurs.
        * **Foncteurs (Function Objects):** Objets qui agissent comme des fonctions.
        * **Adaptateurs:** Adaptent le comportement des conteneurs ou des itérateurs.

        ---

        ### 4. Conteneurs STL Courants

        * **`std::vector` (tableau dynamique)**: Le plus utilisé. Tableau redimensionnable en mémoire contiguë.
            ```cpp
            #include <vector>
            #include <iostream>

            int main() {
                std::vector<int> nombres = {1, 2, 3};
                nombres.push_back(4); // Ajoute un élément à la fin
                std::cout << "Taille du vecteur: " << nombres.size() << std::endl; // 4
                std::cout << "Élément à l'index 2: " << nombres[2] << std::endl; // 3

                for (int n : nombres) { // Boucle for-each (C++11)
                    std::cout << n << " ";
                }
                std::cout << std::endl; // Affiche: 1 2 3 4
                return 0;
            }
            ```

        * **`std::string` (chaîne de caractères)**: Bien que non un "conteneur" au sens strict comme `vector`, c'est une classe fondamentale de la STL pour manipuler des séquences de caractères de manière sûre et pratique.
            ```cpp
            #include <string>
            #include <iostream>

            int main() {
                std::string s1 = "Hello";
                std::string s2 = " World";
                std::string s3 = s1 + s2; // Concaténation
                std::cout << s3 << std::endl; // Hello World
                std::cout << "Longueur: " << s3.length() << std::endl; // 11
                return 0;
            }
            ```

        * **`std::map` (tableau associatif / dictionnaire)**: Stocke des paires clé-valeur, où chaque clé est unique et triée.
            ```cpp
            #include <map>
            #include <string>
            #include <iostream>

            int main() {
                std::map<std::string, int> ages;
                ages["Alice"] = 30;
                ages["Bob"] = 24;
                ages["Charlie"] = 35;

                std::cout << "Age de Bob: " << ages["Bob"] << std::endl; // 24

                // Itération sur la map
                for (const auto& paire : ages) {
                    std::cout << paire.first << " a " << paire.second << " ans." << std::endl;
                }
                return 0;
            }
            ```

        * **`std::list` (liste doublement liée)**: Pour des insertions et suppressions efficaces n'importe où, mais un accès séquentiel.
        * **`std::set` (ensemble trié)**: Stocke des éléments uniques, triés.

        ---

        ### 5. Algorithmes STL Courants

        Les algorithmes opèrent sur des plages d'éléments définies par des itérateurs.

        ```cpp
        #include <vector>
        #include <algorithm> // Pour std::sort, std::find
        #include <iostream>
        #include <numeric>   // Pour std::accumulate

        int main() {
            std::vector<int> nombres = {5, 2, 8, 1, 9, 4};

            // Trier le vecteur
            std::sort(nombres.begin(), nombres.end());
            std::cout << "Vecteur trié: ";
            for (int n : nombres) { std::cout << n << " "; }
            std::cout << std::endl; // 1 2 4 5 8 9

            // Chercher un élément
            auto it = std::find(nombres.begin(), nombres.end(), 8);
            if (it != nombres.end()) {
                std::cout << "8 trouvé à l'index: " << std::distance(nombres.begin(), it) << std::endl; // 4
            } else {
                std::cout << "8 non trouvé." << std::endl;
            }

            // Calculer la somme
            int somme = std::accumulate(nombres.begin(), nombres.end(), 0);
            std::cout << "Somme des éléments: " << somme << std::endl; // 29

            return 0;
        }
        ```
        Les modèles et la STL sont des pierres angulaires du C++ moderne, permettant d'écrire du code générique, efficace et réutilisable, réduisant considérablement le besoin de réinventer la roue.
        """
        self._create_page_template("templates_stl", title, content)
    
    def _create_cpp14_features_page(self):
        title = "Nouveautés C++14"
        content = """
        Le standard **C++14** est une mise à jour mineure de C++11, se concentrant sur des améliorations de la productivité et de petites nouvelles fonctionnalités. Il a été publié en 2014.

        ---

        ### 1. Inférence de Type de Retour Automatique (`auto` pour les fonctions)

        En C++11, `auto` pouvait être utilisé pour inférer le type d'une variable. C++14 étend cette capacité aux **types de retour de fonctions**. Le compilateur déduit le type de retour à partir de l'expression `return`.

        ```cpp
        #include <iostream>
        #include <typeinfo> // Pour typeid

        // Le compilateur déduit que le type de retour est int
        auto addition(int a, int b) {
            return a + b;
        }

        // Peut même être utilisé avec des lambdas sans spécifier le type de retour
        auto creerLambda() {
            return [](double x, double y) {
                return x * y;
            };
        }

        int main() {
            auto res = addition(5, 7);
            std::cout << "Résultat de addition: " << res << " (Type: " << typeid(res).name() << ")" << std::endl; // res est int

            auto ma_lambda = creerLambda();
            std::cout << "Résultat de lambda: " << ma_lambda(2.5, 4.0) << std::endl; // Affiche 10.0
            return 0;
        }
        ```

        ---

        ### 2. Variables Membres Initialisables dans les Lambdas (Capture généralisée)

        C++11 permettait de capturer des variables de la portée englobante par copie ou par référence. C++14 introduit la **capture généralisée** (`init-capture`), qui permet de :
        * Déplacer des objets dans la capture.
        * Capturer des variables membres par leur nom (sans nécessiter que la variable existe déjà dans la portée englobante).

        Ceci est fait en utilisant une syntaxe `[nom_variable = expression]`.

        ```cpp
        #include <iostream>
        #include <memory> // Pour std::unique_ptr

        int main() {
            auto ptr = std::make_unique<int>(123);

            // C++11 ne permettrait pas de capturer 'ptr' directement par déplacement
            // C++14: capture par initialisation pour déplacer le unique_ptr
            auto lambda_avec_capture = [val = std::move(ptr)]() {
                if (val) {
                    std::cout << "Valeur capturée (déplacée): " << *val << std::endl;
                } else {
                    std::cout << "Le pointeur est nul." << std::endl;
                }
            };

            lambda_avec_capture(); // Affiche la valeur
            // std::cout << *ptr << std::endl; // Erreur: ptr a été déplacé et est maintenant nul

            return 0;
        }
        ```

        ---

        ### 3. Modèles de Variables (Variable Templates)

        C++14 permet de définir des **variables templates**, c'est-à-dire des variables qui peuvent être paramétrées par des types ou des valeurs.

        ```cpp
        #include <iostream>

        // Modèle de variable pour la valeur de PI
        template <typename T>
        constexpr T PI = static_cast<T>(3.14159265358979323846L);

        template <typename T>
        constexpr T EulerGamma = static_cast<T>(0.57721566490153286060L);

        int main() {
            std::cout.precision(10); // Pour afficher plus de décimales

            std::cout << "PI (double): " << PI<double> << std::endl;
            std::cout << "PI (float): " << PI<float> << std::endl;
            std::cout << "Euler Gamma (long double): " << EulerGamma<long double> << std::endl;

            return 0;
        }
        ```

        ---

        ### 4. Fonctions `constexpr` Améliorées

        En C++11, les fonctions `constexpr` étaient très restrictives (corps de fonction très simple, une seule instruction `return`). C++14 assouplit ces restrictions, permettant aux fonctions `constexpr` de contenir :
        * Plusieurs instructions `return`.
        * Des boucles (`for`, `while`).
        * Des déclarations de variables locales.
        * Des instructions `if`/`switch`.

        Cela permet d'effectuer des calculs plus complexes au moment de la compilation.

        ```cpp
        #include <iostream>

        constexpr int factorielle(int n) {
            int res = 1;
            for (int i = 1; i <= n; ++i) {
                res *= i;
            }
            return res;
        }

        int main() {
            // Calculé au moment de la compilation
            constexpr int fact5 = factorielle(5);
            std::cout << "Factorielle de 5 (constexpr): " << fact5 << std::endl; // 120

            int val = 4;
            // Peut aussi être appelé à l'exécution
            std::cout << "Factorielle de 4 (runtime): " << factorielle(val) << std::endl; // 24
            return 0;
        }
        ```

        ---

        ### 5. Types Retours Déduits pour `operator->*`

        Cette fonctionnalité est un détail technique pour la surcharge de l'opérateur de pointeur vers membre (`operator->*`) et permet son utilisation plus flexible.

        ---

        C++14 a apporté des améliorations significatives à la convivialité et à l'expressivité du langage, en particulier en exploitant davantage les capacités de `auto` et `constexpr` pour la programmation générique et les calculs au temps de compilation.
        """
        self._create_page_template("cpp14_features", title, content)
    
    def _create_concurrency_page(self):
        title = "Concurrence et Multithreading (C++11/14+)"
        content = """
        La **concurrence** permet à un programme d'exécuter plusieurs parties de son code "simultanément" (en parallèle sur plusieurs cœurs ou de manière entrelacée sur un seul). C++11 a introduit des fonctionnalités standard pour le **multithreading** (l'utilisation de plusieurs fils d'exécution).

        ---

        ### 1. Les Bases du Multithreading (`<thread>`)

        Un **thread (fil d'exécution)** est la plus petite séquence de commandes qui peut être gérée indépendamment par un ordonnanceur de système d'exploitation. Le multithreading permet à votre programme de diviser des tâches en plusieurs threads, qui peuvent s'exécuter en parallèle.

        * **`std::thread`**: La classe pour créer et gérer des threads.
        * **`join()`**: Bloque le thread appelant jusqu'à ce que le thread joint ait terminé son exécution.
        * **`detach()`**: Détache le thread du thread appelant, le laissant s'exécuter indépendamment. Le système d'exploitation gérera sa fin.

        ```cpp
        #include <iostream>
        #include <thread> // Pour std::thread, std::this_thread
        #include <chrono> // Pour std::chrono::seconds

        // Fonction qui sera exécutée par un thread
        void tache1() {
            for (int i = 0; i < 5; ++i) {
                std::cout << "Tache 1: " << i << std::endl;
                std::this_thread::sleep_for(std::chrono::milliseconds(100)); // Pause pour voir l'entrelacement
            }
        }

        // Autre fonction pour un autre thread
        void tache2(int id) {
            for (int i = 0; i < 5; ++i) {
                std::cout << "Tache " << id << ": " << i << std::endl;
                std::this_thread::sleep_for(std::chrono::milliseconds(150));
            }
        }

        int main() {
            std::cout << "Début du programme principal." << std::endl;

            // Création des threads
            std::thread t1(tache1);
            std::thread t2(tache2, 2); // Passe un argument à la fonction du thread

            // Attendre la fin des threads (joindre)
            t1.join(); // Le thread principal attend t1
            t2.join(); // Le thread principal attend t2

            std::cout << "Fin du programme principal." << std::endl;
            return 0;
        }
        ```
        **Problèmes potentiels:** Les threads partagent la même mémoire, ce qui peut conduire à des **conditions de concurrence (race conditions)** et des **blocages (deadlocks)** si l'accès aux ressources partagées n'est pas synchronisé.

        ---

        ### 2. Synchronisation et Protection des Données Partagées

        Pour éviter les conditions de concurrence, il faut synchroniser l'accès aux données partagées.

        * **`std::mutex` (`<mutex>`)**: Un mutex (Mutual Exclusion) est un verrou qui protège une section critique du code. Un seul thread à la fois peut acquérir le verrou et entrer dans cette section.
            * `lock()`: Acquiert le verrou.
            * `unlock()`: Libère le verrou.
            * **`std::lock_guard` (RAII)**: Une classe utilitaire qui acquiert un mutex dans son constructeur et le libère automatiquement dans son destructeur. Fortement recommandé pour éviter les oublis de `unlock()`.

        ```cpp
        #include <iostream>
        #include <thread>
        #include <mutex> // Pour std::mutex, std::lock_guard

        std::mutex mon_mutex; // Le mutex qui protège la ressource partagée
        int compteur_global = 0; // Ressource partagée

        void incrementer_compteur() {
            for (int i = 0; i < 100000; ++i) {
                // Verrouille le mutex avant d'accéder à compteur_global
                std::lock_guard<std::mutex> garde(mon_mutex);
                compteur_global++;
                // Le mutex est automatiquement déverrouillé quand 'garde' sort de portée
            }
        }

        int main() {
            std::thread t1(incrementer_compteur);
            std::thread t2(incrementer_compteur);

            t1.join();
            t2.join();

            std::cout << "Compteur final: " << compteur_global << std::endl; // Devrait être 200000
            // Sans mutex, ce résultat serait imprévisible et souvent incorrect.
            return 0;
        }
        ```

        ---

        ### 3. Conditions Variables (`<condition_variable>`)

        Les **conditions variables** sont utilisées pour signaler des événements entre threads ou pour attendre qu'une certaine condition soit remplie. Elles fonctionnent toujours avec un mutex.

        * **`std::condition_variable`**: La classe pour gérer les conditions.
        * **`wait()`**: Le thread se met en attente (libère le mutex et dort) jusqu'à ce qu'il soit notifié.
        * **`notify_one()`**: Réveille un seul thread en attente.
        * **`notify_all()`**: Réveille tous les threads en attente.

        ```cpp
        #include <iostream>
        #include <thread>
        #include <mutex>
        #include <condition_variable>

        std::mutex mtx;
        std::condition_variable cv;
        bool pret = false; // Condition à attendre

        void fonction_attente() {
            std::unique_lock<std::mutex> lk(mtx); // Verrouille le mutex
            cv.wait(lk, []{ return pret; }); // Attend tant que 'pret' est faux
            std::cout << "Le thread attendu a été réveillé !" << std::endl;
        }

        void fonction_notification() {
            std::this_thread::sleep_for(std::chrono::seconds(1)); // Fait quelque chose
            {
                std::lock_guard<std::mutex> lk(mtx);
                pret = true; // Change la condition
            }
            cv.notify_one(); // Notifie le thread en attente
            std::cout << "Le thread de notification a notifié." << std::endl;
        }

        int main() {
            std::thread t_attente(fonction_attente);
            std::thread t_notif(fonction_notification);

            t_attente.join();
            t_notif.join();

            return 0;
        }
        ```

        ---

        ### 4. Futures et Promesses (`<future>`)

        * **`std::async`**: Lance une fonction dans un nouveau thread (ou de manière asynchrone) et retourne un `std::future`.
        * **`std::future`**: Un objet qui peut récupérer le résultat d'une opération asynchrone (y compris les exceptions). `get()` bloque jusqu'à ce que le résultat soit disponible.
        * **`std::promise`**: Permet de fournir un résultat ou une exception à un `std::future` associé.

        ```cpp
        #include <iostream>
        #include <future> // Pour std::async, std::future
        #include <chrono>

        int calculer_somme(int a, int b) {
            std::this_thread::sleep_for(std::chrono::seconds(2)); // Simule un long calcul
            return a + b;
        }

        int main() {
            std::cout << "Lancement du calcul asynchrone..." << std::endl;
            // Lance calculer_somme dans un nouveau thread
            std::future<int> futur_resultat = std::async(std::launch::async, calculer_somme, 10, 20);

            std::cout << "Faisons autre chose en attendant..." << std::endl;
            // ... (du travail qui ne dépend pas du résultat)

            // Récupère le résultat (bloque si non disponible)
            int resultat = futur_resultat.get();
            std::cout << "Résultat du calcul: " << resultat << std::endl; // Affiche 30
            return 0;
        }
        ```

        La concurrence est un domaine complexe mais essentiel pour les applications modernes et performantes. La bibliothèque standard de C++ offre les outils nécessaires pour gérer le multithreading de manière robuste.
        """
        self._create_page_template("concurrency", title, content)
    
    def _create_testing_debugging_page(self):
        title = "Tests Unitaires et Débogage"
        content = """
        Le **test** et le **débogage** sont des étapes cruciales dans le cycle de vie du développement logiciel, assurant la qualité et la fiabilité de votre code C/C++.

        ---

        ### 1. Tests Unitaires

        Un **test unitaire** est une méthode de test logiciel qui teste de petites unités de code (comme des fonctions individuelles ou des méthodes de classe) de manière isolée pour vérifier qu'elles fonctionnent comme prévu.

        **Principes clés :**
        * **Isolation :** Chaque test doit être indépendant des autres.
        * **Répétabilité :** Un test doit produire le même résultat à chaque exécution.
        * **Automatisation :** Les tests doivent pouvoir être exécutés automatiquement, idéalement après chaque modification du code.
        * **Clarté :** Un test devrait être facile à lire et à comprendre.

        **Frameworks de tests populaires en C++ :**
        * **Google Test / Google Mock :** Un framework très complet et largement utilisé.
        * **Catch2 :** Plus léger, facile à intégrer, et syntaxe expressive.
        * **Boost.Test :** Fait partie de la bibliothèque Boost.

        **Exemple simple avec une fonction C++ et un test conceptuel :**

        ```cpp
        // --- Code à tester (dans un fichier comme 'calculs.cpp') ---
        int addition(int a, int b) {
            return a + b;
        }

        int soustraction(int a, int b) {
            return a - b;
        }

        // --- Code de test (dans un fichier comme 'tests_calculs.cpp') ---
        #include <iostream> // Pour afficher les résultats
        #include <cassert>  // Pour la macro assert

        // Fonction de test pour l'addition
        void testAddition() {
            // Cas de test 1: nombres positifs
            assert(addition(2, 3) == 5);
            // Cas de test 2: nombres négatifs
            assert(addition(-2, -3) == -5);
            // Cas de test 3: positif et négatif
            assert(addition(5, -3) == 2);
            std::cout << "testAddition: Tous les tests sont passés avec succès." << std::endl;
        }

        // Fonction de test pour la soustraction
        void testSoustraction() {
            assert(soustraction(10, 5) == 5);
            assert(soustraction(5, 10) == -5);
            assert(soustraction(0, 0) == 0);
            std::cout << "testSoustraction: Tous les tests sont passés avec succès." << std::endl;
        }

        int main() {
            testAddition();
            testSoustraction();
            std::cout << "Tous les tests unitaires sont terminés." << std::endl;
            return 0;
        }
        ```
        Lorsque `assert` est utilisé, si la condition est fausse, le programme se termine avec un message d'erreur. Les frameworks de test offrent des rapports plus détaillés et des fonctionnalités avancées.

        ---

        ### 2. Débogage

        Le **débogage** est le processus de localisation et de correction des erreurs (bugs) dans le code.

        **Types d'erreurs :**
        * **Erreurs de compilation (Syntax Errors) :** Détectées par le compilateur. Empêchent le programme de compiler (ex: point-virgule manquant).
        * **Erreurs d'exécution (Runtime Errors) :** Se produisent pendant l'exécution du programme (ex: division par zéro, accès mémoire invalide).
        * **Erreurs logiques (Logic Errors) :** Le programme s'exécute, mais produit un résultat incorrect à cause d'une erreur dans la logique du code.

        **Techniques de débogage :**

        * **Affichage de débogage (`printf`/`cout`) :** Insérer des instructions `printf` (C) ou `std::cout` (C++) pour afficher les valeurs des variables et le flux d'exécution. C'est simple mais peut devenir fastidieux.

            ```c
            // Exemple en C
            int x = 10;
            printf("DEBUG: x avant calcul = %d\\n", x);
            x = x * 2;
            printf("DEBUG: x après calcul = %d\\n", x);
            ```

            ```cpp
            // Exemple en C++
            #include <iostream>
            double result = calculComplexe(input_val);
            std::cerr << "DEBUG: input_val=" << input_val << ", result=" << result << std::endl;
            ```
            (Utilisez `std::cerr` pour les messages de débogage, car ils vont au flux d'erreur standard et ne sont pas mis en tampon comme `std::cout`.)

        * **Débogueurs (Debuggers) :** Outils puissants qui vous permettent d'exécuter votre programme étape par étape, d'inspecter les valeurs des variables, de définir des points d'arrêt, etc.
            * **GDB (GNU Debugger) :** Le débogueur de ligne de commande standard pour C/C++ sur les systèmes Unix/Linux.
            * **Visual Studio Debugger (Windows) :** Intégré à l'IDE Visual Studio.
            * **CLion, VS Code, Eclipse :** Les IDE modernes intègrent souvent des interfaces graphiques pour GDB ou d'autres débogueurs.

        **Concepts clés des débogueurs :**
        * **Point d'arrêt (Breakpoint) :** Une ligne de code où le programme s'arrête temporairement.
        * **Pas à pas (Step Over) :** Exécute la ligne de code actuelle et passe à la suivante, sans entrer dans les appels de fonctions.
        * **Pas à pas détaillé (Step Into) :** Exécute la ligne de code actuelle et entre dans l'appel de fonction si c'est une fonction que vous pouvez déboguer.
        * **Pas à pas sorti (Step Out) :** Exécute le reste de la fonction actuelle et s'arrête juste après l'appel de cette fonction.
        * **Continuer (Continue) :** Exécute le programme jusqu'au prochain point d'arrêt ou jusqu'à la fin.
        * **Inspecter les variables (Watch/Locals) :** Afficher et modifier les valeurs des variables en mémoire.
        * **Pile d'appels (Call Stack) :** Montre la séquence d'appels de fonctions qui ont conduit à l'emplacement actuel.

        Le débogage est une compétence essentielle. L'utilisation combinée de tests unitaires et d'un débogueur efficace accélérera considérablement le développement et l'assurance qualité de votre code.
        """
        self._create_page_template("testing_debugging", title, content)

    def _create_best_practices_page(self):
        title = "Bonnes Pratiques de Codage en C/C++"
        content = """
        Adopter de bonnes pratiques de codage est essentiel pour écrire du code C/C++ qui est **lisible, maintenable, performant et robuste**.

        ---

        ### 1. Conventions de Nommage

        La cohérence est clé. Choisissez une convention et respectez-la.

        * **Variables locales:** `camelCase` (ex: `maVariableLocale`) ou `snake_case` (ex: `ma_variable_locale`).
        * **Variables membres de classe:** Souvent avec un préfixe (`m_`) ou un suffixe (`_`) (ex: `m_nomUtilisateur`, `nomUtilisateur_`).
        * **Fonctions:** `camelCase` (ex: `calculerSomme`) ou `snake_case` (ex: `calculer_somme`).
        * **Classes/Structs:** `PascalCase` (ex: `MaClasse`, `Point2D`).
        * **Constantes (macros `#define` ou `const int`) :** `ALL_CAPS_WITH_UNDERSCORES` (ex: `MAX_SIZE`, `PI`).
        * **Énumérations:** Souvent `PascalCase` pour le type et `ALL_CAPS` pour les membres (ex: `enum Couleur { ROUGE, VERT };`).

        ---

        ### 2. Commentaires

        Utilisez les commentaires pour expliquer le *pourquoi* du code, pas seulement le *quoi*.

        * **En-têtes de fichiers/fonctions:** Brève description du rôle, des paramètres, et de la valeur de retour.
        * **Logique complexe:** Expliquez les algorithmes ou les décisions de conception non évidentes.
        * **Code temporaire/à revoir:** Utilisez des balises comme `// TODO:`, `// FIXME:`.

        ```cpp
        // Calcul le produit de deux nombres.
        // @param a Le premier nombre.
        // @param b Le second nombre.
        // @return Le produit de a et b.
        int multiplier(int a, int b) {
            // Utilise l'algorithme de multiplication de Booth pour optimiser les performances
            // (Exemple fictif de commentaire sur une logique interne)
            return a * b; 
        }
        ```

        ---

        ### 3. Gestion des Erreurs et Validation

        * **C :** Vérifiez les valeurs de retour des fonctions (ex: `fopen` retourne `NULL`, `malloc` retourne `NULL`).
            ```c
            FILE *f = fopen("fichier.txt", "r");
            if (f == NULL) {
                perror("Erreur d'ouverture de fichier"); // Affiche l'erreur système
                return 1;
            }
            ```
        * **C++ :** Utilisez la **gestion des exceptions (`try-catch`)** pour les erreurs récupérables et les assertions pour les erreurs de programmation (qui ne devraient jamais arriver).
            ```cpp
            try {
                // Code qui peut lancer une exception
                if (denominateur == 0) {
                    throw std::runtime_error("Division par zéro !");
                }
            } catch (const std::runtime_error& e) {
                std::cerr << "Erreur: " << e.what() << std::endl;
            }
            ```

        ---

        ### 4. Utilisation des `const`

        Utilisez `const` partout où c'est possible pour :
        * Indiquer que la valeur d'une variable ne changera pas (`const int x = 10;`).
        * Empêcher la modification d'un objet via un pointeur ou une référence (`const int* ptr;`, `const MaClasse& obj;`).
        * Indiquer qu'une méthode de classe ne modifie pas l'état de l'objet (`void getValeur() const;`).

        ```cpp
        void afficherPoint(const Point& p) { // p ne peut pas être modifié
            std::cout << "(" << p.x << ", " << p.y << ")" << std::endl;
        }

        class MonCompte {
        private:
            double solde;
        public:
            double getSolde() const { // Cette méthode ne modifie pas 'solde'
                return solde;
            }
        };
        ```

        ---

        ### 5. Gestion de la Mémoire

        * **En C :** Toujours **`free()`** la mémoire allouée avec `malloc`/`calloc`/`realloc`.
        * **En C++ :** Toujours **`delete`** ou **`delete[]`** la mémoire allouée avec `new` ou `new[]`.
        * **C++ moderne :** Préférez les **pointeurs intelligents (`std::unique_ptr`, `std::shared_ptr`)** pour automatiser la gestion de la mémoire et éviter les fuites.
            ```cpp
            #include <memory> // Pour std::unique_ptr

            std::unique_ptr<int> ptr = std::make_unique<int>(10);
            // Pas besoin de delete, la mémoire est libérée automatiquement
            ```

        ---

        ### 6. Éviter les Variables Globales (quand possible)

        Les variables globales peuvent rendre le code difficile à suivre, à tester et à maintenir en introduisant des dépendances cachées. Préférez passer les données via les paramètres de fonctions ou les membres de classe.

        ---

        ### 7. Utilisation des En-têtes

        * Utilisez des **guards d'inclusion** (`#ifndef`, `#define`, `#endif`) pour éviter les inclusions multiples du même fichier d'en-tête.
            ```c
            // mon_header.h
            #ifndef MON_HEADER_H
            #define MON_HEADER_H
            // Déclarations ici
            #endif
            ```
            Ou utilisez `#pragma once` (spécifique au compilateur mais largement supporté).
        * N'incluez que les en-têtes dont vous avez réellement besoin.

        ---

        ### 8. Programmation Générique (Modèles en C++)

        Utilisez les **modèles** et la **STL** pour écrire du code réutilisable et type-sûr.

        ```cpp
        #include <vector>
        #include <algorithm> // Pour std::sort

        std::vector<int> nombres = {3, 1, 4, 1, 5, 9};
        std::sort(nombres.begin(), nombres.end()); // Trier facilement
        ```

        ---

        ### 9. Documentation

        Utilisez des outils comme **Doxygen** pour générer de la documentation à partir de commentaires structurés dans votre code.

        En suivant ces bonnes pratiques, vous écrirez du code C/C++ plus robuste, plus clair et plus facile à travailler, que ce soit pour vous-même ou pour d'autres développeurs.
        """
        self._create_page_template("best_practices", title, content)
    
    def _create_keywords_c_page(self):
        title = "Mots Clés Réservés en C"
        content = """
        Les **mots-clés** sont des mots spéciaux réservés par le langage C qui ont une signification prédéfinie et ne peuvent pas être utilisés comme identifiants (noms de variables, fonctions, etc.). C (standard C99) a 32 mots-clés.

        ---

        ### Liste des Mots Clés C (C99)

        | Catégorie             | Mots Clés                                                                                                          |
        | :-------------------- | :----------------------------------------------------------------------------------------------------------------- |
        | **Types de données** | `char`, `double`, `float`, `int`, `long`, `short`, `signed`, `unsigned`, `void`                                     |
        | **Qualificateurs** | `const`, `volatile`, `restrict`                                                                                    |
        | **Structures de flux**| `break`, `case`, `continue`, `default`, `do`, `else`, `for`, `goto`, `if`, `switch`, `while`                     |
        | **Stockage** | `auto`, `extern`, `register`, `static`, `sizeof`, `typedef`                                                        |
        | **Divers** | `enum`, `return`, `struct`, `union`, `_Bool`, `_Complex`, `_Imaginary` (les 3 derniers sont C99 spécifiques) |

        ---

        ### Explications et Exemples des Mots Clés Courants

        * **`int`, `float`, `char`, `double`, `void`**: Voir la section "Types de Données C/C++".

        * **`if`, `else`, `switch`, `case`, `default`, `for`, `while`, `do`**: Voir la section "Les Bases (C) - Structures de Contrôle".

        * **`return`**: Utilisé pour terminer l'exécution d'une fonction et renvoyer une valeur au code appelant.
            ```c
            int addition(int a, int b) {
                return a + b; // Retourne la somme
            }
            ```

        * **`break`**: Utilisé pour sortir immédiatement d'une boucle (`for`, `while`, `do-while`) ou d'une instruction `switch`.
            ```c
            for (int i = 0; i < 10; i++) {
                if (i == 5) {
                    break; // Sort de la boucle quand i est 5
                }
                printf("%d ", i); // Affiche 0 1 2 3 4
            }
            ```

        * **`continue`**: Saute l'itération actuelle d'une boucle et passe à l'itération suivante.
            ```c
            for (int i = 0; i < 5; i++) {
                if (i == 2) {
                    continue; // Saute l'affichage pour i = 2
                }
                printf("%d ", i); // Affiche 0 1 3 4
            }
            ```

        * **`const`**: Indique que la valeur d'une variable ne peut pas être modifiée après son initialisation.
            ```c
            const int MAX_USERS = 100; // Constante
            // MAX_USERS = 101; // Erreur de compilation
            ```

        * **`static`**: A des significations différentes selon le contexte :
            * **Variable locale statique:** Conserve sa valeur entre les appels de fonction.
            * **Fonction/variable globale statique:** Visibilité limitée au fichier source où elle est définie.
            ```c
            // Variable locale statique
            void compterAppels() {
                static int compteur = 0; // Initialisée une seule fois
                compteur++;
                printf("Appel #%d\\n", compteur);
            }
            // Dans main():
            // compterAppels(); // Appel #1
            // compterAppels(); // Appel #2

            // Fonction statique (limitée à ce fichier .c)
            static void fonctionInterne() {
                printf("Ceci est une fonction interne au fichier.\\n");
            }
            ```

        * **`extern`**: Déclare une variable ou une fonction définie dans un autre fichier source. Informe le compilateur qu'elle existe ailleurs.
            ```c
            // fichier1.c
            int compteur_global = 10; // Définition

            // fichier2.c
            extern int compteur_global; // Déclaration (informe qu'elle existe ailleurs)
            // Puis vous pouvez utiliser compteur_global dans fichier2.c
            ```

        * **`sizeof`**: Un opérateur qui retourne la taille en octets d'un type ou d'une variable.
            ```c
            int var_int;
            printf("Taille de int: %zu octets\\n", sizeof(int));
            printf("Taille de var_int: %zu octets\\n", sizeof(var_int));
            ```

        * **`typedef`**: Permet de créer un nouvel alias (un nouveau nom) pour un type de données existant, ce qui peut améliorer la lisibilité.
            ```c
            typedef unsigned long ULONG; // ULONG est maintenant un alias pour unsigned long
            ULONG id_utilisateur = 123456789UL;

            // typedef pour une structure (très courant)
            typedef struct {
                int x;
                int y;
            } Point; // Plus besoin d'écrire 'struct Point'
            Point p1 = {10, 20};
            ```

        * **`struct`**: Utilisé pour définir une structure (un type de données composé de plusieurs membres). Voir la section "Structures (C)".

        * **`enum`**: Utilisé pour déclarer un type énuméré, qui est un ensemble de constantes entières nommées.
            ```c
            enum JourSemaine {
                LUNDI,    // Par défaut, LUNDI = 0
                MARDI,    // MARDI = 1
                MERCREDI, // MERCREDI = 2
                JEUDI,
                VENDREDI,
                SAMEDI,
                DIMANCHE
            };
            enum JourSemaine aujourdhui = MERCREDI;
            printf("Aujourd'hui est le jour #%d\\n", aujourdhui); // Affiche 2
            ```

        Comprendre ces mots-clés est fondamental pour lire et écrire du code C efficace.
        """
        self._create_page_template("keywords_c", title, content)
    
    def _create_keywords_cpp_page(self):
        title = "Mots Clés Réservés en C++"
        content = """
        Le C++ étant une extension du C, il inclut tous les mots-clés de C et en ajoute de nombreux nouveaux pour supporter les fonctionnalités orientées objet, la programmation générique, la gestion des exceptions et d'autres améliorations. Le nombre exact de mots-clés peut varier légèrement entre les standards C++ (C++98, C++11, C++14, C++17, C++20, etc.).

        ---

        ### Liste des Mots Clés C++ (C++11 et antérieurs, les plus courants)

        En plus des 32 mots-clés du C (listés dans la section "Mots Clés C"), C++ ajoute notamment :

        * **`alignas` (C++11)**, `alignof` (C++11)
        * **`asm`**
        * **`auto` (signification modifiée en C++11)**
        * **`bool`**
        * **`catch`**, `class`, `const_cast`
        * **`decltype` (C++11)**, `delete`, `dynamic_cast`
        * **`explicit`**, `export` (déprécié/retiré en C++11, réintroduit en C++20 pour modules)
        * **`false`**, `friend`
        * **`mutable`**
        * **`namespace`**, `new`, `noexcept` (C++11), `nullptr` (C++11)
        * **`operator`**
        * **`private`**, `protected`, `public`
        * **`reinterpret_cast`**, `static_assert` (C++11), `static_cast`, `template`, `this`, `throw`, `true`, `try`, `typeid`, `typename`
        * **`using`**, `virtual`
        * **`wchar_t`**

        ---

        ### Explications et Exemples des Mots Clés C++ Courants

        * **`class`**: Utilisé pour définir une classe, le concept central de la POO.
            ```cpp
            class MaClasse {
                // membres et méthodes
            };
            ```

        * **`public`, `private`, `protected`**: Spécificateurs d'accès pour les membres des classes. Voir "POO en C++ (Bases)".

        * **`new`**: Alloue de la mémoire dynamiquement sur le tas (heap).
        * **`delete`**: Libère la mémoire allouée par `new`.
            ```cpp
            int* ptr = new int;
            delete ptr;
            ```

        * **`bool`**: Type de données booléen, qui peut prendre les valeurs `true` ou `false`.
            ```cpp
            bool est_valide = true;
            ```
        * **`true`, `false`**: Les deux valeurs possibles pour le type `bool`.

        * **`this`**: Un pointeur implicite disponible dans les fonctions membres d'une classe, pointant vers l'objet courant.
            ```cpp
            class Exemple {
            public:
                int valeur;
                void setValeur(int valeur) {
                    this->valeur = valeur; // 'this->valeur' fait référence au membre de la classe
                }
            };
            ```

        * **`virtual`**: Utilisé avec les fonctions membres pour activer le polymorphisme.
            ```cpp
            class Base {
            public:
                virtual void faireQuelqueChose();
            };
            ```

        * **`override` (C++11)**: Utilisé avec les fonctions membres virtuelles dans les classes dérivées pour indiquer explicitement qu'une fonction redéfinit une fonction virtuelle de la classe de base. Aide à la détection d'erreurs par le compilateur.
            ```cpp
            class Derivee : public Base {
            public:
                void faireQuelqueChose() override; // Indique que c'est une redéfinition
            };
            ```

        * **`final` (C++11)**: Utilisé pour empêcher une classe d'être héritée ou une fonction virtuelle d'être redéfinie.
            ```cpp
            class MaClasseFinale final { /* ... */ }; // Ne peut pas être héritée
            class Base { virtual void methode() final; }; // methode() ne peut pas être redéfinie
            ```

        * **`namespace`**: Définit un espace de noms pour organiser le code et éviter les conflits de noms.
            ```cpp
            namespace MonProjet {
                void maFonction();
            }
            ```

        * **`using`**: Introduit des noms d'un espace de noms dans la portée actuelle, ou crée un alias de type.
            ```cpp
            using namespace std; // Utilisation courante
            using MonAlias = long long; // C++11, alternative à typedef
            ```

        * **`throw`**, **`try`**, **`catch`**: Mots-clés pour la gestion des exceptions. Voir "Gestion des Exceptions (C++)".

        * **`template`**, **`typename`**: Utilisés pour définir des modèles (fonctions ou classes génériques).
            ```cpp
            template <typename T>
            T max_val(T a, T b) { return (a > b) ? a : b; }
            ```

        * **`auto` (C++11)**: Permet au compilateur de déduire automatiquement le type d'une variable (ou d'un retour de fonction en C++14).
            ```cpp
            auto x = 10;           // x est de type int
            auto message = "Hello"; // message est de type const char*
            ```

        * **`nullptr` (C++11)**: Un littéral de pointeur nul. Préférable à `NULL` ou `0` pour les pointeurs.
            ```cpp
            int* ptr = nullptr;
            ```

        * **`static_assert` (C++11)**: Permet de vérifier une assertion au moment de la compilation.
            ```cpp
            static_assert(sizeof(int) >= 4, "Les entiers doivent faire au moins 4 octets !");
            ```

        * **`constexpr` (C++11, amélioré en C++14)**: Indique que la valeur d'une expression ou le résultat d'une fonction peut être évalué au moment de la compilation.
            ```cpp
            constexpr int carre(int n) { return n * n; }
            int arr[carre(3)]; // Taille du tableau déterminée à la compilation
            ```

        * **Opérateurs de cast (`static_cast`, `dynamic_cast`, `const_cast`, `reinterpret_cast`)**: Permettent des conversions de type explicites avec différents niveaux de contrôle et de sécurité.
            * **`static_cast`**: Conversions liées à l'héritage ou conversions de types fondamentaux (plus sûr que le cast à la C).
            * **`dynamic_cast`**: Utilisé avec le polymorphisme pour des conversions de pointeurs/références à l'exécution, avec vérification de type.
            * **`const_cast`**: Ajoute ou retire la qualification `const` ou `volatile`.
            * **`reinterpret_cast`**: Conversions "dangereuses" entre types non liés (ex: pointeur vers int).

        Cette liste est non exhaustive mais couvre les mots-clés les plus importants que vous rencontrerez en C++. Maîtriser leur usage est crucial pour une programmation C++ efficace et idiomatique.
        """
        self._create_page_template("keywords_cpp", title, content)

    def _create_other_pages(self):
        # Vous pouvez ajouter ici les définitions pour d'autres pages si elles ne sont pas complétées
        # Par exemple:
        # self._create_cpp14_features_page()
        # self._create_concurrency_page()
        # self._create_testing_debugging_page()
        # self._create_best_practices_page()
        # self._create_keywords_c_page()
        # self._create_keywords_cpp_page()
        pass


if __name__ == "__main__":
    app = CCppSyntaxApp()
    app.mainloop()

