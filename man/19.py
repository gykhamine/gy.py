import customtkinter as ctk
import tkinter as tk

# Liste complète des objets JavaScript et de leurs méthodes (20 fonctions par objet)
objects_js= {
    "String": {
        "methods": {
            "charAt()": ("Accéder à un caractère par index (C: tableau de char, C++: std::string).", "char c_str[] = \"Hello\"; printf(\"%c\\n\", c_str[1]); // 'e'\nstd::string cpp_str = \"Hello\"; std::cout << cpp_str[1] << std::endl; // 'e'"),
            "concat()": ("Concaténer des chaînes (C: `strcat`, C++: opérateur `+`, `append`).", "char s1_c[20] = \"Hello\"; char s2_c[] = \" World\"; strcat(s1_c, s2_c); printf(\"%s\\n\", s1_c); // 'Hello World'\nstd::string s1_cpp = \"Hello\"; std::string s2_cpp = \" World\"; std::cout << s1_cpp + s2_cpp << std::endl; // 'Hello World'"),
            "includes()": ("Vérifier si une chaîne contient une sous-chaîne (C: `strstr`, C++: `std::string::find`).", "char big_c[] = \"Hello\"; char small_c[] = \"ell\"; if (strstr(big_c, small_c) != NULL) printf(\"Found\\n\"); // 'Found'\nstd::string big_cpp = \"Hello\"; std::string small_cpp = \"ell\"; if (big_cpp.find(small_cpp) != std::string::npos) std::cout << \"Found\\n\"; // 'Found'"),
            "indexOf()": ("Retourne la première position d'une sous-chaîne (C: `strstr` (retourne pointeur), C++: `std::string::find`).", "char s_c[] = \"Hello\"; char sub_c[] = \"l\"; char* ptr_c = strstr(s_c, sub_c); if (ptr_c != NULL) printf(\"%ld\\n\", ptr_c - s_c); // 2\nstd::string s_cpp = \"Hello\"; std::cout << s_cpp.find('l') << std::endl; // 2"),
            "replace()": ("Remplace une partie de la chaîne (C: manuel, C++: `std::string::replace` ou algorithmes).", "// C: plus complexe, souvent manuel avec allocation/copie.\nstd::string s_cpp = \"Hello\"; s_cpp.replace(s_cpp.find('l'), 1, \"L\"); std::cout << s_cpp << std::endl; // 'HeLlo'"),
            "slice()": ("Extraire une portion de chaîne (C: `strncpy`, C++: `std::string::substr`).", "char s_c[] = \"Hello World\"; char sub_c[6]; strncpy(sub_c, s_c, 5); sub_c[5] = '\\0'; printf(\"%s\\n\", sub_c); // 'Hello'\nstd::string s_cpp = \"Hello World\"; std::cout << s_cpp.substr(0, 5) << std::endl; // 'Hello'"),
            "split()": ("Divise une chaîne en sous-chaînes (C: `strtok` (destructif), C++: manuel ou avec `stringstream`).", "// C/C++: souvent manuel avec des boucles et find/substr, ou strtok (pour C).\n// Pas d'équivalent direct simple et non destructif comme en JS/Python."),
            "toLowerCase()": ("Convertit en minuscules (C: `tolower` avec boucle, C++: `std::tolower` avec algorithmes).", "char s_c[] = \"HELLO\"; for (int i = 0; s_c[i]; i++) s_c[i] = tolower(s_c[i]); printf(\"%s\\n\", s_c); // 'hello'\nstd::string s_cpp = \"HELLO\"; for (char &c : s_cpp) c = std::tolower(c); std::cout << s_cpp << std::endl; // 'hello'"),
            "toUpperCase()": ("Convertit en majuscules (C: `toupper` avec boucle, C++: `std::toupper` avec algorithmes).", "char s_c[] = \"hello\"; for (int i = 0; s_c[i]; i++) s_c[i] = toupper(s_c[i]); printf(\"%s\\n\", s_c); // 'HELLO'\nstd::string s_cpp = \"hello\"; for (char &c : s_cpp) c = std::toupper(c); std::cout << s_cpp << std::endl; // 'HELLO'"),
            "trim()": ("Supprime les espaces (C/C++: manuel, ou fonctions utilitaires).", "// C/C++: nécessite une implémentation manuelle pour supprimer les espaces en début/fin."),
            "startsWith()": ("Vérifie si une chaîne commence par un préfixe (C: `strncmp`, C++: `std::string::rfind(0)` ou `std::string::starts_with` (C++20)).", "char s_c[] = \"Hello\"; if (strncmp(s_c, \"He\", 2) == 0) printf(\"Starts with\\n\"); // 'Starts with'\nstd::string s_cpp = \"Hello\"; if (s_cpp.rfind(\"He\", 0) == 0) std::cout << \"Starts with\\n\"; // 'Starts with'"),
            "endsWith()": ("Vérifie si une chaîne se termine par un suffixe (C: manuel, C++: `std::string::ends_with` (C++20)).", "// C: nécessite une implémentation manuelle (vérifier longueur et comparer fin).\nstd::string s_cpp = \"Hello\"; if (s_cpp.length() >= 2 && s_cpp.substr(s_cpp.length() - 2) == \"lo\") std::cout << \"Ends with\\n\"; // 'Ends with'"),
            "repeat()": ("Répète une chaîne de caractères plusieurs fois (C/C++: manuel).", "// C/C++: nécessite une boucle et une concaténation manuelle pour répéter la chaîne."),
            "charCodeAt()": ("Retourne le code ASCII/entier d'un caractère.", "char s_c[] = \"Hello\"; printf(\"%d\\n\", s_c[1]); // 101\nstd::string s_cpp = \"Hello\"; std::cout << (int)s_cpp[1] << std::endl; // 101"),
            "lastIndexOf()": ("Retourne la dernière position d'un élément (C: manuel/`strrchr`, C++: `std::string::rfind`).", "char s_c[] = \"Hello Hello\"; char* ptr_c = strrchr(s_c, 'l'); if (ptr_c != NULL) printf(\"%ld\\n\", ptr_c - s_c); // 9\nstd::string s_cpp = \"Hello Hello\"; std::cout << s_cpp.rfind('l') << std::endl; // 9"),
            # --- 50+ méthodes/concepts pour String ---
            "strcpy() (C: <string.h>)": ("Copie une chaîne source vers une destination.", "char dest[20]; strcpy(dest, \"Source\"); printf(\"%s\\n\", dest); // Source"),
            "strncpy() (C: <string.h>)": ("Copie N caractères d'une chaîne source vers une destination.", "char dest[5]; strncpy(dest, \"Source\", 4); dest[4] = '\\0'; printf(\"%s\\n\", dest); // Sour"),
            "strcat() (C: <string.h>)": ("Concatène une chaîne source à la fin d'une destination.", "char dest[20] = \"Hello \"; strcat(dest, \"World\"); printf(\"%s\\n\", dest); // Hello World"),
            "strncat() (C: <string.h>)": ("Concatène N caractères d'une chaîne source.", "char dest[20] = \"Hello \"; strncat(dest, \"World\", 3); printf(\"%s\\n\", dest); // Hello Wor"),
            "strcmp() (C: <string.h>)": ("Compare deux chaînes lexicographiquement.", "printf(\"%d\\n\", strcmp(\"abc\", \"abd\")); // -1 (abc < abd)"),
            "strncmp() (C: <string.h>)": ("Compare N caractères de deux chaînes.", "printf(\"%d\\n\", strncmp(\"abce\", \"abcd\", 3)); // 0 (abc == abc)"),
            "strlen() (C: <string.h>)": ("Retourne la longueur d'une chaîne.", "printf(\"%ld\\n\", strlen(\"Hello\")); // 5"),
            "strchr() (C: <string.h>)": ("Recherche la première occurrence d'un caractère dans une chaîne.", "char *p = strchr(\"Hello\", 'l'); printf(\"%s\\n\", p); // llo"),
            "strrchr() (C: <string.h>)": ("Recherche la dernière occurrence d'un caractère dans une chaîne.", "char *p = strrchr(\"Hello\", 'l'); printf(\"%s\\n\", p); // lo"),
            "strstr() (C: <string.h>)": ("Recherche la première occurrence d'une sous-chaîne dans une chaîne.", "char *p = strstr(\"Hello World\", \"World\"); printf(\"%s\\n\", p); // World"),
            "strpbrk() (C: <string.h>)": ("Recherche la première occurrence d'un caractère de l'ensemble spécifié.", "char *p = strpbrk(\"Hello\", \"aeiou\"); printf(\"%s\\n\", p); // ello"),
            "strspn() (C: <string.h>)": ("Retourne la longueur du segment initial qui contient seulement des caractères d'un ensemble spécifié.", "printf(\"%ld\\n\", strspn(\"Hello\", \"Helo\")); // 4"),
            "strcspn() (C: <string.h>)": ("Retourne la longueur du segment initial qui ne contient PAS de caractères d'un ensemble spécifié.", "printf(\"%ld\\n\", strcspn(\"Hello\", \"lo\")); // 2"),
            "isdigit() (C: <ctype.h>)": ("Vérifie si un caractère est un chiffre.", "printf(\"%d\\n\", isdigit('5')); // non-zéro (true)"),
            "isalpha() (C: <ctype.h>)": ("Vérifie si un caractère est une lettre alphabétique.", "printf(\"%d\\n\", isalpha('A')); // non-zéro (true)"),
            "isalnum() (C: <ctype.h>)": ("Vérifie si un caractère est alphanumérique.", "printf(\"%d\\n\", isalnum('Z')); // non-zéro (true)"),
            "islower() (C: <ctype.h>)": ("Vérifie si un caractère est une minuscule.", "printf(\"%d\\n\", islower('a')); // non-zéro (true)"),
            "isupper() (C: <ctype.h>)": ("Vérifie si un caractère est une majuscule.", "printf(\"%d\\n\", isupper('A')); // non-zéro (true)"),
            "isspace() (C: <ctype.h>)": ("Vérifie si un caractère est un espace blanc.", "printf(\"%d\\n\", isspace(' ')); // non-zéro (true)"),
            "iscntrl() (C: <ctype.h>)": ("Vérifie si un caractère est un caractère de contrôle.", "printf(\"%d\\n\", iscntrl('\\n')); // non-zéro (true)"),
            "ispunct() (C: <ctype.h>)": ("Vérifie si un caractère est un signe de ponctuation.", "printf(\"%d\\n\", ispunct('!')); // non-zéro (true)"),
            "isxdigit() (C: <ctype.h>)": ("Vérifie si un caractère est un chiffre hexadécimal.", "printf(\"%d\\n\", isxdigit('F')); // non-zéro (true)"),
            "atoi() (C: <stdlib.h>)": ("Convertit une chaîne en entier.", "printf(\"%d\\n\", atoi(\"123\")); // 123"),
            "atof() (C: <stdlib.h>)": ("Convertit une chaîne en flottant (double).", "printf(\"%f\\n\", atof(\"3.14\")); // 3.140000"),
            "atol() / atoll() (C: <stdlib.h>)": ("Convertit une chaîne en entier long/long long.", "printf(\"%ld\\n\", atol(\"1234567890\")); // 1234567890"),
            "strtol() (C: <stdlib.h>)": ("Convertit une chaîne en entier long avec base spécifiée.", "printf(\"%ld\\n\", strtol(\"1010\", NULL, 2)); // 10"),
            "strtod() (C: <stdlib.h>)": ("Convertit une chaîne en double.", "printf(\"%f\\n\", strtod(\"3.14159\", NULL)); // 3.141590"),
            "sprintf() (C: <cstdio>)": ("Formate et écrit une chaîne dans un tampon.", "char buffer[50]; sprintf(buffer, \"Hello %s\", \"World\"); printf(\"%s\\n\", buffer); // Hello World"),
            "sscanf() (C: <cstdio>)": ("Lit des données formatées à partir d'une chaîne.", "int num; char text[10]; sscanf(\"123 ABC\", \"%d %s\", &num, text); printf(\"%d %s\\n\", num, text); // 123 ABC"),
            "std::string::length() (C++)": ("Retourne la longueur de la chaîne (nombre de caractères).", "std::string s = \"Test\"; std::cout << s.length() << std::endl; // 4"),
            "std::string::size() (C++)": ("Identique à `length()`.", "std::string s = \"Test\"; std::cout << s.size() << std::endl; // 4"),
            "std::string::empty() (C++)": ("Vérifie si la chaîne est vide.", "std::string s = \"\"; std::cout << s.empty() << std::endl; // 1 (true)"),
            "std::string::clear() (C++)": ("Vide le contenu de la chaîne.", "std::string s = \"Hello\"; s.clear(); std::cout << s.length() << std::endl; // 0"),
            "std::string::at() (C++)": ("Accès sécurisé au caractère par index (vérifie les bornes).", "std::string s = \"Hello\"; try { std::cout << s.at(1) << std::endl; } catch (const std::out_of_range& oor) {} // e"),
            "std::string::front() (C++)": ("Accède au premier caractère.", "std::string s = \"Hello\"; std::cout << s.front() << std::endl; // H"),
            "std::string::back() (C++)": ("Accède au dernier caractère.", "std::string s = \"Hello\"; std::cout << s.back() << std::endl; // o"),
            "std::string::push_back() (C++)": ("Ajoute un caractère à la fin.", "std::string s = \"Hell\"; s.push_back('o'); std::cout << s << std::endl; // Hello"),
            "std::string::pop_back() (C++11)": ("Supprime le dernier caractère.", "std::string s = \"Hello\"; s.pop_back(); std::cout << s << std::endl; // Hell"),
            "std::string::assign() (C++)": ("Affecte un nouveau contenu à la chaîne.", "std::string s; s.assign(\"New\"); std::cout << s << std::endl; // New"),
            "std::string::insert() (C++)": ("Insère un contenu à une position donnée.", "std::string s = \"World\"; s.insert(0, \"Hello \"); std::cout << s << std::endl; // Hello World"),
            "std::string::erase() (C++)": ("Supprime des caractères d'une position.", "std::string s = \"Hello World\"; s.erase(5, 6); std::cout << s << std::endl; // Hello"),
            "std::string::compare() (C++)": ("Compare deux chaînes (retourne <0, 0, >0).", "std::string s1 = \"abc\"; std::string s2 = \"abd\"; std::cout << s1.compare(s2) << std::endl; // -1"),
            "std::string::c_str() (C++)": ("Retourne un pointeur vers un tableau de char terminé par null.", "std::string s = \"Hello\"; printf(\"%s\\n\", s.c_str()); // Hello"),
            "std::string::data() (C++11)": ("Retourne un pointeur vers les données (peut ne pas être null-terminé).", "std::string s = \"Hello\"; const char* ptr = s.data();"),
            "std::string::capacity() (C++)": ("Retourne la taille allouée actuelle du stockage.", "std::string s; s.reserve(100); std::cout << s.capacity() << std::endl; // 100 (au moins)"),
            "std::string::reserve() (C++)": ("Demande une capacité minimale pour la chaîne.", "std::string s; s.reserve(50);"),
            "std::string::resize() (C++)": ("Redimensionne la chaîne.", "std::string s = \"Hello\"; s.resize(3); std::cout << s << std::endl; // Hel"),
            "std::string::operator[] (C++)": ("Accès au caractère par index (sans vérification des bornes).", "std::string s = \"Hello\"; std::cout << s[0] << std::endl; // H"),
            "std::string::find_first_of() (C++)": ("Recherche la première occurrence de n'importe quel caractère d'un ensemble.", "std::string s = \"Hello\"; std::cout << s.find_first_of(\"lo\") << std::endl; // 2"),
            "std::string::find_last_of() (C++)": ("Recherche la dernière occurrence de n'importe quel caractère d'un ensemble.", "std::string s = \"Hello\"; std::cout << s.find_last_of(\"lo\") << std::endl; // 3"),
            "std::string::rfind() (C++)": ("Recherche la dernière occurrence d'une sous-chaîne.", "std::string s = \"Hello Hello\"; std::cout << s.rfind(\"ell\") << std::endl; // 8"),
            "std::string::npos (C++)": ("Valeur spéciale indiquant 'pas trouvé' pour les fonctions de recherche.", "std::string s = \"Hello\"; if (s.find(\"xyz\") == std::string::npos) std::cout << \"Not found\" << std::endl;"),
            "std::getline() (C++)": ("Lit une ligne entière d'un flux d'entrée dans une `std::string`.", "std::string line; std::getline(std::cin, line);"),
            "std::cin >> (C++)": ("Lit un mot (jusqu'à l'espace blanc) dans une `std::string`.", "std::string word; std::cin >> word;")
        },
        "description": "En C, les chaînes sont des tableaux de caractères terminés par '\\0' avec des fonctions C-style (`<string.h>`, `<ctype.h>`, `<stdlib.h>`, `<cstdio>`). En C++, `std::string` (`<string>`) offre une gestion plus orientée objet et sûre, avec de nombreuses méthodes membres."
    },
    "Array": { # L'équivalent de base d'Array en JS
        "methods": {
            "push()": ("Ajoute un élément à la fin (C: manuel/réallocation, C++: `std::vector::push_back`).", "// C: nécessite réallocation et copie dynamique pour ajouter.\nstd::vector<int> arr_cpp = {1, 2}; arr_cpp.push_back(3); for (int x : arr_cpp) std::cout << x << \" \"; // 1 2 3"),
            "pop()": ("Supprime le dernier élément (C: manuel, C++: `std::vector::pop_back`).", "// C: manipulation manuelle de la taille.\nstd::vector<int> arr_cpp = {1, 2, 3}; arr_cpp.pop_back(); for (int x : arr_cpp) std::cout << x << \" \"; // 1 2"),
            "shift()": ("Supprime le premier élément (C/C++: manuel, `std::vector::erase`).", "// C/C++: nécessite le décalage manuel des éléments, ou `erase` pour std::vector."),
            "unshift()": ("Ajoute un élément au début (C/C++: manuel, `std::vector::insert`).", "// C/C++: nécessite le décalage manuel des éléments, ou `insert` pour std::vector."),
            "map()": ("Appliquer une fonction à chaque élément et créer une nouvelle collection (C/C++: boucle manuelle).", "// C/C++: implémentation manuelle avec une boucle et création d'un nouveau tableau/vecteur."),
            "filter()": ("Filtrer les éléments (C/C++: boucle manuelle).", "// C/C++: implémentation manuelle avec une boucle et copie des éléments filtrés dans un nouveau tableau/vecteur."),
            "reduce()": ("Réduire à une seule valeur (C/C++: boucle manuelle).", "// C/C++: implémentation manuelle avec une boucle et un accumulateur."),
            "forEach()": ("Exécuter une fonction sur chaque élément (C/C++: boucle for/for-each).", "int arr_c[] = {1, 2, 3}; for (int i = 0; i < 3; i++) printf(\"%d \", arr_c[i]); // 1 2 3\nstd::vector<int> arr_cpp = {1, 2, 3}; for (int x : arr_cpp) std::cout << x << \" \"; // 1 2 3"),
            "concat()": ("Fusionne deux ou plusieurs tableaux/vecteurs (C: manuel, C++: `std::vector::insert` ou opérateur `+`).", "// C: nécessite allocation et copie.\nstd::vector<int> arr1_cpp = {1, 2}; std::vector<int> arr2_cpp = {3, 4}; std::vector<int> combined_cpp = arr1_cpp; combined_cpp.insert(combined_cpp.end(), arr2_cpp.begin(), arr2_cpp.end()); for (int x : combined_cpp) std::cout << x << \" \"; // 1 2 3 4"),
            "join()": ("Fusionne les éléments en une chaîne (C/C++: manuel avec `stringstream` ou boucles).", "// C/C++: nécessite une boucle pour itérer et construire la chaîne avec des délimiteurs."),
            "indexOf()": ("Retourne la première position d'un élément (C: boucle, C++: `std::find`).", "int arr_c[] = {1, 2, 3}; int search_c = 2; for (int i = 0; i < 3; i++) if (arr_c[i] == search_c) { printf(\"%d\\n\", i); break; } // 1\nstd::vector<int> arr_cpp = {1, 2, 3}; auto it_cpp = std::find(arr_cpp.begin(), arr_cpp.end(), 2); if (it_cpp != arr_cpp.end()) std::cout << std::distance(arr_cpp.begin(), it_cpp) << std::endl; // 1"),
            "find()": ("Retourne le premier élément qui passe un test (C/C++: boucle manuelle, C++: `std::find_if`).", "// C/C++: nécessite une boucle et une condition. `std::find_if` pour C++."),
            "sort()": ("Trie les éléments (C: `qsort`, C++: `std::sort`).", "int arr_c[] = {3, 1, 2}; qsort(arr_c, 3, sizeof(int), [](const void* a, const void* b){ return (*(int*)a - *(int*)b); }); for (int i=0; i<3; i++) printf(\"%d \", arr_c[i]); // 1 2 3\nstd::vector<int> arr_cpp = {3, 1, 2}; std::sort(arr_cpp.begin(), arr_cpp.end()); for (int x : arr_cpp) std::cout << x << \" \"; // 1 2 3"),
            "reverse()": ("Inverse l'ordre des éléments (C: manuel, C++: `std::reverse`).", "int arr_c[] = {1, 2, 3}; /* implémentation manuelle */\nstd::vector<int> arr_cpp = {1, 2, 3}; std::reverse(arr_cpp.begin(), arr_cpp.end()); for (int x : arr_cpp) std::cout << x << \" \"; // 3 2 1"),
            "slice()": ("Extrait une portion (C: manuel, C++: `std::vector::assign` ou constructeur de copie).", "// C/C++: nécessite la création d'un nouveau tableau/vecteur et copie des éléments."),
            "splice()": ("Modifie un tableau en ajoutant ou supprimant (C: manuel, C++: `std::vector::erase`/`insert`).", "// C: très complexe, nécessite réallocation et copie.\nstd::vector<int> arr_cpp = {1, 2, 3}; arr_cpp.erase(arr_cpp.begin() + 1); arr_cpp.insert(arr_cpp.begin() + 1, 4); for (int x : arr_cpp) std::cout << x << \" \"; // 1 4 3"),
            "some()": ("Teste si au moins un élément passe un test (C/C++: boucle manuelle, C++: `std::any_of`).", "// C/C++: implémentation manuelle avec une boucle et une condition."),
            "every()": ("Teste si tous les éléments passent un test (C/C++: boucle manuelle, C++: `std::all_of`).", "// C/C++: implémentation manuelle avec une boucle et une condition."),
            "findIndex()": ("Retourne l'index du premier élément qui passe un test (C/C++: boucle manuelle, C++: `std::find_if` et `std::distance`).", "// C/C++: implémentation manuelle avec une boucle et une condition."),
            "fill()": ("Remplit tous les éléments (C: `memset`, C++: `std::fill`).", "int arr_c[3]; memset(arr_c, 0, sizeof(arr_c)); for (int i=0; i<3; i++) printf(\"%d \", arr_c[i]); // 0 0 0\nstd::vector<int> arr_cpp(3); std::fill(arr_cpp.begin(), arr_cpp.end(), 0); for (int x : arr_cpp) std::cout << x << \" \"; // 0 0 0"),
            # --- 50+ méthodes/concepts pour Array/Vector ---
            "malloc() (C: <stdlib.h>)": ("Alloue dynamiquement de la mémoire pour un tableau.", "int *arr = (int*)malloc(3 * sizeof(int)); if (arr) arr[0] = 1; free(arr);"),
            "calloc() (C: <stdlib.h>)": ("Alloue dynamiquement et initialise la mémoire à zéro.", "int *arr = (int*)calloc(3, sizeof(int)); if (arr) printf(\"%d\\n\", arr[0]); // 0"),
            "realloc() (C: <stdlib.h>)": ("Redimensionne un bloc de mémoire alloué dynamiquement.", "int *arr = (int*)malloc(2 * sizeof(int)); arr = (int*)realloc(arr, 4 * sizeof(int));"),
            "free() (C: <stdlib.h>)": ("Libère la mémoire allouée dynamiquement.", "int *arr = (int*)malloc(sizeof(int)); free(arr);"),
            "new[] (C++)": ("Alloue dynamiquement un tableau d'objets (C++).", "int* arr = new int[3]; arr[0] = 1; delete[] arr;"),
            "delete[] (C++)": ("Désalloue un tableau d'objets alloué avec `new[]`.", "int* arr = new int[3]; delete[] arr;"),
            "sizeof (C/C++)": ("Opérateur qui retourne la taille en octets d'un type ou d'une variable.", "int arr[5]; printf(\"%ld\\n\", sizeof(arr) / sizeof(arr[0])); // 5"),
            "std::vector::size() (C++)": ("Retourne le nombre d'éléments dans le vecteur.", "std::vector<int> v = {1, 2}; std::cout << v.size() << std::endl; // 2"),
            "std::vector::capacity() (C++)": ("Retourne la taille du stockage alloué pour le vecteur.", "std::vector<int> v; v.reserve(10); std::cout << v.capacity() << std::endl; // 10 (au moins)"),
            "std::vector::empty() (C++)": ("Vérifie si le vecteur est vide.", "std::vector<int> v; std::cout << v.empty() << std::endl; // 1 (true)"),
            "std::vector::clear() (C++)": ("Supprime tous les éléments du vecteur.", "std::vector<int> v = {1, 2}; v.clear(); std::cout << v.size() << std::endl; // 0"),
            "std::vector::at() (C++)": ("Accès sécurisé à un élément par index (vérifie les bornes).", "std::vector<int> v = {10, 20}; try { std::cout << v.at(0) << std::endl; } catch (const std::out_of_range& oor) {} // 10"),
            "std::vector::front() (C++)": ("Accède au premier élément.", "std::vector<int> v = {10, 20}; std::cout << v.front() << std::endl; // 10"),
            "std::vector::back() (C++)": ("Accède au dernier élément.", "std::vector<int> v = {10, 20}; std::cout << v.back() << std::endl; // 20"),
            "std::vector::data() (C++11)": ("Retourne un pointeur vers les données sous-jacentes du vecteur.", "std::vector<int> v = {1, 2, 3}; int* ptr = v.data();"),
            "std::vector::insert() (C++)": ("Insère un ou plusieurs éléments à une position spécifiée.", "std::vector<int> v = {1, 3}; v.insert(v.begin() + 1, 2); for (int x : v) std::cout << x << \" \"; // 1 2 3"),
            "std::vector::erase() (C++)": ("Supprime un ou plusieurs éléments d'une position spécifiée.", "std::vector<int> v = {1, 2, 3}; v.erase(v.begin() + 1); for (int x : v) std::cout << x << \" \"; // 1 3"),
            "std::vector::resize() (C++)": ("Redimensionne le vecteur.", "std::vector<int> v = {1, 2}; v.resize(4, 0); for (int x : v) std::cout << x << \" \"; // 1 2 0 0"),
            "std::vector::reserve() (C++)": ("Demande une capacité minimale pour le vecteur.", "std::vector<int> v; v.reserve(100);"),
            "std::vector::swap() (C++)": ("Échange le contenu de deux vecteurs de même type.", "std::vector<int> v1 = {1, 2}; std::vector<int> v2 = {3, 4}; v1.swap(v2); for (int x : v1) std::cout << x << \" \"; // 3 4"),
            "std::copy() (C++: <algorithm>)": ("Copie des éléments d'une plage à une autre.", "std::vector<int> src = {1, 2, 3}; std::vector<int> dest(3); std::copy(src.begin(), src.end(), dest.begin());"),
            "std::move() (C++: <algorithm>, C++11)": ("Déplace des éléments d'une plage à une autre (optimisé).", "std::vector<int> src = {1, 2}; std::vector<int> dest(src.size()); std::move(src.begin(), src.end(), dest.begin());"),
            "std::fill_n() (C++: <algorithm>)": ("Remplit N éléments à partir d'un début d'itérateur.", "std::vector<int> v(3); std::fill_n(v.begin(), 3, 7); for (int x : v) std::cout << x << \" \"; // 7 7 7"),
            "std::generate() (C++: <algorithm>)": ("Génère des valeurs pour une plage avec une fonction.", "std::vector<int> v(3); int i = 0; std::generate(v.begin(), v.end(), [&](){ return ++i; }); for (int x : v) std::cout << x << \" \"; // 1 2 3"),
            "std::count() (C++: <algorithm>)": ("Compte le nombre d'occurrences d'une valeur.", "std::vector<int> v = {1, 2, 2, 3}; std::cout << std::count(v.begin(), v.end(), 2) << std::endl; // 2"),
            "std::count_if() (C++: <algorithm>)": ("Compte le nombre d'éléments qui satisfont une condition.", "std::vector<int> v = {1, 2, 3}; std::cout << std::count_if(v.begin(), v.end(), [](int x){ return x > 1; }) << std::endl; // 2"),
            "std::remove() (C++: <algorithm>)": ("Supprime les occurrences d'une valeur (ne réduit pas la taille).", "std::vector<int> v = {1, 2, 3, 2}; auto it = std::remove(v.begin(), v.end(), 2); v.erase(it, v.end()); for (int x : v) std::cout << x << \" \"; // 1 3"),
            "std::remove_if() (C++: <algorithm>)": ("Supprime les éléments qui satisfont une condition (ne réduit pas la taille).", "std::vector<int> v = {1, 2, 3, 4}; auto it = std::remove_if(v.begin(), v.end(), [](int x){ return x % 2 == 0; }); v.erase(it, v.end()); for (int x : v) std::cout << x << \" \"; // 1 3"),
            "std::unique() (C++: <algorithm>)": ("Supprime les doublons adjacents (ne réduit pas la taille).", "std::vector<int> v = {1, 1, 2, 2, 3}; auto it = std::unique(v.begin(), v.end()); v.erase(it, v.end()); for (int x : v) std::cout << x << \" \"; // 1 2 3"),
            "std::lower_bound() (C++: <algorithm>)": ("Retourne un itérateur au premier élément pas plus petit que la valeur.", "std::vector<int> v = {1, 2, 3, 4, 5}; auto it = std::lower_bound(v.begin(), v.end(), 3); std::cout << *it << std::endl; // 3"),
            "std::upper_bound() (C++: <algorithm>)": ("Retourne un itérateur au premier élément plus grand que la valeur.", "std::vector<int> v = {1, 2, 3, 4, 5}; auto it = std::upper_bound(v.begin(), v.end(), 3); std::cout << *it << std::endl; // 4"),
            "std::equal_range() (C++: <algorithm>)": ("Retourne une paire d'itérateurs délimitant une plage de valeurs égales.", "std::vector<int> v = {1, 2, 3, 3, 3, 4}; auto range = std::equal_range(v.begin(), v.end(), 3); for (auto it = range.first; it != range.second; ++it) std::cout << *it << \" \"; // 3 3 3"),
            "std::min_element() (C++: <algorithm>)": ("Retourne un itérateur vers le plus petit élément.", "std::vector<int> v = {3, 1, 2}; std::cout << *std::min_element(v.begin(), v.end()) << std::endl; // 1"),
            "std::max_element() (C++: <algorithm>)": ("Retourne un itérateur vers le plus grand élément.", "std::vector<int> v = {3, 1, 2}; std::cout << *std::max_element(v.begin(), v.end()) << std::endl; // 3"),
            "std::minmax_element() (C++11: <algorithm>)": ("Retourne une paire d'itérateurs vers le min et le max.", "std::vector<int> v = {3, 1, 2}; auto p = std::minmax_element(v.begin(), v.end()); std::cout << *p.first << \" \" << *p.second << std::endl; // 1 3"),
            "std::accumulate() (C++: <numeric>)": ("Calcule la somme des éléments dans une plage.", "std::vector<int> v = {1, 2, 3}; std::cout << std::accumulate(v.begin(), v.end(), 0) << std::endl; // 6"),
            "std::iota() (C++11: <numeric>)": ("Remplit une plage avec des valeurs croissantes à partir d'une valeur de départ.", "std::vector<int> v(5); std::iota(v.begin(), v.end(), 10); for (int x : v) std::cout << x << \" \"; // 10 11 12 13 14"),
            "std::list (C++: <list>)": ("Liste doublement chaînée, efficace pour les insertions/suppressions au milieu.", "std::list<int> l = {1, 2, 3}; l.push_back(4); l.push_front(0);"),
            "std::deque (C++: <deque>)": ("File à double sens, efficace pour les insertions/suppressions aux deux extrémités.", "std::deque<int> d = {1, 2}; d.push_front(0); d.push_back(3);"),
            "std::array (C++11: <array>)": ("Tableau de taille fixe au compile-time, avec interface de conteneur.", "std::array<int, 3> arr = {1, 2, 3};"),
            "Pointers (C/C++)": ("Utilisation directe des pointeurs pour la navigation et manipulation de tableaux.", "int arr[] = {1, 2, 3}; int* p = arr; printf(\"%d\\n\", *(p+1)); // 2"),
            "Offset access `arr[i]` (C/C++)": ("Accès aux éléments par index.", "int arr[] = {1, 2}; printf(\"%d\\n\", arr[0]); // 1"),
            "Array initialization (C/C++)": ("Initialisation des tableaux.", "int arr[] = {1, 2, 3}; int arr2[5] = {0};"),
            "Multi-dimensional arrays (C/C++)": ("Déclaration et accès aux tableaux multidimensionnels.", "int matrix[2][3] = {{1,2,3},{4,5,6}}; printf(\"%d\\n\", matrix[1][1]); // 5"),
            "Passing arrays to functions (C/C++)": ("Comment passer des tableaux aux fonctions.", "void print_arr(int arr[], int size) { for(int i=0; i<size; i++) printf(\"%d \", arr[i]); }"),
            "Return value optimization (C++):": ("Optimisation pour le retour de `std::vector`.", "// Concept d'optimisation du compilateur pour les objets retournés."),
            "std::distance() (C++: <iterator>)": ("Calcule la distance entre deux itérateurs.", "std::vector<int> v = {1, 2, 3}; auto it = std::find(v.begin(), v.end(), 2); std::cout << std::distance(v.begin(), it) << std::endl; // 1"),
            "std::advance() (C++: <iterator>)": ("Fait avancer un itérateur de N positions.", "std::vector<int> v = {1, 2, 3}; auto it = v.begin(); std::advance(it, 1); std::cout << *it << std::endl; // 2"),
            "std::next() (C++11: <iterator>)": ("Retourne un itérateur avancé de N positions (sans modifier l'original).", "std::vector<int> v = {1, 2, 3}; auto it = std::next(v.begin(), 1); std::cout << *it << std::endl; // 2"),
            "std::prev() (C++11: <iterator>)": ("Retourne un itérateur reculé de N positions (sans modifier l'original).", "std::vector<int> v = {1, 2, 3}; auto it = std::prev(v.end(), 1); std::cout << *it << std::endl; // 3"),
            "std::for_each() (C++: <algorithm>)": ("Exécute une fonction sur chaque élément d'une plage.", "std::vector<int> v = {1, 2, 3}; std::for_each(v.begin(), v.end(), [](int x){ std::cout << x * 2 << \" \"; }); // 2 4 6"),
            "std::transform() (C++: <algorithm>)": ("Applique une fonction à une plage et stocke les résultats ailleurs.", "std::vector<int> v = {1, 2, 3}; std::vector<int> r(3); std::transform(v.begin(), v.end(), r.begin(), [](int x){ return x * 2; }); for (int x : r) std::cout << x << \" \"; // 2 4 6"),
            "std::partition() (C++: <algorithm>)": ("Réorganise les éléments de manière à ce que ceux qui satisfont une condition soient avant ceux qui ne la satisfont pas.", "std::vector<int> v = {1, 5, 2, 8, 3}; std::partition(v.begin(), v.end(), [](int x){ return x % 2 != 0; }); for (int x : v) std::cout << x << \" \"; // 1 5 3 8 2 (ordre relatif non garanti)"),
            "std::stable_partition() (C++: <algorithm>)": ("Comme `partition`, mais maintient l'ordre relatif des éléments.", "std::vector<int> v = {1, 5, 2, 8, 3}; std::stable_partition(v.begin(), v.end(), [](int x){ return x % 2 != 0; }); for (int x : v) std::cout << x << \" \"; // 1 5 3 2 8"),
            "std::copy_if() (C++11: <algorithm>)": ("Copie des éléments d'une plage à une autre si une condition est remplie.", "std::vector<int> src = {1, 2, 3, 4}; std::vector<int> dest; std::copy_if(src.begin(), src.end(), std::back_inserter(dest), [](int x){ return x % 2 == 0; }); for (int x : dest) std::cout << x << \" \"; // 2 4"),
            "std::find_end() (C++: <algorithm>)": ("Recherche la dernière sous-séquence dans une séquence.", "std::vector<int> v = {1, 2, 3, 1, 2}; std::vector<int> sub = {1, 2}; auto it = std::find_end(v.begin(), v.end(), sub.begin(), sub.end()); std::cout << std::distance(v.begin(), it) << std::endl; // 3"),
            "std::search() (C++: <algorithm>)": ("Recherche la première sous-séquence dans une séquence.", "std::vector<int> v = {1, 2, 3, 1, 2}; std::vector<int> sub = {1, 2}; auto it = std::search(v.begin(), v.end(), sub.begin(), sub.end()); std::cout << std::distance(v.begin(), it) << std::endl; // 0"),
            "std::mismatch() (C++: <algorithm>)": ("Trouve la première position où deux plages d'éléments diffèrent.", "std::vector<int> v1 = {1, 2, 3}; std::vector<int> v2 = {1, 5, 3}; auto p = std::mismatch(v1.begin(), v1.end(), v2.begin()); std::cout << *p.first << \" \" << *p.second << std::endl; // 2 5"),
            "std::is_sorted() (C++11: <algorithm>)": ("Vérifie si une plage est triée.", "std::vector<int> v = {1, 2, 3}; std::cout << std::is_sorted(v.begin(), v.end()) << std::endl; // 1 (true)"),
            "std::rotate() (C++: <algorithm>)": ("Fait pivoter les éléments d'une plage.", "std::vector<int> v = {1, 2, 3, 4, 5}; std::rotate(v.begin(), v.begin() + 2, v.end()); for (int x : v) std::cout << x << \" \"; // 3 4 5 1 2"),
            "std::shuffle() (C++11: <algorithm>)": ("Mélange aléatoirement les éléments d'une plage.", "std::vector<int> v = {1, 2, 3, 4, 5}; std::random_device rd; std::mt19937 g(rd()); std::shuffle(v.begin(), v.end(), g); // Mélange aléatoire")
        },
        "description": "En C, les tableaux sont des blocs de mémoire de taille fixe. La gestion est manuelle (`<stdlib.h>`, `<string.h>`). En C++, `std::vector` (`<vector>`) est une collection dynamique beaucoup plus flexible, et `std::algorithm` (`<algorithm>`) fournit de nombreux algorithmes génériques."
    },
    "Tuple": { # Simulé par std::pair, std::tuple (C++11) ou struct
        "methods": {
            "make_pair() (C++)": ("Crée une paire de valeurs (tuple de 2 éléments).", "std::pair<int, std::string> p = std::make_pair(1, \"hello\"); std::cout << p.first << \" \" << p.second << std::endl; // 1 hello"),
            "get<>() (C++11 tuple)": ("Accède aux éléments d'un tuple par index (C++11 et plus).", "std::tuple<int, std::string, bool> t(1, \"world\", true); std::cout << std::get<0>(t) << std::endl; // 1"),
            "struct (C/C++)": ("Structure personnalisée pour regrouper des données de types différents.", "struct MyTuple { int a; char b; }; MyTuple mt = {1, 'x'}; printf(\"%d %c\\n\", mt.a, mt.b); // 1 x"),
            # --- 50+ méthodes/concepts pour Tuple/Pair ---
            "std::pair (C++: <utility>)": ("Type de paire de valeurs.", "std::pair<int, double> p; p.first = 10; p.second = 3.14;"),
            "std::tuple (C++11: <tuple>)": ("Type de tuple pour n'importe quel nombre d'éléments.", "std::tuple<int, char, double> t(1, 'A', 2.5);"),
            "std::get<index>(tuple) (C++11)": ("Accède à l'élément du tuple par son index.", "std::tuple<int, char> t(1, 'a'); std::cout << std::get<1>(t) << std::endl; // a"),
            "std::get<Type>(tuple) (C++14)": ("Accède à l'élément du tuple par son type (si unique).", "std::tuple<int, double> t(1, 2.5); std::cout << std::get<double>(t) << std::endl; // 2.5"),
            "std::tuple_size (C++11)": ("Obtient le nombre d'éléments dans un tuple au compile-time.", "std::tuple<int, double> t; std::cout << std::tuple_size<decltype(t)>::value << std::endl; // 2"),
            "std::tuple_element (C++11)": ("Obtient le type d'un élément du tuple par son index au compile-time.", "std::tuple<int, double> t; std::cout << typeid(std::tuple_element<0, decltype(t)>::type).name() << std::endl; // i (pour int)"),
            "std::tie (C++11)": ("Crée un tuple de références, utile pour décomposer des tuples/paires.", "int x; std::string s; std::tie(x, s) = std::make_pair(10, \"hello\"); std::cout << x << \" \" << s << std::endl; // 10 hello"),
            "Structured Bindings (C++17)": ("Décompose un tuple/pair/struct en variables individuelles.", "auto [val1, val2] = std::make_pair(1, 2.5); std::cout << val1 << \" \" << val2 << std::endl; // 1 2.5"),
            "Constructors (std::pair/tuple)": ("Différentes façons de construire des paires/tuples.", "std::pair<int, int> p1(1, 2); std::pair<int, int> p2{3, 4};"),
            "Comparison operators (std::pair/tuple)": ("Comparaison lexicographique des paires/tuples.", "std::pair<int, int> p1{1, 2}, p2{1, 3}; std::cout << (p1 < p2) << std::endl; // 1 (true)"),
            "Swap (std::pair/tuple)": ("Échange les contenus de deux paires/tuples.", "std::pair<int, int> p1{1, 2}, p2{3, 4}; p1.swap(p2);"),
            "Forwarding references (perfect forwarding) (C++11)": ("Permet de passer des arguments à `std::make_pair` ou `std::make_tuple` en préservant leurs qualifications lvalue/rvalue.", "// Concept de Rvalue references et perfect forwarding pour éviter les copies inutiles.")
        },
        "description": "En C, les tuples sont simulés par des `struct`. En C++, `std::pair` (`<utility>`) pour deux éléments et `std::tuple` (`<tuple>`, C++11) pour un nombre variable d'éléments sont les équivalents modernes et sûrs. La décomposition avec les liaisons structurées (`C++17`) est très pratique."
    },
    "Set": { # Équivalent par std::set (C++) ou gestion manuelle (C)
        "methods": {
            "insert() (C++)": ("Ajoute un élément à l'ensemble (`std::set`).", "std::set<int> s_cpp = {1, 2}; s_cpp.insert(3); for (int x : s_cpp) std::cout << x << \" \"; // 1 2 3"),
            "erase() (C++)": ("Supprime un élément de l'ensemble (`std::set`).", "std::set<int> s_cpp = {1, 2, 3}; s_cpp.erase(3); for (int x : s_cpp) std::cout << x << \" \"; // 1 2"),
            "clear() (C++)": ("Supprime tous les éléments (`std::set`).", "std::set<int> s_cpp = {1, 2, 3}; s_cpp.clear(); std::cout << s_cpp.size() << std::endl; // 0"),
            "union() / intersection() / difference() (C++)": ("Opérations sur les ensembles (`std::set` avec algorithmes ou boucles).", "// Ces opérations sont généralement implémentées manuellement avec des boucles ou des algorithmes comme `std::set_union`, `std::set_intersection`, etc. nécessitant des itérateurs."),
            # --- 50+ méthodes/concepts pour Set ---
            "std::set (C++: <set>)": ("Conteneur ordonné qui stocke des éléments uniques.", "std::set<int> mySet; mySet.insert(10); mySet.insert(5); mySet.insert(10); for(int x : mySet) std::cout << x << \" \"; // 5 10"),
            "std::unordered_set (C++11: <unordered_set>)": ("Conteneur non ordonné qui stocke des éléments uniques (basé sur hachage).", "std::unordered_set<int> myUnorderedSet; myUnorderedSet.insert(10); myUnorderedSet.insert(5);"),
            "std::set::count() (C++)": ("Retourne 1 si l'élément est présent, 0 sinon.", "std::set<int> s = {1, 2}; std::cout << s.count(1) << std::endl; // 1"),
            "std::set::find() (C++)": ("Retourne un itérateur vers l'élément ou `end()` si non trouvé.", "std::set<int> s = {1, 2}; auto it = s.find(1); if (it != s.end()) std::cout << *it << std::endl; // 1"),
            "std::set::lower_bound() (C++)": ("Retourne un itérateur vers le premier élément pas plus petit que la valeur (pour `std::set` ordonné).", "std::set<int> s = {1, 3, 5}; auto it = s.lower_bound(2); std::cout << *it << std::endl; // 3"),
            "std::set::upper_bound() (C++)": ("Retourne un itérateur vers le premier élément plus grand que la valeur (pour `std::set` ordonné).", "std::set<int> s = {1, 3, 5}; auto it = s.upper_bound(3); std::cout << *it << std::endl; // 5"),
            "std::set::equal_range() (C++)": ("Retourne une paire d'itérateurs délimitant la plage d'éléments équivalents (pour `std::set` ordonné).", "std::set<int> s = {1, 3, 5}; auto p = s.equal_range(3); std::cout << *p.first << \" \" << *p.second << std::endl; // 3 5"),
            "std::set::empty() (C++)": ("Vérifie si l'ensemble est vide.", "std::set<int> s; std::cout << s.empty() << std::endl; // 1 (true)"),
            "std::set::size() (C++)": ("Retourne le nombre d'éléments dans l'ensemble.", "std::set<int> s = {1, 2}; std::cout << s.size() << std::endl; // 2"),
            "std::set::max_size() (C++)": ("Retourne le nombre maximum d'éléments que l'ensemble peut contenir.", "std::set<int> s; std::cout << s.max_size() << std::endl;"),
            "std::set::emplace() (C++11)": ("Construit et insère un nouvel élément directement dans l'ensemble.", "std::set<int> s; s.emplace(10);"),
            "std::set::swap() (C++)": ("Échange le contenu de deux ensembles de même type.", "std::set<int> s1 = {1, 2}; std::set<int> s2 = {3, 4}; s1.swap(s2);"),
            "std::set::key_comp() (C++)": ("Retourne l'objet de comparaison de clés utilisé.", "std::set<int> s; std::set<int>::key_compare comp = s.key_comp();"),
            "std::set::value_comp() (C++)": ("Identique à `key_comp()` pour les ensembles.", "std::set<int> s; std::set<int>::value_compare comp = s.value_comp();"),
            "std::set::get_allocator() (C++)": ("Retourne l'allocateur d'objets utilisé par l'ensemble.", "std::set<int> s; std::allocator<int> alloc = s.get_allocator();"),
            "std::set_union() (C++: <algorithm>)": ("Calcule l'union de deux ensembles triés et la stocke dans un troisième conteneur.", "std::set<int> s1={1,2}, s2={2,3}; std::vector<int> res; std::set_union(s1.begin(), s1.end(), s2.begin(), s2.end(), std::back_inserter(res)); // res: 1 2 3"),
            "std::set_intersection() (C++: <algorithm>)": ("Calcule l'intersection de deux ensembles triés.", "std::set<int> s1={1,2}, s2={2,3}; std::vector<int> res; std::set_intersection(s1.begin(), s1.end(), s2.begin(), s2.end(), std::back_inserter(res)); // res: 2"),
            "std::set_difference() (C++: <algorithm>)": ("Calcule la différence entre deux ensembles triés.", "std::set<int> s1={1,2}, s2={2,3}; std::vector<int> res; std::set_difference(s1.begin(), s1.end(), s2.begin(), s2.end(), std::back_inserter(res)); // res: 1"),
            "std::set_symmetric_difference() (C++: <algorithm>)": ("Calcule la différence symétrique entre deux ensembles triés.", "std::set<int> s1={1,2}, s2={2,3}; std::vector<int> res; std::set_symmetric_difference(s1.begin(), s1.end(), s2.begin(), s2.end(), std::back_inserter(res)); // res: 1 3"),
            "std::includes() (C++: <algorithm>)": ("Vérifie si une plage est incluse dans une autre plage triée.", "std::set<int> s1={1,2,3}, s2={1,2}; std::cout << std::includes(s1.begin(), s1.end(), s2.begin(), s2.end()) << std::endl; // 1 (true)"),
            "Custom comparators (C++)": ("Utilisation de comparateurs personnalisés pour définir l'ordre des éléments dans `std::set`.", "struct { bool operator()(int a, int b) const { return a > b; } } customLess; std::set<int, decltype(customLess)> s(customLess);"),
            "Hash functions (C++: `std::unordered_set`)": ("Nécessite des fonctions de hachage (ex: `std::hash`) pour les types personnalisés.", "// Implémentation de `operator==` et `std::hash` pour les types personnalisés utilisés dans `unordered_set`."),
            "Bucket interface (`std::unordered_set`)": ("Méthodes pour interagir avec les compartiments (buckets) du `unordered_set`.", "std::unordered_set<int> us = {1, 2, 3}; for (size_t i = 0; i < us.bucket_count(); ++i) { std::cout << \"Bucket \" << i << \": \"; for (auto it = us.begin(i); it != us.end(i); ++it) std::cout << *it << \" \"; std::cout << std::endl; }"),
            "Load factor (`std::unordered_set`)": ("Gère la charge moyenne par compartiment et le re-hachage.", "std::unordered_set<int> us; us.max_load_factor(0.75f);"),
            "Rehash (`std::unordered_set`)": ("Force le re-hachage du conteneur.", "std::unordered_set<int> us; us.rehash(100);")
        },
        "description": "En C, il n'y a pas de type 'set' natif, cela doit être implémenté manuellement. En C++, `std::set` (`<set>`, ordonné) et `std::unordered_set` (`<unordered_set>`, non ordonné, C++11) sont les conteneurs équivalents, offrant des opérations sur les ensembles et une recherche rapide. Les opérations ensemblistes génériques sont dans `<algorithm>`."
    },
    "Boolean": {
        "methods": {
            "bool (type)": ("Type booléen natif.", "bool b = true; if (b) printf(\"True\\n\"); // True"),
            "! (NOT)": ("Opérateur logique NOT.", "bool b = true; printf(\"%d\\n\", !b); // 0 (false)"),
            "&& (AND)": ("Opérateur logique AND.", "printf(\"%d\\n\", true && false); // 0 (false)"),
            "|| (OR)": ("Opérateur logique OR.", "printf(\"%d\\n\", true || false); // 1 (true)"),
            # --- 50+ méthodes/concepts pour Boolean ---
            "true / false (keywords)": ("Littéraux booléens.", "bool value = true;"),
            "_Bool (C99 keyword)": ("Type booléen en C99.", "_Bool flag = 1;"),
            "stdbool.h (C)": ("En-tête pour utiliser `bool`, `true`, `false` en C.", "#include <stdbool.h> bool my_flag = true;"),
            "Implicit conversion to int": ("Conversion implicite de `bool` en `int` (true -> 1, false -> 0).", "bool b = true; int i = b; printf(\"%d\\n\", i); // 1"),
            "Implicit conversion from arithmetic types": ("Conversion implicite de types arithmétiques en `bool` (non-zéro -> true, zéro -> false).", "int x = 0; bool b = x; printf(\"%d\\n\", b); // 0 (false)"),
            "Comparison operators (==, !=, <, <=, >, >=)": ("Opérateurs de comparaison qui produisent des booléens.", "int x = 5, y = 3; bool res = (x > y); printf(\"%d\\n\", res); // 1 (true)"),
            "Short-circuit evaluation (&&, ||)": ("Évaluation des expressions logiques de gauche à droite, s'arrêtant dès que le résultat est connu.", "int a = 0; int b = 1; if (a && (b = 5)) { /* not executed */ } printf(\"%d\\n\", b); // 1"),
            "Ternary operator (?:)": ("Opérateur conditionnel qui prend un booléen pour décider quelle expression évaluer.", "int x = (true ? 10 : 20); printf(\"%d\\n\", x); // 10"),
            "Bitwise operators on integers (acting like booleans on bits)": ("Opérateurs bit à bit peuvent être vus comme booléens sur chaque bit.", "unsigned char flags = 0b0011; // 3\nif (flags & 0b0001) { /* bit 0 set */ }"),
            "Boolean literals in C++": ("Littéraux `true` et `false`.", "const bool STATUS_OK = true;"),
            "`std::ios_base::boolalpha` (C++)": ("Manipulateur pour afficher les booléens comme 'true' ou 'false' au lieu de 1 ou 0.", "std::cout << std::boolalpha << true << std::endl; // true"),
            "Logical `not` operator (`!`) (C++)": ("Opérateur logique NON.", "bool is_active = false; if (!is_active) std::cout << \"Inactive\\n\";"),
            "Logical `and` operator (`&&`) (C++)": ("Opérateur logique ET.", "if (cond1 && cond2) std::cout << \"Both true\\n\";"),
            "Logical `or` operator (`||`) (C++)": ("Opérateur logique OU.", "if (cond1 || cond2) std::cout << \"At least one true\\n\";")
        },
        "description": "Le type `bool` est natif en C++ et depuis C99 en C (via `_Bool` ou `stdbool.h`). Il représente les valeurs de vérité : `true` (non-zéro) ou `false` (zéro). Les opérateurs logiques (`&&`, `||`, `!`) et les conversions implicites sont fondamentaux."
    },
    "Integer": {
        "methods": {
            "int / long / short": ("Types pour les nombres entiers.", "int x = 10; long y = 1000000000L; short z = 5;"),
            "abs() / labs() / llabs()": ("Valeur absolue (pour différents types d'entiers).", "int x = -5; printf(\"%d\\n\", abs(x)); // 5"),
            "pow() (C: `math.h`, C++: `cmath`)": ("Puissance d'un nombre (retourne un double).", "printf(\"%f\\n\", pow(2, 3)); // 8.000000"),
            "/ (division entière)": ("Division entière (tronque la partie décimale).", "printf(\"%d\\n\", 10 / 3); // 3"),
            "% (modulo)": ("Opérateur modulo (reste de la division).", "printf(\"%d\\n\", 10 % 3); // 1"),
            # --- 50+ méthodes/concepts pour Integer ---
            "signed / unsigned (keywords)": ("Qualificateurs pour les entiers signés ou non signés.", "unsigned int u = 10; signed int s = -5;"),
            "char (integer type)": ("Type pour les petits entiers (souvent 1 octet), peut être utilisé pour de petites valeurs numériques.", "char c_val = 120;"),
            "long long (C99/C++11)": ("Type entier de grande taille.", "long long ll = 1234567890123LL;"),
            "Integer literals (decimal, octal, hex, binary)": ("Différentes bases pour les littéraux entiers.", "int dec = 10; int oct = 012; int hex = 0xA; int bin = 0b1010; (C++14)"),
            "sizeof (operator)": ("Taille en octets d'un type entier.", "printf(\"%ld\\n\", sizeof(int));"),
            "MIN / MAX constants (C: <limits.h>, C++: <limits>)": ("Constantes pour les valeurs min/max des types entiers.", "printf(\"%d\\n\", INT_MAX);"),
            "Addition (`+`)": ("Opérateur d'addition.", "int sum = 5 + 3; // 8"),
            "Subtraction (`-`)": ("Opérateur de soustraction.", "int diff = 5 - 3; // 2"),
            "Multiplication (`*`)": ("Opérateur de multiplication.", "int prod = 5 * 3; // 15"),
            "Increment (`++`) (prefix/postfix)": ("Opérateur d'incrémentation.", "int x = 5; x++; ++x;"),
            "Decrement (`--`) (prefix/postfix)": ("Opérateur de décrémentation.", "int x = 5; x--; --x;"),
            "Compound assignment operators (`+=`, `-=`, `*=`, `/=`, `%=`, etc.)": ("Opérateurs d'affectation combinée.", "int x = 5; x += 3; // x is 8"),
            "Comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`)": ("Opérateurs de comparaison.", "int x = 5, y = 3; bool res = (x == y);"),
            "Bitwise AND (`&`)": ("Opérateur AND bit à bit.", "int res = 5 & 3; // 1"),
            "Bitwise OR (`|`)": ("Opérateur OR bit à bit.", "int res = 5 | 3; // 7"),
            "Bitwise XOR (`^`)": ("Opérateur XOR bit à bit.", "int res = 5 ^ 3; // 6"),
            "Bitwise NOT (`~`)": ("Opérateur NOT bit à bit (complément à un).", "int res = ~5; // -6"),
            "Left Shift (`<<`)": ("Opérateur de décalage à gauche.", "int res = 5 << 1; // 10"),
            "Right Shift (`>>`)": ("Opérateur de décalage à droite.", "int res = 5 >> 1; // 2"),
            "Type casting (explicit conversion)": ("Conversion explicite d'un type à un autre.", "double d = 3.14; int i = (int)d; // 3"),
            "printf() with integer format specifiers (`%d`, `%i`, `%u`, `%ld`, `%lld`, `%x`, `%o`)": ("Formatage de sortie des entiers.", "printf(\"%d %x\\n\", 10, 10); // 10 a"),
            "scanf() with integer format specifiers": ("Lecture d'entiers formatés.", "int num; scanf(\"%d\", &num);"),
            "rand() (C: <stdlib.h>)": ("Génère un nombre entier pseudo-aléatoire.", "int r = rand();"),
            "srand() (C: <stdlib.h>)": ("Initialise le générateur de nombres aléatoires.", "srand(time(NULL));"),
            "div() (C: <stdlib.h>)": ("Retourne quotient et reste pour `int`.", "div_t d = div(10, 3); printf(\"%d %d\\n\", d.quot, d.rem); // 3 1"),
            "ldiv() / lldiv() (C: <stdlib.h>)": ("Pour `long` et `long long`.", "ldiv_t d = ldiv(10L, 3L);"),
            "__builtin_popcount() (GCC/Clang)": ("Compte les bits à 1 dans un entier.", "int x = 7; printf(\"%d\\n\", __builtin_popcount(x)); // 3 (0b111)"),
            "__builtin_clz() (GCC/Clang)": ("Compte les zéros en tête.", "unsigned int x = 8; printf(\"%d\\n\", __builtin_clz(x)); // 28 (pour 32-bit int)"),
            "__builtin_ctz() (GCC/Clang)": ("Compte les zéros en fin.", "unsigned int x = 8; printf(\"%d\\n\", __builtin_ctz(x)); // 3 (0b1000)"),
            "Overflow/Underflow behavior": ("Comportement en cas de dépassement/sous-dépassement (défini pour non signés, indéfini pour signés).", "unsigned char x = 255; x++; // x becomes 0"),
            "Promotion rules (integer promotion)": ("Règles de conversion implicite pour les opérations.", "short a = 1; int b = 2; int res = a + b; // a est promu en int"),
            "constexpr (C++11)": ("Permet de calculer des valeurs entières au moment de la compilation.", "constexpr int MY_CONST = 10 * 5;"),
            "enum / enum class (C/C++)": ("Définir des ensembles d'entiers nommés.", "enum Color { RED, GREEN, BLUE }; Color c = RED;"),
            "Type aliases (typedef/using)": ("Créer des alias pour les types entiers.", "typedef int MyInt; MyInt x = 10;"),
            "Fixed-width integers (C++11: <cstdint>)": ("Types entiers avec une taille garantie (ex: `int32_t`, `uint64_t`).", "#include <cstdint> int32_t i = 10;"),
            "`std::numeric_limits<T>::max()` / `min()` (C++: <limits>)": ("Obtenir les valeurs min/max spécifiques à un type.", "std::cout << std::numeric_limits<int>::max() << std::endl;"),
            "`std::numeric_limits<T>::digits` (C++)": ("Nombre de bits de mantisse pour les flottants ou de bits pour les entiers.", "std::cout << std::numeric_limits<int>::digits << std::endl;"),
            "`std::numeric_limits<T>::is_signed` / `is_integer` (C++)": ("Propriétés des types numériques.", "std::cout << std::numeric_limits<int>::is_signed << std::endl; // 1 (true)")
        },
        "description": "C et C++ ont plusieurs types d'entiers (`int`, `long`, `short`, `char`, `long long`) avec des qualificateurs `signed`/`unsigned`. Les opérations arithmétiques et bit à bit sont natives. La gestion des limites et des conversions est explicite. `<limits.h>`/`<limits>` fournit des informations sur les types."
    },
    "Float": {
        "methods": {
            "float (type)": ("Type pour les nombres à virgule flottante simple précision.", "float f = 3.14f;"),
            "abs() / fabsf()": ("Valeur absolue (pour `float`).", "float f = -3.14f; printf(\"%f\\n\", fabsf(f)); // 3.140000"),
            "ceilf() / floorf() / roundf() (C: `math.h`, C++: `cmath`)": ("Arrondi supérieur/inférieur/le plus proche (pour `float`).", "printf(\"%f\\n\", ceilf(4.3f)); // 5.000000"),
            "/ (division flottante)": ("Division (retourne un `float`).", "printf(\"%f\\n\", 10.0f / 3.0f); // 3.333333"),
            "fmodf() (C: `math.h`, C++: `cmath`)": ("Reste de la division flottante (pour `float`).", "printf(\"%f\\n\", fmodf(10.0f, 3.0f)); // 1.000000"),
            "FLT_MAX / FLT_MIN / FLT_EPSILON (C: `float.h`, C++: `cfloat`)": ("Constantes pour les limites et la précision des `float`.", "printf(\"%e %e %e\\n\", FLT_MAX, FLT_MIN, FLT_EPSILON);"),
            # --- 50+ méthodes/concepts pour Float ---
            "float_t / double_t (C99: <math.h>)": ("Types pour des calculs plus rapides (souvent `float` ou `double`).", "float_t x = 1.0f;"),
            "long double (type)": ("Type pour les nombres à virgule flottante étendue (précision supérieure).", "long double ld = 3.1415926535L;"),
            "Float literals (suffix f/F)": ("Littéraux flottants avec suffixe `f` pour `float`.", "float my_f = 12.34f;"),
            "printf() with float format specifiers (`%f`, `%e`, `%g`, `%a`)": ("Formatage de sortie des flottants.", "printf(\"%f %e\\n\", 3.14, 3.14); // 3.140000 3.140000e+00"),
            "scanf() with float format specifiers": ("Lecture de flottants formatés.", "float f; scanf(\"%f\", &f);"),
            "sqrtf() (C: `math.h`, C++: `cmath`)": ("Racine carrée.", "printf(\"%f\\n\", sqrtf(9.0f)); // 3.000000"),
            "cbrtf() (C: `math.h`, C++: `cmath`)": ("Racine cubique.", "printf(\"%f\\n\", cbrtf(27.0f)); // 3.000000"),
            "expf() (C: `math.h`, C++: `cmath`)": ("Fonction exponentielle e^x.", "printf(\"%f\\n\", expf(1.0f)); // 2.718282"),
            "logf() (C: `math.h`, C++: `cmath`)": ("Logarithme naturel.", "printf(\"%f\\n\", logf(2.71828f)); // 1.000000"),
            "log10f() (C: `math.h`, C++: `cmath`)": ("Logarithme base 10.", "printf(\"%f\\n\", log10f(100.0f)); // 2.000000"),
            "sinf() / cosf() / tanf() (C: `math.h`, C++: `cmath`)": ("Fonctions trigonométriques.", "printf(\"%f\\n\", sinf(0.0f)); // 0.000000"),
            "asinf() / acosf() / atanf() (C: `math.h`, C++: `cmath`)": ("Fonctions trigonométriques inverses.", "printf(\"%f\\n\", asinf(0.0f)); // 0.000000"),
            "atan2f() (C: `math.h`, C++: `cmath`)": ("Arc tangente de y/x.", "printf(\"%f\\n\", atan2f(1.0f, 1.0f)); // 0.785398 (PI/4)"),
            "hypotf() (C: `math.h`, C++: `cmath`)": ("Hypoténuse de deux côtés.", "printf(\"%f\\n\", hypotf(3.0f, 4.0f)); // 5.000000"),
            "coshf() / sinhf() / tanhf() (C: `math.h`, C++: `cmath`)": ("Fonctions hyperboliques.", "printf(\"%f\\n\", coshf(0.0f)); // 1.000000"),
            "modff() (C: `math.h`, C++: `cmath`)": ("Sépare un flottant en partie entière et fractionnaire.", "float frac, integer; frac = modff(3.14f, &integer); printf(\"%f %f\\n\", integer, frac); // 3.000000 0.140000"),
            "frexpf() (C: `math.h`, C++: `cmath`)": ("Sépare un flottant en mantisse et exposant.", "int exp; float mantissa = frexpf(8.0f, &exp); printf(\"%f %d\\n\", mantissa, exp); // 0.500000 4 (8 = 0.5 * 2^4)"),
            "ldexpf() (C: `math.h`, C++: `cmath`)": ("Multiplie un flottant par une puissance de 2.", "printf(\"%f\\n\", ldexpf(0.5f, 4)); // 8.000000"),
            "fmaf() (C: `math.h`, C++: `cmath`)": ("Fait (a * b) + c avec une seule erreur d'arrondi (Fused Multiply-Add).", "printf(\"%f\\n\", fmaf(1.0f, 2.0f, 3.0f)); // 5.000000"),
            "roundf() / truncf() / rintf() / nearbyintf() (C: `math.h`, C++: `cmath`)": ("Différentes méthodes d'arrondi.", "printf(\"%f\\n\", roundf(3.5f)); // 4.000000"),
            "nextafterf() / nexttowardf() (C: `math.h`, C++: `cmath`)": ("Retourne le prochain nombre flottant représentable.", "printf(\"%a\\n\", nextafterf(1.0f, 2.0f)); // 0x1.000002p+0"),
            "copysignf() (C: `math.h`, C++: `cmath`)": ("Copie le signe d'un nombre à un autre.", "printf(\"%f\\n\", copysignf(1.0f, -2.0f)); // -1.000000"),
            "isnanf() / isinff() / isfinitef() (C: `math.h`, C++: `cmath`)": ("Vérifie si flottant est NaN, Infini ou Fini.", "printf(\"%d\\n\", isnanf(0.0f/0.0f)); // 1 (true)"),
            "signbitf() (C: `math.h`, C++: `cmath`)": ("Vérifie le bit de signe.", "printf(\"%d\\n\", signbitf(-5.0f)); // 1 (true)"),
            "isnormalf() (C: `math.h`, C++: `cmath`)": ("Vérifie si un flottant est normal (non subnormal, non nul, non inf, non NaN).", "printf(\"%d\\n\", isnormalf(1.0f)); // 1 (true)"),
            "fdimf() (C: `math.h`, C++: `cmath`)": ("Retourne la différence positive entre deux nombres (max(0, x-y)).", "printf(\"%f\\n\", fdimf(5.0f, 3.0f)); // 2.000000"),
            "fmaxf() / fminf() (C: `math.h`, C++: `cmath`)": ("Retourne le maximum/minimum de deux flottants.", "printf(\"%f\\n\", fmaxf(5.0f, 3.0f)); // 5.000000"),
            "truncf() (C: `math.h`, C++: `cmath`)": ("Tronque la partie fractionnaire vers zéro.", "printf(\"%f\\n\", truncf(-3.7f)); // -3.000000"),
            "lroundf() / llroundf() (C: `math.h`, C++: `cmath`)": ("Arrondit au `long`/`long long` le plus proche.", "printf(\"%ld\\n\", lroundf(3.5f)); // 4"),
            "rintf() / lrintf() / llrintf() (C: `math.h`, C++: `cmath`)": ("Arrondit au nombre entier le plus proche, utilisant le mode d'arrondi courant.", "printf(\"%f\\n\", rintf(3.5f)); // 4.000000 (dépend du mode d'arrondi)"),
            "nearbyintf() (C: `math.h`, C++: `cmath`)": ("Arrondit au nombre entier le plus proche sans lever d'exception en cas d'imprécision.", "printf(\"%f\\n\", nearbyintf(3.5f)); // 4.000000 (dépend du mode d'arrondi)"),
            "remquof() (C: `math.h`, C++: `cmath`)": ("Calcule le reste de division et un quotient partiel.", "int quot; printf(\"%f\\n\", remquof(10.0f, 3.0f, &quot)); // 1.000000"),
            "atan2() (C: `math.h`, C++: `cmath`)": ("Arc tangente avec deux arguments pour déterminer le quadrant.", "printf(\"%f\\n\", atan2f(1.0f, -1.0f)); // 2.356194 (3PI/4)"),
            "erff() / erfcf() (C: `math.h`, C++: `cmath`)": ("Fonction d'erreur / fonction d'erreur complémentaire.", "printf(\"%f\\n\", erff(1.0f)); // 0.842701"),
            "gammaf() / lgammaf() (C: `math.h`, C++: `cmath`)": ("Fonction Gamma / log Gamma absolu.", "printf(\"%f\\n\", gammaf(0.5f)); // 1.772454"),
            "tgammaf() (C: `math.h`, C++: `cmath`)": ("Fonction Gamma.", "printf(\"%f\\n\", tgammaf(0.5f)); // 1.772454"),
            "nanf() (C: `math.h`, C++: `cmath`)": ("Retourne une représentation NaN.", "float val = nanf(\"\");"),
            "isgreaterf() / isgreaterequalf() (C: `math.h`, C++: `cmath`)": ("Comparaison sans lancer d'exception pour NaN.", "printf(\"%d\\n\", isgreaterf(5.0f, 3.0f)); // 1"),
            "islessf() / islessequalf() (C: `math.h`, C++: `cmath`)": ("Comparaison sans lancer d'exception pour NaN.", "printf(\"%d\\n\", islessf(3.0f, 5.0f)); // 1"),
            "isunorderedf() (C: `math.h`, C++: `cmath`)": ("Vérifie si deux flottants sont non ordonnés (ex: l'un est NaN).", "printf(\"%d\\n\", isunorderedf(NAN, 5.0f)); // 1"),
            "long double (type)": ("Type pour les nombres à virgule flottante de très haute précision (si supporté par le compilateur).", "long double PI = 3.14159265358979323846L;")
        },
        "description": "Le type **`float`** représente les nombres à virgule flottante en simple précision. Les opérations arithmétiques sont natives. La plupart des fonctions mathématiques avancées sont fournies par la bibliothèque `<math.h>` en C ou `<cmath>` en C++, avec des versions spécifiques pour `float` (suffixe `f`)."
    },
    "Double": { # Pour les nombres à virgule flottante double précision
        "methods": {
            "double (type)": ("Type pour les nombres à virgule flottante double précision.", "double d = 2.718;"),
            "abs() / fabs()": ("Valeur absolue (pour `double`).", "double d = -2.718; printf(\"%lf\\n\", fabs(d)); // 2.718000"),
            "ceil() / floor() / round() (C: `math.h`, C++: `cmath`)": ("Arrondi supérieur/inférieur/le plus proche (pour `double`).", "printf(\"%lf\\n\", ceil(4.7)); // 5.000000"),
            "/ (division flottante)": ("Division (retourne un `double`).", "printf(\"%lf\\n\", 10.0 / 3.0); // 3.333333"),
            "fmod() (C: `math.h`, C++: `cmath`)": ("Reste de la division flottante (pour `double`).", "printf(\"%lf\\n\", fmod(10.0, 3.0)); // 1.000000"),
            "DBL_MAX / DBL_MIN / DBL_EPSILON (C: `float.h`, C++: `cfloat`)": ("Constantes pour les limites et la précision des `double`.", "printf(\"%e %e %e\\n\", DBL_MAX, DBL_MIN, DBL_EPSILON);"),
            "NAN / INFINITY (C: `math.h`, C++: `cmath`)": ("Constantes pour Not-a-Number et infini.", "printf(\"%lf %lf\\n\", NAN, INFINITY); // nan inf"),
            # --- 50+ méthodes/concepts pour Double ---
            "long double (type)": ("Type pour les nombres à virgule flottante étendue (peut avoir la même taille que `double` ou plus).", "long double ld = 1.234567890123456789L;"),
            "Double literals (no suffix or d/D)": ("Littéraux flottants (par défaut `double` si pas de suffixe `f`).", "double my_d = 12.34; double my_d2 = 5.67d;"),
            "printf() with double format specifiers (`%lf`, `%e`, `%g`, `%a`)": ("Formatage de sortie des `double`.", "printf(\"%lf %e\\n\", 3.14159, 3.14159);"),
            "scanf() with double format specifiers (`%lf`)": ("Lecture de `double` formatés.", "double d; scanf(\"%lf\", &d);"),
            "sqrt() (C: `math.h`, C++: `cmath`)": ("Racine carrée.", "printf(\"%lf\\n\", sqrt(9.0));"),
            "cbrt() (C: `math.h`, C++: `cmath`)": ("Racine cubique.", "printf(\"%lf\\n\", cbrt(27.0));"),
            "exp() (C: `math.h`, C++: `cmath`)": ("Fonction exponentielle e^x.", "printf(\"%lf\\n\", exp(1.0));"),
            "log() (C: `math.h`, C++: `cmath`)": ("Logarithme naturel.", "printf(\"%lf\\n\", log(2.71828));"),
            "log10() (C: `math.h`, C++: `cmath`)": ("Logarithme base 10.", "printf(\"%lf\\n\", log10(100.0));"),
            "sin() / cos() / tan() (C: `math.h`, C++: `cmath`)": ("Fonctions trigonométriques.", "printf(\"%lf\\n\", sin(0.0));"),
            "asin() / acos() / atan() (C: `math.h`, C++: `cmath`)": ("Fonctions trigonométriques inverses.", "printf(\"%lf\\n\", asin(0.0));"),
            "atan2() (C: `math.h`, C++: `cmath`)": ("Arc tangente de y/x.", "printf(\"%lf\\n\", atan2(1.0, 1.0));"),
            "hypot() (C: `math.h`, C++: `cmath`)": ("Hypoténuse de deux côtés.", "printf(\"%lf\\n\", hypot(3.0, 4.0));"),
            "cosh() / sinh() / tanh() (C: `math.h`, C++: `cmath`)": ("Fonctions hyperboliques.", "printf(\"%lf\\n\", cosh(0.0));"),
            "modf() (C: `math.h`, C++: `cmath`)": ("Sépare un double en partie entière et fractionnaire.", "double frac, integer; frac = modf(3.14, &integer);"),
            "frexp() (C: `math.h`, C++: `cmath`)": ("Sépare un double en mantisse et exposant.", "int exp; double mantissa = frexp(8.0, &exp);"),
            "ldexp() (C: `math.h`, C++: `cmath`)": ("Multiplie un double par une puissance de 2.", "printf(\"%lf\\n\", ldexp(0.5, 4));"),
            "fma() (C: `math.h`, C++: `cmath`)": ("Fait (a * b) + c avec une seule erreur d'arrondi (Fused Multiply-Add).", "printf(\"%lf\\n\", fma(1.0, 2.0, 3.0));"),
            "round() / trunc() / rint() / nearbyint() (C: `math.h`, C++: `cmath`)": ("Différentes méthodes d'arrondi.", "printf(\"%lf\\n\", round(3.5));"),
            "nextafter() / nexttoward() (C: `math.h`, C++: `cmath`)": ("Retourne le prochain nombre flottant représentable.", "printf(\"%a\\n\", nextafter(1.0, 2.0));"),
            "copysign() (C: `math.h`, C++: `cmath`)": ("Copie le signe d'un nombre à un autre.", "printf(\"%lf\\n\", copysign(1.0, -2.0));"),
            "isnan() / isinf() / isfinite() (C: `math.h`, C++: `cmath`)": ("Vérifie si double est NaN, Infini ou Fini.", "printf(\"%d\\n\", isnan(0.0/0.0));"),
            "signbit() (C: `math.h`, C++: `cmath`)": ("Vérifie le bit de signe.", "printf(\"%d\\n\", signbit(-5.0));"),
            "isnormal() (C: `math.h`, C++: `cmath`)": ("Vérifie si un double est normal.", "printf(\"%d\\n\", isnormal(1.0));"),
            "fdim() (C: `math.h`, C++: `cmath`)": ("Retourne la différence positive entre deux nombres.", "printf(\"%lf\\n\", fdim(5.0, 3.0));"),
            "fmax() / fmin() (C: `math.h`, C++: `cmath`)": ("Retourne le maximum/minimum de deux doubles.", "printf(\"%lf\\n\", fmax(5.0, 3.0));"),
            "trunc() (C: `math.h`, C++: `cmath`)": ("Tronque la partie fractionnaire vers zéro.", "printf(\"%lf\\n\", trunc(-3.7));"),
            "lround() / llround() (C: `math.h`, C++: `cmath`)": ("Arrondit au `long`/`long long` le plus proche.", "printf(\"%ld\\n\", lround(3.5));"),
            "rint() / lrint() / llrint() (C: `math.h`, C++: `cmath`)": ("Arrondit au nombre entier le plus proche, utilisant le mode d'arrondi courant.", "printf(\"%lf\\n\", rint(3.5));"),
            "nearbyint() (C: `math.h`, C++: `cmath`)": ("Arrondit au nombre entier le plus proche sans lever d'exception en cas d'imprécision.", "printf(\"%lf\\n\", nearbyint(3.5));"),
            "remquo() (C: `math.h`, C++: `cmath`)": ("Calcule le reste de division et un quotient partiel.", "int quot; printf(\"%lf\\n\", remquo(10.0, 3.0, &quot));"),
            "erf() / erfc() (C: `math.h`, C++: `cmath`)": ("Fonction d'erreur / fonction d'erreur complémentaire.", "printf(\"%lf\\n\", erf(1.0));"),
            "gamma() / lgamma() (C: `math.h`, C++: `cmath`)": ("Fonction Gamma / log Gamma absolu.", "printf(\"%lf\\n\", gamma(0.5));"),
            "tgamma() (C: `math.h`, C++: `cmath`)": ("Fonction Gamma.", "printf(\"%lf\\n\", tgamma(0.5));"),
            "nan() (C: `math.h`, C++: `cmath`)": ("Retourne une représentation NaN.", "double val = nan(\"\");"),
            "isgreater() / isgreaterequal() (C: `math.h`, C++: `cmath`)": ("Comparaison sans lancer d'exception pour NaN.", "printf(\"%d\\n\", isgreater(5.0, 3.0));"),
            "isless() / islessequal() (C: `math.h`, C++: `cmath`)": ("Comparaison sans lancer d'exception pour NaN.", "printf(\"%d\\n\", isless(3.0, 5.0));"),
            "isunordered() (C: `math.h`, C++: `cmath`)": ("Vérifie si deux doubles sont non ordonnés.", "printf(\"%d\\n\", isunordered(NAN, 5.0));"),
            "long double (type)": ("Type pour les nombres à virgule flottante de très haute précision (si supporté par le compilateur).", "long double PI_ld = 3.14159265358979323846L;"),
            "std::numeric_limits<double>::epsilon() (C++: <limits>)": ("Plus petit nombre tel que 1 + epsilon != 1.", "std::cout << std::numeric_limits<double>::epsilon() << std::endl;"),
            "std::numeric_limits<double>::max() / min() (C++: <limits>)": ("Valeurs max/min du type `double`.", "std::cout << std::numeric_limits<double>::max() << std::endl;"),
            "std::numeric_limits<double>::lowest() (C++11: <limits>)": ("Plus petite valeur finie représentable.", "std::cout << std::numeric_limits<double>::lowest() << std::endl;"),
            "std::numeric_limits<double>::infinity() (C++: <limits>)": ("Valeur positive infinie.", "std::cout << std::numeric_limits<double>::infinity() << std::endl;"),
            "std::numeric_limits<double>::quiet_NaN() (C++: <limits>)": ("Représentation NaN silencieuse.", "std::cout << std::numeric_limits<double>::quiet_NaN() << std::endl;"),
            "std::fmod (C++: <cmath>)": ("Fonction pour le reste de division flottante (C++ surchargée).", "std::cout << std::fmod(10.0, 3.0) << std::endl;"),
            "std::round (C++: <cmath>)": ("Fonction d'arrondi au plus proche (C++ surchargée).", "std::cout << std::round(3.5) << std::endl;"),
            "std::trunc (C++: <cmath>)": ("Fonction de troncature (C++ surchargée).", "std::cout << std::trunc(-3.7) << std::endl;")
        },
        "description": "Le type **`double`** représente les nombres à virgule flottante en double précision. Il offre une plus grande précision que `float` et est le type flottant par défaut pour la plupart des calculs. Les fonctions mathématiques de `<math.h>`/`<cmath>` sont généralement surchargées pour `double`."
    },
    "Binary Data": {
        "methods": {
            "Bitwise Operators": {
                "& (AND)": ("Effectue un ET logique bit à bit.", "int a = 5 (0b101); int b = 3 (0b011); printf(\"%d\\n\", a & b); // 1 (0b001)"),
                "| (OR)": ("Effectue un OU logique bit à bit.", "int a = 5 (0b101); int b = 3 (0b011); printf(\"%d\\n\", a | b); // 7 (0b111)"),
                "^ (XOR)": ("Effectue un OU exclusif bit à bit.", "int a = 5 (0b101); int b = 3 (0b011); printf(\"%d\\n\", a ^ b); // 6 (0b110)"),
                "~ (NOT)": ("Inverse tous les bits (complément à un).", "int a = 5; printf(\"%d\\n\", ~a); // -6"),
                "<< (Décalage à gauche)": ("Décale les bits vers la gauche.", "int a = 5; printf(\"%d\\n\", a << 1); // 10"),
                ">> (Décalage à droite)": ("Décale les bits vers la droite.", "int a = 5; printf(\"%d\\n\", a >> 1); // 2")
            },
            "Binary representation (C++14 et +)": ("Littéraux binaires pour les entiers.", "int x = 0b1010; std::cout << x << std::endl; // 10"),
            "Bit fields (struct C/C++)": ("Permet de définir des membres de structure avec une taille en bits spécifique.", "struct MyFlags { unsigned int is_active : 1; unsigned int type : 3; }; MyFlags flags; flags.is_active = 1;"),
            "char array / unsigned char array": ("Utilisés pour stocker des données binaires brutes au niveau de l'octet.", "unsigned char buffer[4] = {0x12, 0x34, 0x56, 0x78};"),
            # --- 50+ méthodes/concepts pour Binary Data ---
            "Hexadecimal literals (0x...)": ("Littéraux hexadécimaux pour les entiers.", "int hex_val = 0xFF; // 255"),
            "Octal literals (0...)": ("Littéraux octaux pour les entiers.", "int oct_val = 077; // 63"),
            "Bit masks": ("Utilisation d'entiers pour masquer/isoler des bits spécifiques.", "unsigned int flags = 0b1101; if ((flags & 0b0001) != 0) { /* bit 0 is set */ }"),
            "Setting a bit": ("Mettre un bit à 1.", "unsigned int flags = 0; flags |= (1 << 2); // set bit 2 (0b0100)"),
            "Clearing a bit": ("Mettre un bit à 0.", "unsigned int flags = 0b0111; flags &= ~(1 << 1); // clear bit 1 (0b0101)"),
            "Toggling a bit": ("Inverser un bit.", "unsigned int flags = 0b0100; flags ^= (1 << 2); // toggle bit 2 (0b0000)"),
            "Checking if a bit is set": ("Vérifier si un bit est à 1.", "unsigned int flags = 0b0101; if ((flags >> 0) & 1) { /* bit 0 set */ }"),
            "Endianness (byte order)": ("Concept de l'ordre des octets (little-endian vs big-endian) lors de la manipulation binaire multi-octets.", "// Concept architectural, pas une fonction directe."),
            "Bit manipulation functions (e.g., in `stdint.h` or custom)": ("Fonctions pour des manipulations de bits complexes (ex: rotation, comptage).", "// Généralement implémentées manuellement ou par des intrinsèques du compilateur."),
            "Packed structs (C/C++)": ("Structures où les membres sont alignés sur des frontières d'octets minimales.", "#pragma pack(1) struct PackedData { char c; int i; }; #pragma pack()"),
            "Bitsets (C++: <bitset>)": ("Conteneur pour manipuler des séquences de bits de taille fixe.", "std::bitset<8> b(std::string(\"10101010\")); std::cout << b.count() << std::endl; // 4"),
            "std::bitset::count() (C++)": ("Compte le nombre de bits à 1 dans un `std::bitset`.", "std::bitset<8> b(\"10101010\"); std::cout << b.count() << std::endl; // 4"),
            "std::bitset::size() (C++)": ("Retourne la taille du `std::bitset` en bits.", "std::bitset<8> b; std::cout << b.size() << std::endl; // 8"),
            "std::bitset::test() (C++)": ("Teste si un bit est à 1 à une position donnée.", "std::bitset<8> b(\"00000001\"); std::cout << b.test(0) << std::endl; // 1 (true)"),
            "std::bitset::set() (C++)": ("Met un bit à 1 ou tous les bits à 1.", "std::bitset<8> b; b.set(0); std::cout << b << std::endl; // 00000001"),
            "std::bitset::reset() (C++)": ("Met un bit à 0 ou tous les bits à 0.", "std::bitset<8> b(\"11111111\"); b.reset(0); std::cout << b << std::endl; // 11111110"),
            "std::bitset::flip() (C++)": ("Inverse un bit ou tous les bits.", "std::bitset<8> b(\"00000001\"); b.flip(0); std::cout << b << std::endl; // 00000000"),
            "std::bitset::to_string() (C++)": ("Convertit un `bitset` en `std::string`.", "std::bitset<4> b(\"1010\"); std::string s = b.to_string(); std::cout << s << std::endl; // 1010"),
            "std::bitset::to_ulong() / to_ullong() (C++)": ("Convertit un `bitset` en `unsigned long` ou `unsigned long long`.", "std::bitset<8> b(\"1010\"); unsigned long ul = b.to_ulong(); std::cout << ul << std::endl; // 10"),
            "`std::vector<bool>` (C++)": ("Spécialisation de `std::vector` pour optimiser le stockage des booléens (chaque booléen peut prendre 1 bit).", "std::vector<bool> vb(10, true);"),
            "reinterpret_cast (C++)": ("Utilisé pour convertir des pointeurs entre types non liés, souvent pour des manipulations binaires bas niveau.", "int x = 0x12345678; char* p = reinterpret_cast<char*>(&x); printf(\"%x\\n\", (unsigned char)p[0]); // 78 (sur little-endian)"),
            "union (C/C++)": ("Permet à plusieurs membres de partager le même espace mémoire, utile pour interpréter des données binaires de différentes manières.", "union Data { int i; float f; char bytes[4]; }; Data d; d.i = 0x40490FDB; printf(\"%f\\n\", d.f); // 3.141593"),
            "Input/output with binary files (C: `fread`/`fwrite`, C++: `ifstream`/`ofstream` with `std::ios::binary`)": ("Lecture/écriture de données binaires brutes depuis/vers des fichiers.", "FILE *fp = fopen(\"file.bin\", \"wb\"); fwrite(buffer, 1, sizeof(buffer), fp); fclose(fp);"),
            "Endian conversion functions (e.g., `htons`, `ntohs` in network programming)": ("Fonctions pour convertir l'ordre des octets entre l'hôte et le réseau (spécifiques aux systèmes/réseau).", "// Nécessitent des headers spécifiques (ex: `<arpa/inet.h>`).")
        },
        "description": "La manipulation binaire en C/C++ est très explicite. Elle se fait via les **opérateurs bit à bit** sur les types entiers (`int`, `char`, etc.), les **littéraux binaires/hexadécimaux**, les **champs de bits** dans les structures. En C++, `std::bitset` (`<bitset>`) et `std::vector<bool>` sont des outils plus abstraits. La lecture/écriture de **fichiers binaires** est gérée au niveau des octets."
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


