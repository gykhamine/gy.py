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
        "options": ["On", "Off", "4096", "8192", "16384"],
        "recommended_prod": "Off"
    },
    "zlib.output_compression": {
        "description": "Active la compression de sortie Gzip transparente si le navigateur la supporte.",
        "recommendation": "Mettez 'On' pour réduire la taille des réponses HTTP et améliorer la vitesse de chargement pour les utilisateurs.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "zlib.output_compression_level": {
        "description": "Le niveau de compression Gzip (1-9). Plus élevé = meilleure compression, plus lent.",
        "recommendation": "Une valeur de 5 ou 6 offre un bon compromis. 9 pour la compression maximale.",
        "security_paths": "N/A",
        "options": ["1", "5", "6", "9"],
        "recommended_prod": "5"
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
        "options": ["30", "60", "120", "300", "600", "-1"],
        "recommended_prod": "30"
    },
    "max_input_time": {
        "description": "Le temps maximal, en secondes, pendant lequel un script peut analyser les données d'entrée (POST/GET).",
        "recommendation": "Similaire à max_execution_time. Définissez-le en fonction de la taille attendue des données d'entrée (ex: uploads de fichiers).",
        "security_paths": "Empêche les attaques par déni de service liées à des entrées très volumineuses qui bloqueraient le serveur.",
        "options": ["60", "120", "300", "-1"],
        "recommended_prod": "60"
    },
    "memory_limit": {
        "description": "La quantité maximale de mémoire, en octets, qu'un script est autorisé à consommer.",
        "recommendation": "Augmentez si vos applications ont des erreurs de 'mémoire insuffisante'. Des valeurs typiques sont '128M', '256M', '512M'. Une valeur trop élevée peut masquer des problèmes de code ou faciliter des attaques par déni de service si non contrôlé.",
        "security_paths": "Limiter la mémoire permet de mitiger les attaques par déni de service consommant trop de ressources.",
        "options": ["64M", "128M", "256M", "512M", "1024M", "2G", "-1"],
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
        "options": ["/var/log/php_errors.log", "/dev/null"]
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
        "options": ["./:/usr/share/php"]
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
        "options": ["UTF-8", "ISO-8859-1", "Latin1"],
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
        "options": ["Off", "public_html", "www"],
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
        "options": ["2M", "8M", "16M", "32M", "64M", "128M", "512M", "1G"],
        "recommended_prod": "32M"
    },
    "post_max_size": {
        "description": "La taille maximale des données POST que PHP acceptera.",
        "recommendation": "Doit être au moins égal ou supérieur à `upload_max_filesize`.",
        "security_paths": "Limiter la taille des requêtes POST pour prévenir les attaques par déni de service.",
        "options": ["8M", "16M", "32M", "64M", "128M", "512M", "1G"],
        "recommended_prod": "32M"
    },
    "max_file_uploads": {
        "description": "Le nombre maximal de fichiers qui peuvent être téléchargés simultanément.",
        "recommendation": "La valeur par défaut (20) est souvent suffisante. Ajustez si vous avez des formulaires de téléchargement multiples.",
        "security_paths": "Peut aider à mitiger les attaques par déni de service si un attaquant tente de télécharger un très grand nombre de fichiers.",
        "options": ["1", "5", "10", "20", "50", "100"],
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
        "options": ["10", "30", "60", "120", "300"],
        "recommended_prod": "60"
    },
    "date.timezone": {
        "description": "Le fuseau horaire par défaut utilisé par toutes les fonctions date/heure.",
        "recommendation": "C'est **essentiel** pour éviter des avertissements et garantir l'exactitude des horodatages. Définissez-le selon votre localisation, par exemple 'Africa/Brazzaville'.",
        "security_paths": "Bien que pas directement une faille de sécurité, des horodatages incorrects peuvent compliquer le débogage et l'analyse forensique des logs.",
        "options": ["UTC", "Europe/Paris", "America/New_York", "Africa/Brazzaville", "Asia/Tokyo"],
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
        "options": ["/var/lib/php/sessions", "/tmp", "/dev/shm"]
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
        "options": ["100", "1000", "10000", "50000"],
        "recommended_prod": "100"
    },
    "session.gc_maxlifetime": {
        "description": "Durée de vie maximale des sessions (en secondes) après l'accès du dernier utilisateur.",
        "recommendation": "Une valeur plus courte (ex: 1440 secondes = 24 minutes) réduit la fenêtre de temps pour le détournement de session. Adaptez-le aux besoins de votre application.",
        "security_paths": "Minimise le risque de détournement de session (session hijacking) en réduisant la durée de vie des sessions inactives.",
        "options": ["1440", "3600", "7200", "86400"],
        "recommended_prod": "1440"
    },
    "session.sid_length": {
        "description": "La longueur en caractères de l'ID de session.",
        "recommendation": "La valeur par défaut (26) est généralement suffisante pour la sécurité. Ne la diminuez pas.",
        "security_paths": "Une longueur plus grande rend l'ID de session plus difficile à deviner par force brute.",
        "options": ["26", "32", "40", "48"],
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
        "recommendation": "Désactivez les fonctions potentiellement dangereuses si votre application n'en a pas besoin, comme `exec`, `shell_exec`, `system`, `passthru`, `proc_open`, `popen`, `symlink`, `link`, `apache_child_terminate`, `posix_kill`, `posix_mkfifo`, `posix_setpgid`, `posix_setsid`, `posix_setuid`, `posix_setegid`, `posix_seteuid`, `pcntl_exec`, `dl`, `putenv`, `ini_alter`, `ini_restore`, `ini_set`, `chown`, `chgrp`, `chmod`, `socket_create_listen`, `socket_accept`, `socket_listen`, `socket_bind`, `socket_connect`, `fsockopen`, `pfsockopen`, `stream_socket_server`, `stream_socket_client`, `stream_socket_accept`.",
        "security_paths": "Réduit considérablement la capacité d'un attaquant à exécuter des commandes système ou à manipuler le système de fichiers si une vulnérabilité est trouvée dans votre application.",
        "options": ["exec,shell_exec,system,passthru,proc_open,popen,symlink,link,apache_child_terminate,posix_kill,posix_mkfifo,posix_setpgid,posix_setsid,posix_setuid,posix_setegid,posix_seteuid,pcntl_exec,dl,putenv,ini_alter,ini_restore,ini_set,chown,chgrp,chmod,socket_create_listen,socket_accept,socket_listen,socket_bind,socket_connect,fsockopen,pfsockopen,stream_socket_server,stream_socket_client,stream_socket_accept"]
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
        "options": ["/var/www/html", "/home/user/public_html"]
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
        "options": ["/var/log/php_mail.log"]
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
        "options": ["64", "128", "256", "512", "1024"],
        "recommended_prod": "256"
    },
    "opcache.interned_strings_buffer": {
        "description": "La quantité de mémoire pour les chaînes de caractères interpolées (en Mo).",
        "recommendation": "Augmentez si vous utilisez beaucoup de chaînes uniques (ex: ORM).",
        "security_paths": "N/A",
        "options": ["4", "8", "16", "32"],
        "recommended_prod": "8"
    },
    "opcache.max_accelerated_files": {
        "description": "Le nombre maximal de scripts qui peuvent être stockés dans le cache d'opcode.",
        "recommendation": "Choisissez une valeur supérieure au nombre total de fichiers PHP de votre application.",
        "security_paths": "N/A",
        "options": ["1000", "5000", "10000", "20000", "50000", "100000"],
        "recommended_prod": "10000"
    },
    "opcache.revalidate_freq": {
        "description": "Fréquence de vérification de l'horodatage des scripts pour les modifications (en secondes).",
        "recommendation": "En **production**, une valeur plus élevée (ex: 60 ou 0) réduit la surcharge. En **développement**, mettez à 0 pour que les changements soient immédiatement pris en compte.",
        "security_paths": "Une valeur trop élevée en développement peut causer l'exécution de code obsolète. En production, 0 peut être utilisé si les déploiements gèrent la réinitialisation de l'opcache.",
        "options": ["0", "1", "5", "30", "60", "300"],
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
        "options": ["16K", "32K", "64K", "128K", "1M", "2M", "4M"],
        "recommended_prod": "2M"
    },
    "realpath_cache_ttl": {
        "description": "Durée de vie du cache de chemin réel (en secondes).",
        "recommendation": "La valeur par défaut (120) est souvent suffisante. Réduisez en développement si les chemins changent souvent.",
        "security_paths": "N/A",
        "options": ["60", "120", "300", "3600"],
        "recommended_prod": "120"
    },
    "request_order": {
        "description": "L'ordre dans lequel les variables EGPCS (Environment, GET, POST, Cookie, Server) sont parsées dans les tableaux _REQUEST.",
        "recommendation": "Généralement 'GP' (GET puis POST). Évitez 'C' (Cookie) et 'E' (Environment) pour des raisons de sécurité.",
        "security_paths": "Un ordre incorrect peut entraîner des surcharges de variables si un attaquant peut manipuler plusieurs sources d'entrée.",
        "options": ["GP", "GPC", "PG", "PGC", "EGPCS", "GPCS"],
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
        "options": ["1000", "3000", "5000", "10000"],
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
        "options": ["E_ALL", "E_ALL & ~E_NOTICE & ~E_DEPRECATED", "E_ALL & ~E_DEPRECATED & ~E_STRICT & ~E_NOTICE", "E_ERROR | E_WARNING | E_PARSE"],
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
        "options": ["text/html", "application/json", "application/xml"],
        "recommended_prod": "text/html"
    },
    "doc_files_path": {
        "description": "Chemin vers le répertoire des fichiers de documentation PHP.",
        "recommendation": "N/A (rarement défini ou utilisé).",
        "security_paths": "N/A",
        "options": []
    },
    "from": {
        "description": "L'adresse email utilisée comme 'From' pour les mails envoyés via `mail()` sans l'en-tête 'From' explicitement défini.",
        "recommendation": "Définissez une adresse email valide et pertinente (ex: noreply@votre-domaine.com).",
        "security_paths": "Empêche l'envoi de mails avec un champ 'From' vide ou générique, ce qui peut affecter la délivrabilité et la confiance.",
        "options": ["noreply@example.com"]
    },
    "max_input_nesting_level": {
        "description": "Profondeur maximale des tableaux imbriqués et des variables superglobales.",
        "recommendation": "La valeur par défaut (64) est généralement suffisante. Augmentez si vous traitez des données JSON ou XML très imbriquées.",
        "security_paths": "Empêche les attaques par déni de service où un attaquant envoie des données trop imbriquées pour épuiser les ressources du serveur.",
        "options": ["64", "128", "256", "512"],
        "recommended_prod": "64"
    },
    "url_rewriter.tags": {
        "description": "Spécifie les balises HTML pour lesquelles PHP réécrit les URL pour inclure l'ID de session.",
        "recommendation": "Laissez vide ou commentez si `session.use_only_cookies` est activé. La réécriture d'URL est une mauvaise pratique de sécurité.",
        "security_paths": "La réécriture d'URL expose les ID de session dans les URL, les rendant vulnérables au vol, à la journalisation et au partage.",
        "options": ["", "a=href,area=href,frame=src,form=action,fieldset="]
    },
    "assert.active": {
        "description": "Active ou désactive la fonction `assert()`.",
        "recommendation": "Mettez 'Off' en production. Les assertions ne doivent pas être utilisées pour valider les entrées utilisateur ou pour le code de production.",
        "security_paths": "Si 'On', une assertion mal placée ou une expression contrôlée par l'utilisateur peut entraîner l'exécution de code arbitraire.",
        "options": ["0", "1"],
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
        "options": ["0", "1"],
        "recommended_prod": "0"
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
        "recommendation": "La valeur par default (300) est raisonnable. Augmentez en production pour réduire les I/O si les .user.ini ne changent pas souvent.",
        "security_paths": "N/A",
        "options": ["0", "300", "600", "3600"],
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
        "recommendation": "Définissez si vous utilisez un socket local pour la connexion à MySQL (ex: `/var/run/mysqld/mysqld.sock`).",
        "security_paths": "N/A",
        "options": ["/var/run/mysqld/mysqld.sock", "/tmp/mysql.sock"]
    },
    "mysqli.default_socket": {
        "description": "Chemin par défaut du socket MySQL pour MySQLi.",
        "recommendation": "Définissez si vous utilisez un socket local pour la connexion à MySQL (ex: `/var/run/mysqld/mysqld.sock`).",
        "security_paths": "N/A",
        "options": ["/var/run/mysqld/mysqld.sock", "/tmp/mysql.sock"]
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
        "recommendation": "Assurez-vous que ce chemin est correct et que le fichier est à jour pour la validation des certificats SSL (ex: `/etc/ssl/certs/ca-certificates.crt`).",
        "security_paths": "Crucial pour la sécurité des connexions HTTPS sortantes. Un CA Bundle manquant ou obsolète peut entraîner des avertissements ou des failles de sécurité (attaques MITM).",
        "options": ["/etc/ssl/certs/ca-certificates.crt", "/etc/pki/tls/certs/ca-bundle.crt"]
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
    "date.default_latitude": {
        "description": "Latitude par défaut utilisée par les fonctions GPS de date/heure.",
        "recommendation": "N/A (rarement nécessaire de configurer).",
        "security_paths": "N/A",
        "options": ["34.0522"] # Exemple pour Los Angeles
    },
    "date.default_longitude": {
        "description": "Longitude par default utilisée par les fonctions GPS de date/heure.",
        "recommendation": "N/A (rarement nécessaire de configurer).",
        "security_paths": "N/A",
        "options": ["-118.2437"] # Exemple pour Los Angeles
    },
    "date.sunrise_zenith": {
        "description": "Zénith utilisé pour le calcul du lever du soleil.",
        "recommendation": "N/A (valeur par défaut 90.83 est standard pour les calculs de lever/coucher de soleil).",
        "security_paths": "N/A",
        "options": ["90.83"]
    },
    "date.sunset_zenith": {
        "description": "Zénith utilisé pour le calcul du coucher du soleil.",
        "recommendation": "N/A (valeur par défaut 90.83 est standard pour les calculs de lever/coucher de soleil).",
        "security_paths": "N/A",
        "options": ["90.83"]
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
        "recommendation": "Définissez sur 'Neutral' ou la langue de votre application (ex: 'English', 'French').",
        "security_paths": "N/A",
        "options": ["Neutral", "English", "French"],
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
        "options": ["UTF-8", "pass", "SJIS"],
        "recommended_prod": "UTF-8"
    },
    "mbstring.http_input": {
        "description": "Encodage de caractères HTTP pour l'entrée mbstring.",
        "recommendation": "Définissez sur 'pass' (laissez PHP détecter) ou 'UTF-8'.",
        "security_paths": "N/A",
        "options": ["pass", "UTF-8", "auto"],
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
        "options": ["-1", "10", "20", "50", "100"],
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
        "options": ["/tmp", "/var/tmp", "/dev/shm"]
    },
    "cli.pager": {
        "description": "Programme utilisé pour paginer la sortie CLI de PHP (ex: less, more).",
        "recommendation": "N/A (principalement pour le confort de l'utilisateur CLI).",
        "security_paths": "N/A",
        "options": ["less", "more"]
    },
    "cli.prompt": {
        "description": "Chaîne de caractères utilisée comme invite de commande pour PHP CLI.",
        "recommendation": "N/A (principalement pour le confort de l'utilisateur CLI).",
        "security_paths": "N/A",
        "options": ["PHP >"]
    },
    "upload_tmp_dir": {
        "description": "Répertoire temporaire pour les fichiers uploadés. Par défaut, utilise le répertoire temporaire système.",
        "recommendation": "Définissez un chemin explicite vers un répertoire sécurisé et non accessible via le web, avec des permissions strictes.",
        "security_paths": "Un répertoire temporaire d'upload non sécurisé peut exposer des fichiers avant leur traitement ou permettre l'exécution de scripts si le serveur web y a les permissions d'exécution.",
        "options": ["/var/www/tmp_uploads", "/tmp"]
    },
    "extension_dir": {
        "description": "Le répertoire où PHP cherche les extensions dynamiquement chargées (DLLs ou .so).",
        "recommendation": "Laissez la valeur par défaut. Ne le modifiez que si vous savez ce que vous faites.",
        "security_paths": "Une mauvaise configuration pourrait permettre à PHP de charger des extensions malveillantes si des fichiers sont injectés dans ce répertoire.",
        "options": ["/usr/lib/php/20210902", "/opt/php/ext"] # Exemple de chemins typiques
    },
    "enable_post_data_reading": {
        "description": "Active ou désactive la lecture automatique des données POST.",
        "recommendation": "Mettez 'On' sauf si vous gérez les données POST manuellement pour des raisons très spécifiques.",
        "security_paths": "Désactiver pourrait empêcher le fonctionnement normal des applications web.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "request_terminate_timeout": {
        "description": "Le délai d'attente, en secondes, après lequel les requêtes PHP-FPM sont tuées (pour FastCGI).",
        "recommendation": "Utile pour éviter les scripts longs bloquants. Définissez une valeur légèrement supérieure à `max_execution_time`.",
        "security_paths": "Protège contre les scripts bloquants ou défectueux qui pourraient consommer des ressources indéfiniment.",
        "options": ["0", "30", "60", "120", "300"],
        "recommended_prod": "0" # 0 pour illimité, ou valeur comme max_execution_time
    },
    "date.default_timezone": {
        "description": "Alias de `date.timezone` (voir cette directive).",
        "recommendation": "Utilisez `date.timezone`.",
        "security_paths": "Voir `date.timezone`.",
        "options": ["UTC", "Europe/Paris", "Africa/Brazzaville"],
        "recommended_prod": "Africa/Brazzaville"
    },
    "error_append_string": {
        "description": "Chaîne à ajouter à la fin de chaque message d'erreur.",
        "recommendation": "Laissez vide en production pour ne pas ajouter d'informations inutiles.",
        "security_paths": "Évitez d'y mettre des informations sensibles qui pourraient aider un attaquant.",
        "options": []
    },
    "error_prepend_string": {
        "description": "Chaîne à ajouter au début de chaque message d'erreur.",
        "recommendation": "Laissez vide en production pour ne pas ajouter d'informations inutiles.",
        "security_paths": "Évitez d'y mettre des informations sensibles qui pourraient aider un attaquant.",
        "options": []
    },
    "file_uploads_max_size": {
        "description": "Alias ou confusion fréquente avec `upload_max_filesize`.",
        "recommendation": "Utilisez `upload_max_filesize`.",
        "security_paths": "Voir `upload_max_filesize`.",
        "options": ["32M"]
    },
    "highlight.bg": {
        "description": "Couleur d'arrière-plan pour le code source PHP mis en surbrillance (par `show_source()` ou `highlight_file()`).",
        "recommendation": "N/A (cosmétique).",
        "security_paths": "Si vous utilisez `highlight_file()` ou `show_source()` sur des fichiers sensibles, assurez-vous qu'ils ne sont pas accessibles publiquement.",
        "options": []
    },
    "highlight.comment": {
        "description": "Couleur des commentaires pour le code source PHP mis en surbrillance.",
        "recommendation": "N/A (cosmétique).",
        "security_paths": "Voir `highlight.bg`.",
        "options": []
    },
    "highlight.default": {
        "description": "Couleur par défaut pour le code source PHP mis en surbrillance.",
        "recommendation": "N/A (cosmétique).",
        "security_paths": "Voir `highlight.bg`.",
        "options": []
    },
    "highlight.html": {
        "description": "Couleur du HTML pour le code source PHP mis en surbrillance.",
        "recommendation": "N/A (cosmétique).",
        "security_paths": "Voir `highlight.bg`.",
        "options": []
    },
    "highlight.keyword": {
        "description": "Couleur des mots-clés pour le code source PHP mis en surbrillance.",
        "recommendation": "N/A (cosmétique).",
        "security_paths": "Voir `highlight.bg`.",
        "options": []
    },
    "highlight.string": {
        "description": "Couleur des chaînes pour le code source PHP mis en surbrillance.",
        "recommendation": "N/A (cosmétique).",
        "security_paths": "Voir `highlight.bg`.",
        "options": []
    },
    "highlight.default": {
        "description": "Couleur par défaut pour le code source PHP mis en surbrillance.",
        "recommendation": "N/A (cosmétique).",
        "security_paths": "Voir `highlight.bg`.",
        "options": []
    },
    "user_agent": {
        "description": "Chaîne d'agent utilisateur envoyée par défaut lorsque PHP effectue des requêtes HTTP (ex: avec `file_get_contents()` sur des URL).",
        "recommendation": "Définissez une chaîne d'agent utilisateur pertinente pour votre application. Évitez les chaînes génériques qui pourraient être bloquées.",
        "security_paths": "Un agent utilisateur non identifiable peut compliquer le débogage. Pas une faille de sécurité directe.",
        "options": ["PHPApp/1.0", "Mozilla/5.0"]
    },
    "output_handler": {
        "description": "Un gestionnaire de sortie personnalisé. Peut être utilisé pour compresser ou transformer la sortie.",
        "recommendation": "N'utilisez pas cette directive à moins de savoir ce que vous faites, car elle peut interférer avec la mise en tampon de sortie.",
        "security_paths": "Un gestionnaire mal configuré ou malveillant pourrait modifier la sortie de manière inattendue ou injecter du code.",
        "options": ["null", "ob_gzhandler"]
    },
    "post_max_size_ini_parse": {
        "description": "Une directive interne liée à `post_max_size`.",
        "recommendation": "N/A (géré automatiquement).",
        "security_paths": "N/A",
        "options": []
    },
    "precision_serialize": {
        "description": "Précision de sérialisation des nombres à virgule flottante.",
        "recommendation": "La valeur par défaut (17) est généralement suffisante.",
        "security_paths": "N/A",
        "options": ["14", "17"]
    },
    "report_zend_debug": {
        "description": "Rapporte les erreurs de Zend Debugger.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "Peut divulguer des informations sur le débogueur.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "safe_mode_allowed_env_vars": {
        "description": "Prefixes des variables d'environnement accessibles en mode sécurisé (déprécié).",
        "recommendation": "Ignorer, car `safe_mode` est déprécié.",
        "security_paths": "N/A",
        "options": []
    },
    "safe_mode_exec_dir": {
        "description": "Répertoire où les exécutables peuvent être exécutés en mode sécurisé (déprécié).",
        "recommendation": "Ignorer, car `safe_mode` est déprécié.",
        "security_paths": "N/A",
        "options": []
    },
    "safe_mode_gid": {
        "description": "Utilise l'ID de groupe du script pour les vérifications de fichiers en mode sécurisé (déprécié).",
        "recommendation": "Ignorer, car `safe_mode` est déprécié.",
        "security_paths": "N/A",
        "options": ["On", "Off"]
    },
    "session.cache_expire": {
        "description": "Délai d'expiration du cache des pages avec les sessions actives (en minutes).",
        "recommendation": "La valeur par défaut (180 minutes) est souvent suffisante.",
        "security_paths": "N/A",
        "options": ["180", "60", "30", "0"]
    },
    "session.cache_limiter": {
        "description": "Contrôle les en-têtes de cache HTTP envoyés avec les sessions.",
        "recommendation": "Utilisez 'nocache' ou 'private' pour la sécurité afin de ne pas mettre en cache les pages avec des sessions sensibles. 'public' est moins sécurisé.",
        "security_paths": "Un cache mal géré peut exposer des informations sensibles via le cache du navigateur ou du proxy.",
        "options": ["nocache", "private", "public", "no value"],
        "recommended_prod": "nocache"
    },
    "session.cookie_domain": {
        "description": "Le domaine pour lequel le cookie de session est valide.",
        "recommendation": "Définissez-le explicitement sur votre domaine (`yourdomain.com`) pour éviter la fixation de session. Ne le laissez pas vide sauf si vous comprenez les implications.",
        "security_paths": "Une mauvaise configuration peut permettre à des sous-domaines malveillants ou d'autres domaines de lire le cookie de session.",
        "options": [".yourdomain.com", ""]
    },
    "session.cookie_path": {
        "description": "Le chemin sur le serveur pour lequel le cookie de session est valide.",
        "recommendation": "Définissez sur '/' pour que le cookie soit valide pour tout le site. Restreignez si nécessaire.",
        "security_paths": "N/A",
        "options": ["/", "/path/to/app"]
    },
    "session.cookie_salt": {
        "description": "Ajoute un sel aléatoire au cookie de session (PHP 7.0+).",
        "recommendation": "N/A (généré automatiquement).",
        "security_paths": "N/A",
        "options": []
    },
    "session.name": {
        "description": "Nom du cookie de session.",
        "recommendation": "Changez le nom par défaut (`PHPSESSID`) pour réduire les chances que des outils automatisés reconnaissent immédiatement la technologie.",
        "security_paths": "Un nom non standard rend l'empreinte de la session légèrement plus difficile à identifier par des scanners automatisés.",
        "options": ["PHPSESSID", "MYAPP_SESSIONID", "SESSID"]
    },
    "session.referer_check": {
        "description": "Vérifie l'en-tête HTTP Referer pour chaque ID de session.",
        "recommendation": "Laissez vide. Cette méthode n'est pas fiable pour la sécurité car le Referer peut être falsifié.",
        "security_paths": "Ne pas compter sur cette directive pour la sécurité. La vérification du Referer est une mesure faible contre le détournement de session.",
        "options": []
    },
    "session.serialize_handler": {
        "description": "Nom du gestionnaire utilisé pour sérialiser/désérialiser les données de session.",
        "recommendation": "Laissez la valeur par défaut (`php` ou `php_serialize`). Changez si vous utilisez un gestionnaire personnalisé.",
        "security_paths": "Une mauvaise configuration peut entraîner des problèmes de désérialisation non sûre.",
        "options": ["php", "php_binary", "wddx"]
    },
    "session.url_rewriter.tags": {
        "description": "Tags HTML pour la réécriture d'URL des ID de session (voir `url_rewriter.tags`).",
        "recommendation": "Laissez vide et utilisez `session.use_only_cookies = 1`.",
        "security_paths": "Voir `url_rewriter.tags`.",
        "options": ["a=href,area=href,frame=src,input=src,form=action,fieldset="]
    },
    "session.upload_progress.cleanup": {
        "description": "Supprime les informations de progression des téléchargements une fois terminés.",
        "recommendation": "Mettez 'On'.",
        "security_paths": "Évite de laisser des informations de progression sensibles dans la session une fois le téléchargement terminé.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "session.upload_progress.enabled": {
        "description": "Active la fonctionnalité de progression des téléchargements.",
        "recommendation": "Mettez 'On' si vous avez besoin de cette fonctionnalité.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "session.upload_progress.freq": {
        "description": "Fréquence de mise à jour des informations de progression (ex: '1%' ou '512KB').",
        "recommendation": "Adaptez à vos besoins.",
        "security_paths": "N/A",
        "options": ["1%", "5%", "1KB", "512KB"]
    },
    "session.upload_progress.min_freq": {
        "description": "Fréquence minimale de mise à jour de la progression (en secondes).",
        "recommendation": "Adaptez à vos besoins.",
        "security_paths": "N/A",
        "options": ["1", "0.5"]
    },
    "session.upload_progress.name": {
        "description": "Nom de la clé dans $_SESSION pour les informations de progression des téléchargements.",
        "recommendation": "Laissez la valeur par défaut (`PHP_SESSION_UPLOAD_PROGRESS`).",
        "security_paths": "N/A",
        "options": ["PHP_SESSION_UPLOAD_PROGRESS"]
    },
    "session.upload_progress.prefix": {
        "description": "Préfixe pour les clés de progression des téléchargements dans $_SESSION.",
        "recommendation": "Laissez la valeur par défaut (`upload_progress_`).",
        "security_paths": "N/A",
        "options": ["upload_progress_"]
    },
    "soap.wsdl_cache": {
        "description": "Active ou désactive le cache WSDL pour les requêtes SOAP.",
        "recommendation": "Mettez '1' (On) en production pour de meilleures performances. '0' (Off) en développement.",
        "security_paths": "N/A",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "soap.wsdl_cache_dir": {
        "description": "Répertoire où les fichiers WSDL mis en cache sont stockés.",
        "recommendation": "Définissez un chemin absolu vers un répertoire sécurisé et non accessible via le web.",
        "security_paths": "Un répertoire de cache accessible publiquement pourrait exposer des informations sur vos services web ou permettre l'injection de fichiers WSDL malveillants.",
        "options": ["/tmp"]
    },
    "soap.wsdl_cache_enabled": {
        "description": "Alias de `soap.wsdl_cache`.",
        "recommendation": "Utilisez `soap.wsdl_cache`.",
        "security_paths": "Voir `soap.wsdl_cache`.",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "soap.wsdl_cache_limit": {
        "description": "Nombre maximal de fichiers WSDL à mettre en cache.",
        "recommendation": "La valeur par défaut (5) est souvent suffisante. Augmentez si vous avez beaucoup de services SOAP.",
        "security_paths": "N/A",
        "options": ["1", "5", "10", "50"]
    },
    "soap.wsdl_cache_ttl": {
        "description": "Durée de vie (en secondes) des fichiers WSDL dans le cache.",
        "recommendation": "La valeur par défaut (86400 secondes = 24 heures) est souvent suffisante.",
        "security_paths": "N/A",
        "options": ["3600", "86400", "259200"]
    },
    "sybase.allow_persistent": {
        "description": "Permet ou non les connexions persistantes Sybase (déprécié).",
        "recommendation": "Mettez 'Off'. Évitez les fonctions et extensions dépréciées.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "sybase.max_links": {
        "description": "Nombre maximal de liens Sybase par processus PHP (déprécié).",
        "recommendation": "Mettez '0'. Évitez les fonctions et extensions dépréciées.",
        "security_paths": "N/A",
        "options": ["-1", "0", "10"]
    },
    "sybase.max_persistent": {
        "description": "Nombre maximal de liens persistants Sybase par processus PHP (déprécié).",
        "recommendation": "Mettez '0'. Évitez les fonctions et extensions dépréciées.",
        "security_paths": "N/A",
        "options": ["-1", "0", "10"]
    },
    "syslog.facility": {
        "description": "Type de programme qui génère le message syslog (pour les logs PHP envoyés à syslog).",
        "recommendation": "Laissez la valeur par défaut (`LOG_USER`) ou `LOG_LOCAL0` à `LOG_LOCAL7` si vous utilisez un syslog centralisé.",
        "security_paths": "Une mauvaise configuration pourrait rendre les logs PHP difficiles à trouver ou à analyser dans un système de logging centralisé.",
        "options": ["LOG_USER", "LOG_LOCAL0", "LOG_DAEMON"]
    },
    "syslog.ident": {
        "description": "Chaîne d'identification pour les messages syslog PHP.",
        "recommendation": "Définissez une chaîne claire (ex: 'php-fpm', 'php-apache').",
        "security_paths": "Aide à identifier la source des messages PHP dans les logs système.",
        "options": ["php-fpm", "php-apache"]
    },
    "tidy.clean_output": {
        "description": "Nettoie automatiquement la sortie HTML avec l'extension Tidy.",
        "recommendation": "Mettez 'Off' en production, car cela ajoute une surcharge et peut modifier le HTML.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "tidy.default_config": {
        "description": "Chemin vers le fichier de configuration par défaut de Tidy.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "user_agent_from_request": {
        "description": "Si activé, le `User-Agent` utilisé par les fonctions HTTP sera tiré de la requête client.",
        "recommendation": "Mettez 'Off'. Les requêtes sortantes de votre serveur ne doivent pas imiter l'agent utilisateur du client, sauf cas spécifiques.",
        "security_paths": "Peut être trompeur ou problématique pour certaines intégrations API.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "xmlrpc_error_indez": {
        "description": "Index de l'erreur XML-RPC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "xmlrpc_errors": {
        "description": "Active ou désactive les erreurs XML-RPC.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "zend.exception_ignore_args": {
        "description": "Empêche l'inclusion des arguments de fonction dans les traces d'exception (PHP 7.4+).",
        "recommendation": "Mettez 'On' en production pour ne pas divulguer d'informations sensibles via les traces d'erreurs.",
        "security_paths": "Empêche la fuite d'informations sensibles (mots de passe, clés API) qui pourraient être passées en arguments de fonction et apparaître dans les logs d'erreurs.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "zend.assertions": {
        "description": "Active/désactive la génération de code pour les assertions (PHP 7.0+).",
        "recommendation": "**Mettez -1 en production** pour que les assertions ne génèrent pas de code. Mettez 1 en développement pour l'activer.",
        "security_paths": "Les assertions ne doivent jamais être actives en production car elles peuvent être exploitées pour l'exécution de code arbitraire si une expression est contrôlée par l'utilisateur.",
        "options": ["1", "0", "-1"],
        "recommended_prod": "-1"
    },
    "zend.exception_string_param_max_len": {
        "description": "Longueur maximale de la chaîne de caractères pour les paramètres d'exception (PHP 7.4+).",
        "recommendation": "La valeur par défaut (15) est suffisante.",
        "security_paths": "N/A",
        "options": ["0", "15", "50"]
    },
    "variables_order": {
        "description": "L'ordre des superglobales (`_GET`, `_POST`, `_COOKIE`, `_SERVER`, `_ENV`).",
        "recommendation": "Par défaut `GPCS`. `E` pour `_ENV` n'est généralement pas souhaité.",
        "security_paths": "S'assurer que `E` (Environment) n'est pas utilisé pour éviter la fuite de variables d'environnement sensibles.",
        "options": ["GPCS", "EGPCS"],
        "recommended_prod": "GPCS"
    },
    "auto_globals_jit": {
        "description": "Active une optimisation JIT pour les superglobales, les chargeant uniquement si elles sont utilisées.",
        "recommendation": "Mettez 'On' pour de meilleures performances.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "browscap": {
        "description": "Chemin vers le fichier `browscap.ini` pour la détection du navigateur.",
        "recommendation": "Laissez vide si non utilisé. Déprécié et généralement remplacé par des bibliothèques.",
        "security_paths": "N/A",
        "options": []
    },
    "com.allow_dcom": {
        "description": "Permet ou non l'utilisation de DCOM dans l'extension COM (Windows uniquement).",
        "recommendation": "Mettez 'Off' sauf si vous l'utilisez spécifiquement et que vous comprenez les risques.",
        "security_paths": "DCOM peut exposer des vulnérabilités si non géré avec soin.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "com.autoregister_typelib": {
        "description": "Enregistre automatiquement les bibliothèques de types COM.",
        "recommendation": "Mettez 'Off'.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "com.autoregister_verbose": {
        "description": "Affiche des messages d'avertissement pendant l'enregistrement COM.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "com.code_page": {
        "description": "Code page par défaut pour l'extension COM.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "com.typelib_file": {
        "description": "Fichier de cache des bibliothèques de types COM.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "date.default_year_end": {
        "description": "L'année par défaut à utiliser si seulement deux chiffres sont donnés pour l'année (ex: 99 pour 1999 ou 2099).",
        "recommendation": "N/A (devrait être géré par des formats complets).",
        "security_paths": "N/A",
        "options": ["2000"]
    },
    "fileinfo.mime_database_path": {
        "description": "Chemin vers la base de données MIME utilisée par l'extension Fileinfo.",
        "recommendation": "Laissez la valeur par défaut. Ne modifiez que si vous avez une base de données personnalisée.",
        "security_paths": "N/A",
        "options": []
    },
    "gd.jpeg_ignore_warning": {
        "description": "Ignore les avertissements JPEG lors du chargement d'images.",
        "recommendation": "Mettez '1' (On) en production pour éviter les erreurs d'avertissement sur des images légèrement corrompues.",
        "security_paths": "N/A",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "imagick.exception_verbosity": {
        "description": "Le niveau de verbosité des exceptions Imagick.",
        "recommendation": "Mettez '0' (Off) en production.",
        "security_paths": "Des messages d'erreur trop verbeux peuvent divulguer des informations sur la configuration du système.",
        "options": ["0", "1", "2"],
        "recommended_prod": "0"
    },
    "imap.enable_insecure_rsh": {
        "description": "Permet l'utilisation de rsh ou ssh non sécurisé avec IMAP.",
        "recommendation": "**Mettez '0' (Off).** N'utilisez jamais rsh ou ssh de manière non sécurisée.",
        "security_paths": "**CRITIQUE.** L'activation de ceci permet des connexions réseau non chiffrées et très vulnérables.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "intl.default_locale": {
        "description": "La locale par défaut à utiliser pour les fonctions de l'extension Intl.",
        "recommendation": "Définissez une locale pertinente pour votre application (ex: 'fr_FR', 'en_US').",
        "security_paths": "N/A",
        "options": ["en_US", "fr_FR", "de_DE"]
    },
    "intl.error_level": {
        "description": "Le niveau de rapport d'erreurs pour l'extension Intl.",
        "recommendation": "Mettez '0' (Off) ou `E_WARNING` en production.",
        "security_paths": "N/A",
        "options": ["0", "1", "2", "E_WARNING", "E_NOTICE"]
    },
    "ldap.max_links": {
        "description": "Nombre maximal de liens persistants LDAP par processus PHP.",
        "recommendation": "-1 pour illimité, ou une valeur raisonnable.",
        "security_paths": "Un nombre trop élevé peut être exploité pour des attaques par épuisement de ressources.",
        "options": ["-1", "10", "20", "50"]
    },
    "libxml.disable_entity_loader": {
        "description": "Désactive la capacité de LibXML à charger des entités externes.",
        "recommendation": "**Mettez '1' (On).** C'est une protection essentielle contre les attaques XXE (XML External Entity).",
        "security_paths": "**CRITIQUE.** Protège contre les attaques XXE, qui peuvent permettre l'inclusion de fichiers locaux, la lecture de secrets ou des attaques DoS.",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "mail.force_extra_parameters": {
        "description": "Ajoute des paramètres supplémentaires à l'appel `sendmail`.",
        "recommendation": "Laissez vide sauf si vous avez besoin de passer des options spécifiques à `sendmail`.",
        "security_paths": "N/A",
        "options": []
    },
    "max_file_uploads_old": {
        "description": "Une directive obsolète liée aux téléchargements.",
        "recommendation": "Ignorer, utiliser `max_file_uploads`.",
        "security_paths": "N/A",
        "options": []
    },
    "memcached.sess_binary": {
        "description": "Active ou désactive le protocole binaire pour les sessions Memcached.",
        "recommendation": "Mettez 'On' pour de meilleures performances et moins de surcharge réseau.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "memcached.sess_connect_timeout": {
        "description": "Délai d'attente de connexion pour les sessions Memcached (en ms).",
        "recommendation": "Définissez une valeur raisonnable (ex: 1000ms = 1s).",
        "security_paths": "N/A",
        "options": ["1000", "5000"]
    },
    "memcached.sess_consistent_hash": {
        "description": "Active le hachage cohérent pour les sessions Memcached.",
        "recommendation": "Mettez 'On' pour une meilleure distribution des clés et une meilleure résilience des serveurs Memcached.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "memcached.sess_distribute_replicated_reads": {
        "description": "Distribue les lectures répliquées pour les sessions Memcached.",
        "recommendation": "Mettez 'On' pour de meilleures performances en lecture.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "memcached.sess_lock_wait": {
        "description": "Délai d'attente pour le verrouillage des sessions Memcached (en microsecondes).",
        "recommendation": "La valeur par défaut (150000) est souvent suffisante.",
        "security_paths": "Un délai d'attente trop court peut entraîner des erreurs de session. Trop long peut entraîner des blocages.",
        "options": ["150000", "500000"]
    },
    "memcached.sess_locking": {
        "description": "Active ou désactive le verrouillage des sessions Memcached.",
        "recommendation": "Mettez 'On' pour éviter les corruptions de session en cas d'accès concurrentiel.",
        "security_paths": "Crucial pour l'intégrité des données de session concurrentes.",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "memcached.sess_persistent": {
        "description": "Utilise des connexions Memcached persistantes pour les sessions.",
        "recommendation": "Mettez 'On' pour de meilleures performances en évitant de re-connecter à chaque requête.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "memcached.sess_prefix": {
        "description": "Préfixe pour les clés de session Memcached.",
        "recommendation": "Définissez un préfixe unique pour éviter les collisions avec d'autres applications.",
        "security_paths": "N/A",
        "options": ["memc.sess.key."]
    },
    "memcached.sess_number_of_replicas": {
        "description": "Le nombre de réplicas à stocker pour chaque clé de session Memcached.",
        "recommendation": "Définissez '0' pour aucune réplication. Augmentez pour la redondance.",
        "security_paths": "N/A",
        "options": ["0", "1", "2"]
    },
    "memcached.sess_sasl_password": {
        "description": "Mot de passe SASL pour l'authentification Memcached.",
        "recommendation": "Utilisez si votre serveur Memcached nécessite une authentification. Gardez confidentiel.",
        "security_paths": "**CRITIQUE.** Ne doit jamais être en clair dans le code ou des logs accessibles.",
        "options": []
    },
    "memcached.sess_sasl_username": {
        "description": "Nom d'utilisateur SASL pour l'authentification Memcached.",
        "recommendation": "Utilisez si votre serveur Memcached nécessite une authentification. Gardez confidentiel.",
        "security_paths": "**CRITIQUE.** Ne doit jamais être en clair dans le code ou des logs accessibles.",
        "options": []
    },
    "memcached.sess_server_failure_limit": {
        "description": "Nombre de tentatives après lesquelles un serveur Memcached est marqué comme mort.",
        "recommendation": "La valeur par défaut (2) est souvent suffisante.",
        "security_paths": "N/A",
        "options": ["1", "2", "5"]
    },
    "mongodb.debug": {
        "description": "Active le mode de débogage pour l'extension MongoDB.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "Peut divulguer des informations sensibles sur les requêtes ou le serveur MongoDB.",
        "options": ["Off", "On"],
        "recommended_prod": "Off"
    },
    "mysqli.allow_local_infile": {
        "description": "Permet le chargement de données locales avec `LOAD DATA LOCAL INFILE`.",
        "recommendation": "**Mettez 'Off' en production.** Une faille de sécurité majeure si un attaquant peut manipuler le chemin du fichier.",
        "security_paths": "**CRITIQUE.** Permet à un attaquant d'accéder à des fichiers arbitraires sur le système de fichiers du client ou du serveur (selon la version de MySQL et le contexte).",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "mysqli.default_host": {
        "description": "Hôte par défaut pour les connexions MySQLi.",
        "recommendation": "Laissez vide ou 'localhost' si la base de données est locale.",
        "security_paths": "N/A",
        "options": ["localhost"]
    },
    "mysqli.default_port": {
        "description": "Port par défaut pour les connexions MySQLi.",
        "recommendation": "3306 est le port standard.",
        "security_paths": "N/A",
        "options": ["3306"]
    },
    "mysqli.default_pw": {
        "description": "Mot de passe par défaut pour les connexions MySQLi (à ne JAMAIS utiliser en production).",
        "recommendation": "**Laissez vide.** Les mots de passe ne doivent jamais être dans php.ini.",
        "security_paths": "**CRITIQUE.** Exposerait le mot de passe de la base de données. Utilisez un fichier de configuration d'application sécurisé.",
        "options": []
    },
    "mysqli.default_user": {
        "description": "Nom d'utilisateur par défaut pour les connexions MySQLi (à ne JAMAIS utiliser en production).",
        "recommendation": "**Laissez vide.** Les noms d'utilisateur ne doivent jamais être dans php.ini.",
        "security_paths": "**CRITIQUE.** Exposerait le nom d'utilisateur de la base de données. Utilisez un fichier de configuration d'application sécurisé.",
        "options": []
    },
    "oci8.default_prefetch": {
        "description": "Nombre de lignes par défaut à extraire en une seule requête pour OCI8 (Oracle).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["100"]
    },
    "oci8.old_oci_names": {
        "description": "Utilise les anciens noms de fonctions OCI8.",
        "recommendation": "Mettez 'Off' et utilisez les noms de fonctions modernes.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "oci8.persistent_timeout": {
        "description": "Délai d'attente pour les connexions persistantes OCI8.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["-1"]
    },
    "oci8.statement_cache_size": {
        "description": "Taille du cache des requêtes pour OCI8.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["20"]
    },
    "open_basedir_old": {
        "description": "Ancienne directive `open_basedir`. Utilisez `open_basedir`.",
        "recommendation": "Ignorer, utiliser `open_basedir`.",
        "security_paths": "N/A",
        "options": []
    },
    "pcre.backtrack_limit": {
        "description": "Limite le nombre de retours en arrière pour les expressions régulières PCRE.",
        "recommendation": "La valeur par défaut (1000000) est généralement suffisante. Peut aider à prévenir les attaques DoS via des regexes complexes.",
        "security_paths": "Empêche les attaques par déni de service (ReDoS) causées par des expressions régulières mal conçues ou des entrées spécialement conçues.",
        "options": ["100000", "1000000", "5000000"],
        "recommended_prod": "1000000"
    },
    "pcre.recursion_limit": {
        "description": "Limite la profondeur de récursion pour les expressions régulières PCRE.",
        "recommendation": "La valeur par défaut (100000) est généralement suffisante. Similaire à `pcre.backtrack_limit`.",
        "security_paths": "Empêche les attaques ReDoS.",
        "options": ["10000", "100000", "500000"],
        "recommended_prod": "100000"
    },
    "pdo_odbc.default_collation": {
        "description": "Collation par défaut pour PDO_ODBC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "pdo_odbc.default_connection_pool_size": {
        "description": "Taille par défaut du pool de connexions pour PDO_ODBC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "pdo_odbc.default_connection_timeout": {
        "description": "Délai d'attente de connexion par défaut pour PDO_ODBC (en secondes).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["60"]
    },
    "phar.cache_list": {
        "description": "Liste de fichiers PHAR à mettre en cache pour un accès plus rapide.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "phar.total_max_bzip2_size": {
        "description": "Taille maximale cumulée des fichiers compressés Bzip2 dans une archive PHAR.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["4096K"]
    },
    "phar.total_max_gz_size": {
        "description": "Taille maximale cumulée des fichiers compressés Gzip dans une archive PHAR.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["4096K"]
    },
    "phar.total_max_tar_size": {
        "description": "Taille maximale cumulée des fichiers Tar dans une archive PHAR.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["4096K"]
    },
    "phar.total_max_zip_size": {
        "description": "Taille maximale cumulée des fichiers Zip dans une archive PHAR.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["4096K"]
    },
    "post_max_size_ini_parse_warning": {
        "description": "Directive interne liée à `post_max_size` et aux avertissements de parsing.",
        "recommendation": "N/A (géré automatiquement).",
        "security_paths": "N/A",
        "options": []
    },
    "session.trans_sid_hosts": {
        "description": "Liste des hôtes pour lesquels l'ID de session est transmis via l'URL (trans_sid).",
        "recommendation": "**Laissez vide.** La transmission de l'ID de session dans l'URL est une faille de sécurité majeure.",
        "security_paths": "**CRITIQUE.** Exposerait les ID de session dans les URL, les rendant vulnérables au vol, à la journalisation et au partage.",
        "options": []
    },
    "session.trans_sid_tags": {
        "description": "Tags HTML pour la transmission de l'ID de session via l'URL (trans_sid).",
        "recommendation": "**Laissez vide.** La transmission de l'ID de session dans l'URL est une faille de sécurité majeure.",
        "security_paths": "**CRITIQUE.** Exposerait les ID de session dans les URL.",
        "options": ["a=href,area=href,frame=src,form=action,fieldset="]
    },
    "short_tags": {
        "description": "Alias de `short_open_tag` (voir cette directive).",
        "recommendation": "Utilisez `short_open_tag`.",
        "security_paths": "Voir `short_open_tag`.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "sqlite3.extension_dir": {
        "description": "Répertoire où SQLite3 cherche les extensions.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "unserialize_callback_func": {
        "description": "Fonction de rappel appelée si une classe non définie est rencontrée lors de la désérialisation.",
        "recommendation": "N'utilisez pas cette directive à moins de comprendre les implications de sécurité. Peut être une vulnérabilité de désérialisation si mal gérée.",
        "security_paths": "Une fonction de rappel malveillante ou vulnérable peut être exploitée pour l'exécution de code arbitraire si des données désérialisées proviennent d'une source non fiable.",
        "options": []
    },
    "url_rewriter.log_errors": {
        "description": "Enregistre les erreurs de réécriture d'URL dans le journal des erreurs.",
        "recommendation": "Mettez 'Off' en production si vous ne vous souciez pas des logs de réécriture d'URL. Laissez 'On' en développement pour le débogage.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "windows.cp_default": {
        "description": "Page de code par défaut pour les systèmes Windows.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["65001"] # UTF-8
    },
    "windows.load_config_only": {
        "description": "Charge uniquement le fichier de configuration PHP, pas les extensions (Windows uniquement).",
        "recommendation": "Mettez 'Off' sauf si vous déboguez des problèmes de chargement d'extensions.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "xdebug.cli_color": {
        "description": "Active la coloration de la sortie Xdebug dans la ligne de commande.",
        "recommendation": "N/A (cosmétique).",
        "security_paths": "N/A",
        "options": ["0", "1", "2"],
        "recommended_prod": "0" # Off en production
    },
    "xdebug.default_enable": {
        "description": "Active Xdebug par défaut.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "Voir `xdebug.remote_enable`.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "xdebug.remote_connect_back": {
        "description": "Si activé, Xdebug essaiera de se connecter à l'adresse IP de la requête HTTP.",
        "recommendation": "**Mettez 'Off' en production.** Peut exposer le débogueur à des connexions inattendues.",
        "security_paths": "**CRITIQUE.** Peut permettre à des attaquants de forcer une connexion Xdebug à leur machine, permettant potentiellement l'exécution de code.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "xdebug.remote_host": {
        "description": "L'hôte auquel Xdebug doit se connecter pour le débogage distant.",
        "recommendation": "Définissez sur '127.0.0.1' ou l'IP de votre machine de développement. Laissez vide en production.",
        "security_paths": "Si défini sur une IP publique en production, peut exposer le débogueur.",
        "options": ["localhost", "127.0.0.1"]
    },
    "xdebug.remote_log": {
        "description": "Chemin du fichier journal Xdebug distant.",
        "recommendation": "N/A (uniquement pour le débogage).",
        "security_paths": "Ne doit pas être accessible publiquement.",
        "options": []
    },
    "xdebug.show_exception_trace": {
        "description": "Affiche la trace d'exception lorsque Xdebug est actif.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "Peut divulguer des informations sensibles dans les traces d'erreurs.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "xdebug.show_local_vars": {
        "description": "Affiche les variables locales dans les traces d'exception Xdebug.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "Peut divulguer des informations sensibles contenues dans les variables locales.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "xdebug.var_display_max_children": {
        "description": "Nombre maximal d'éléments pour les enfants d'un tableau/objet affichés par Xdebug.",
        "recommendation": "N/A (déboguage uniquement).",
        "security_paths": "N/A",
        "options": ["128", "256"]
    },
    "xdebug.var_display_max_data": {
        "description": "Quantité maximale de données affichées pour une variable par Xdebug (en octets).",
        "recommendation": "N/A (déboguage uniquement).",
        "security_paths": "N/A",
        "options": ["512", "1024", "4096"]
    },
    "xdebug.var_display_max_depth": {
        "description": "Profondeur maximale de récursion pour l'affichage des variables par Xdebug.",
        "recommendation": "N/A (déboguage uniquement).",
        "security_paths": "N/A",
        "options": ["3", "5", "10"]
    },
    "pdo_sqlsrv.client_buffer_max_size": {
        "description": "Taille maximale du tampon client pour PDO_SQLSRV.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["1024"]
    },
    "pdo_sqlsrv.log_severity": {
        "description": "Niveau de journalisation pour les erreurs PDO_SQLSRV.",
        "recommendation": "Mettez '0' (Off) ou '1' (Erreurs) en production.",
        "security_paths": "Peut exposer des détails de connexion ou de requête dans les logs.",
        "options": ["0", "1", "2", "3"]
    },
    "sqlsrv.client_buffer_max_size": {
        "description": "Taille maximale du tampon client pour SQLSRV.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["1024"]
    },
    "sqlsrv.log_severity": {
        "description": "Niveau de journalisation pour les erreurs SQLSRV.",
        "recommendation": "Mettez '0' (Off) ou '1' (Erreurs) en production.",
        "security_paths": "Peut exposer des détails de connexion ou de requête dans les logs.",
        "options": ["0", "1", "2", "3"]
    },
    "apc.enabled": {
        "description": "Active ou désactive le cache APC (Alternative PHP Cache).",
        "recommendation": "Utilisez OPcache à la place si disponible. Si APC est nécessaire, mettez 'On' en production.",
        "security_paths": "N/A",
        "options": ["0", "1"],
        "recommended_prod": "0" # Préférer OPcache
    },
    "apc.enable_cli": {
        "description": "Active le cache APC pour le CLI.",
        "recommendation": "Mettez 'Off' à moins d'avoir des scripts CLI de longue durée bénéficiant du cache.",
        "security_paths": "N/A",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "apc.filters": {
        "description": "Filtres pour inclure/exclure des fichiers du cache APC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "apc.localcache": {
        "description": "Active ou désactive le cache local d'APC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["0", "1"]
    },
    "apc.optimization": {
        "description": "Active ou désactive les optimisations APC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["0", "1"]
    },
    "apc.shm_segments": {
        "description": "Nombre de segments de mémoire partagée utilisés par APC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["1"]
    },
    "apc.shm_size": {
        "description": "Taille de la mémoire partagée allouée pour APC (en Mo).",
        "recommendation": "Définissez une taille suffisante pour votre application (ex: 128M).",
        "security_paths": "N/A",
        "options": ["32M", "64M", "128M", "256M"]
    },
    "apc.stat": {
        "description": "Vérifie l'horodatage des fichiers pour les modifications (APC).",
        "recommendation": "Mettez '0' (Off) en production pour de meilleures performances (nécessite de vider le cache manuellement après chaque déploiement). '1' (On) en développement.",
        "security_paths": "Si '0' en production, assurez-vous de vider le cache APC après chaque déploiement pour éviter l'exécution de code obsolète/vulnérable.",
        "options": ["0", "1"],
        "recommended_prod": "0"
    },
    "apc.ttl": {
        "description": "Durée de vie (en secondes) des entrées dans le cache APC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["0", "3600", "7200"]
    },
    "apc.user_enabled": {
        "description": "Active ou désactive le cache utilisateur APC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["0", "1"]
    },
    "apc.user_ttl": {
        "description": "Durée de vie (en secondes) des entrées utilisateur dans le cache APC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["0", "3600", "7200"]
    },
    "apc.write_lock": {
        "description": "Active ou désactive les verrous d'écriture pour le cache APC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["0", "1"]
    },
    "extension": {
        "description": "Charge une extension PHP dynamique (ex: `extension=pdo_mysql.so`).",
        "recommendation": "Listez ici les extensions dont votre application a besoin. Chaque extension est une ligne séparée.",
        "security_paths": "Assurez-vous que seules les extensions nécessaires sont chargées pour réduire la surface d'attaque. Des extensions inutiles peuvent introduire des vulnérabilités.",
        "options": ["pdo_mysql", "mysqli", "gd", "curl", "zip", "mbstring", "intl"]
    },
    "allow_webdav_methods": {
        "description": "Permet les méthodes WebDAV (PROPFIND, PUT, etc.) sur les fichiers PHP.",
        "recommendation": "Mettez 'Off' sauf si vous utilisez explicitement WebDAV avec PHP.",
        "security_paths": "Peut exposer des vecteurs d'attaque si WebDAV n'est pas correctement sécurisé.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "bcmath.scale": {
        "description": "Nombre de décimales par défaut pour les fonctions BCMath.",
        "recommendation": "La valeur par défaut (0) est suffisante pour la plupart des cas. Augmentez pour des calculs de haute précision (ex: financiers).",
        "security_paths": "N/A",
        "options": ["0", "2", "4", "10"]
    },
    "brotli.chunk_size": {
        "description": "Taille de segment pour la compression Brotli.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["4096"]
    },
    "brotli.compressed_mode": {
        "description": "Mode de compression Brotli (0 pour texte, 1 pour données brutes).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["0", "1"]
    },
    "brotli.disable": {
        "description": "Désactive la compression Brotli.",
        "recommendation": "Mettez 'Off' si vous voulez utiliser la compression Brotli.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "brotli.level": {
        "description": "Niveau de compression Brotli (0-11). Plus élevé = meilleure compression, plus lent.",
        "recommendation": "Une valeur de 4-6 est un bon équilibre. 11 pour la compression maximale.",
        "security_paths": "N/A",
        "options": ["0", "4", "6", "11"]
    },
    "cgi.discard_path": {
        "description": "Définit si PHP-CGI doit rejeter les informations de chemin non-CGI.",
        "recommendation": "Mettez 'On' en production. Empêche les attaques d'exécution de code en cachant le code source.",
        "security_paths": "Empêche les attaquants d'exécuter des fichiers PHP en ajoutant `/path/to/script.php/.evil` à l'URL, ce qui pourrait exécuter le script avec des conséquences inattendues.",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "cgi.force_redirect": {
        "description": "Force les redirections internes pour PHP-CGI.",
        "recommendation": "**Mettez '1' (On) en production.** Une protection importante si vous utilisez PHP-CGI.",
        "security_paths": "**CRITIQUE.** Protège contre l'exécution de PHP dans des configurations Apache/Nginx mal configurées, ce qui pourrait exposer le code source ou permettre l'exécution de commandes système.",
        "options": ["0", "1"],
        "recommended_prod": "1"
    },
    "cgi.nph": {
        "description": "Active le mode NPH (Non-Parsed Headers) pour CGI.",
        "recommendation": "Mettez 'Off'. Rarement utilisé et peut causer des problèmes.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "cgi.redirect_status_env": {
        "description": "Variable d'environnement utilisée pour transmettre le statut de redirection au serveur web.",
        "recommendation": "N/A (utilisé par CGI).",
        "security_paths": "N/A",
        "options": []
    },
    "cli_server.color": {
        "description": "Active la coloration pour le serveur web intégré de PHP CLI.",
        "recommendation": "N/A (développement uniquement).",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "curl.direct_proxy_tunnel": {
        "description": "Active un tunnel proxy direct pour cURL.",
        "recommendation": "Mettez 'On' sauf si vous avez des problèmes spécifiques avec les proxys.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "date.const_fallback": {
        "description": "Permet aux fonctions date/heure d'utiliser des constantes pour le fuseau horaire en cas d'échec de la détection.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "default_mimetypes": {
        "description": "Fichier des types MIME par défaut. Alias de `mime_magic.magicfile` (déprécié).",
        "recommendation": "Utiliser `default_mimetype`.",
        "security_paths": "N/A",
        "options": []
    },
    "detect_unicode": {
        "description": "Détecte si les chaînes Unicode peuvent être utilisées.",
        "recommendation": "Mettez 'On' si vous utilisez des chaînes Unicode.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "disable_classes_old": {
        "description": "Ancienne directive `disable_classes`. Utilisez `disable_classes`.",
        "recommendation": "Ignorer, utiliser `disable_classes`.",
        "security_paths": "N/A",
        "options": []
    },
    "dom.max_element_depth": {
        "description": "Profondeur maximale des éléments dans le parseur DOM.",
        "recommendation": "La valeur par défaut est 2000. Augmentez si vous traitez de très grands documents XML/HTML complexes. Aide à prévenir les attaques DoS.",
        "security_paths": "Peut prévenir les attaques par déni de service (DoS) causées par des documents XML/HTML trop imbriqués.",
        "options": ["2000", "5000", "10000"]
    },
    "enable_dl_old": {
        "description": "Ancienne directive `enable_dl`. Utilisez `enable_dl`.",
        "recommendation": "Ignorer, utiliser `enable_dl`.",
        "security_paths": "N/A",
        "options": []
    },
    "extension_dir_old": {
        "description": "Ancienne directive `extension_dir`. Utilisez `extension_dir`.",
        "recommendation": "Ignorer, utiliser `extension_dir`.",
        "security_paths": "N/A",
        "options": []
    },
    "file_uploads_old": {
        "description": "Ancienne directive `file_uploads`. Utilisez `file_uploads`.",
        "recommendation": "Ignorer, utiliser `file_uploads`.",
        "security_paths": "N/A",
        "options": []
    },
    "filter.default_options_old": {
        "description": "Ancienne directive `filter.default_options`. Utilisez `filter.default_options`.",
        "recommendation": "Ignorer, utiliser `filter.default_options`.",
        "security_paths": "N/A",
        "options": []
    },
    "gd.jpeg_quality": {
        "description": "Qualité par défaut pour l'encodage JPEG (0-100).",
        "recommendation": "Définissez une qualité qui équilibre la taille du fichier et la qualité visuelle (ex: 75-85).",
        "security_paths": "N/A",
        "options": ["75", "80", "85", "90"]
    },
    "gd.png_compression_level": {
        "description": "Niveau de compression PNG (0-9). Plus élevé = meilleure compression, plus lent.",
        "recommendation": "Une valeur de 6-7 est un bon équilibre.",
        "security_paths": "N/A",
        "options": ["0", "6", "7", "9"]
    },
    "ldap.max_time": {
        "description": "Délai d'attente maximum pour les requêtes LDAP (en secondes).",
        "recommendation": "La valeur par défaut (illimité) est souvent acceptable, mais vous pouvez le limiter.",
        "security_paths": "N/A",
        "options": ["-1", "60", "120"]
    },
    "mail.log_old": {
        "description": "Ancienne directive `mail.log`. Utilisez `mail.log`.",
        "recommendation": "Ignorer, utiliser `mail.log`.",
        "security_paths": "N/A",
        "options": []
    },
    "max_input_vars_old": {
        "description": "Ancienne directive `max_input_vars`. Utilisez `max_input_vars`.",
        "recommendation": "Ignorer, utiliser `max_input_vars`.",
        "security_paths": "N/A",
        "options": []
    },
    "memory_limit_old": {
        "description": "Ancienne directive `memory_limit`. Utilisez `memory_limit`.",
        "recommendation": "Ignorer, utiliser `memory_limit`.",
        "security_paths": "N/A",
        "options": []
    },
    "mime_magic.debug": {
        "description": "Active le mode de débogage pour la détection du type MIME.",
        "recommendation": "Mettez 'Off' en production.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "mime_magic.magicfile": {
        "description": "Chemin vers le fichier de données MIME Magic (déprécié).",
        "recommendation": "N/A (utilisez l'extension `fileinfo` à la place).",
        "security_paths": "N/A",
        "options": []
    },
    "mysqli.max_links_old": {
        "description": "Ancienne directive `mysqli.max_links`. Utilisez `mysqli.max_links`.",
        "recommendation": "Ignorer, utiliser `mysqli.max_links`.",
        "security_paths": "N/A",
        "options": []
    },
    "mysql.allow_local_infile": {
        "description": "Permet le chargement de données locales avec `LOAD DATA LOCAL INFILE` (extension MySQL obsolète).",
        "recommendation": "**Mettez 'Off'.** Utilisez `mysqli` ou `PDO` et désactivez cette option.",
        "security_paths": "**CRITIQUE.** Vulnérabilité similaire à `mysqli.allow_local_infile`.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "mysql.allow_persistent": {
        "description": "Permet ou non les connexions persistantes MySQL (extension MySQL obsolète).",
        "recommendation": "Mettez 'Off'. Utilisez `mysqli` ou `PDO`.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "mysql.connect_timeout": {
        "description": "Délai d'attente de connexion MySQL (en secondes) (extension MySQL obsolète).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["60"]
    },
    "mysql.default_host": {
        "description": "Hôte par défaut pour MySQL (extension MySQL obsolète).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["localhost"]
    },
    "mysql.default_password": {
        "description": "Mot de passe par défaut pour MySQL (extension MySQL obsolète).",
        "recommendation": "**Laissez vide.** Ne jamais stocker de mots de passe ici.",
        "security_paths": "**CRITIQUE.**",
        "options": []
    },
    "mysql.default_port": {
        "description": "Port par défaut pour MySQL (extension MySQL obsolète).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["3306"]
    },
    "mysql.default_socket": {
        "description": "Socket par défaut pour MySQL (extension MySQL obsolète).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["/var/run/mysqld/mysqld.sock"]
    },
    "mysql.default_user": {
        "description": "Nom d'utilisateur par défaut pour MySQL (extension MySQL obsolète).",
        "recommendation": "**Laissez vide.** Ne jamais stocker de noms d'utilisateur ici.",
        "security_paths": "**CRITIQUE.**",
        "options": []
    },
    "mysql.max_links": {
        "description": "Nombre maximal de liens MySQL par processus PHP (extension MySQL obsolète).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["-1"]
    },
    "mysql.max_persistent": {
        "description": "Nombre maximal de liens persistants MySQL par processus PHP (extension MySQL obsolète).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["-1"]
    },
    "mysql.trace_mode": {
        "description": "Active le mode de trace MySQL (extension MySQL obsolète).",
        "recommendation": "Mettez 'Off'.",
        "security_paths": "Peut divulguer des requêtes SQL et des informations sensibles.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "odbc.allow_persistent": {
        "description": "Permet ou non les connexions persistantes ODBC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["On", "Off"]
    },
    "odbc.check_dsn": {
        "description": "Vérifie les DSN ODBC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["On", "Off"]
    },
    "odbc.default_cursortype": {
        "description": "Type de curseur ODBC par défaut.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["SQL_CURSOR_FORWARD_ONLY", "SQL_CURSOR_STATIC"]
    },
    "odbc.default_db": {
        "description": "Base de données ODBC par défaut.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "odbc.default_pw": {
        "description": "Mot de passe par défaut pour ODBC (à ne JAMAIS utiliser en production).",
        "recommendation": "**Laissez vide.**",
        "security_paths": "**CRITIQUE.**",
        "options": []
    },
    "odbc.default_user": {
        "description": "Nom d'utilisateur par défaut pour ODBC (à ne JAMAIS utiliser en production).",
        "recommendation": "**Laissez vide.**",
        "security_paths": "**CRITIQUE.**",
        "options": []
    },
    "odbc.max_links": {
        "description": "Nombre maximal de liens ODBC par processus PHP.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["-1"]
    },
    "odbc.max_persistent": {
        "description": "Nombre maximal de liens persistants ODBC par processus PHP.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["-1"]
    },
    "odbc.default_driver": {
        "description": "Pilote ODBC par défaut.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": []
    },
    "open_basedir_safe_mode": {
        "description": "Ancienne directive `open_basedir` combinée au mode sécurisé (déprécié).",
        "recommendation": "Ignorer. Utilisez `open_basedir` et désactivez `safe_mode`.",
        "security_paths": "N/A",
        "options": []
    },
    "pgsql.allow_persistent": {
        "description": "Permet ou non les connexions persistantes PostgreSQL.",
        "recommendation": "Mettez 'On' pour de meilleures performances avec les bases de données. Assurez-vous que votre application gère correctement les connexions.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "pgsql.auto_reset_persistent": {
        "description": "Réinitialise automatiquement les connexions persistantes PostgreSQL après chaque requête.",
        "recommendation": "Mettez 'Off'. Cela annule la plupart des avantages de performance des connexions persistantes.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "pgsql.max_links": {
        "description": "Nombre maximal de liens PostgreSQL par processus PHP.",
        "recommendation": "-1 pour illimité, ou une valeur raisonnable.",
        "security_paths": "Un nombre trop élevé peut être exploité pour des attaques par épuisement de ressources.",
        "options": ["-1", "10", "20", "50"]
    },
    "pgsql.max_persistent": {
        "description": "Nombre maximal de liens persistants PostgreSQL par processus PHP.",
        "recommendation": "-1 pour illimité, ou une valeur raisonnable.",
        "security_paths": "Un nombre trop élevé peut être exploité pour des attaques par épuisement de ressources.",
        "options": ["-1", "10", "20", "50"]
    },
    "post_max_size_parse_ini": {
        "description": "Directive interne liée à `post_max_size` et au parsing de ini.",
        "recommendation": "N/A (géré automatiquement).",
        "security_paths": "N/A",
        "options": []
    },
    "session.bug_compat_42": {
        "description": "Active la compatibilité avec un bug de session de PHP 4.2. **Déprécié.**",
        "recommendation": "**Mettez 'Off'.** Mettez à jour votre code si vous dépendez de ce bug.",
        "security_paths": "Dépendre de bugs obsolètes peut exposer à des comportements imprévus et des failles de sécurité.",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "session.bug_compat_warn": {
        "description": "Affiche un avertissement si le code dépend d'un bug de session obsolète (PHP 4.2).",
        "recommendation": "Mettez 'On' en développement pour détecter les dépendances obsolètes.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "session.entropy_file": {
        "description": "Chemin d'accès à une source d'entropie externe (pour la génération d'ID de session).",
        "recommendation": "Laissez vide. PHP utilise `/dev/urandom` ou ` /dev/random` par défaut, ce qui est suffisant.",
        "security_paths": "Fournir une source d'entropie faible peut rendre les ID de session prévisibles et vulnérables au détournement.",
        "options": ["/dev/urandom", "/dev/random"]
    },
    "session.entropy_length": {
        "description": "Nombre d'octets de l'entropie à lire à partir du fichier d'entropie.",
        "recommendation": "N/A (géré automatiquement si `session.entropy_file` n'est pas défini).",
        "security_paths": "N/A",
        "options": ["0", "16", "32"]
    },
    "session.hash_bits_per_character_old": {
        "description": "Ancienne directive `session.hash_bits_per_character`. Utilisez la nouvelle.",
        "recommendation": "Ignorer, utiliser `session.hash_bits_per_character`.",
        "security_paths": "N/A",
        "options": []
    },
    "session.hash_function_old": {
        "description": "Ancienne directive `session.hash_function`. Utilisez la nouvelle.",
        "recommendation": "Ignorer, utiliser `session.hash_function`.",
        "security_paths": "N/A",
        "options": []
    },
    "session.referer_check_old": {
        "description": "Ancienne directive `session.referer_check`. Utilisez la nouvelle.",
        "recommendation": "Ignorer, utiliser `session.referer_check`.",
        "security_paths": "N/A",
        "options": []
    },
    "session.url_rewriter.tags_old": {
        "description": "Ancienne directive `session.url_rewriter.tags`. Utilisez la nouvelle.",
        "recommendation": "Ignorer, utiliser `session.url_rewriter.tags`.",
        "security_paths": "N/A",
        "options": []
    },
    "soap.wsdl_cache_etag": {
        "description": "Utilise l'ETag HTTP pour valider le cache WSDL.",
        "recommendation": "Mettez 'Off' en production à moins que vous ne soyez sûr que cela ne cause pas de problèmes avec votre configuration.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "sqlite.empty_string_is_null": {
        "description": "Traite les chaînes vides comme NULL pour SQLite (version obsolète de l'extension).",
        "recommendation": "Mettez 'Off'. Ne comptez pas sur ce comportement.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "sqlite.max_memory": {
        "description": "Quantité maximale de mémoire à utiliser par SQLite (version obsolète de l'extension).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["100M"]
    },
    "sqlite.num_columns_to_handle_as_blobs": {
        "description": "Nombre de colonnes à traiter comme des BLOBs par SQLite (version obsolète de l'extension).",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["0"]
    },
    "user_dir_old": {
        "description": "Ancienne directive `user_dir`. Utilisez la nouvelle.",
        "recommendation": "Ignorer, utiliser `user_dir`.",
        "security_paths": "N/A",
        "options": []
    },
    "xmlrpc_error_encoding": {
        "description": "Encodage de caractères pour les erreurs XML-RPC.",
        "recommendation": "N/A",
        "security_paths": "N/A",
        "options": ["UTF-8"]
    },
    "y2k_compliance": {
        "description": "Active la conformité Y2K (déprécié).",
        "recommendation": "Mettez 'Off'. PHP gère correctement les dates postérieures à l'an 2000.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "Off"
    },
    "zend.detect_unicode": {
        "description": "Active la détection d'Unicode par le Zend Engine.",
        "recommendation": "Mettez 'On' si vous utilisez l'Unicode.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "zend.multibyte": {
        "description": "Active le support des caractères multi-octets pour le Zend Engine.",
        "recommendation": "Mettez 'On' si vous utilisez des encodages multi-octets.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "zend.script_encoding": {
        "description": "Encodage par défaut des scripts PHP.",
        "recommendation": "Définissez sur 'UTF-8' pour les applications modernes.",
        "security_paths": "Un encodage incorrect peut entraîner des problèmes d'interprétation et des vulnérabilités.",
        "options": ["UTF-8", "ISO-8859-1"],
        "recommended_prod": "UTF-8"
    },
    "realpath_cache_size_old": {
        "description": "Ancienne directive `realpath_cache_size`. Utilisez la nouvelle.",
        "recommendation": "Ignorer, utiliser `realpath_cache_size`.",
        "security_paths": "N/A",
        "options": []
    },
    "realpath_cache_ttl_old": {
        "description": "Ancienne directive `realpath_cache_ttl`. Utilisez la nouvelle.",
        "recommendation": "Ignorer, utiliser `realpath_cache_ttl`.",
        "security_paths": "N/A",
        "options": []
    },
    "serialize_precision": {
        "description": "Précision de sérialisation des nombres à virgule flottante.",
        "recommendation": "La valeur par défaut (17) est généralement suffisante.",
        "security_paths": "N/A",
        "options": ["17", "14"]
    },
    "session.lazy_write": {
        "description": "Écrit les données de session uniquement si elles ont été modifiées.",
        "recommendation": "Mettez 'On' pour de meilleures performances E/S.",
        "security_paths": "N/A",
        "options": ["On", "Off"],
        "recommended_prod": "On"
    },
    "session.module_name": {
        "description": "Alias de `session.save_handler`.",
        "recommendation": "Utilisez `session.save_handler`.",
        "security_paths": "N/A",
        "options": ["files", "memcached", "redis"]
    },
    "url_rewriter.tags_php": {
        "description": "Tags HTML pour la réécriture d'URL spécifiques à PHP (par défaut ou `url_rewriter.tags`).",
        "recommendation": "Laissez vide et utilisez `session.use_only_cookies = 1`.",
        "security_paths": "Voir `url_rewriter.tags`.",
        "options": ["a=href,area=href,frame=src,input=src,form=action,fieldset="]
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
                        self.original_config[f"__RAW_LINE_{line_num}__"] = {"line_content": line, "type": "raw", "line_num": line_num}
                        self.current_config[f"__RAW_LINE_{line_num}__"] = {"line_content": line, "type": "raw", "line_num": line_num}
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
                        self.original_config[f"__RAW_LINE_{line_num}__"] = {"line_content": line, "type": "raw", "line_num": line_num}
                        self.current_config[f"__RAW_LINE_{line_num}__"] = {"line_content": line, "type": "raw", "line_num": line_num}

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
        
        # Obtenir toutes les directives à afficher, en s'assurant que celles de notre BDD soient en premier
        # et que celles du fichier non reconnues suivent, tout en conservant l'ordre original
        
        # 1. Directives de la BDD, triées alphabétiquement
        directives_to_display = sorted(self.php_ini_directives_info.keys())
        
        # 2. Directives du fichier non reconnues, en gardant l'ordre d'apparition
        unrecognized_directive_names = []
        recognized_directives_set = set(self.php_ini_directives_info.keys())
        
        # Collecter toutes les clés dans l'ordre de leur apparition dans le fichier original
        ordered_original_keys = sorted([k for k, v in self.original_config.items() if "line_num" in v], key=lambda k: self.original_config[k]["line_num"])

        for k in ordered_original_keys:
            if not k.startswith("__RAW_LINE__") and k not in recognized_directives_set and k not in directives_to_display:
                unrecognized_directive_names.append(k)
        
        # Ajouter les directives non reconnues à la liste principale pour l'affichage
        directives_to_display.extend(unrecognized_directive_names)

        displayed_directives_count = 0

        for directive_name in directives_to_display:
            # Skip if it's a raw line marker
            if directive_name.startswith("__RAW_LINE__"):
                continue

            info = self.php_ini_directives_info.get(directive_name) # Info from our knowledge base
            current_value_info = self.current_config.get(directive_name) # Info from the loaded php.ini

            if not current_value_info:
                # If directive is in our knowledge base but not in the loaded php.ini, show it as 'Off'/'Commented' or recommended
                current_value = info.get('recommended_prod', '') if info and info.get('options') else ''
                is_commented = True # Assume commented/inactive if not found
                # Add it to current_config so it can be saved if changed
                self.current_config[directive_name] = {"value": current_value, "commented": is_commented, "original_line": "", "line_num": -1}
                current_value_info = self.current_config[directive_name]
            else:
                current_value = current_value_info["value"]
                is_commented = current_value_info["commented"]

            # Frame pour chaque directive
            directive_frame = ctk.CTkFrame(self.scroll_frame)
            directive_frame.grid(row=row, column=0, columnspan=3, pady=5, padx=5, sticky="ew")
            row += 1
            displayed_directives_count += 1

            # Nom de la directive
            ctk.CTkLabel(directive_frame, text=f"**{directive_name}**", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)

            # Valeur actuelle
            status_text = f"Valeur actuelle: {current_value} ({'Commentée' if is_commented else 'Active'})"
            ctk.CTkLabel(directive_frame, text=status_text).grid(row=1, column=0, sticky="w", padx=5, pady=2)

            # Description, Recommandation, Sécurité
            description = info.get('description', 'Directive non reconnue par l\'outil.') if info else 'Directive non reconnue par l\'outil.'
            recommendation = info.get('recommendation', 'Procédure avec prudence.') if info else 'Procédure avec prudence.'
            security_paths = info.get('security_paths', 'Impact sécurité non spécifié.') if info else 'Impact sécurité non spécifié.'
            options_list = info.get('options', []) if info else []
            recommended_prod_value = info.get('recommended_prod') if info else None

            ctk.CTkLabel(directive_frame, text=f"Description: {description}", wraplength=800, justify="left").grid(row=2, column=0, sticky="w", padx=5, pady=2)

            rec_text = f"**Recommandation:** {recommendation}"
            rec_color = "orange"
            if recommended_prod_value is not None:
                norm_current = str(current_value).lower().replace('on', '1').replace('off', '0').replace('true', '1').replace('false', '0').strip()
                norm_rec = str(recommended_prod_value).lower().replace('on', '1').replace('off', '0').replace('true', '1').replace('false', '0').strip()

                if (norm_current == norm_rec and not is_commented) or \
                   (norm_rec == '0' and is_commented) or \
                   (norm_rec == 'off' and is_commented) or \
                   (norm_rec == '-1' and current_value == '-1' and is_commented): # Handle specific recommended_prod for "commented" state
                    rec_color = "green"
            
            # Special handling for "disable_functions" as it's a list
            if directive_name == "disable_functions" and recommended_prod_value:
                current_functions_set = set(re.split(r'[\s,]+', current_value))
                recommended_functions_set = set(re.split(r'[\s,]+', recommended_prod_value))
                
                if current_functions_set.issuperset(recommended_functions_set) and not is_commented:
                    rec_color = "green"
                elif is_commented: # If it's commented, it's not following recommendation
                    rec_color = "orange"
                
            ctk.CTkLabel(directive_frame, text=rec_text, wraplength=800, justify="left", text_color=rec_color).grid(row=3, column=0, sticky="w", padx=5, pady=2)

            sec_color = "red" if "CRITIQUE" in security_paths else "black"
            ctk.CTkLabel(directive_frame, text=f"**Sécurité:** {security_paths}", wraplength=800, justify="left", text_color=sec_color).grid(row=4, column=0, sticky="w", padx=5, pady=2)

            # Widget de modification
            edit_frame = ctk.CTkFrame(directive_frame)
            edit_frame.grid(row=0, column=1, rowspan=5, padx=10, sticky="nswe")
            edit_frame.grid_columnconfigure(0, weight=1)

            comment_var = ctk.BooleanVar(value=is_commented)
            comment_checkbox = ctk.CTkCheckBox(edit_frame, text="Commenter/Désactiver", variable=comment_var, command=lambda d=directive_name, cv=comment_var: self.toggle_comment(d, cv))
            comment_checkbox.grid(row=0, column=0, pady=5, sticky="w")
            self.widgets[f"comment_{directive_name}"] = comment_var

            if options_list:
                selected_option = ctk.StringVar(value=current_value if current_value in options_list else (str(recommended_prod_value) if recommended_prod_value is not None else options_list[0]))
                option_menu = ctk.CTkOptionMenu(edit_frame, values=[str(x) for x in options_list], variable=selected_option, command=lambda value, d=directive_name: self.update_directive_value(d, value))
                option_menu.grid(row=1, column=0, pady=5, sticky="ew")
                self.widgets[f"value_{directive_name}"] = selected_option
            else:
                entry_value = ctk.StringVar(value=current_value)
                entry = ctk.CTkEntry(edit_frame, textvariable=entry_value)
                entry.grid(row=1, column=0, pady=5, sticky="ew")
                entry_value.trace_add("write", lambda name, index, mode, d=directive_name, ev=entry_value: self.update_directive_value(d, ev.get()))
                self.widgets[f"value_{directive_name}"] = entry_value

            if recommended_prod_value is not None:
                rec_button = ctk.CTkButton(edit_frame, text=f"Appliquer Recommandé ({recommended_prod_value})", command=lambda d=directive_name, val=recommended_prod_value: self.apply_recommended(d, val))
                rec_button.grid(row=2, column=0, pady=5, sticky="ew")

            ctk.CTkFrame(self.scroll_frame, height=2, fg_color="gray").grid(row=row, column=0, columnspan=3, sticky="ew", pady=5)
            row += 1
        
        messagebox.showinfo("Directives Affichées", f"Affichage de {displayed_directives_count} directives.")


    def toggle_comment(self, directive_name, comment_var):
        if directive_name in self.current_config:
            self.current_config[directive_name]["commented"] = comment_var.get()
            # No need to call update_display_after_change directly here, the next save will apply.
            # However, for visual feedback, one could re-render the specific directive's frame.
            # For simplicity in a large list, we're relying on the next "Load" or "Apply Changes" to fully reflect.
        else:
            # Handle cases where a directive is toggled but wasn't originally in current_config
            # This means it's a new directive from our knowledge base that wasn't in the .ini
            info = self.php_ini_directives_info.get(directive_name, {})
            current_value = info.get('recommended_prod', '') if info.get('options') else ''
            self.current_config[directive_name] = {
                "value": current_value,
                "commented": comment_var.get(),
                "original_line": "",
                "line_num": -1 # Indicates it's a new entry
            }


    def update_directive_value(self, directive_name, new_value):
        if directive_name in self.current_config:
            self.current_config[directive_name]["value"] = new_value
        else:
            # Handle cases where a directive is updated but wasn't originally in current_config
            info = self.php_ini_directives_info.get(directive_name, {})
            self.current_config[directive_name] = {
                "value": new_value,
                "commented": False, # Assume it's active if its value is manually set
                "original_line": "",
                "line_num": -1 # Indicates it's a new entry
            }


    def apply_recommended(self, directive_name, recommended_value):
        if directive_name in self.current_config:
            # S'assurer que la directive est décommentée et la valeur est mise à jour
            self.current_config[directive_name]["commented"] = False
            self.current_config[directive_name]["value"] = str(recommended_value) # Assurez-vous que c'est une chaîne

            # Mettre à jour les widgets de l'interface pour la rétroaction visuelle immédiate
            if f"comment_{directive_name}" in self.widgets:
                self.widgets[f"comment_{directive_name}"].set(False) # Décocher la case "Commenter"
            
            if f"value_{directive_name}" in self.widgets:
                widget_var = self.widgets[f"value_{directive_name}"]
                if isinstance(widget_var, ctk.StringVar):
                    widget_var.set(str(recommended_value))
                
            messagebox.showinfo("Recommandation Appliquée", f"La valeur recommandée pour '{directive_name}' a été appliquée : '{recommended_value}'.")
            # For a complex UI with many directives, re-displaying all can be slow.
            # A more refined approach would be to update only the specific directive's display elements.
            # For this example, we'll let the user apply changes and then re-load if they want a full visual update.


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
        # Keep track of directives that were originally present and potentially modified
        processed_original_directives = set() 
        
        # Mapping for quick lookup of directives by their original line number
        original_config_by_line = {v["line_num"]: (k, v) for k, v in self.original_config.items() if "line_num" in v}

        # Iterate through original file line by line to preserve order and comments
        with open(self.php_ini_path, 'r') as f:
            for line_num, line in enumerate(f):
                if line_num in original_config_by_line:
                    directive_name, original_info = original_config_by_line[line_num]

                    if directive_name.startswith("__RAW_LINE__"):
                        # This is an original raw line (comment, section, etc.), just copy it
                        new_lines.append(original_info["line_content"])
                    else:
                        # This is an original directive, check its current state
                        if directive_name in self.current_config:
                            current_info = self.current_config[directive_name]
                            new_line_content = ""
                            if current_info["commented"]:
                                new_line_content = f"; {directive_name} = {current_info['value']}\n"
                            else:
                                new_line_content = f"{directive_name} = {current_info['value']}\n"
                            new_lines.append(new_line_content)
                            processed_original_directives.add(directive_name)
                        else:
                            # This directive was in original_config but somehow not in current_config, keep original
                            new_lines.append(line)
                else:
                    # Line was not in original_config_by_line (shouldn't happen if original_config is built correctly)
                    # Or it's a line that's not a directive or a tracked raw line
                    new_lines.append(line)
        
        # Add directives from current_config that were NOT in the original file
        # (i.e., new directives added from the knowledge base, or directives that were fully missing)
        for directive_name, current_info in self.current_config.items():
            if directive_name.startswith("__RAW_LINE__"):
                continue

            if directive_name not in processed_original_directives and current_info.get("line_num", -1) == -1:
                # This directive was not originally in the file or was added by the GUI
                new_line_content = ""
                if current_info["commented"]:
                    new_line_content = f"; {directive_name} = {current_info['value']}\n"
                else:
                    new_line_content = f"{directive_name} = {current_info['value']}\n"
                
                # Add to the end of the file, or a logical section if we had sections parsing
                # For simplicity, appending to the end
                new_lines.append(f"\n{new_line_content.strip()}\n")


        try:
            with open(self.php_ini_path, 'w') as f:
                f.writelines(new_lines)
            messagebox.showinfo("Succès", "Le fichier php.ini a été mis à jour avec succès.\n\n"
                                          "**N'oubliez pas de redémarrer votre serveur web (Apache/Nginx) ou PHP-FPM** "
                                          "pour que les changements prennent effet !")
            self.load_php_ini() # Re-load to refresh the UI and current_config
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
    