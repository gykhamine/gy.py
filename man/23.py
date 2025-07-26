import customtkinter as ctk
import os
import re
import shutil
from tkinter import messagebox, filedialog

# --- Base de Connaissances des Directives PHP (intégrée au script) ---
# Ce dictionnaire contient des informations, des recommandations et des options pour les directives clés.
# C'est une sélection des directives les plus importantes pour la performance et la sécurité.
# Vous pouvez étendre cette liste directement ici.
PHP_INI_DIRECTIVES_INFO = {
    "engine": {
        "description": "Active ou désactive le moteur d'exécution PHP. Si désactivé, les scripts PHP ne seront pas exécutés.",
        "recommendation": "Généralement 'On' pour que PHP fonctionne. 'Off' peut être utilisé temporairement pour désactiver PHP sur un serveur.",
        "security_paths": "S'assurer qu'il est 'Off' sur les serveurs qui ne doivent pas exécuter de PHP (par exemple, des serveurs statiques) pour réduire la surface d'attaque.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "short_open_tag": {
        "description": "Permet ou non la forme raccourcie des balises d'ouverture PHP (<? ?>).",
        "recommendation": "Mettez 'Off'. Utiliser les balises longues (<?php ?>) est recommandé pour une meilleure portabilité et compatibilité.",
        "security_paths": "Évite les ambiguïtés et les problèmes potentiels d'interprétation si d'autres langages (comme XML) utilisent des balises similaires.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "asp_tags": {
        "description": "Permet ou non l'utilisation des balises de style ASP (<% %>).",
        "recommendation": "Mettez 'Off'. C'est une fonctionnalité obsolète qui peut causer des conflits ou être exploitée si mal utilisée.",
        "security_paths": "Supprime une fonctionnalité rarement utilisée et potentiellement risquée.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "precision": {
        "description": "Nombre de décimales affichées pour les nombres à virgule flottante.",
        "recommendation": "La valeur par défaut (14) est généralement suffisante. Ajustez si nécessaire pour des calculs très précis.",
        "security_paths": "Pas directement lié à la sécurité, mais des erreurs de précision peuvent affecter les calculs sensibles (ex: financiers).",
        "options": ["14", "16"],
        "recommended_prod": "14"
    },
    "output_buffering": {
        "description": "Active ou désactive la mise en tampon de sortie pour toutes les requêtes.",
        "recommendation": "Peut être 'On' ou une taille (ex: 4096) pour des raisons de performance. 'Off' par défaut.",
        "security_paths": "N/A",
        "options": ["On", "Off", "4096"],
        "recommended_prod": "Off"
    },
    "zlib.output_compression": {
        "description": "Active la compression de sortie Gzip transparente si le navigateur la supporte.",
        "recommendation": "Mettez 'On' pour réduire la taille des réponses HTTP et améliorer la vitesse de chargement pour les utilisateurs.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "implicit_flush": {
        "description": "Force PHP à vider automatiquement la mémoire tampon après chaque instruction `print` ou `echo`.",
        "recommendation": "Mettez 'Off'. Affecte la performance. La mise en tampon est généralement préférable.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "max_execution_time": {
        "description": "Le temps maximal, en secondes, pendant lequel un script peut s'exécuter.",
        "recommendation": "Augmentez-le pour les opérations longues (importations de données, traitements d'images, etc.). Des valeurs typiques sont 30, 60, 120, 300.",
        "security_paths": "Empêche les scripts malveillants ou défectueux de s'exécuter indéfiniment, consommant des ressources serveur.",
        "options": ["30", "60", "120", "300", "600"],
        "recommended_prod": "30"
    },
    "max_input_time": {
        "description": "Le temps maximal, en secondes, pendant lequel un script peut analyser les données d'entrée (POST/GET).",
        "recommendation": "Similaire à max_execution_time. Définissez-le en fonction de la taille attendue des données d'entrée (ex: uploads de fichiers).",
        "security_paths": "Empêche les attaques par déni de service liées à des entrées très volumineuses qui bloqueraient le serveur.",
        "options": ["60", "120", "300"],
        "recommended_prod": "60"
    },
    "memory_limit": {
        "description": "La quantité maximale de mémoire, en octets, qu'un script est autorisé à consommer.",
        "recommendation": "Augmentez si vos applications ont des erreurs de 'mémoire insuffisante'. Des valeurs typiques sont '128M', '256M', '512M'. Une valeur trop élevée peut masquer des problèmes de code ou faciliter des attaques par déni de service si non contrôlé.",
        "security_paths": "Limiter la mémoire permet de mitiger les attaques par déni de service consommant trop de ressources.",
        "options": ["64M", "128M", "256M", "512M", "1024M", "-1"],
        "recommended_prod": "256M"
    },
    "display_errors": {
        "description": "Contrôle si les erreurs PHP sont affichées dans la sortie HTML.",
        "recommendation": "Pour la **production**, mettez sur 'Off' pour éviter de divulguer des informations sensibles. En **développement**, mettez sur 'On'.",
        "security_paths": "Évite la divulgation d'informations (chemins de fichiers, requêtes SQL) aux attaquants.",
        "options": ["On", "Off", "stderr", "STDOUT"],
        "recommended_prod": "Off"
    },
    "display_startup_errors": {
        "description": "Affiche les erreurs qui surviennent lors du démarrage de PHP.",
        "recommendation": "Mettez sur 'Off' en **production**. Similaire à `display_errors`.",
        "security_paths": "Évite de divulguer des informations sur la configuration du serveur et les extensions PHP au démarrage.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "log_errors": {
        "description": "Indique si les erreurs PHP doivent être écrites dans un fichier journal.",
        "recommendation": "Mettez sur 'On' en **production** pour enregistrer les erreurs et les analyser. Assurez-vous que le fichier `error_log` est défini et accessible en écriture.",
        "security_paths": "Permet de suivre les tentatives d'exploitation et les problèmes sans exposer d'informations.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "error_log": {
        "description": "Chemin du fichier où les erreurs PHP sont enregistrées.",
        "recommendation": "Définissez un chemin absolu vers un fichier journal sécurisé et non accessible via le web. Assurez-vous que le serveur web ou PHP-FPM a les permissions d'écriture.",
        "security_paths": "Centralise les logs d'erreurs pour une surveillance efficace. Garder hors de la racine web est crucial.",
        "options": []
    },
    "report_memleaks": {
        "description": "Indique si les fuites de mémoire détectées par le gestionnaire de mémoire de Zend doivent être affichées ou non.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "Les fuites de mémoire peuvent indiquer des vulnérabilités ou des problèmes de performance, mais ne doivent pas être divulguées publiquement.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "track_errors": {
        "description": "Si activé, le dernier message d'erreur sera stocké dans la variable $php_errormsg.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "Évite la fuite potentielle d'informations d'erreur via la variable globale.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "html_errors": {
        "description": "Active le formatage HTML pour les messages d'erreur.",
        "recommendation": "Mettez 'Off' en production. 'On' en développement pour une meilleure lisibilité dans le navigateur.",
        "security_paths": "N'expose pas le format HTML des erreurs qui pourrait être mal interprété par certains parsers automatiques d'attaquants.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "include_path": {
        "description": "Liste des répertoires où la fonction `require()` ou `include()` va chercher les fichiers.",
        "recommendation": "Définissez des chemins absolus vers vos bibliothèques. Ne laissez pas le répertoire courant ('.') sauf si nécessaire et sécurisé. Évitez d'inclure des répertoires accessibles en écriture par des utilisateurs non fiables.",
        "security_paths": "Un `include_path` mal configuré peut conduire à des attaques d'inclusion de fichiers locaux (LFI) en incluant des fichiers non prévus.",
        "options": []
    },
    "auto_prepend_file": {
        "description": "Spécifie le nom d'un fichier qui est automatiquement inclus avant le script principal.",
        "recommendation": "N'utilisez pas cette directive à moins que vous ne soyez absolument certain de ce que vous faites. Si utilisée, assurez-vous que le fichier est sécurisé et non modifiable par un utilisateur malveillant.",
        "security_paths": "Peut être exploité pour injecter du code arbitraire si le fichier spécifié n'est pas sécurisé.",
        "options": []
    },
    "auto_append_file": {
        "description": "Spécifie le nom d'un fichier qui est automatiquement inclus après le script principal.",
        "recommendation": "Similaire à `auto_prepend_file`, à utiliser avec une extrême prudence.",
        "security_paths": "Peut être exploité pour injecter du code arbitraire si le fichier spécifié n'est pas sécurisé.",
        "options": []
    },
    "default_charset": {
        "description": "Le jeu de caractères par défaut pour les en-têtes Content-Type.",
        "recommendation": "Définissez sur 'UTF-8' pour les applications modernes. Assure une gestion correcte des caractères internationaux.",
        "security_paths": "Un jeu de caractères incorrect peut entraîner des problèmes d'injection XSS si les données ne sont pas correctement interprétées par le navigateur.",
        "options": ["UTF-8", "ISO-8859-1"],
        "recommended_prod": "UTF-8"
    },
    "doc_root": {
        "description": "Le répertoire racine de votre serveur web. Définit l'endroit où PHP cherche les scripts.",
        "recommendation": "Laissez vide si vous utilisez le `DocumentRoot` de votre serveur web (Apache/Nginx). Sinon, définissez-le avec précaution.",
        "security_paths": "Une mauvaise configuration peut exposer des fichiers sensibles en dehors de votre racine web.",
        "options": []
    },
    "user_dir": {
        "description": "Le nom du répertoire de base utilisé pour les répertoires personnels des utilisateurs (ex: ~user/public_html).",
        "recommendation": "Mettez 'Off' si vous n'utilisez pas cette fonctionnalité. Si 'On', assurez-vous que les permissions des répertoires sont strictes.",
        "security_paths": "Peut exposer des fichiers si des utilisateurs non privilégiés peuvent mettre des scripts PHP dans leurs répertoires personnels.",
        "options": ["Off", "public_html"],
        "recommended_prod": "Off"
    },
    "enable_dl": {
        "description": "Permet ou non le chargement dynamique des extensions PHP via la fonction `dl()`.",
        "recommendation": "**Désactivez ('Off') en production.** C'est une fonction dangereuse qui peut permettre l'exécution de code arbitraire.",
        "security_paths": "**CRITIQUE.** La fonction `dl()` est une vulnérabilité majeure si un attaquant peut exécuter du code PHP. Désactivez-la toujours.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "file_uploads": {
        "description": "Permet ou non les téléchargements de fichiers HTTP.",
        "recommendation": "Mettez 'On' si votre application a besoin de télécharger des fichiers. Si 'Off', la fonction `move_uploaded_file()` ne fonctionnera pas.",
        "security_paths": "Si 'On', assurez-vous que tous les téléchargements sont validés, scannés et que les fichiers sont stockés en dehors de la racine web, et que les types MIME sont vérifiés.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "upload_max_filesize": {
        "description": "La taille maximale des fichiers qui peuvent être téléchargés.",
        "recommendation": "Définissez-le en fonction de vos besoins. Doit être inférieur ou égal à `post_max_size`.",
        "security_paths": "Limiter la taille des uploads aide à prévenir les attaques par déni de service (DoS) par upload excessif de fichiers.",
        "options": ["2M", "8M", "16M", "32M", "64M", "128M"],
        "recommended_prod": "32M"
    },
    "post_max_size": {
        "description": "La taille maximale des données POST que PHP acceptera.",
        "recommendation": "Doit être au moins égal ou supérieur à `upload_max_filesize`.",
        "security_paths": "Limiter la taille des requêtes POST pour prévenir les attaques par déni de service.",
        "options": ["8M", "16M", "32M", "64M", "128M"],
        "recommended_prod": "32M"
    },
    "max_file_uploads": {
        "description": "Le nombre maximal de fichiers qui peuvent être téléchargés simultanément.",
        "recommendation": "La valeur par défaut (20) est souvent suffisante. Ajustez si vous avez des formulaires de téléchargement multiples.",
        "security_paths": "Peut aider à mitiger les attaques par déni de service si un attaquant tente de télécharger un très grand nombre de fichiers.",
        "options": ["20", "50", "100"],
        "recommended_prod": "20"
    },
    "allow_url_fopen": {
        "description": "Permet aux fonctions fopen() avec les URL. Utile pour télécharger des fichiers distants.",
        "recommendation": "Mettez sur 'Off' si vous n'avez pas besoin de lire des fichiers distants via des URL. Si 'On', assurez-vous de valider toutes les entrées utilisateur utilisées pour les chemins d'URL afin de prévenir les attaques d'inclusion de fichiers distants (RFI).",
        "security_paths": "Une source majeure de vulnérabilités RFI si non géré correctement. Désactiver réduit la surface d'attaque.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "allow_url_include": {
        "description": "Permet d'inclure des fichiers distants via des URL avec `include()` ou `require()`.",
        "recommendation": "**Doit toujours être 'Off' en production.** L'activer est une faille de sécurité critique permettant les attaques d'inclusion de fichiers distantes (RFI).",
        "security_paths": "**CRITIQUE.** L'activation de ceci ouvre la porte aux attaques RFI, permettant aux attaquants d'exécuter du code arbitraire sur votre serveur.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "default_socket_timeout": {
        "description": "Délai d'attente par défaut (en secondes) pour les flux basés sur les sockets.",
        "recommendation": "La valeur par défaut (60) est généralement acceptable. Ajustez si vous rencontrez des problèmes de timeout avec des services distants.",
        "security_paths": "N/A",
        "options": ["60", "120", "300"],
        "recommended_prod": "60"
    },
    "date.timezone": {
        "description": "Le fuseau horaire par défaut utilisé par toutes les fonctions date/heure.",
        "recommendation": "C'est **essentiel** pour éviter des avertissements et garantir l'exactitude des horodatages. Définissez-le selon votre localisation, par exemple 'Africa/Brazzaville'.",
        "security_paths": "Bien que pas directement une faille de sécurité, des horodatages incorrects peuvent compliquer le débogage et l'analyse forensique des logs.",
        "options": ["UTC", "Europe/Paris", "America/New_York", "Africa/Brazzaville"],
        "recommended_prod": "Africa/Brazzaville"
    },
    "filter.default": {
        "description": "Le filtre par défaut à appliquer à toutes les données GET/POST/COOKIE.",
        "recommendation": "Laissez 'unsafe_raw'. Ne vous fiez jamais à ce filtre pour la sécurité; filtrez et validez toujours les entrées manuellement.",
        "security_paths": "Une mauvaise compréhension de ce filtre peut donner un faux sentiment de sécurité. Ne l'utilisez pas comme mesure de sécurité principale.",
        "options": ["unsafe_raw", "add_slashes", "strip_tags", "full_special_chars", "email", "url", "number_int", "number_float"],
        "recommended_prod": "unsafe_raw"
    },
    "session.save_handler": {
        "description": "Définit le gestionnaire qui est utilisé pour stocker et récupérer les données associées à une session.",
        "recommendation": "Utilisez 'files' par défaut ou 'memcached'/'redis' pour des performances distribuées. Assurez-vous que le répertoire de sauvegarde est sécurisé.",
        "security_paths": "Un gestionnaire de session mal configuré (ex: stockage dans un répertoire accessible publiquement) peut entraîner le détournement de session.",
        "options": ["files", "memcached", "redis", "user"],
        "recommended_prod": "files"
    },
    "session.save_path": {
        "description": "Argument passé au gestionnaire de sauvegarde de session. Pour 'files', c'est le chemin vers le répertoire où les fichiers de session sont stockés.",
        "recommendation": "Définissez un chemin absolu vers un répertoire non accessible via le web (ex: `/var/lib/php/sessions`). Assurez-vous que les permissions sont strictes.",
        "security_paths": "**CRITIQUE.** Un chemin accessible publiquement permettrait le vol ou le détournement de sessions.",
        "options": []
    },
    "session.use_strict_mode": {
        "description": "Si activé, le module de session n'acceptera pas les ID de session non initialisés envoyés par le navigateur.",
        "recommendation": "Mettez '1' (On) en production. Aide à prévenir le détournement de session par fixation de session.",
        "security_paths": "Protection importante contre la fixation de session. Si un attaquant injecte un ID de session, il ne sera pas accepté.",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "session.use_cookies": {
        "description": "Indique si les modules de session utilisent des cookies pour stocker l'ID de session.",
        "recommendation": "Mettez '1' (On). C'est la méthode recommandée pour gérer les sessions.",
        "security_paths": "N/A",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "session.use_only_cookies": {
        "description": "Indique si le module de session doit uniquement utiliser des cookies pour stocker l'ID de session sur le client.",
        "recommendation": "Mettez '1' (On) en production. Empêche la transmission d'ID de session dans les URL, ce qui est une faille de sécurité.",
        "security_paths": "Empêche l'exposition des ID de session dans les URL, qui peuvent être loggées, mises en cache, ou partagées. Prévient le vol de session.",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "session.cookie_lifetime": {
        "description": "Durée de vie du cookie de session, en secondes. '0' signifie jusqu'à la fermeture du navigateur.",
        "recommendation": "'0' pour les sessions basées sur le navigateur. Une valeur plus longue si vous avez des sessions 'rester connecté'.",
        "security_paths": "Une durée de vie trop longue peut augmenter la fenêtre de temps pour le vol de session si le cookie est compromis.",
        "options": ["0", "3600", "86400", "2592000"],
        "recommended_prod": "0"
    },
    "session.cookie_httponly": {
        "description": "Marque le cookie comme 'HttpOnly', empêchant l'accès au cookie via JavaScript.",
        "recommendation": "Mettez '1' (On) en production. Protection cruciale contre les attaques XSS.",
        "security_paths": "**CRITIQUE.** Empêche les scripts malveillants injectés via XSS de voler les cookies de session des utilisateurs.",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "session.cookie_secure": {
        "description": "Marque le cookie comme 'Secure', signifiant qu'il ne doit être envoyé que sur des connexions HTTPS.",
        "recommendation": "Mettez '1' (On) si votre site utilise HTTPS. Si vous utilisez HTTP et HTTPS, cela peut causer des problèmes.",
        "security_paths": "Empêche l'ID de session d'être transmis en clair sur un réseau non chiffré, protégeant contre les attaques 'man-in-the-middle'.",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "session.cookie_samesite": {
        "description": "Définit l'attribut SameSite pour le cookie de session, aidant à prévenir les attaques CSRF.",
        "recommendation": "Mettez 'Lax' ou 'Strict'. 'Lax' est un bon équilibre entre sécurité et fonctionnalité. 'Strict' est plus sécurisé mais peut casser certains workflows.",
        "security_paths": "Protection contre les attaques de falsification de requête inter-sites (CSRF).",
        "options": ["None", "Lax", "Strict"],
        "recommended_prod": "Lax"
    },
    "session.gc_probability": {
        "description": "Définit la probabilité (en pourcentage) que le processus de garbage collection des sessions soit lancé à chaque initialisation de session.",
        "recommendation": "Avec `session.gc_divisor`, une valeur de '1' est souvent suffisante.",
        "security_paths": "Assure le nettoyage régulier des anciennes sessions, réduisant le risque de session détournée si les fichiers ne sont pas supprimés.",
        "options": ["1", "5", "10"],
        "recommended_prod": "1"
    },
    "session.gc_divisor": {
        "description": "Combiné avec `session.gc_probability`, définit la probabilité mathématique du lancement du garbage collector.",
        "recommendation": "Avec `session.gc_probability = 1`, une valeur de '100' ou '1000' est courante. (1/100 ou 1/1000 chance).",
        "security_paths": "Voir `session.gc_probability`.",
        "options": ["100", "1000", "10000"],
        "recommended_prod": "100"
    },
    "session.gc_maxlifetime": {
        "description": "Durée de vie maximale des sessions (en secondes) après l'accès du dernier utilisateur.",
        "recommendation": "Une valeur plus courte (ex: 1440 secondes = 24 minutes) réduit la fenêtre de temps pour le détournement de session. Adaptez-le aux besoins de votre application.",
        "security_paths": "Minimise le risque de détournement de session (session hijacking) en réduisant la durée de vie des sessions inactives.",
        "options": ["1440", "3600", "7200"],
        "recommended_prod": "1440"
    },
    "session.sid_length": {
        "description": "La longueur en caractères de l'ID de session.",
        "recommendation": "La valeur par défaut (26) est généralement suffisante pour la sécurité. Ne la diminuez pas.",
        "security_paths": "Une longueur plus grande rend l'ID de session plus difficile à deviner par force brute.",
        "options": ["26", "32", "48"],
        "recommended_prod": "26"
    },
    "session.sid_bits_per_character": {
        "description": "Le nombre de bits par caractère pour l'ID de session.",
        "recommendation": "La valeur par défaut (5 ou 6) est appropriée. Plus élevé augmente la complexité de l'ID.",
        "security_paths": "Augmente l'entropie de l'ID de session, rendant le devinette plus difficile.",
        "options": ["4", "5", "6"],
        "recommended_prod": "5"
    },
    "session.hash_function": {
        "description": "La fonction de hachage (algorithme) à utiliser pour générer les ID de session.",
        "recommendation": "Utilisez 'sha256' ou 'sha512' si disponible. Les valeurs numériques (0=MD5, 1=SHA1) sont obsolètes.",
        "security_paths": "Utiliser une fonction de hachage forte rend l'ID de session plus difficile à deviner.",
        "options": ["0", "1", "sha256", "sha512"],
        "recommended_prod": "sha256"
    },
    "session.hash_bits_per_character": {
        "description": "Le nombre de bits par caractère pour les ID de session générés par le hachage.",
        "recommendation": "6 (0-9, a-z, A-Z, \"-\", \",\") est une bonne valeur.",
        "security_paths": "Augmente l'entropie de l'ID de session.",
        "options": ["4", "5", "6"],
        "recommended_prod": "6"
    },
    "disable_functions": {
        "description": "Liste de fonctions à désactiver. Par exemple, les fonctions d'exécution de commandes système.",
        "recommendation": "Désactivez les fonctions potentiellement dangereuses si votre application n'en a pas besoin, comme `exec`, `shell_exec`, `system`, `passthru`, `proc_open`, `popen`, `symlink`, `link`, `apache_child_terminate`, `posix_kill`, `posix_mkfifo`, `posix_setpgid`, `posix_setsid`, `posix_setuid`, `posix_setegid`, `posix_seteuid`, `pcntl_exec`, `dl`, `putenv`, `ini_alter`, `ini_restore`, `ini_set`, `chown`, `chgrp`, `chmod`, `socket_create_listen`, `socket_accept`, `socket_listen`, `socket_bind`, `socket_connect`, `fsockopen`, `pfsockopen`, `stream_socket_server`, `stream_socket_client`, `stream_socket_accept`, `pfsockopen`.",
        "security_paths": "Réduit considérablement la capacité d'un attaquant à exécuter des commandes système ou à manipuler le système de fichiers si une vulnérabilité est trouvée dans votre application.",
        "options": []
    },
    "disable_classes": {
        "description": "Liste des classes à désactiver.",
        "recommendation": "Peut être utilisé pour désactiver des classes dangereuses si nécessaire, mais moins couramment utilisé que `disable_functions`.",
        "security_paths": "Similaire à `disable_functions` mais pour les classes.",
        "options": []
    },
    "open_basedir": {
        "description": "Limite tous les accès de fichiers par PHP à l'arborescence spécifiée.",
        "recommendation": "Définissez-le sur le répertoire racine de votre application PHP (ex: `/var/www/html/monapp`). Cela empêche PHP d'accéder à des fichiers en dehors de ce répertoire.",
        "security_paths": "Une protection cruciale contre les attaques de traversée de répertoire (directory traversal) et l'inclusion de fichiers locaux (LFI).",
        "options": []
    },
    "expose_php": {
        "description": "Détermine si PHP doit ajouter un en-tête HTTP 'X-Powered-By: PHP/version' dans la réponse.",
        "recommendation": "Mettez sur 'Off' en **production** pour masquer la version de PHP. Cela réduit les informations disponibles pour un attaquant qui chercherait des vulnérabilités spécifiques à une version.",
        "security_paths": "Obscurcissement de l'information (security by obscurity), rendant plus difficile pour les attaquants de cibler des vulnérabilités connues dans des versions spécifiques de PHP.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "mail.add_x_header": {
        "description": "Ajoute un en-tête X-PHP-Originating-Script au mail envoyé.",
        "recommendation": "Mettez 'Off' en production pour ne pas exposer le nom du script PHP d'origine.",
        "security_paths": "Empêche la divulgation d'informations sur l'emplacement du script PHP qui a envoyé l'e-mail, ce qui pourrait aider un attaquant.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "mail.log": {
        "description": "Enregistre tous les appels de la fonction mail() dans un fichier journal.",
        "recommendation": "Mettez sur le chemin d'un fichier journal pour surveiller l'envoi d'e-mails par votre application. Utile pour détecter le spam ou l'abus de fonction mail.",
        "security_paths": "Permet de tracer l'envoi d'e-mails, utile pour identifier si un script est utilisé à des fins malveillantes (envoi de spam).",
        "options": []
    },
    "opcache.enable": {
        "description": "Active/désactive le cache d'opcode PHP.",
        "recommendation": "Mettez sur '1' (On) en **production** pour des performances significativement améliorées.",
        "security_paths": "Pas directement lié à la sécurité, mais une mauvaise configuration (ex: `validate_timestamps=0` en dev) peut laisser du code obsolète vulnérable.",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "opcache.enable_cli": {
        "description": "Active/désactive le cache d'opcode PHP pour la version CLI.",
        "recommendation": "Mettez sur '0' (Off) à moins d'avoir des scripts CLI de longue durée bénéficiant du cache.",
        "security_paths": "Un cache d'opcode pour CLI est rarement utile et peut potentiellement poser des problèmes si des scripts sont modifiés fréquemment.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "opcache.memory_consumption": {
        "description": "La taille de la mémoire partagée allouée pour le stockage des opcodes PHP en Mo.",
        "recommendation": "Définissez une valeur suffisante pour votre application (ex: 128, 256, 512).",
        "security_paths": "Trop bas peut entraîner des exclusions de cache, trop haut peut consommer des ressources inutiles.",
        "options": ["64", "128", "256", "512"],
        "recommended_prod": "256"
    },
    "opcache.interned_strings_buffer": {
        "description": "La quantité de mémoire pour les chaînes de caractères interpolées (en Mo).",
        "recommendation": "Augmentez si vous utilisez beaucoup de chaînes uniques (ex: ORM).",
        "security_paths": "N/A",
        "options": ["4", "8", "16"],
        "recommended_prod": "8"
    },
    "opcache.max_accelerated_files": {
        "description": "Le nombre maximal de scripts qui peuvent être stockés dans le cache d'opcode.",
        "recommendation": "Choisissez une valeur supérieure au nombre total de fichiers PHP de votre application.",
        "security_paths": "N/A",
        "options": ["1000", "5000", "10000", "20000"],
        "recommended_prod": "10000"
    },
    "opcache.revalidate_freq": {
        "description": "Fréquence de vérification de l'horodatage des scripts pour les modifications (en secondes).",
        "recommendation": "En **production**, une valeur plus élevée (ex: 60 ou 0) réduit la surcharge. En **développement**, mettez à 0 pour que les changements soient immédiatement pris en compte.",
        "security_paths": "Une valeur trop élevée en développement peut causer l'exécution de code obsolète. En production, 0 peut être utilisé si les déploiements gèrent la réinitialisation de l'opcache.",
        "options": ["0", "1", "5", "30", "60"],
        "recommended_prod": "60"
    },
    "opcache.validate_timestamps": {
        "description": "Si activé, OPcache vérifiera si le fichier source a été modifié après sa mise en cache.",
        "recommendation": "Mettez '1' (On) en développement. Mettez '0' (Off) en production pour une performance maximale (nécessite de vider le cache manuellement après chaque déploiement).",
        "security_paths": "Si '0' en production, assurez-vous de vider le cache OPcache après chaque déploiement pour éviter l'exécution de code obsolète/vulnérable.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "phar.readonly": {
        "description": "Empêche la modification des archives PHAR sur le serveur.",
        "recommendation": "Mettez 'On' en production pour la sécurité. Empêche la modification accidentelle ou malveillante des PHAR.",
        "security_paths": "Empêche un attaquant de modifier le contenu des archives PHAR sur le serveur, ce qui pourrait mener à l'exécution de code malveillant.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "realpath_cache_size": {
        "description": "La taille du cache de chemin réel de PHP (en octets).",
        "recommendation": "Augmentez si vous avez des applications avec beaucoup de fichiers pour de meilleures performances (ex: 2M, 4M).",
        "security_paths": "N/A",
        "options": ["16K", "32K", "1M", "2M", "4M"],
        "recommended_prod": "2M"
    },
    "realpath_cache_ttl": {
        "description": "Durée de vie du cache de chemin réel (en secondes).",
        "recommendation": "La valeur par défaut (120) est souvent suffisante. Réduisez en développement si les chemins changent souvent.",
        "security_paths": "N/A",
        "options": ["60", "120", "300"],
        "recommended_prod": "120"
    },
    "request_order": {
        "description": "L'ordre dans lequel les variables EGPCS (Environment, GET, POST, Cookie, Server) sont parsées dans les tableaux _REQUEST.",
        "recommendation": "Généralement 'GP' (GET puis POST). Évitez 'C' (Cookie) et 'E' (Environment) pour des raisons de sécurité.",
        "security_paths": "Un ordre incorrect peut entraîner des surcharges de variables si un attaquant peut manipuler plusieurs sources d'entrée.",
        "options": ["GP", "GPC", "PG", "PGC"],
        "recommended_prod": "GP"
    },
    "variables_order": {
        "description": "L'ordre dans lequel les variables EGPCS sont mises dans l'environnement global (e.g. $_ENV, $_GET, $_POST, $_COOKIE, $_SERVER).",
        "recommendation": "Généralement 'GPCS'. Évitez 'E' (Environment) pour des raisons de sécurité.",
        "security_paths": "Similaire à `request_order`, une mauvaise configuration peut entraîner des problèmes de sécurité si les variables sont écrasées.",
        "options": ["GPCS", "EGPCS"],
        "recommended_prod": "GPCS"
    },
    "max_input_vars": {
        "description": "Limite le nombre de variables de requête qu'un script peut recevoir (GET/POST/COOKIES).",
        "recommendation": "Augmentez si vous avez de gros formulaires (ex: 1000, 3000, 5000). Aide à prévenir les attaques par déni de service.",
        "security_paths": "Empêche les attaques par déni de service où un attaquant envoie un nombre excessif de variables pour épuiser les ressources du serveur.",
        "options": ["1000", "3000", "5000"],
        "recommended_prod": "1000"
    },
    "disable_display_errors_on_startup": {
        "description": "Désactive l'affichage des erreurs au démarrage de PHP.",
        "recommendation": "Mettez 'On' en production. Empêche la fuite d'informations sensibles au démarrage.",
        "security_paths": "Empêche les messages d'erreur de démarrage de PHP d'être affichés, ce qui pourrait contenir des informations sensibles sur le système.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "error_reporting": {
        "description": "Définit le niveau de rapport d'erreurs PHP.",
        "recommendation": "En **production**, utilisez `E_ALL & ~E_DEPRECATED & ~E_STRICT & ~E_NOTICE`. En **développement**, utilisez `E_ALL`.",
        "security_paths": "Un rapport d'erreurs trop verbeux en production peut divulguer des informations utiles aux attaquants.",
        "options": ["E_ALL", "E_ALL & ~E_NOTICE & ~E_DEPRECATED", "E_ERROR | E_WARNING | E_PARSE"],
        "recommended_prod": "E_ALL & ~E_DEPRECATED & ~E_STRICT & ~E_NOTICE"
    },
    "arg_separator.output": {
        "description": "Séparateur utilisé pour séparer les arguments dans les URL générées par PHP.",
        "recommendation": "Utilisez '&amp;' pour une conformité HTML stricte, ou '&' pour la simplicité. 'amp;' est un encodage HTML pour '&'.",
        "security_paths": "N/A",
        "options": ["&", "&amp;"],
        "recommended_prod": "&amp;"
    },
    "arg_separator.input": {
        "description": "Liste de séparateurs que PHP considèrera comme des séparateurs d'arguments pour les URL d'entrée.",
        "recommendation": "Laissez '&' par défaut. ';&' permet d'utiliser les deux.",
        "security_paths": "N/A",
        "options": ["&", ";&"],
        "recommended_prod": "&"
    },
    "default_mimetype": {
        "description": "Le type MIME par défaut pour les en-têtes Content-Type.",
        "recommendation": "Utilisez 'text/html' pour les applications web standard.",
        "security_paths": "Une mauvaise configuration peut entraîner des problèmes de XSS si le navigateur interprète mal le contenu.",
        "options": ["text/html", "application/json"],
        "recommended_prod": "text/html"
    },
    "doc_files_path": {
        "description": "Chemin vers le répertoire des fichiers de documentation PHP.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "from": {
        "description": "L'adresse email utilisée comme 'From' pour les mails envoyés via `mail()` sans l'en-tête 'From' explicitement défini.",
        "recommendation": "Définissez une adresse email valide et pertinente (ex: noreply@votre-domaine.com).",
        "security_paths": "Empêche l'envoi de mails avec un champ 'From' vide ou générique, ce qui peut affecter la délivrabilité et la confiance.",
        "options": []
    },
    "max_input_nesting_level": {
        "description": "Profondeur maximale des tableaux imbriqués et des variables superglobales.",
        "recommendation": "La valeur par défaut (64) est généralement suffisante. Augmentez si vous traitez des données JSON ou XML très imbriquées.",
        "security_paths": "Empêche les attaques par déni de service où un attaquant envoie des données trop imbriquées pour épuiser les ressources du serveur.",
        "options": ["64", "128", "256"],
        "recommended_prod": "64"
    },
    "url_rewriter.tags": {
        "description": "Spécifie les balises HTML pour lesquelles PHP réécrit les URL pour inclure l'ID de session.",
        "recommendation": "Laissez vide ou commentez si `session.use_only_cookies` est activé. La réécriture d'URL est une mauvaise pratique de sécurité.",
        "security_paths": "La réécriture d'URL expose les ID de session dans les URL, les rendant vulnérables au vol, à la journalisation et au partage.",
        "options": []
    },
    "assert.active": {
        "description": "Active ou désactive la fonction `assert()`.",
        "recommendation": "Mettez 'Off' en production. Les assertions ne doivent pas être utilisées pour valider les entrées utilisateur ou pour le code de production.",
        "security_paths": "Si 'On', une assertion mal placée ou une expression contrôlée par l'utilisateur peut entraîner l'exécution de code arbitraire.",
        "options": ["1", "0"],
        "recommended_prod": "0"
    },
    "assert.callback": {
        "description": "Appelle une fonction de rappel en cas d'échec d'une assertion.",
        "recommendation": "Laissez vide en production si `assert.active` est 'Off'.",
        "security_paths": "Voir `assert.active`.",
        "options": []
    },
    "assert.exception": {
        "description": "Si activé, les assertions échouées généreront une exception au lieu d'un avertissement.",
        "recommendation": "Mettez 'Off' en production. Si 'On', assurez-vous de bien gérer les exceptions.",
        "security_paths": "Voir `assert.active`.",
        "options": ["1", "0"],
        "recommended_prod": "0"
    },
    "max_input_max_input_vars": {
        "description": "Alias ou erreur de frappe pour `max_input_vars` dans certaines configurations.",
        "recommendation": "Vérifiez `max_input_vars`.",
        "security_paths": "N/A",
        "options": []
    },
    "user_ini.filename": {
        "description": "Le nom du fichier .user.ini que PHP cherchera dans chaque répertoire.",
        "recommendation": "Laissez le nom par défaut. Assurez-vous que ces fichiers ne sont pas accessibles via le web.",
        "security_paths": "Les fichiers `.user.ini` peuvent potentiellement modifier le comportement de PHP pour un répertoire donné. Assurez-vous qu'ils sont utilisés avec prudence.",
        "options": [".user.ini"],
        "recommended_prod": ".user.ini"
    },
    "user_ini.cache_ttl": {
        "description": "La durée de vie du cache du fichier .user.ini (en secondes).",
        "recommendation": "La valeur par défaut (300) est raisonnable. Augmentez en production pour réduire les I/O si les .user.ini ne changent pas souvent.",
        "security_paths": "N/A",
        "options": ["300", "600"],
        "recommended_prod": "300"
    },
    "phar.require_hash": {
        "description": "Exige que les archives PHAR aient une signature valide pour être exécutées.",
        "recommendation": "Mettez 'On' en production. Assure l'intégrité des archives PHAR.",
        "security_paths": "Vérifie l'intégrité des archives PHAR, empêchant l'exécution de PHAR corrompus ou modifiés de manière malveillante.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "pcre.jit": {
        "description": "Active ou désactive la compilation juste-à-temps (JIT) pour PCRE (expressions régulières).",
        "recommendation": "Généralement 'On' pour de meilleures performances des expressions régulières.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "pdo_mysql.default_socket": {
        "description": "Chemin par défaut du socket MySQL pour PDO.",
        "recommendation": "Définissez si vous utilisez un socket local pour la connexion à MySQL.",
        "security_paths": "N/A",
        "options": []
    },
    "mysqli.default_socket": {
        "description": "Chemin par défaut du socket MySQL pour MySQLi.",
        "recommendation": "Définissez si vous utilisez un socket local pour la connexion à MySQL.",
        "security_paths": "N/A",
        "options": []
    },
    "mysqlnd.collect_statistics": {
        "description": "Collecte des statistiques sur l'utilisation de MySQLND (extension native MySQL Driver).",
        "recommendation": "Mettez 'Off' en production pour une légère amélioration des performances.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "mysqlnd.collect_memory_statistics": {
        "description": "Collecte des statistiques sur la mémoire utilisée par MySQLND.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "curl.cainfo": {
        "description": "Le chemin d'accès au fichier CA Bundle pour la vérification SSL/TLS avec cURL.",
        "recommendation": "Assurez-vous que ce chemin est correct et que le fichier est à jour pour la validation des certificats SSL.",
        "security_paths": "Crucial pour la sécurité des connexions HTTPS sortantes. Un CA Bundle manquant ou obsolète peut entraîner des avertissements ou des failles de sécurité (attaques MITM).",
        "options": []
    },
    "opcache.blacklist_filename": {
        "description": "Chemin vers un fichier contenant des noms de fichiers (un par ligne) à ne pas mettre en cache par OPcache.",
        "recommendation": "Utilisez ceci si vous avez des fichiers PHP qui ne doivent jamais être mis en cache (ex: fichiers de configuration sensibles dynamiques, ou pour le débogage).",
        "security_paths": "Peut aider à garantir que certains fichiers sensibles ou fréquemment modifiés ne restent pas dans le cache, évitant ainsi l'exécution de code obsolète.",
        "options": []
    },
    "xdebug.remote_enable": {
        "description": "Active ou désactive le débogueur distant Xdebug.",
        "recommendation": "Mettez 'Off' en production. **Ne doit être activé qu'en développement.**",
        "security_paths": "**CRITIQUE.** L'activation de Xdebug en production expose un port et peut permettre à un attaquant de prendre le contrôle de l'exécution du code.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "xdebug.remote_port": {
        "description": "Le port sur lequel Xdebug écoute les connexions.",
        "recommendation": "La valeur par défaut (9003) est courante. Ne laissez pas ouvert en production.",
        "security_paths": "Voir `xdebug.remote_enable`.",
        "options": ["9000", "9003"],
        "recommended_prod": "9003"
    },
    "xdebug.remote_autostart": {
        "description": "Démarre automatiquement une session de débogage lorsque PHP est exécuté.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "Voir `xdebug.remote_enable`.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "max_input_max_input_time": {
        "description": "Alias ou erreur de frappe pour `max_input_time` dans certaines configurations.",
        "recommendation": "Vérifiez `max_input_time`.",
        "security_paths": "N/A",
        "options": []
    },
    "date.default_latitude": {
        "description": "Latitude par défaut utilisée par les fonctions GPS de date/heure.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "date.default_longitude": {
        "description": "Longitude par défaut utilisée par les fonctions GPS de date/heure.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "date.sunrise_zenith": {
        "description": "Zénith utilisé pour le calcul du lever du soleil.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "date.sunset_zenith": {
        "description": "Zénith utilisé pour le calcul du coucher du soleil.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "filter.default_options": {
        "description": "Les options par défaut à passer au filtre par défaut.",
        "recommendation": "Laissez vide. Filtrez toujours les entrées manuellement.",
        "security_paths": "N/A",
        "options": []
    },
    "iconv.input_encoding": {
        "description": "L'encodage de caractères par défaut pour les entrées iconv.",
        "recommendation": "Définissez sur 'UTF-8' pour les applications modernes.",
        "security_paths": "N/A",
        "options": ["UTF-8", "ISO-8859-1"],
        "recommended_prod": "UTF-8"
    },
    "iconv.internal_encoding": {
        "description": "L'encodage de caractères interne pour iconv.",
        "recommendation": "Définissez sur 'UTF-8' pour les applications modernes.",
        "security_paths": "N/A",
        "options": ["UTF-8", "ISO-8859-1"],
        "recommended_prod": "UTF-8"
    },
    "iconv.output_encoding": {
        "description": "L'encodage de caractères par défaut pour les sorties iconv.",
        "recommendation": "Définissez sur 'UTF-8' pour les applications modernes.",
        "security_paths": "N/A",
        "options": ["UTF-8", "ISO-8859-1"],
        "recommended_prod": "UTF-8"
    },
    "mbstring.language": {
        "description": "Langue par défaut pour les fonctions mbstring.",
        "recommendation": "Définissez sur 'Neutral' ou la langue de votre application.",
        "security_paths": "N/A",
        "options": ["Neutral", "English"],
        "recommended_prod": "Neutral"
    },
    "mbstring.internal_encoding": {
        "description": "Encodage de caractères interne pour mbstring.",
        "recommendation": "Définissez sur 'UTF-8'.",
        "security_paths": "N/A",
        "options": ["UTF-8", "ISO-8859-1"],
        "recommended_prod": "UTF-8"
    },
    "mbstring.http_output": {
        "description": "Encodage de caractères HTTP pour la sortie mbstring.",
        "recommendation": "Définissez sur 'UTF-8'.",
        "security_paths": "N/A",
        "options": ["UTF-8", "pass"],
        "recommended_prod": "UTF-8"
    },
    "mbstring.http_input": {
        "description": "Encodage de caractères HTTP pour l'entrée mbstring.",
        "recommendation": "Définissez sur 'pass' (laissez PHP détecter) ou 'UTF-8'.",
        "security_paths": "N/A",
        "options": ["pass", "UTF-8"],
        "recommended_prod": "pass"
    },
    "mbstring.encoding_translation": {
        "description": "Active la traduction automatique de l'encodage des caractères.",
        "recommendation": "Mettez 'Off'. La gestion manuelle est plus fiable et sécurisée.",
        "security_paths": "Une traduction automatique mal gérée peut introduire des vulnérabilités par confusion d'encodage.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "mbstring.func_overload": {
        "description": "Surcharge les fonctions de chaîne de caractères PHP avec des fonctions mbstring.",
        "recommendation": "**Mettez '0' (Off).** Cette fonctionnalité est déconseillée car elle peut causer des comportements inattendus.",
        "security_paths": "Peut introduire des vulnérabilités subtiles si les fonctions de chaîne de caractères sont utilisées avec des encodages multi-octets non prévus.",
        "options": ["0", "1", "2", "4", "5", "6", "7"],
        "recommended_prod": "0"
    },
    "sql.safe_mode": {
        "description": "Active le mode sécurisé SQL (déprécié et retiré en PHP 5.4+).",
        "recommendation": "**Ne comptez pas sur ce mode.** Il est obsolète. Utilisez les prepared statements et la validation d'entrée.",
        "security_paths": "Si votre version de PHP est trop ancienne pour le retirer, sachez que ce n'est pas une protection suffisante contre l'injection SQL.",
        "options": ["On", "Off"],
        "recommended_prod": "Off" # Ou retirer si version PHP > 5.4
    },
    "mysqli.max_links": {
        "description": "Nombre maximum de liens persistants MySQLi par processus PHP.",
        "recommendation": "-1 pour illimité, ou une valeur raisonnable. Attention aux abus de ressources.",
        "security_paths": "Un nombre trop élevé peut être exploité pour des attaques par épuisement de ressources.",
        "options": ["-1", "10", "20"],
        "recommended_prod": "-1"
    },
    "pdo_mysql.make_emulated": {
        "description": "Active ou désactive l'émulation des requêtes préparées pour PDO_MySQL.",
        "recommendation": "Mettez 'Off' ou 'false' en production. L'émulation peut exposer aux injections SQL si les entrées ne sont pas correctement échappées.",
        "security_paths": "**CRITIQUE.** L'émulation des requêtes préparées peut rendre les applications vulnérables aux injections SQL si les données ne sont pas correctement bindées (lié au fait que la validation des données se fait côté client PHP au lieu de côté serveur MySQL).",
        "options": ["On", "Off", "true", "false"],
        "recommended_prod": "Off"
    },
    "sys_temp_dir": {
        "description": "Répertoire utilisé pour les fichiers temporaires du système PHP.",
        "recommendation": "Définissez un chemin explicite vers un répertoire temporaire sécurisé avec des permissions strictes (ex: `/tmp` ou `/var/tmp`).",
        "security_paths": "Un répertoire temporaire non sécurisé peut être un point d'entrée pour des attaques si des fichiers malveillants y sont stockés et exécutés.",
        "options": []
    },
    "cli.pager": {
        "description": "Programme utilisé pour paginer la sortie CLI de PHP (ex: less, more).",
        "recommendation": "N/A (principalement pour le confort de l'utilisateur CLI).",
        "security_paths": "N/A",
        "options": []
    },
    "cli.prompt": {
        "description": "Chaîne de caractères utilisée comme invite de commande pour PHP CLI.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    }
}


class PHPIniEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Éditeur de Configuration PHP.ini")
        self.geometry("1000x800")

        self.php_ini_path = ""
        self.original_config = {}
        self.current_config = {}
        self.widgets = {} # Pour stocker les widgets associés à chaque directive
        # La base de connaissances est directement utilisée
        self.php_ini_directives_info = PHP_INI_DIRECTIVES_INFO

        self.create_widgets()

    def create_widgets(self):
        # Frame pour la sélection du fichier
        file_frame = ctk.CTkFrame(self)
        file_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(file_frame, text="Chemin du Fichier php.ini:").pack(side="left", padx=5)
        self.php_ini_entry = ctk.CTkEntry(file_frame, width=400)
        self.php_ini_entry.pack(side="left", fill="x", expand=True, padx=5)
        # Suggestion de chemin basé sur un système courant (Ubuntu/Debian PHP 8.2 Apache)
        self.php_ini_entry.insert(0, "/etc/php/8.2/apache2/php.ini") 

        browse_button = ctk.CTkButton(file_frame, text="Parcourir", command=self.browse_php_ini)
        browse_button.pack(side="left", padx=5)

        load_button = ctk.CTkButton(file_frame, text="Charger", command=self.load_php_ini)
        load_button.pack(side="left", padx=5)

        # Frame pour les directives (utilisable pour le défilement)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=950, height=600)
        self.scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Boutons d'action
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(pady=10, padx=10, fill="x")

        save_button = ctk.CTkButton(action_frame, text="Appliquer les Changements", command=self.apply_changes)
        save_button.pack(side="right", padx=5)

        reset_button = ctk.CTkButton(action_frame, text="Réinitialiser (depuis le fichier original)", command=self.reset_to_original)
        reset_button.pack(side="right", padx=5)

    def browse_php_ini(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionnez votre fichier php.ini",
            filetypes=[("PHP Ini Files", "php.ini"), ("All Files", "*.*")]
        )
        if file_path:
            self.php_ini_entry.delete(0, ctk.END)
            self.php_ini_entry.insert(0, file_path)

    def load_php_ini(self):
        self.php_ini_path = self.php_ini_entry.get()
        if not os.path.exists(self.php_ini_path):
            messagebox.showerror("Erreur", f"Le fichier '{self.php_ini_path}' n'existe pas.")
            return

        self.original_config = {}
        self.current_config = {}
        try:
            with open(self.php_ini_path, 'r') as f:
                for line_num, line in enumerate(f):
                    # Ignorer les lignes vides et les commentaires complets
                    if not line.strip() or line.strip().startswith(';'):
                        # Stocker les commentaires complets ou lignes vides comme "raw" pour les conserver
                        self.original_config[f"__RAW_LINE_{line_num}__"] = {"line_content": line, "type": "raw"}
                        self.current_config[f"__RAW_LINE_{line_num}__"] = {"line_content": line, "type": "raw"}
                        continue

                    # Regex pour capturer le préfixe (commenté ou non), la directive et la valeur
                    match = re.match(r'^\s*(;?\s*)([a-zA-Z0-9._-]+)\s*=\s*(.*)', line)
                    if match:
                        prefix = match.group(1)
                        directive = match.group(2).strip()
                        value = match.group(3).strip()

                        is_commented = prefix.strip().startswith(';')

                        self.original_config[directive] = {"value": value, "commented": is_commented, "original_line": line, "line_num": line_num}
                        self.current_config[directive] = {"value": value, "commented": is_commented, "original_line": line, "line_num": line_num}
                    else:
                        # Stocker les lignes non reconnues ou de section comme "raw" pour les conserver
                        self.original_config[f"__RAW_LINE_{line_num}__"] = {"line_content": line, "type": "raw"}
                        self.current_config[f"__RAW_LINE_{line_num}__"] = {"line_content": line, "type": "raw"}

            self.display_directives()
            messagebox.showinfo("Chargement Réussi", "Fichier php.ini chargé avec succès.")

        except Exception as e:
            messagebox.showerror("Erreur de Lecture", f"Impossible de lire le fichier php.ini : {e}\n"
                                                     "Assurez-vous que le script a les permissions de lecture.")

    def display_directives(self):
        # Nettoyer les widgets existants
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.widgets = {}

        row = 0
        # Afficher d'abord les directives que nous reconnaissons
        for directive_name, info in self.php_ini_directives_info.items():
            current_value_info = self.current_config.get(directive_name, {"value": "Non trouvé", "commented": True, "original_line": ""})
            current_value = current_value_info["value"]
            is_commented = current_value_info["commented"]

            # Frame pour chaque directive
            directive_frame = ctk.CTkFrame(self.scroll_frame)
            directive_frame.grid(row=row, column=0, columnspan=3, pady=5, padx=5, sticky="ew")
            row += 1

            # Nom de la directive
            ctk.CTkLabel(directive_frame, text=f"**{directive_name}**", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)

            # Valeur actuelle
            ctk.CTkLabel(directive_frame, text=f"Valeur actuelle: {current_value} ({'Commentée' if is_commented else 'Active'})").grid(row=1, column=0, sticky="w", padx=5, pady=2)

            # Description
            ctk.CTkLabel(directive_frame, text=f"Description: {info['description']}", wraplength=800, justify="left").grid(row=2, column=0, sticky="w", padx=5, pady=2)

            # Recommandation
            rec_text = f"**Recommandation:** {info['recommendation']}"
            rec_color = "orange"
            # Logique de coloration pour "recommandé"
            if info.get('recommended_prod') is not None:
                # Normaliser les valeurs pour la comparaison (ex: On/off vs 1/0)
                norm_current = str(current_value).lower().replace('on', '1').replace('off', '0').replace('true', '1').replace('false', '0')
                norm_rec = str(info['recommended_prod']).lower().replace('on', '1').replace('off', '0').replace('true', '1').replace('false', '0')

                if norm_current == norm_rec and not is_commented:
                    rec_color = "green"
                elif norm_rec == '0' and is_commented: # Si la recommandation est "Off" et qu'elle est commentée, c'est aussi bon
                    rec_color = "green"

            ctk.CTkLabel(directive_frame, text=rec_text, wraplength=800, justify="left", text_color=rec_color).grid(row=3, column=0, sticky="w", padx=5, pady=2)

            # Chemin de sécurité
            ctk.CTkLabel(directive_frame, text=f"**Sécurité:** {info['security_paths']}", wraplength=800, justify="left").grid(row=4, column=0, sticky="w", padx=5, pady=2)

            # Widget de modification
            edit_frame = ctk.CTkFrame(directive_frame)
            edit_frame.grid(row=0, column=1, rowspan=5, padx=10, sticky="nswe")
            edit_frame.grid_columnconfigure(0, weight=1) # Permet à l'entrée de s'étendre

            # Cases à cocher pour commenter/décommenter
            comment_var = ctk.BooleanVar(value=is_commented)
            comment_checkbox = ctk.CTkCheckBox(edit_frame, text="Commenter/Désactiver", variable=comment_var, command=lambda d=directive_name, cv=comment_var: self.toggle_comment(d, cv))
            comment_checkbox.grid(row=0, column=0, pady=5, sticky="w")
            self.widgets[f"comment_{directive_name}"] = comment_var

            if info["options"]:
                # Menu déroulant pour les options prédéfinies
                selected_option = ctk.StringVar(value=current_value if current_value in info["options"] else (info.get('recommended_prod', info["options"][0]) if info["options"] else ""))
                option_menu = ctk.CTkOptionMenu(edit_frame, values=[str(x) for x in info["options"]], variable=selected_option, command=lambda value, d=directive_name: self.update_directive_value(d, value))
                option_menu.grid(row=1, column=0, pady=5, sticky="ew")
                self.widgets[f"value_{directive_name}"] = selected_option
            else:
                # Champ de texte libre pour les valeurs non prédéfinies
                entry_value = ctk.StringVar(value=current_value)
                entry = ctk.CTkEntry(edit_frame, textvariable=entry_value)
                entry.grid(row=1, column=0, pady=5, sticky="ew")
                # Utiliser lambda pour capturer la directive_name et entry_value correctement
                entry_value.trace_add("write", lambda name, index, mode, d=directive_name, ev=entry_value: self.update_directive_value(d, ev.get()))
                self.widgets[f"value_{directive_name}"] = entry_value

            # Bouton "Appliquer Recommandé"
            if info.get('recommended_prod') is not None:
                rec_button = ctk.CTkButton(edit_frame, text=f"Appliquer Recommandé ({info['recommended_prod']})", command=lambda d=directive_name, val=info['recommended_prod']: self.apply_recommended(d, val))
                rec_button.grid(row=2, column=0, pady=5, sticky="ew")

            # Séparateur visuel
            ctk.CTkFrame(self.scroll_frame, height=2, fg_color="gray").grid(row=row, column=0, columnspan=3, sticky="ew", pady=5)
            row += 1

        # Ajouter les directives non reconnues mais présentes dans le fichier
        self.add_unrecognized_directives(row)


    def add_unrecognized_directives(self, start_row):
        row = start_row
        recognized_directives = set(self.php_ini_directives_info.keys())
        unrecognized_count = 0

        # Récupérer les clés dans l'ordre de leur apparition dans le fichier original
        # Cela demande de reconstruire l'ordre si on a mélangé des directives et des RAW_LINE
        ordered_keys_from_original = sorted([k for k, v in self.original_config.items() if "line_num" in v], key=lambda k: self.original_config[k]["line_num"])
        
        # Ajouter les lignes "raw" à l'ordre, pour préserver la structure.
        raw_lines_info = []
        for k, v in self.original_config.items():
            if "type" in v and v["type"] == "raw":
                raw_lines_info.append((k, v["line_content"], v["line_num"]))
        
        # Sortir les clés non reconnues qui ne sont PAS des lignes brutes
        unrecognized_directive_names = []
        for k in ordered_keys_from_original:
            if not k.startswith("__RAW_LINE__") and k not in recognized_directives:
                unrecognized_directive_names.append(k)

        # Afficher les directives non reconnues
        for directive_name in unrecognized_directive_names:
            unrecognized_count += 1
            info = self.current_config.get(directive_name, {"value": "Non trouvé", "commented": True})
            current_value = info["value"]
            is_commented = info["commented"]

            directive_frame = ctk.CTkFrame(self.scroll_frame)
            directive_frame.grid(row=row, column=0, columnspan=3, pady=5, padx=5, sticky="ew")
            row += 1

            ctk.CTkLabel(directive_frame, text=f"**{directive_name} (Non Reconnu)**", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
            ctk.CTkLabel(directive_frame, text=f"Valeur actuelle: {current_value} ({'Commentée' if is_commented else 'Active'})").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            ctk.CTkLabel(directive_frame, text="Description: Directive non reconnue par l'outil. Procédez avec prudence.", wraplength=800, justify="left", text_color="red").grid(row=2, column=0, sticky="w", padx=5, pady=2)

            edit_frame = ctk.CTkFrame(directive_frame)
            edit_frame.grid(row=0, column=1, rowspan=3, padx=10, sticky="nswe")
            edit_frame.grid_columnconfigure(0, weight=1)

            comment_var = ctk.BooleanVar(value=is_commented)
            comment_checkbox = ctk.CTkCheckBox(edit_frame, text="Commenter/Désactiver", variable=comment_var, command=lambda d=directive_name, cv=comment_var: self.toggle_comment(d, cv))
            comment_checkbox.grid(row=0, column=0, pady=5, sticky="w")
            self.widgets[f"comment_{directive_name}"] = comment_var

            entry_value = ctk.StringVar(value=current_value)
            entry = ctk.CTkEntry(edit_frame, textvariable=entry_value)
            entry.grid(row=1, column=0, pady=5, sticky="ew")
            entry_value.trace_add("write", lambda name, index, mode, d=directive_name, ev=entry_value: self.update_directive_value(d, ev.get()))
            self.widgets[f"value_{directive_name}"] = entry_value

            ctk.CTkFrame(self.scroll_frame, height=2, fg_color="gray").grid(row=row, column=0, columnspan=3, sticky="ew", pady=5)
            row += 1
        
        if unrecognized_count > 0:
            messagebox.showwarning("Directives Non Reconnues",
                                   f"{unrecognized_count} directives ont été trouvées dans le fichier php.ini mais ne sont pas dans la base de connaissances de cet outil. Elles sont affichées avec une alerte rouge. Modifiez-les avec prudence.")

    def toggle_comment(self, directive_name, comment_var):
        if directive_name in self.current_config:
            self.current_config[directive_name]["commented"] = comment_var.get()
            self.update_display_after_change(directive_name)


    def update_directive_value(self, directive_name, new_value):
        if directive_name in self.current_config:
            self.current_config[directive_name]["value"] = new_value
            self.update_display_after_change(directive_name)


    def apply_recommended(self, directive_name, recommended_value):
        if directive_name in self.current_config:
            # S'assurer que la directive est décommentée et la valeur est mise à jour
            self.current_config[directive_name]["commented"] = False
            self.current_config[directive_name]["value"] = str(recommended_value) # Assurez-vous que c'est une chaîne

            # Mettre à jour les widgets de l'interface
            if f"comment_{directive_name}" in self.widgets:
                self.widgets[f"comment_{directive_name}"].set(False) # Décocher la case "Commenter"
            
            if f"value_{directive_name}" in self.widgets:
                widget_var = self.widgets[f"value_{directive_name}"]
                if isinstance(widget_var, ctk.StringVar):
                    widget_var.set(str(recommended_value))
                # CTkOptionMenu utilise déjà une StringVar interne, donc set() devrait fonctionner.

            messagebox.showinfo("Recommandation Appliquée", f"La valeur recommandée pour '{directive_name}' a été appliquée : '{recommended_value}'.")
            self.update_display_after_change(directive_name)

    def update_display_after_change(self, directive_name):
        # Pour rafraîchir la couleur de la recommandation ou la valeur affichée pour la directive
        # Ceci est plus complexe avec l'architecture actuelle car les labels ne sont pas directement stockés par directive
        # Une solution simple serait de re-dessiner l'ensemble des directives, mais cela peut être lent.
        # Pour l'instant, les changements sont stockés dans self.current_config et seront reflétés lors de l'écriture.
        pass


    def apply_changes(self):
        if not self.php_ini_path:
            messagebox.showwarning("Aucun Fichier", "Veuillez d'abord charger un fichier php.ini.")
            return

        if not messagebox.askyesno("Confirmer les Changements",
                                   "Ceci va modifier votre fichier php.ini. Souhaitez-vous continuer ? "
                                   "Une sauvegarde sera créée."):
            return

        backup_path = f"{self.php_ini_path}.bak.{os.getenv('USER', 'python_gui')}.{os.getpid()}"
        try:
            shutil.copy2(self.php_ini_path, backup_path)
            messagebox.showinfo("Sauvegarde Créée", f"Sauvegarde du fichier original créée : {backup_path}")
        except Exception as e:
            messagebox.showerror("Erreur de Sauvegarde", f"Impossible de créer la sauvegarde : {e}\n"
                                                     "Assurez-vous d'avoir les permissions nécessaires.")
            return

        new_lines = []
        processed_directive_names = set() # Pour garder une trace des directives déjà traitées

        # Pour préserver l'ordre et les commentaires/sections non directives, nous devons reconstruire
        # le fichier ligne par ligne à partir de l'original.
        with open(self.php_ini_path, 'r') as f:
            for line_num, line in enumerate(f):
                directive_found_on_this_line = False
                
                # Vérifier si cette ligne correspond à une directive que nous gérons ou avons reconnue
                for d_name, d_info in self.current_config.items():
                    if d_name.startswith("__RAW_LINE__"):
                        continue # Les lignes brutes sont des marqueurs, pas des directives à matcher ici

                    # Regex plus spécifique pour éviter les faux positifs et capturer le préfixe ';'
                    match = re.match(r'^\s*(;?\s*)(' + re.escape(d_name) + r')\s*=\s*(.*)', line, re.IGNORECASE)
                    
                    if match:
                        # C'est une directive que nous avons identifiée
                        current_value_from_config = d_info["value"]
                        should_be_commented = d_info["commented"]

                        new_line_content = ""
                        if should_be_commented:
                            new_line_content = f";{d_name} = {current_value_from_config}\n"
                        else:
                            new_line_content = f"{d_name} = {current_value_from_config}\n"
                        
                        new_lines.append(new_line_content)
                        processed_directive_names.add(d_name)
                        directive_found_on_this_line = True
                        break # Passer à la ligne suivante du fichier original

                if not directive_found_on_this_line:
                    # Si la ligne n'est pas une directive que nous avons traitée (c'est un commentaire, une section, ou une ligne brute non modifiée)
                    new_lines.append(line)
        
        # Ajouter les directives qui sont dans self.php_ini_directives_info (notre base de connaissances)
        # ou qui ont été modifiées/ajoutées par l'utilisateur (même si non reconnues initialement)
        # et qui n'étaient pas présentes ou étaient entièrement commentées dans le fichier original
        # ou ont été ajoutées par l'interface.
        added_directives_count = 0
        for directive_name, current_info in self.current_config.items():
            if directive_name.startswith("__RAW_LINE__"):
                continue

            if directive_name not in processed_directive_names:
                # Cette directive n'a pas été trouvée et modifiée in-situ dans le fichier original.
                # Cela signifie qu'elle était soit manquante, soit complètement commentée au point d'être ignorée par le regex.
                # Ou bien c'est une directive non reconnue mais modifiée par l'utilisateur.

                # Si elle est marquée comme "active" dans notre current_config, nous devons l'ajouter.
                if not current_info["commented"]:
                    new_lines.append(f"\n{directive_name} = {current_info['value']}\n")
                    added_directives_count += 1
                elif current_info["commented"] and directive_name in self.php_ini_directives_info:
                    # Si elle est reconnue par notre base, mais commentée (et donc potentiellement manquante)
                    # On la rajoute commentée pour la clarté.
                    # Ou si elle était commentée dans le fichier et a été modifiée par l'utilisateur
                    original_status = self.original_config.get(directive_name, {"commented": True, "value": ""})
                    if (original_status["commented"] and current_info["value"] != original_status["value"]) or \
                       (directive_name not in self.original_config): # Si elle n'était pas là du tout
                        new_lines.append(f"\n;{directive_name} = {current_info['value']}\n")
                        added_directives_count += 1

        try:
            with open(self.php_ini_path, 'w') as f:
                f.writelines(new_lines)
            messagebox.showinfo("Succès", "Le fichier php.ini a été mis à jour avec succès.\n\n"
                                          "**N'oubliez pas de redémarrer votre serveur web (Apache/Nginx) ou PHP-FPM** "
                                          "pour que les changements prennent effet !")
        except Exception as e:
            messagebox.showerror("Erreur d'Écriture", f"Impossible d'écrire dans le fichier php.ini : {e}\n"
                                                     "Assurez-vous d'avoir les permissions (ex: exécutez le script avec sudo).")

    def reset_to_original(self):
        if not self.php_ini_path:
            messagebox.showwarning("Aucun Fichier", "Veuillez d'abord charger un fichier php.ini.")
            return

        if not self.original_config:
            messagebox.showinfo("Rien à Réinitialiser", "Aucune configuration originale chargée.")
            return

        if messagebox.askyesno("Confirmer la Réinitialisation",
                               "Ceci va annuler toutes vos modifications non sauvegardées et recharger l'état initial. Êtes-vous sûr ?"):
            # Recharger current_config à partir de original_config (faire une copie profonde)
            self.current_config = {}
            for k, v in self.original_config.items():
                if "type" in v and v["type"] == "raw":
                    self.current_config[k] = {"line_content": v["line_content"], "type": "raw", "line_num": v["line_num"]}
                else:
                    self.current_config[k] = {"value": v["value"], "commented": v["commented"], "original_line": v["original_line"], "line_num": v["line_num"]}

            self.display_directives()
            messagebox.showinfo("Réinitialisation Réussie", "La configuration a été réinitialisée à son état original chargé.")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    app = PHPIniEditor()
    app.mainloop()