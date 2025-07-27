import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class LinuxFilesystemExplainer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Explorateur Détaillé de l'Arborescence Linux")
        self.geometry("1100x850") # Slightly taller for even more content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Detailed content for Linux directory explanations
        self.linux_directories = {
            "Introduction": {
                "title": "Introduction à l'Arborescence Linux : Tout est Fichier !",
                "text": """
                L'arborescence des fichiers sous Linux est une structure hiérarchique unifiée et logique où **tout est considéré comme un fichier**, y compris les périphériques matériels comme les disques durs, les webcams ou les imprimantes. Elle démarre à son point unique, le **répertoire racine**, représenté par le symbole **`/`**.

                Comprendre cette structure est absolument fondamental pour naviguer efficacement, gérer les permissions d'accès, installer et désinstaller des logiciels, et même dépanner des problèmes sur un système Linux. La plupart des distributions Linux modernes adhèrent à la **Filesystem Hierarchy Standard (FHS)**, une norme qui définit l'objectif et l'emplacement des fichiers et des répertoires pour assurer une cohérence entre les différentes versions de Linux.

                Imaginez une bibliothèque immense et parfaitement organisée : chaque livre a sa place logique et spécifique. L'arborescence Linux est cette structure rigoureuse, garantissant que le système d'exploitation, les applications et les utilisateurs savent toujours où trouver ou stocker ce dont ils ont besoin, rendant le système robuste et prévisible.
                """
            },
            "/ (Racine)": {
                "title": "Le Répertoire Racine : Le Fondement de l'Arborescence",
                "text": """
                Le répertoire **`/`** est le **sommet absolu de l'arborescence**. C'est le parent ultime de tous les autres répertoires, sous-répertoires et fichiers du système. C'est le point de départ de toute exploration du système de fichiers sous Linux.

                **Points clés à retenir :**
                * **Point de Départ Unique :** Tout chemin absolu sous Linux commence obligatoirement par `/`. Par exemple, pour accéder au dossier des documents de votre utilisateur, le chemin sera `/home/votre_nom_utilisateur/Documents`.
                * **Unification des Stockages :** Peu importe le nombre de disques durs physiques, de clés USB, de CD/DVD, ou de partages réseau que vous avez, tous sont "montés" (attachés) comme des sous-répertoires de la racine. Cela crée une vue logique unique du système de fichiers, où l'utilisateur n'a pas besoin de se soucier de l'emplacement physique du fichier.
                * **Disponibilité Essentielle au Démarrage :** Le répertoire racine, ainsi que ses sous-répertoires critiques comme `/bin`, `/etc`, `/lib`, et `/sbin`, doivent être accessibles très tôt dans le processus de démarrage du système. Sans eux, le système ne peut tout simplement pas fonctionner.
                * **Séparateur de Chemin :** Le caractère `/` est aussi utilisé comme séparateur de répertoires dans les chemins (par exemple, `/usr/local/bin`).
                """
            },
            "/bin": {
                "title": "/bin : Commandes Exécutables Essentielles pour Tous",
                "text": """
                Le répertoire **`/bin`** (pour "**bin**aries") contient les commandes exécutables (programmes) essentielles et fondamentales qui sont **utilisées par tous les utilisateurs du système**, y compris l'administrateur **root**.

                **Rôle et Importance :**
                * **Opérations de Base Vitales :** Les commandes présentes ici sont absolument cruciales pour le fonctionnement minimal du système, pour le démarrage (booting) et pour les opérations de dépannage en mode de récupération. Elles doivent être disponibles même si d'autres parties du système de fichiers (comme `/usr`) ne sont pas encore montées.
                * **Accessibilité Universelle :** Les binaires de `/bin` sont généralement inclus dans la variable d'environnement `PATH` de tous les utilisateurs, ce qui signifie que vous pouvez les exécuter en tapant simplement leur nom dans le terminal (par exemple, `ls` au lieu de `/bin/ls`).
                * **Exemples de commandes critiques :**
                    * `ls` : Pour lister le contenu d'un répertoire.
                    * `cp` : Pour copier des fichiers ou des répertoires.
                    * `mv` : Pour déplacer ou renommer des fichiers ou des répertoires.
                    * `mkdir` : Pour créer un nouveau répertoire.
                    * `rm` : Pour supprimer des fichiers ou des répertoires.
                    * `cat` : Pour concaténer et afficher le contenu de fichiers texte.
                    * `echo` : Pour afficher une ligne de texte.
                    * `bash` : L'interpréteur de commandes (shell) Bash.
                    * `mount`, `umount` : Pour monter et démonter des systèmes de fichiers (également présents dans `/usr/bin` ou `/sbin` pour des raisons historiques).

                Sur de nombreuses distributions Linux modernes (comme Debian/Ubuntu), `/bin` est souvent un **lien symbolique** (un raccourci) vers `/usr/bin` afin d'unifier l'emplacement de tous les exécutables utilisateur sous `/usr`.
                """
            },
            "/sbin": {
                "title": "/sbin : Commandes Exécutables Essentielles pour l'Administrateur",
                "text": """
                Le répertoire **`/sbin`** (pour "**s**ystem **bin**aries") contient les commandes exécutables (programmes) essentielles qui sont principalement destinées à être **utilisées par l'administrateur système (utilisateur root)** pour l'administration, la maintenance et le dépannage du système.

                **Rôle et Importance :**
                * **Gestion Système Avancée :** Ces commandes sont vitales pour la configuration du matériel, la gestion du réseau, le démarrage et l'arrêt du système, la gestion des disques et des systèmes de fichiers. Elles sont souvent utilisées pour des tâches qui modifient l'état du système de manière significative.
                * **Accès Restreint :** En règle générale, les utilisateurs ordinaires n'ont pas `/sbin` dans leur `PATH` par défaut. Cela signifie qu'ils doivent soit spécifier le chemin complet de la commande (par exemple, `/sbin/fdisk`), soit utiliser des outils d'élévation de privilèges comme `sudo` (par exemple, `sudo fdisk`) pour exécuter ces commandes, renforçant ainsi la sécurité.
                * **Exemples de commandes critiques :**
                    * `fdisk` : Utilitaire puissant pour gérer les tables de partitions des disques.
                    * `mkfs` : Pour créer des systèmes de fichiers sur des partitions (par exemple, `mkfs.ext4`).
                    * `fsck` : Pour vérifier et réparer l'intégrité des systèmes de fichiers.
                    * `ip` : L'outil de configuration réseau moderne (remplace l'ancien `ifconfig`).
                    * `reboot` : Pour redémarrer le système.
                    * `shutdown` : Pour arrêter le système.
                    * `modprobe` : Pour ajouter ou supprimer des modules du noyau.
                    * `init`, `systemctl` : Pour gérer les processus de démarrage et les services système.

                Similaire à `/bin`, `/sbin` est souvent un **lien symbolique** vers `/usr/sbin` sur les distributions récentes, unifiant l'emplacement de tous les exécutables système sous `/usr`.
                """
            },
            "/etc": {
                "title": "/etc : Le Cœur des Fichiers de Configuration du Système",
                "text": """
                Le répertoire **`/etc`** (historiquement "et cetera", mais maintenant couramment interprété comme "editable text configurations") est un des répertoires les plus cruciaux du système. Il contient **tous les fichiers de configuration spécifiques à la machine locale** pour le système d'exploitation et les applications installées.

                **Rôle et Caractéristiques :**
                * **Fichiers Texte Lisibles :** La grande majorité des fichiers dans `/etc` sont des fichiers texte ASCII, ce qui les rend facilement lisibles et, avec les permissions appropriées, éditables par un administrateur. Ils sont souvent accompagnés de commentaires expliquant leur fonction.
                * **Configurations Statiques :** Les fichiers de configuration sont généralement statiques, c'est-à-dire qu'ils ne sont pas des exécutables binaires et ne changent pas d'eux-mêmes (sauf lors d'une mise à jour logicielle, d'une modification manuelle par l'administrateur, ou par des outils de configuration système).
                * **Personnalisation du Système :** C'est le lieu central où vous personnalisez le comportement de votre système, de la gestion des utilisateurs aux paramètres réseau, en passant par la configuration des services.
                * **Exemples de fichiers et sous-répertoires importants :**
                    * `/etc/passwd` : Contient des informations sur les comptes utilisateurs (noms, IDs, répertoires personnels, shells par défaut).
                    * `/etc/shadow` : Stocke les mots de passe chiffrés des utilisateurs et les informations de vieillissement des mots de passe (avec des permissions très restreintes).
                    * `/etc/fstab` : Définit les systèmes de fichiers qui doivent être montés automatiquement au démarrage du système.
                    * `/etc/resolv.conf` : Configure les serveurs DNS que le système utilise pour résoudre les noms de domaine.
                    * `/etc/hosts` : Contient des mappages manuels entre noms d'hôtes et adresses IP (utilisé avant la consultation des DNS).
                    * `/etc/network/interfaces` ou `/etc/netplan/` : Configurations pour les interfaces réseau.
                    * `/etc/hostname` : Le nom d'hôte du système.
                    * `/etc/crontab`, `/etc/cron.d/`, `/etc/cron.hourly/`, etc. : Fichiers et répertoires pour les tâches planifiées (cron jobs) au niveau du système.
                    * `/etc/apache2/` ou `/etc/nginx/` : Répertoires contenant toutes les configurations détaillées des serveurs web Apache et Nginx.
                    * `/etc/systemd/` ou `/etc/init.d/` : Fichiers de configuration pour les services système gérés par systemd ou System V init.
                    * `/etc/sudoers` : Fichier crucial qui configure quels utilisateurs peuvent utiliser la commande `sudo` et avec quelles permissions. Il doit être édité avec l'outil `visudo`.
                    * `/etc/default/` : Contient des paramètres par défaut pour divers services et scripts de démarrage.
                """
            },
            "/dev": {
                "title": "/dev : Les Fichiers de Périphériques (Tout est Fichier !)",
                "text": """
                Le répertoire **`/dev`** (pour "**dev**ices") contient des **fichiers spéciaux qui représentent les périphériques matériels** connectés au système, ainsi que des pseudo-périphériques. C'est l'incarnation de la philosophie Unix/Linux selon laquelle "tout est fichier" : même votre clavier, votre disque dur ou votre carte réseau sont vus comme des fichiers.

                **Rôle et Caractéristiques :**
                * **Interface Matérielle :** Ces "fichiers" ne sont pas des fichiers de stockage classiques (ils ne contiennent pas de données directement lisibles avec un éditeur de texte), mais sont des interfaces que les programmes utilisent pour interagir avec le matériel sous-jacent via les appels système du noyau.
                * **Types de Fichiers Spéciaux :**
                    * **Fichiers de blocs (b)** : Représentent des périphériques qui transfèrent des données par blocs (taille fixe), typiquement les disques durs entiers (`/dev/sda`, `/dev/nvme0n1`) ou leurs partitions spécifiques (`/dev/sdb1`). Ils permettent un accès direct aux blocs de données.
                    * **Fichiers de caractères (c)** : Représentent des périphériques qui transfèrent des données caractère par caractère (flux de données), comme les ports série (`/dev/ttyS0`), les terminaux (`/dev/tty`, `/dev/pts/0`), ou des générateurs de nombres aléatoires.
                * **Création Dynamique :** La plupart des fichiers de périphériques sont créés et supprimés dynamiquement par le système (`udev` ou `mdev` sur certains systèmes) au fur et à mesure que les périphériques sont détectés, connectés ou déconnectés.
                * **Exemples courants et leur utilisation :**
                    * `/dev/sda`, `/dev/sdb`, etc. : Représentent les disques durs SATA ou SCSI. `/dev/sda1` serait la première partition du premier disque.
                    * `/dev/nvme0n1` : Disques NVMe.
                    * `/dev/cdrom` : Un lien symbolique vers votre lecteur de CD/DVD.
                    * `/dev/null` : Le "trou noir" du système. Toute donnée écrite ici est ignorée. Très utile pour jeter la sortie non désirée des commandes (ex: `commande > /dev/null 2>&1`).
                    * `/dev/zero` : Un périphérique qui fournit un flux continu de caractères "null" (zéros binaires). Utile pour créer des fichiers de taille fixe remplis de zéros (ex: `dd if=/dev/zero of=fichier_vide bs=1M count=100`).
                    * `/dev/random` et `/dev/urandom` : Sources de nombres aléatoires. `/dev/random` est cryptographiquement plus sûr mais peut bloquer si l'entropie est insuffisante, tandis que `/dev/urandom` ne bloque jamais mais est moins "vrai" aléatoire.
                    * `/dev/tty` : Le terminal de contrôle actuel d'où la commande est exécutée.
                    * `/dev/console` : La console système.
                    * `/dev/loop0`, `/dev/loop1`, etc. : Périphériques de bouclage, utilisés pour monter des fichiers image (comme des ISO) comme s'il s'agissait de systèmes de fichiers physiques.
                """
            },
            "/proc": {
                "title": "/proc : Le Système de Fichiers Virtuel pour Processus et Noyau",
                "text": """
                Le répertoire **`/proc`** (pour "**proc**esses") est un **système de fichiers virtuel (procfs)**, une caractéristique unique des systèmes Unix-like. Il ne contient pas de "vrais" fichiers stockés sur le disque dur. Au lieu de cela, les fichiers et répertoires dans `/proc` sont créés dynamiquement par le **noyau Linux** en mémoire au moment de l'accès.

                **Rôle et Caractéristiques :**
                * **Interface Noyau en Temps Réel :** Il fournit une interface en temps réel pour obtenir des informations sur l'état des processus en cours d'exécution, la configuration du noyau, les statistiques système, et les paramètres du matériel. C'est comme une fenêtre ouverte sur l'activité interne du système.
                * **Données Éphémères et Dynamiques :** Les informations dans `/proc` sont toujours à jour et reflètent l'état actuel du système. Elles disparaissent complètement lorsque le système est redémarré, car elles sont générées à la volée.
                * **Lecture et Écriture (pour certains) :** La plupart des fichiers dans `/proc` sont uniquement lisibles. Cependant, certains fichiers sous `/proc/sys/` peuvent être écrits par l'administrateur (avec les permissions root) pour modifier des paramètres du noyau à la volée, sans nécessiter un redémarrage du système. C'est très utile pour des optimisations de performance ou des changements de comportement réseau.
                * **Exemples courants d'informations et d'utilisation :**
                    * `/proc/cpuinfo` : Informations détaillées sur le(s) processeur(s) du système (modèle, fréquence, caches, etc.).
                    * `/proc/meminfo` : Informations complètes sur l'utilisation de la mémoire vive et de la mémoire virtuelle (swap).
                    * `/proc/version` : Version du noyau Linux et informations de compilation.
                    * `/proc/cmdline` : Les paramètres de démarrage passés au noyau lors du boot.
                    * `/proc/uptime` : La durée depuis le dernier démarrage du système.
                    * `/proc/loadavg` : La charge moyenne du système sur 1, 5 et 15 minutes.
                    * `/proc/mounts` : Une liste de tous les systèmes de fichiers actuellement montés.
                    * `/proc/net/dev` : Statistiques détaillées d'utilisation des interfaces réseau.
                    * `/proc/[PID]/` : Pour chaque processus en cours d'exécution, il y a un sous-répertoire numérique (où `[PID]` est l'ID du processus). Ce répertoire contient des informations spécifiques à ce processus (par exemple, `/proc/1234/status` pour son état, `/proc/1234/exe` pour un lien vers son exécutable, `/proc/1234/fd/` pour ses descripteurs de fichiers ouverts).
                    * `/proc/sys/` : Contient des fichiers qui permettent de modifier les paramètres du noyau (par exemple, `echo 1 > /proc/sys/net/ipv4/ip_forward` pour activer le routage IP).
                """
            },
            "/var": {
                "title": "/var : Données Variables des Applications et du Système (Logs, Caches, Spools)",
                "text": """
                Le répertoire **`/var`** (pour "**var**iable") est un des répertoires les plus dynamiques et importants. Il contient les données qui sont **susceptibles de changer fréquemment ou de croître** au cours du fonctionnement normal du système. Contrairement aux configurations statiques de `/etc`, les données de `/var` sont destinées à être écrites régulièrement par les applications et les services.

                **Rôle et Caractéristiques :**
                * **Données Écrites par le Système :** C'est l'endroit où les applications et les services écrivent leurs journaux (logs), leurs caches, leurs files d'attente (spool), et d'autres données transitoires qui doivent persister entre les redémarrages (contrairement à `/tmp`).
                * **Croissance Potentielle :** Le contenu de `/var` peut croître considérablement avec le temps, surtout dans les sous-répertoires de logs. Il est crucial de surveiller l'espace disque de cette partition pour éviter qu'elle ne se remplisse.
                * **Exemples de sous-répertoires importants et leur contenu :**
                    * `/var/log/` : **Le sous-répertoire le plus fréquemment consulté.** Contient tous les fichiers journaux (logs) du système et des applications. C'est la première étape pour le dépannage.
                        * Ex: `syslog` (messages système généraux), `auth.log` (tentatives de connexion, sudo), `kern.log` (messages du noyau), `dmesg` (messages du démarrage du noyau), logs des serveurs web (Apache, Nginx : `/var/log/apache2/`, `/var/log/nginx/`), logs de base de données (MySQL, PostgreSQL).
                    * `/var/www/` : Le répertoire par défaut pour les fichiers des sites web sur de nombreuses distributions (souvent un lien symbolique ou configuré via le serveur web pour pointer vers un autre emplacement).
                    * `/var/lib/` : Contient des informations d'état persistantes pour les programmes et les bibliothèques. C'est là que les applications stockent des données vitales qu'elles utilisent pour fonctionner correctement.
                        * Ex: bases de données SQLite pour certains services, fichiers d'état des gestionnaires de paquets comme `apt` ou `dnf` (`/var/lib/apt/`, `/var/lib/dpkg/`), données pour les serveurs de base de données (MySQL, PostgreSQL).
                    * `/var/mail/` : Boîtes aux lettres des utilisateurs (spool de courrier entrant).
                    * `/var/spool/` : Répertoire pour les données "en attente" d'être traitées par une application.
                        * Ex: files d'attente d'impression (`/var/spool/cups/`), tâches cron en attente d'exécution (`/var/spool/cron/`), courriers électroniques sortants.
                    * `/var/tmp/` : Fichiers temporaires qui sont destinés à persister entre les redémarrages du système (contrairement à `/tmp`, qui est généralement vidé).
                    * `/var/cache/` : Données de cache pour les applications et les gestionnaires de paquets. Ces données peuvent être supprimées sans perdre de données critiques.
                        * Ex: packages téléchargés par `apt` ou `dnf` (`/var/cache/apt/archives/`), caches de navigateur, caches de programmes.
                    * `/var/run/` ou `/run/` : (Souvent un lien symbolique vers `/run` sur les systèmes modernes) Contient des informations d'état d'exécution du système depuis le dernier démarrage, comme les fichiers PID des démons en cours d'exécution. Ces fichiers sont supprimés au redémarrage.
                """
            },
            "/tmp": {
                "title": "/tmp : Fichiers Temporaires Volatiles et Éphémères",
                "text": """
                Le répertoire **`/tmp`** (pour "**temp**orary") est un espace public destiné à stocker des fichiers temporaires créés par des programmes ou des utilisateurs. Il est conçu pour des données à très courte durée de vie.

                **Rôle et Caractéristiques :**
                * **Volatilité :** Le contenu de `/tmp` est **généralement effacé à chaque redémarrage du système**. Sur de nombreux systèmes modernes, `/tmp` est monté en tant que **`tmpfs`** (un système de fichiers basé sur la mémoire vive), ce qui garantit qu'il est vidé au redémarrage et offre des performances accrues (pas d'accès disque).
                * **Accès Universel mais Isolé :** Tous les utilisateurs ont la permission d'écrire dans `/tmp`. Cependant, grâce à un attribut spécial appelé le "**sticky bit**" (permission `t`), un utilisateur ne peut supprimer ou renommer que ses propres fichiers dans `/tmp`, même s'il ne les a pas créés. Cela empêche les utilisateurs de supprimer accidentellement ou intentionnellement les fichiers temporaires des autres.
                * **Ne pas stocker de données importantes :** Étant donné sa nature volatile et temporaire, il ne faut **jamais y stocker des données qui doivent être conservées**. Elles sont garanties d'être perdues.
                * **Utilisations typiques :**
                    * Fichiers de session pour les applications web.
                    * Fichiers intermédiaires lors de la compilation de logiciels.
                    * Données en transit pour des opérations de copie ou de téléchargement.
                    * Emplacement temporaire pour les archives décompressées lors d'installations.
                """
            },
            "/home": {
                "title": "/home : Vos Données Personnelles et Configurations Utilisateur",
                "text": """
                Le répertoire **`/home`** est le point de départ de votre vie numérique sous Linux. Il contient les **répertoires personnels de tous les utilisateurs non-root du système**. Chaque utilisateur (sauf `root`) se voit attribuer son propre sous-répertoire ici, portant généralement son nom d'utilisateur (par exemple, `/home/alice`, `/home/bob`).

                **Rôle et Caractéristiques :**
                * **Espace Personnel et Isolé :** C'est l'endroit principal où les utilisateurs stockent tous leurs documents, images, vidéos, téléchargements, configurations d'applications personnelles, et autres données. C'est votre "bac à sable" où vous avez un contrôle total.
                * **Configurations Personnelles (Fichiers Cachés) :** De nombreux fichiers de configuration spécifiques à l'utilisateur sont stockés dans des répertoires ou des fichiers "cachés" à l'intérieur de votre répertoire personnel. Ces fichiers commencent par un point (`.`) et sont masqués par défaut dans les explorateurs de fichiers (vous pouvez les afficher avec `ls -a` ou Ctrl+H).
                    * Ex: `.bashrc` (configuration du shell Bash), `.zshrc` (configuration du shell Zsh), `.profile` (variables d'environnement utilisateur), `.ssh/` (clés SSH), `.config/` (configurations pour XDG Base Directory Specification), `.local/` (applications et données locales).
                * **Permissions Stricte :** Les permissions sont configurées de manière très stricte : seul l'utilisateur propriétaire a un accès complet (lecture, écriture, exécution) à son propre répertoire personnel. D'autres utilisateurs peuvent avoir des permissions très limitées (lecture seule sur certains fichiers ou dossiers partagés) ou aucune permission, garantissant la confidentialité de vos données.
                * **Séparabilité pour la Stabilité :** Le répertoire `/home` est très souvent placé sur une partition de disque séparée. Cela offre plusieurs avantages :
                    * **Réinstallation Facile :** Permet de réinstaller le système d'exploitation sans perdre les données utilisateur.
                    * **Gestion des Quotas :** Facilite l'application de quotas d'espace disque par utilisateur.
                    * **Sécurité :** Isole les données utilisateur des fichiers système critiques.
                """
            },
            "/root": {
                "title": "/root : Le Répertoire Personnel de l'Administrateur (Super-Utilisateur)",
                "text": """
                Le répertoire **`/root`** est le **répertoire personnel de l'utilisateur `root`**, le super-utilisateur ou administrateur système. Il est délibérément séparé de `/home` (où résident les répertoires des utilisateurs normaux) pour des raisons de sécurité, de stabilité et d'organisation.

                **Rôle et Caractéristiques :**
                * **Indépendance Critiques :** La séparation de `/root` garantit que l'administrateur peut toujours se connecter et effectuer des tâches critiques de maintenance ou de réparation même si la partition `/home` est corrompue, pleine ou inaccessible. `/root` est généralement situé sur la partition racine (`/`).
                * **Accès Hautement Restreint :** Par défaut, seul l'utilisateur `root` a les permissions d'accéder à ce répertoire. Les utilisateurs normaux ne peuvent ni lire, ni écrire, ni exécuter de fichiers dans `/root`. Cela protège les outils et les configurations de l'administrateur d'un accès non autorisé.
                * **Contenu Typique :**
                    * Fichiers de configuration personnels de l'administrateur (ex: `.bashrc` pour le shell de root).
                    * Scripts d'administration et outils personnalisés pour la gestion du système.
                    * Journaux ou fichiers temporaires spécifiques aux tâches de `root`.
                    * Fichiers de sauvegarde critiques ou temporaires utilisés pour la maintenance.
                * **Bonne Pratique :** Il est fortement déconseillé d'utiliser le compte `root` pour les opérations quotidiennes. La pratique recommandée est d'utiliser votre compte utilisateur normal, puis d'utiliser la commande `sudo` pour exécuter des commandes nécessitant des privilèges `root`, ce qui fournit une meilleure traçabilité et une sécurité accrue.
                """
            },
            "/usr": {
                "title": "/usr : Logiciels Partagés et Ressources Utilisateur",
                "text": """
                Le répertoire **`/usr`** (historiquement "Unix System Resources", mais maintenant souvent interprété comme "User System Resources" ou "Universal System Resources") est l'un des plus grands et des plus importants répertoires sous Linux. Il contient la **majorité des exécutables, bibliothèques, documentations, et autres fichiers partagés par les applications installées sur le système**.

                **Rôle et Caractéristiques :**
                * **Statique et Partageable :** Le contenu de `/usr` est censé être **statique** (ne change pas après l'installation, sauf lors des mises à jour logicielles via le gestionnaire de paquets) et **partageable** (il pourrait potentiellement être monté en lecture seule sur plusieurs systèmes clients à partir d'un seul serveur pour économiser de l'espace disque).
                * **Programmes Non Essentiels au Démarrage :** Il abrite la plupart des programmes qui ne sont pas strictement nécessaires au démarrage minimal du système ou à la réparation d'urgence. Ces programmes sont généralement installés et gérés par le système de gestion de paquets de la distribution (apt, yum, pacman, etc.).
                * **Hierarchie Interne Riche :** `/usr` possède sa propre hiérarchie interne qui reflète celle de la racine, mais pour les programmes installés :
                    * `/usr/bin/` : **Exécutables des applications courantes** qui ne sont pas essentiels au démarrage (ex: `firefox`, `libreoffice`, `git`, `python`, `gcc`, `grep`, `find`, `vim`). Sur de nombreuses distributions, `/bin` est un lien symbolique vers celui-ci.
                    * `/usr/sbin/` : Binaires système pour l'administration qui ne sont pas essentiels au démarrage (ex: `sshd`, `nginx`, `rsyslogd`, `networkd`). Sur de nombreuses distributions, `/sbin` est un lien symbolique vers celui-ci.
                    * `/usr/lib/` : **Bibliothèques partagées** (`.so` files) utilisées par les programmes situés dans `/usr/bin` et `/usr/sbin`. Contient également des modules de logiciels et des fichiers d'état qui ne sont pas destinés à être directement manipulés par l'utilisateur.
                    * `/usr/local/` : Très important pour les **logiciels installés manuellement** (souvent compilés à partir des sources) par l'administrateur du système. Cela permet d'éviter les conflits avec les paquets gérés par la distribution, car les fichiers ici ne seront pas écrasés par les mises à jour du système de paquets.
                        * `/usr/local/bin/` : Exécutables installés localement.
                        * `/usr/local/lib/` : Bibliothèques installées localement.
                        * `/usr/local/share/` : Données et documentations partagées pour les programmes locaux.
                    * `/usr/share/` : **(Nouveau détail ci-dessous)**
                    * `/usr/include/` : Fichiers d'en-tête (header files) pour le développement de logiciels en C/C++. Ces fichiers définissent les fonctions et structures des bibliothèques.
                    * `/usr/src/` : Contient le code source (souvent le code source du noyau Linux si installé et des modules additionnels). Utile pour la compilation de modules de noyau ou pour le débogage.
                """
            },
            "/usr/share": {
                "title": "/usr/share : Données Indépendantes de l'Architecture (Documentation, Icônes, Locales)",
                "text": """
                Le répertoire **`/usr/share`** est un sous-répertoire clé de `/usr`. Il contient toutes les **données indépendantes de l'architecture matérielle (arch-independent data)** partagées par les applications installées sur le système.

                **Rôle et Contenu Typique :**
                * **Indépendance de la Plateforme :** Les fichiers ici ne dépendent pas du type de CPU (x86, ARM, etc.) ni de l'ordre des octets (little-endian/big-endian). Ils peuvent être partagés entre différentes architectures si nécessaire.
                * **Ressources Statiques :** Le contenu est généralement statique et ne change que lors des mises à jour logicielles.
                * **Types de Données stockées :**
                    * **`/usr/share/doc/`** : Documentation variée pour les paquets installés (README, CHANGELOG, COPYRIGHT, etc.). Chaque paquet a généralement son propre sous-répertoire.
                    * **`/usr/share/man/`** : Pages de manuel (man pages) pour toutes les commandes et fichiers de configuration du système. C'est votre référence principale pour comprendre l'utilisation des commandes Linux.
                    * **`/usr/share/locale/`** : Fichiers de localisation et de traduction pour les applications, permettant au système d'afficher les messages et les interfaces dans différentes langues.
                    * **`/usr/share/icons/`** : Icônes utilisées par les environnements de bureau et les applications.
                    * **`/usr/share/fonts/`** : Polices de caractères disponibles pour le système.
                    * **`/usr/share/themes/`** : Thèmes visuels pour les environnements de bureau.
                    * **`/usr/share/applications/`** : Fichiers `.desktop` qui décrivent les applications et comment les lancer, utilisés par les lanceurs d'applications des environnements de bureau.
                    * **`/usr/share/backgrounds/`** : Images de fond d'écran par défaut.
                    * **`/usr/share/pixmaps/`** : Petites images bitmap utilisées par les applications.
                    * **`/usr/share/misc/`** : Fichiers divers non classés ailleurs (ex: listes de mots, données de fuseau horaire).

                En résumé, `/usr/share` est un dépôt centralisé pour toutes les ressources non exécutables et non spécifiques à une architecture, rendant le système de fichiers plus organisé et facilitant la gestion des paquets.
                """
            },
            "/opt": {
                "title": "/opt : Paquets Logiciels Optionnels et Autonomes",
                "text": """
                Le répertoire **`/opt`** (pour "**opt**ional") est destiné à l'installation de grands paquets logiciels tiers et autonomes qui ne respectent pas nécessairement la structure FHS habituelle ou qui sont fournis par des vendeurs.

                **Rôle et Caractéristiques :**
                * **Installation Autonome :** Les applications installées ici sont généralement auto-contenues et ne mélangent pas leurs fichiers avec ceux des autres répertoires système (comme `/usr/bin` ou `/usr/lib`). Chaque logiciel a généralement son propre sous-répertoire distinct à l'intérieur de `/opt` (ex: `/opt/google/chrome/`, `/opt/spotify/`, `/opt/zoom/`). Cela signifie qu'une application dans `/opt` est censée contenir tout ce dont elle a besoin pour fonctionner.
                * **Facilite la Désinstallation :** Cette organisation rend l'installation, la mise à jour et la désinstallation de ces logiciels tiers beaucoup plus propre et simple, car tous les fichiers d'une application sont regroupés au même endroit. Il suffit souvent de supprimer le sous-répertoire de l'application.
                * **Logiciels Commerciaux et Manuels :** `/opt` est souvent utilisé par des logiciels propriétaires, des applications qui ne font pas partie des dépôts de paquets standards de la distribution, ou des applications installées manuellement à partir d'archives compressées (tarballs).
                * **Chemin d'Accès :** Bien que les exécutables d'applications dans `/opt` puissent ne pas être directement dans le `PATH` par défaut, les installateurs créent souvent des liens symboliques vers `/usr/local/bin` ou des fichiers `.desktop` pour les rendre facilement accessibles.
                """
            },
            "/mnt": {
                "title": "/mnt : Points de Montage Temporaires pour Systèmes de Fichiers",
                "text": """
                Le répertoire **`/mnt`** (pour "**m**ou**nt**") est un répertoire vide traditionnellement utilisé comme point de montage temporaire pour les systèmes de fichiers.

                **Rôle et Utilisation :**
                * **Montage Manuel et Temporaire :** C'est l'endroit où un administrateur système ou un utilisateur pourrait manuellement monter (attacher) un système de fichiers externe ou une partition de disque pour un accès temporaire. L'idée est que ce répertoire est un point d'accès ponctuel.
                * **Exemples d'utilisation :**
                    * Monter une partition Windows (NTFS) ou macOS (HFS+) existante pour accéder à ses fichiers.
                    * Accéder au contenu d'une autre partition Linux sur le même disque.
                    * Monter un CD/DVD ou une clé USB si le système ne le fait pas automatiquement (par exemple, dans un environnement en ligne de commande sans environnement de bureau).
                    * Monter un partage réseau NFS ou SMB (Samba) depuis un autre serveur.
                * **Différence avec `/media` :** Tandis que `/media` est spécifiquement conçu pour les montages automatiques de périphériques amovibles par le système (généralement via votre environnement de bureau), `/mnt` est plus souvent utilisé pour des montages manuels, ponctuels et plus techniques, comme la récupération de données ou la maintenance.
                * **Exemple de commande :** `sudo mount /dev/sdb1 /mnt/myusb` (montre la première partition du deuxième disque vers le répertoire `/mnt/myusb`). Une fois les opérations terminées, il faut `sudo umount /mnt/myusb`.
                """
            },
            "/media": {
                "title": "/media : Points de Montage pour Périphériques Amovibles Automatiques",
                "text": """
                Le répertoire **`/media`** est le point de montage standard et recommandé pour les **périphériques de stockage amovibles** qui sont montés **automatiquement** par le système (généralement par votre environnement de bureau) lorsque vous les insérez.

                **Rôle et Facilité d'Utilisation :**
                * **Montage Automatique et Convivial :** Lorsque vous insérez une clé USB, un CD/DVD, un appareil photo numérique ou une carte SD, votre environnement de bureau (GNOME, KDE, XFCE, Cinnamon, etc.) crée généralement un sous-répertoire sous `/media` (par exemple, `/media/votre_nom_utilisateur/NOM_DU_PERIPHERIQUE` ou `/media/LABEL_DU_DISQUE`) et y monte automatiquement le périphérique.
                * **Accès Intuitif :** Cela rend l'accès aux données sur ces périphériques très intuitif et "plug-and-play" pour les utilisateurs finaux, sans avoir besoin de commandes de montage manuelles.
                * **Exemples de chemins typiques :**
                    * `/media/utilisateur/cle_usb_de_bob`
                    * `/media/cdrom` (pour un lecteur de CD/DVD)
                    * `/media/disk_externe_sauvegarde`
                * **Standardisation :** L'utilisation de `/media` est une pratique standardisée par la FHS pour améliorer la cohérence et la compatibilité des systèmes Linux.
                * **Différence avec `/mnt` :** La distinction clé est que `/media` est pour les périphériques amovibles et les montages automatiques par l'environnement de bureau, tandis que `/mnt` est pour les montages temporaires manuels à des fins d'administration ou de maintenance.
                """
            },
            "/boot": {
                "title": "/boot : Les Fichiers Essentiels au Démarrage du Système",
                "text": """
                Le répertoire **`/boot`** contient les fichiers absolument essentiels nécessaires au **démarrage (bootstrapping)** du système Linux. Ces fichiers sont lus par le firmware du BIOS/UEFI avant même que le système d'exploitation complet ne soit chargé et fonctionnel.

                **Rôle et Caractéristiques :**
                * **Processus de Démarrage :** `/boot` est le premier point d'entrée pour le système d'exploitation. Il contient tout ce qu'il faut pour charger le noyau et lui permettre de prendre le contrôle du matériel.
                * **Noyau Linux (Kernel) :** C'est ici que se trouve le fichier binaire du **noyau Linux** lui-même. Sans le noyau, le système ne peut pas démarrer.
                * **Chargeur de Démarrage (Bootloader) :** Il contient également les fichiers de configuration et les modules du chargeur de démarrage, le plus couramment **GRUB (GRand Unified Bootloader)** ou l'ancien LILO. Le chargeur de démarrage est le premier programme exécuté par le BIOS/UEFI, et il est responsable de la localisation et du chargement du noyau.
                * **Critique pour la Démarrabilité :** Si des fichiers dans `/boot` sont corrompus, supprimés ou mal configurés, le système ne pourra pas démarrer. Les messages d'erreur à ce stade sont souvent des messages du BIOS/UEFI ou du chargeur de démarrage, pas du système d'exploitation lui-même.
                * **Séparabilité :** `/boot` est souvent placé sur une partition séparée pour diverses raisons :
                    * Peut être une petite partition au début du disque pour être accessible par le BIOS/UEFI.
                    * Peut être en lecture seule après le démarrage pour des raisons de sécurité.
                * **Exemples de fichiers et sous-répertoires critiques :**
                    * `/boot/vmlinuz-...` : Le fichier du noyau Linux (peut avoir différentes versions pour permettre le choix au démarrage).
                    * `/boot/initrd.img-...` ou `/boot/initramfs-...` : Le **disque RAM initial (initial ramdisk)**. C'est un petit système de fichiers compressé qui est chargé en mémoire au début du processus de démarrage. Il contient les pilotes essentiels pour que le noyau puisse accéder et monter le "vrai" système de fichiers racine (par exemple, les pilotes de contrôleur de disque, les modules de système de fichiers comme LVM ou RAID).
                    * `/boot/grub/` : Répertoire contenant tous les fichiers de configuration et les modules du chargeur de démarrage GRUB (par exemple, `grub.cfg`, `grub.efi`).
                    * `/boot/System.map-...` : Un fichier de symboles du noyau, utilisé pour le débogage et l'analyse des crashs du noyau.
                    * `/boot/config-...` : Le fichier de configuration qui a été utilisé lors de la compilation de la version spécifique du noyau.
                """
            },
            "/srv": {
                "title": "/srv : Données des Services Fournis par le Système",
                "text": """
                Le répertoire **`/srv`** (pour "**s**e**rv**ice") est un répertoire défini par la FHS pour contenir les données des services qui sont proposés par le système. Son utilisation est moins universelle que d'autres répertoires, car de nombreux services utilisent encore des emplacements plus traditionnels comme `/var/www` ou des répertoires dans `/home` ou `/opt`.

                **Rôle et Utilisation :**
                * **Données Spécifiques au Service :** L'objectif de `/srv` est de fournir un emplacement structuré et standardisé pour les données spécifiques à un service donné qui sont "servies" (rendues disponibles) aux clients sur le réseau. L'idée est d'isoler les données d'un service donné.
                * **Exemples d'utilisation (selon FHS et pratique occasionnelle) :**
                    * Si vous exécutez un serveur web, les fichiers de votre site web pourraient être placés dans `/srv/www/` (avec un sous-répertoire pour chaque hôte virtuel : `/srv/www/example.com/htdocs/`).
                    * Si vous avez un serveur FTP, les données partagées via FTP pourraient se trouver dans `/srv/ftp/`.
                    * Si vous avez un serveur de contrôle de version (ex: Git, SVN), les dépôts pourraient être dans `/srv/git/` ou `/srv/svn/`.
                * **Rareté Relative :** Bien que définie par la FHS, cette convention n'est pas toujours strictement suivie par toutes les applications ou distributions. Par exemple, Apache et Nginx utilisent souvent `/var/www` par défaut pour leurs fichiers de sites web. Cependant, c'est une option valide et propre pour organiser les données de services de manière claire, surtout dans les environnements où plusieurs services sont hébergés sur le même serveur.
                """
            },
            "/sys": {
                "title": "/sys : Le Système de Fichiers Virtuel pour le Noyau et les Périphériques",
                "text": """
                Le répertoire **`/sys`** (pour "**sys**tem") est un **système de fichiers virtuel (sysfs)**, similaire à `/proc` mais avec un objectif différent. Il ne stocke pas de "vrais" fichiers sur le disque, mais expose une interface en temps réel pour interagir avec le **noyau Linux** et les **périphériques matériels** qu'il gère.

                **Rôle et Caractéristiques :**
                * **Vue du Matériel :** Sysfs présente une vue hiérarchique et structurée de tous les périphériques matériels détectés et gérés par le noyau (bus, contrôleurs, périphériques spécifiques). Il fournit une cartographie détaillée du hardware du système.
                * **Configuration et Information du Noyau :** Il expose également de nombreux paramètres et statistiques du noyau directement liés au matériel et aux pilotes de périphériques.
                * **Gestion des Périphériques à la Volée :** Les utilitaires système et les scripts peuvent lire et, dans certains cas (avec les permissions root), écrire dans ces "fichiers" pour obtenir des informations détaillées sur le matériel ou modifier dynamiquement le comportement des périphériques ou des pilotes sans redémarrage.
                * **Exemples courants d'informations et d'utilisation :**
                    * `/sys/class/` : Contient des informations organisées par classes de périphériques (par exemple, `/sys/class/net` pour les interfaces réseau comme `eth0` ou `wlan0`, `/sys/class/block` pour les périphériques de bloc comme les disques).
                    * `/sys/devices/` : La hiérarchie physique des périphériques matériels découverts par le noyau, organisés par bus et par contrôleur (ex: `pci`, `usb`). C'est une représentation de l'arbre des périphériques du noyau.
                    * `/sys/module/` : Informations sur les modules du noyau actuellement chargés, permettant de voir leurs paramètres ou de les manipuler.
                    * `/sys/power/` : Paramètres de gestion de l'énergie du système (ex: suspendre, hibernat, état de la batterie).
                    * `/sys/fs/` : Informations sur les systèmes de fichiers virtuels montés (comme sysfs lui-même, procfs, cgroupfs).
                    * Modification de la luminosité de l'écran : `echo 500 > /sys/class/backlight/intel_backlight/brightness` (nécessite root).
                    * Activation/désactivation de périphériques : `echo 1 > /sys/bus/usb/devices/1-1/power/control` (pour un périphérique USB).

                **Distinction entre `/proc` et `/sys` :**
                * **`/proc`** est plus général, orienté processus, informations système et paramètres du noyau qui n'ont pas de lien direct avec un périphérique.
                * **`/sys`** est spécifiquement axé sur le **matériel** et les interactions du noyau avec les **périphériques**. Il offre une vue plus structurée et moins "plate" du matériel que certaines informations dispersées dans `/proc`.
                """
            }
        }

        # Sidebar Frame (Larger for more detailed directory names)
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(len(self.linux_directories), weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Arborescence Linux", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Buttons for each section
        self.section_buttons = []
        for i, dir_name in enumerate(self.linux_directories.keys()):
            button = ctk.CTkButton(self.sidebar_frame, text=dir_name,
                                   command=lambda name=dir_name: self.show_section(name),
                                   fg_color=("gray70", "gray25"),
                                   hover_color=("gray60", "gray35"),
                                   anchor="w") # Align text to the left
            button.grid(row=i + 1, column=0, padx=20, pady=6, sticky="ew") # Adjust padding
            self.section_buttons.append(button)

        # Main content Frame
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30) # More padding
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self.main_content_frame, text="", font=ctk.CTkFont(size=28, weight="bold")) # Larger font for title
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 30), sticky="ew") # Adjust padding

        self.text_area = ctk.CTkTextbox(self.main_content_frame, wrap="word", width=750, height=650, font=("Segoe UI", 14), # Adjusted width and font size
                                        activate_scrollbars=True)
        self.text_area.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.configure(state="disabled")

        # Initial display
        self.show_section("Introduction")

    def show_section(self, section_name):
        section_data = self.linux_directories.get(section_name)
        if section_data:
            self.title_label.configure(text=section_data["title"])
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", section_data["text"])
            self.text_area.configure(state="disabled")
            self.text_area.see("1.0")

            # Highlight the active button
            for btn in self.section_buttons:
                if btn.cget("text") == section_name:
                    btn.configure(fg_color=("gray60", "gray40"))
                else:
                    btn.configure(fg_color=("gray70", "gray25"))

if __name__ == "__main__":
    app = LinuxFilesystemExplainer()
    app.mainloop()