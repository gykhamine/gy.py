import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class NginxConfigExplainer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Explorateur de Configuration Nginx Avancé")
        self.geometry("1000x750") # Adjust geometry for more content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Contenu de l'explication de Nginx
        self.nginx_sections = {
            "Introduction": {
                "title": "Introduction à Nginx",
                "text": """
                Nginx (prononcé "engine-x") est un serveur web léger, performant et puissant, un proxy inverse, un équilibreur de charge et un proxy de messagerie. Il est largement utilisé pour servir des sites web à fort trafic grâce à son architecture événementielle asynchrone qui lui permet de gérer de nombreuses connexions simultanées avec une faible consommation de ressources.

                Les fichiers de configuration de Nginx sont généralement situés dans :
                - `/etc/nginx/nginx.conf` (fichier de configuration principal)
                - `/etc/nginx/conf.d/` (pour des configurations spécifiques)
                - `/etc/nginx/sites-available/` et `/etc/nginx/sites-enabled/` (pour les configurations de virtual hosts sur Debian/Ubuntu)

                Comprendre la structure de configuration est essentiel pour exploiter la puissance de Nginx.
                """
            },
            "Directives Globales (Contexte Main)": {
                "title": "Directives Globales (Contexte Main)",
                "text": """
                Ces directives se trouvent en dehors de tout bloc (`events`, `http`, `server`, `location`) et affectent l'ensemble du processus Nginx. Elles sont cruciales pour le comportement général du serveur.

                Exemple de configuration :
                ```nginx
                user www-data; # L'utilisateur sous lequel les processus de travail Nginx s'exécuteront.
                               # Souvent 'nginx' ou 'www-data' selon la distribution.

                worker_processes auto; # Nombre de processus de travail (workers).
                                       # 'auto' est souvent recommandé pour s'adapter au nombre de cœurs CPU.

                pid /run/nginx.pid;    # Fichier PID (identifiant de processus) pour le processus maître Nginx.
                                       # Utilisé par les scripts de démarrage et d'arrêt.

                include /etc/nginx/modules-enabled/*.conf; # Inclut des fichiers de configuration de modules dynamiques.

                worker_rlimit_nofile 8192; # Définit la valeur de l'ulimit -n pour les processus worker.
                                           # Augmente le nombre maximum de fichiers ouverts, important pour de nombreuses connexions.
                ```

                **Explication des Directives :**
                - **`user`**: Définit l'utilisateur et/ou le groupe sous lequel les **processus de travail** Nginx s'exécutent. C'est essentiel pour la sécurité et les permissions sur les fichiers et répertoires que Nginx doit servir ou accéder.
                - **`worker_processes`**: Spécifie le nombre de processus "workers" que Nginx doit lancer. Chaque worker est un processus séparé capable de gérer des milliers de connexions. Régler sur `auto` (ou le nombre de cœurs de votre CPU) maximise l'efficacité en utilisant pleinement les ressources du processeur.
                - **`pid`**: Indique le chemin du fichier où Nginx enregistrera l'ID du processus maître. Ce fichier est utilisé par les outils de gestion du service (comme `systemctl`) pour démarrer, arrêter ou recharger Nginx.
                - **`include`**: Une directive très puissante pour modulariser votre configuration. Elle permet d'insérer le contenu d'autres fichiers de configuration. Souvent utilisée pour inclure des configurations spécifiques (`conf.d/*.conf`) ou des virtual hosts (`sites-enabled/*`).
                - **`worker_rlimit_nofile`**: Définit le nombre maximal de descripteurs de fichiers que chaque processus de travail peut ouvrir. Une valeur trop basse peut limiter le nombre de connexions simultanées que Nginx peut gérer. Une valeur élevée est cruciale pour les serveurs à fort trafic.
                """
            },
            "Bloc Events": {
                "title": "Bloc 'events'",
                "text": """
                Le bloc `events` contient des directives qui affectent la façon dont Nginx gère les connexions.

                Exemple :
                ```nginx
                events {
                    worker_connections 1024; # Définit le nombre maximal de connexions simultanées
                                             # qu'un processus de travail peut ouvrir. (Par défaut: 512).

                    # multi_accept on;       # Si activé, Nginx essaiera d'accepter autant de nouvelles connexions que possible
                                             # après qu'une connexion a été établie.

                    # use epoll;             # Spécifie la méthode de notification des connexions à utiliser.
                                             # Nginx choisit généralement la meilleure méthode automatiquement (ex: epoll sur Linux, kqueue sur FreeBSD/macOS).
                }
                ```

                **Directives clés :**
                - **`worker_connections`**: Le nombre maximal de connexions simultanées que chaque processus de travail Nginx peut gérer. La performance de Nginx est souvent limitée par cette valeur, en combinaison avec `worker_processes` et les limites du système d'exploitation.
                - **`multi_accept`**: Lorsque cette directive est activée, un processus de travail accepte toutes les nouvelles connexions disponibles sur la file d'attente. Si désactivée (par défaut), il n'accepte qu'une seule nouvelle connexion par itération du cycle événementiel.
                - **`use`**: Indique la méthode d'E/S (I/O multiplexing method) que Nginx doit utiliser. Les options courantes incluent `epoll` (Linux), `kqueue` (FreeBSD, macOS), `devpoll`, `select`, etc. Nginx est généralement intelligent et choisit la meilleure méthode pour votre système, donc cette directive est rarement nécessaire.
                """
            },
            "Bloc HTTP": {
                "title": "Bloc 'http'",
                "text": """
                Le bloc `http` est le plus important et contient les directives pour le service HTTP. La plupart de vos configurations de sites web se trouveront à l'intérieur de ce bloc. Il définit les paramètres globaux pour tous les serveurs virtuels.

                Exemple de directives communes :
                ```nginx
                http {
                    sendfile on;       # Active l'envoi direct de fichiers depuis le disque, très efficace.
                    tcp_nopush on;     # Optimisation TCP : envoie les en-têtes et le début du fichier en un seul paquet.
                    tcp_nodelay on;    # Optimisation TCP : désactive le délai de Nagle pour les paquets envoyés.

                    keepalive_timeout 65; # Durée pendant laquelle une connexion keep-alive reste ouverte.

                    types_hash_max_size 2048; # Taille maximale de la table de hachage pour les types MIME.
                    server_tokens off;        # Désactive la divulgation de la version de Nginx dans les en-têtes.

                    include /etc/nginx/mime.types; # Inclut les mappings des types MIME (text/html, image/jpeg, etc.).
                    default_type application/octet-stream; # Type MIME par défaut pour les fichiers inconnus.

                    access_log /var/log/nginx/access.log; # Fichier de journalisation des accès par défaut.
                    error_log /var/log/nginx/error.log warn; # Fichier de journalisation des erreurs par défaut, niveau 'warn'.

                    gzip on; # Active la compression Gzip des réponses.
                    gzip_vary on; # Ajoute l'en-tête Vary: Accept-Encoding.
                    gzip_proxied any; # Compresse aussi pour les requêtes via proxy.
                    gzip_comp_level 6; # Niveau de compression (1-9).
                    gzip_buffers 16 8k; # Nombre et taille des tampons de compression.
                    gzip_http_version 1.1; # Version minimale HTTP pour la compression.
                    gzip_types text/plain text/css application/json application/javascript text/xml application/xml+rss text/javascript image/svg+xml; # Types de fichiers à compresser.

                    include /etc/nginx/conf.d/*.conf;       # Inclut des fichiers de configuration supplémentaires.
                    include /etc/nginx/sites-enabled/*; # Inclut les configurations de virtual hosts.
                }
                ```
                """
            },
            "Bloc Server": {
                "title": "Bloc 'server' (Virtual Host)",
                "text": """
                Le bloc `server` définit un "virtual host" (hôte virtuel), permettant à Nginx de gérer plusieurs sites web sur la même adresse IP et le même port. Chaque bloc `server` correspond généralement à un site web ou une application distincte.

                Exemple :
                ```nginx
                server {
                    listen 80; # Écoute sur le port 80 (HTTP standard).
                    listen [::]:80; # Écoute sur le port 80 pour IPv6.

                    server_name example.com [www.example.com](https://www.example.com); # Nom de domaine(s) pour ce serveur.

                    root /var/www/html/example.com; # Répertoire racine du site.
                    index index.html index.htm index.php; # Fichiers d'index par défaut.

                    location / {
                        try_files $uri $uri/ =404; # Tente de servir le fichier ou le répertoire, sinon renvoie une 404.
                    }

                    error_page 404 /404.html; # Page d'erreur personnalisée pour les 404.
                    location = /404.html {
                        internal; # Marque cette page comme interne, non accessible directement.
                    }

                    # Pour un site HTTPS (souvent dans un bloc server séparé ou dans le même avec listen 443 ssl)
                    # listen 443 ssl;
                    # ssl_certificate /etc/letsencrypt/live/[example.com/fullchain.pem](https://example.com/fullchain.pem);
                    # ssl_certificate_key /etc/letsencrypt/live/[example.com/privkey.pem](https://example.com/privkey.pem);
                }
                ```

                **Directives clés :**
                - **`listen`**: Le port et l'adresse IP sur lesquels le serveur doit écouter. Vous pouvez spécifier IPv4, IPv6, ou même des options comme `default_server` ou `ssl`.
                - **`server_name`**: Le(s) nom(s) de domaine que ce serveur doit traiter. Nginx utilise ce nom pour faire correspondre les requêtes entrantes au bon bloc `server`. Supporte les jokers (`*.example.com`) et les expressions régulières (`~^www\.(?<domain>.+)\.com$`).
                - **`root`**: Le répertoire racine pour les fichiers du site web. Tous les chemins relatifs dans les blocs `location` à l'intérieur de ce `server` seront résolus par rapport à ce `root`.
                - **`index`**: La liste des fichiers que Nginx doit rechercher et servir lorsqu'un répertoire est demandé (par exemple, `example.com/` cherchera `index.html`, puis `index.htm`, etc.).
                - **`error_page`**: Configure des pages HTML personnalisées à afficher pour des codes de statut HTTP spécifiques.
                - **`internal`**: Utilise dans un bloc `location` pour marquer la ressource comme "interne" à Nginx, ce qui signifie qu'elle ne peut pas être accédée directement par un client externe.
                """
            },
            "Bloc Location": {
                "title": "Bloc 'location'",
                "text": """
                Le bloc `location` est utilisé pour définir comment Nginx doit traiter les requêtes pour des URIs spécifiques ou des chemins de fichiers. C'est le cœur de la gestion des requêtes.

                Syntaxe : `location [modificateur] /chemin/ { ... }`

                **Modificateurs de Correspondance (Priorité : `=`, `^~`, `~` / `~*`, sans modificateur) :**
                - **Pas de modificateur (préfixe)** : `location /images/ { ... }`
                  Correspond si l'URI commence par `/images/`. C'est le type de correspondance le plus courant. Si plusieurs locations de préfixe correspondent, Nginx utilise la correspondance la plus longue.
                - **`=` (correspondance exacte)** : `location = /login { ... }`
                  Correspond seulement si l'URI est *exactement* `/login`. Si une correspondance exacte est trouvée, la recherche de location s'arrête immédiatement.
                - **`^~` (préfixe non-regex)** : `location ^~ /static/ { ... }`
                  Si l'URI commence par `/static/`, cette location est utilisée et aucune recherche de regex n'est effectuée. Plus rapide que les regex si le préfixe est une condition forte.
                - **`~` (regex sensible à la casse)** : `location ~ \.php$ { ... }`
                  Correspond si l'URI se termine par `.php`. Les expressions régulières sont évaluées dans l'ordre de leur apparition dans la configuration.
                - **`~*` (regex insensible à la casse)** : `location ~* \.(jpg|jpeg|gif|png)$ { ... }`
                  Correspond aux extensions d'images (JPG, PNG, etc.) sans tenir compte de la casse.

                Exemples de configuration :
                ```nginx
                # Servir les fichiers statiques et gérer la mise en cache
                location /static/ {
                    alias /var/www/html/mysite/static/; # Indique un chemin de système de fichiers différent pour les fichiers.
                    expires 30d; # Cache en navigateur pendant 30 jours.
                    add_header Cache-Control "public, must-revalidate";
                    log_not_found off; # Ne pas logguer les erreurs 404 pour les fichiers non trouvés.
                }

                # Proxy passer les requêtes PHP à un serveur FastCGI (PHP-FPM)
                location ~ \.php$ {
                    include snippets/fastcgi-php.conf; # Inclut des configurations FastCGI par défaut (communes sur Debian/Ubuntu).
                    fastcgi_pass unix:/run/php/php7.4-fpm.sock; # Chemin vers le socket PHP-FPM.
                    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                    fastcgi_read_timeout 300; # Temps d'attente pour la réponse du backend PHP.
                }

                # Redirection d'une ancienne URL
                location = /old-page {
                    return 301 /new-page; # Redirection permanente vers une nouvelle page.
                }

                # Empêche l'accès direct aux fichiers de configuration
                location ~ /\.ht|/\.user\.ini {
                    deny all; # Interdit l'accès à tous les fichiers .ht* et .user.ini.
                }
                ```
                """
            },
            "Gestion des Erreurs et Journalisation": {
                "title": "Gestion des Erreurs et Journalisation",
                "text": """
                Nginx offre des options robustes pour la journalisation des accès et des erreurs, ainsi que pour la gestion des pages d'erreur personnalisées. Ces fonctionnalités sont essentielles pour le débogage, le suivi des performances et la compréhension du comportement de votre serveur.

                Exemple de configuration :
                ```nginx
                http {
                    # ...

                    # Journalisation des accès :
                    # access_log /var/log/nginx/access.log combined; # Le format 'combined' est standard.
                    # access_log off; # Désactiver le log d'accès pour un bloc ou une location spécifique.

                    # Journalisation des erreurs :
                    # error_log /var/log/nginx/error.log warn; # Niveau de log : debug, info, notice, warn, error, crit, alert, emerg.

                    # Définition d'un format de log personnalisé :
                    log_format custom_vhost '$host $remote_addr - $remote_user [$time_local] '
                                            '"$request" $status $body_bytes_sent '
                                            '"$http_referer" "$http_user_agent"';

                    server {
                        # ...
                        access_log /var/log/nginx/mysite_access.log custom_vhost; # Utilise le format personnalisé pour ce serveur.
                        error_log /var/log/nginx/mysite_error.log error; # Log d'erreurs spécifique pour ce site.

                        # Pages d'erreur personnalisées :
                        error_page 404 /custom_404.html; # Redirige les erreurs 404 vers cette page.
                        error_page 500 502 503 504 /50x.html; # Pour les erreurs serveur.

                        location = /custom_404.html {
                            root /usr/share/nginx/html; # Chemin vers votre page 404.
                            internal; # Empêche l'accès direct à cette page par l'utilisateur.
                        }
                        location = /50x.html {
                            root /usr/share/nginx/html;
                            internal;
                        }
                    }
                }
                ```

                **Directives clés :**
                - **`access_log`**: Spécifie le fichier où Nginx enregistre chaque requête entrante. Vous pouvez définir un format de log (par exemple, `combined` pour le format NCSA combiné) ou désactiver la journalisation.
                - **`error_log`**: Définit le fichier où Nginx enregistre les informations sur les erreurs. Le niveau de log (de `debug` à `emerg`) contrôle la quantité de détails enregistrés. `warn` est souvent un bon compromis pour la production.
                - **`log_format`**: Permet de créer des formats de journalisation personnalisés en utilisant diverses variables Nginx (comme `$remote_addr`, `$request`, `$status`, etc.). Très utile pour l'intégration avec des outils d'analyse de logs.
                - **`error_page`**: Permet de configurer Nginx pour afficher une page HTML personnalisée (ou effectuer une redirection interne) lorsqu'un code d'erreur HTTP spécifique se produit (par exemple, 404 Not Found, 500 Internal Server Error).
                - **`internal`**: Dans le contexte d'une `error_page`, la directive `internal` garantit que la page d'erreur personnalisée ne peut être servie qu'à la suite d'une erreur interne de Nginx et non directement par une requête client.
                """
            },
            "Cache et Optimisation des Fichiers Statiques": {
                "title": "Cache et Optimisation des Fichiers Statiques",
                "text": """
                Nginx est excellent pour servir des fichiers statiques et peut grandement améliorer la performance de votre site en gérant la mise en cache côté client et côté serveur.

                Exemple de configuration :
                ```nginx
                http {
                    # ...

                    # Optimisation des performances réseau :
                    sendfile on;       # Active l'envoi direct de fichiers depuis le disque au réseau, sans passer par l'espace utilisateur. Très efficace.
                    tcp_nopush on;     # Utilisé avec 'sendfile', regroupe les petits paquets en un seul pour une meilleure efficacité.
                    tcp_nodelay on;    # Désactive l'algorithme de Nagle, réduisant les latences pour les applications interactives.

                    # Mise en cache côté client (navegateur) pour les fichiers statiques :
                    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2?|ttf|eot|svg)$ {
                        expires 30d; # Demande au navigateur de cacher ces fichiers pendant 30 jours.
                        add_header Cache-Control "public, no-transform"; # Contrôle plus fin de la mise en cache.
                        log_not_found off; # Empêche Nginx de logguer les erreurs 404 pour ces types de fichiers s'ils sont manquants.
                    }

                    # Mise en cache côté serveur (Nginx comme proxy cache) :
                    # Définition du cache (dans le bloc http)
                    # proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_app_cache:10m max_size=10g
                    #                  inactive=60m use_temp_path=off;

                    # Utilisation du cache dans un bloc server/location
                    # server {
                    #     listen 80;
                    #     server_name cached.example.com;
                    #     location / {
                    #         proxy_cache my_app_cache; # Active le cache pour cette location.
                    #         proxy_cache_valid 200 302 10m; # Cache les réponses 200/302 pendant 10 minutes.
                    #         proxy_cache_valid 404 1m; # Cache les 404 pendant 1 minute.
                    #         proxy_cache_use_stale error timeout invalid_header updating http_500 http_502 http_503 http_504; # Sert du contenu périmé si le backend est en panne.
                    #         add_header X-Proxy-Cache $upstream_cache_status; # Ajoute un en-tête pour voir le statut du cache.
                    #         proxy_pass http://backend_application;
                    #     }
                    # }
                }
                ```

                **Directives clés :**
                - **`sendfile`**: Une directive d'optimisation fondamentale pour Nginx. Elle permet au noyau de transférer directement les données d'un fichier à un socket, contournant ainsi la copie des données en mémoire utilisateur. Cela réduit la charge CPU et améliore le débit.
                - **`tcp_nopush` / `tcp_nodelay`**: Ces directives optimisent le comportement de Nginx avec le protocole TCP. `tcp_nopush` est souvent utilisé avec `sendfile` pour s'assurer que les données ne sont envoyées qu'une fois qu'un paquet complet a été assemblé ou que la dernière partie du fichier a été transférée. `tcp_nodelay` désactive l'algorithme de Nagle, ce qui peut améliorer la réactivité pour les petites requêtes mais augmenter légèrement le nombre de paquets.
                - **`expires`**: Contrôle les en-têtes HTTP `Expires` et `Cache-Control` dans les réponses. Cela indique aux navigateurs clients et aux proxys intermédiaires pendant combien de temps ils peuvent conserver une copie d'une ressource en cache avant de devoir la revalider auprès du serveur. Utile pour réduire la charge sur le serveur pour les fichiers statiques.
                - **`add_header`**: Permet d'ajouter des en-têtes HTTP personnalisés aux réponses de Nginx. Très polyvalent pour des raisons de sécurité, de mise en cache ou d'informations.
                - **`log_not_found`**: Si activé (`off`), Nginx ne logguera pas les erreurs 404 pour les fichiers qui ne sont pas trouvés. C'est utile pour les sites avec beaucoup de petites ressources qui peuvent ne pas exister ou pour des raisons d'optimisation de logs.
                - **`proxy_cache_path` / `proxy_cache`**: Ces directives sont utilisées pour configurer et activer la mise en cache des réponses des serveurs backend par Nginx lui-même. Nginx stocke les réponses et les sert directement pour les requêtes ultérieures, réduisant considérablement la charge sur les serveurs d'applications et améliorant les temps de réponse.
                """
            },
            "Proxy Inverse": {
                "title": "Nginx en tant que Proxy Inverse",
                "text": """
                Nginx excelle en tant que proxy inverse, acheminant les requêtes des clients vers un ou plusieurs serveurs backend (par exemple, Node.js, Python Gunicorn, Apache Tomcat). Il agit comme un intermédiaire, protégeant le serveur backend et permettant des optimisations.

                Exemple :
                ```nginx
                server {
                    listen 80;
                    server_name api.example.com;

                    location / {
                        proxy_pass http://localhost:3000; # Fait suivre la requête au serveur backend s'exécutant sur le port 3000.
                                                         # Peut être une adresse IP, un nom de domaine, ou un groupe 'upstream'.

                        proxy_set_header Host $host;     # Conserve l'en-tête Host original de la requête client.
                        proxy_set_header X-Real-IP $remote_addr; # Transmet l'adresse IP réelle du client au backend.
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # Ajoute/met à jour l'en-tête X-Forwarded-For avec l'IP du client et des proxys précédents.
                        proxy_set_header X-Forwarded-Proto $scheme; # Transmet le protocole utilisé par le client (http ou https).
                        proxy_set_header X-Forwarded-Host $host; # Conserve l'hôte original dans un en-tête standard.

                        proxy_redirect off; # Ne pas réécrire les en-têtes de redirection (Location et Refresh) des réponses du backend.

                        proxy_connect_timeout 60s; # Temps d'attente maximum pour établir une connexion avec le serveur proxy.
                        proxy_send_timeout 60s;    # Temps d'attente maximum pour envoyer une requête au serveur proxy.
                        proxy_read_timeout 60s;    # Temps d'attente maximum pour recevoir une réponse du serveur proxy.
                    }
                }
                ```

                **Directives clés pour le proxy inverse :**
                - **`proxy_pass`**: La directive la plus importante pour le proxy inverse. Elle spécifie l'URL du serveur backend (ou d'un groupe `upstream`) vers lequel les requêtes doivent être transférées.
                - **`proxy_set_header`**: Permet à Nginx d'ajouter ou de modifier les en-têtes HTTP de la requête avant de la transmettre au serveur backend. Essentiel pour que le serveur backend puisse identifier l'hôte d'origine, l'adresse IP du client réel, et le protocole utilisé.
                    - `$host`: L'en-tête `Host` de la requête originale.
                    - `$remote_addr`: L'adresse IP du client.
                    - `$proxy_add_x_forwarded_for`: Ajoute l'adresse IP du client à l'en-tête `X-Forwarded-For` existant, créant une chaîne d'IP si plusieurs proxys sont impliqués.
                    - `$scheme`: Le schéma de la requête (HTTP ou HTTPS).
                - **`proxy_redirect`**: Permet à Nginx de réécrire les en-têtes `Location` et `Refresh` dans les réponses du serveur backend. `off` est souvent utilisé si le backend génère des URLs absolues correctes.
                - **`proxy_connect_timeout`**: Le temps maximum qu'une tentative d'établissement d'une connexion avec un serveur proxy en amont attendra.
                - **`proxy_send_timeout`**: Le temps maximum pendant lequel Nginx attendra qu'une réponse soit envoyée au serveur proxy en amont.
                - **`proxy_read_timeout`**: Le temps maximum pendant lequel Nginx attendra qu'une réponse soit reçue du serveur proxy en amont.
                """
            },
            "Équilibrage de Charge (Load Balancing)": {
                "title": "Nginx pour l'Équilibrage de Charge",
                "text": """
                Nginx peut distribuer les requêtes entrantes entre plusieurs serveurs backend pour améliorer la performance, la fiabilité et l'évolutivité de votre application. C'est une fonctionnalité essentielle pour les applications à haute disponibilité.

                Exemple :
                ```nginx
                http {
                    # Définition du groupe de serveurs backend
                    upstream backend_servers {
                        server 192.168.1.100:8080 weight=3; # Serveur backend 1, avec un poids (plus de requêtes).
                        server 192.168.1.101:8080;         # Serveur backend 2.
                        server 192.168.1.102:8080 backup;  # Serveur de secours, utilisé si les autres sont hors service.
                        server 192.168.1.103:8080 down;    # Serveur désactivé (temporairement ou pour maintenance).

                        # Méthodes d'équilibrage de charge :
                        # least_conn; # La requête est envoyée au serveur avec le moins de connexions actives.
                        # ip_hash;    # Basé sur l'IP du client, assure la persistance de session (même client va au même serveur).
                        # round_robin; # Par défaut : distribue les requêtes de manière cyclique.
                        # hash $request_uri consistent; # Basé sur une clé personnalisée (ex: URI) avec consistent hashing.
                        # random; # Sélectionne un serveur aléatoirement.

                        keepalive 32; # Nombre maximum de connexions keep-alive inactives au groupe 'upstream'.
                    }

                    server {
                        listen 80;
                        server_name myapp.example.com;

                        location / {
                            proxy_pass http://backend_servers; # Fait suivre les requêtes au groupe de serveurs défini.
                            proxy_set_header Host $host;
                            proxy_set_header X-Real-IP $remote_addr;
                            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        }
                    }
                }
                ```

                **Directives clés pour l'équilibrage de charge :**
                - **`upstream`**: Définit un groupe de serveurs backend. Vous donnez un nom à ce groupe (ici `backend_servers`) et listez les serveurs qu'il contient.
                - **`server` (dans upstream)**: Chaque directive `server` à l'intérieur du bloc `upstream` spécifie un serveur backend.
                    - **`weight`**: Définit la pondération du serveur (par défaut 1). Un serveur avec un poids plus élevé recevra plus de requêtes.
                    - **`backup`**: Marque le serveur comme un serveur de secours. Il ne recevra des requêtes que si tous les autres serveurs primaires du groupe sont indisponibles.
                    - **`down`**: Marque le serveur comme indisponible. Il ne recevra aucune requête. Utile pour la maintenance.
                - **Méthodes d'équilibrage de charge**:
                    - **`round_robin` (par défaut)**: Les requêtes sont distribuées séquentiellement à chaque serveur du groupe. Simple et efficace pour la plupart des cas.
                    - **`least_conn`**: La requête est envoyée au serveur qui a le moins de connexions actives. Idéal pour les applications où les connexions peuvent être longues.
                    - **`ip_hash`**: L'adresse IP du client est utilisée comme clé de hachage pour déterminer quel serveur doit recevoir la requête. Cela garantit qu'un client donné est toujours dirigé vers le même serveur, ce qui est utile pour la persistance de session.
                    - **`hash key [consistent]`**: Permet d'utiliser une clé de hachage personnalisée (par exemple, une variable Nginx comme `$request_uri` ou `$cookie_name`) pour distribuer les requêtes. `consistent` améliore la stabilité en cas de modification des serveurs.
                    - **`random [least_conn]`**: Sélectionne un serveur aléatoirement. Peut être combiné avec `least_conn` pour une sélection aléatoire parmi les serveurs avec le moins de connexions.
                - **`keepalive` (dans upstream)**: Permet à Nginx de maintenir des connexions persistantes avec les serveurs backend, réduisant la latence et la charge sur les serveurs en évitant la recréation de connexions pour chaque requête.
                """
            },
            "HTTPS et SSL/TLS": {
                "title": "Configuration HTTPS avec SSL/TLS",
                "text": """
                Sécuriser votre site web avec HTTPS est crucial pour la confidentialité des données et la confiance des utilisateurs. Nginx simplifie la configuration SSL/TLS et supporte les certificats de différentes sources.

                Exemple :
                ```nginx
                server {
                    listen 443 ssl; # Écoute sur le port 443 pour HTTPS.
                    listen [::]:443 ssl; # Pour IPv6.

                    server_name example.com [www.example.com](https://www.example.com);

                    # Chemins vers votre certificat SSL et votre clé privée
                    ssl_certificate /etc/letsencrypt/live/[example.com/fullchain.pem](https://example.com/fullchain.pem); # Chemin vers le certificat complet.
                    ssl_certificate_key /etc/letsencrypt/live/[example.com/privkey.pem](https://example.com/privkey.pem); # Chemin vers la clé privée.

                    # Paramètres SSL/TLS recommandés pour la sécurité et la performance :
                    ssl_protocols TLSv1.2 TLSv1.3; # Protocoles TLS à autoriser (ne pas utiliser SSLv3, TLSv1, TLSv1.1).
                    ssl_prefer_server_ciphers on; # Préférer les suites de chiffrement du serveur plutôt que celles du client.
                    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
                                                 # Liste des suites de chiffrement fortes et sécurisées.
                    ssl_session_cache shared:SSL:10m; # Active le cache des sessions SSL pour améliorer les performances (réduction du handshake).
                    ssl_session_timeout 1h;          # Durée de validité du cache de session SSL.
                    ssl_stapling on;                 # Active SSL Stapling (OCSP Stapling) pour accélérer la validation du certificat.
                    ssl_stapling_verify on;          # Vérifie la réponse OCSP.
                    resolver 8.8.8.8 8.8.4.4 valid=300s; # Serveurs DNS pour la résolution OCSP.

                    # Redirection HTTP vers HTTPS (souvent configurée dans un bloc server séparé pour le port 80)
                    # server {
                    #     listen 80;
                    #     server_name example.com [www.example.com](https://www.example.com);
                    #     return 301 https://$host$request_uri; # Redirection permanente.
                    # }

                    location / {
                        # Votre configuration de site web ici
                        root /var/www/html/example.com;
                        index index.html;
                        try_files $uri $uri/ =404;
                    }
                }
                ```

                **Directives clés :**
                - **`listen 443 ssl`**: Indique à Nginx d'écouter sur le port 443 pour les connexions SSL/TLS (HTTPS).
                - **`ssl_certificate`**: Spécifie le chemin vers le fichier de certificat SSL (souvent un `.crt` ou `.pem`).
                - **`ssl_certificate_key`**: Spécifie le chemin vers le fichier de la clé privée SSL (souvent un `.key` ou `.pem`).
                - **`ssl_protocols`**: Définit les versions des protocoles TLS autorisées. Il est crucial d'éviter les versions obsolètes et non sécurisées comme SSLv3, TLSv1.0 et TLSv1.1. `TLSv1.2` et `TLSv1.3` sont les standards actuels.
                - **`ssl_prefer_server_ciphers`**: Si activé, Nginx préférera les suites de chiffrement configurées sur le serveur plutôt que celles proposées par le client. Cela permet de s'assurer que des chiffrements forts sont utilisés.
                - **`ssl_ciphers`**: Liste des suites de chiffrement autorisées. Il est recommandé d'utiliser des listes de chiffrements modernes et robustes pour une sécurité maximale.
                - **`ssl_session_cache` / `ssl_session_timeout`**: Ces directives activent la mise en cache des sessions SSL. Cela permet aux clients de réutiliser les paramètres de session précédemment négociés, ce qui accélère les reconnexions en évitant un nouveau "handshake" TLS complet.
                - **`ssl_stapling` / `ssl_stapling_verify` / `resolver`**: Améliorent la performance et la sécurité en permettant à Nginx de "agrafer" les réponses OCSP (Online Certificate Status Protocol) à ses certificats TLS. Cela permet aux navigateurs de vérifier la révocation du certificat sans faire une requête OCSP séparée, ce qui accélère la connexion.
                """
            },
            "Autres Directives et Astuces Utiles": {
                "title": "Autres Directives et Astuces Utiles",
                "text": """
                Nginx offre une multitude d'autres directives pour affiner son comportement et répondre à des besoins spécifiques.

                - **`return code [text|URL]`** :
                  Renvoie un code de statut HTTP et optionnellement un texte ou une URL de redirection. C'est la méthode préférée pour les redirections simples car elle est plus performante que `rewrite`.
                  Ex: `return 301 https://newdomain.com$request_uri;` (Redirection permanente vers un nouveau domaine)
                  Ex: `return 403 "Accès Interdit";` (Renvoie une erreur 403 avec un message personnalisé)

                - **`rewrite regex replacement [flag]`** :
                  Réécrit l'URI des requêtes. Moins performant que `return` pour les redirections simples, mais très puissant pour des manipulations d'URL complexes basées sur des expressions régulières.
                  Flags:
                  - `last`: Arrête le traitement du jeu de règles actuel et commence un nouveau cycle de recherche de `location` avec l'URI réécrite.
                  - `break`: Arrête le traitement du jeu de règles actuel ; les requêtes sont traitées dans le `location` actuel.
                  - `redirect`: Renvoie une redirection temporaire (302) avec la nouvelle URL.
                  - `permanent`: Renvoie une redirection permanente (301) avec la nouvelle URL.
                  Ex: `rewrite ^/old-path/(.*)$ /new-path/$1 permanent;`

                - **`try_files file ... uri`** :
                  Permet de vérifier l'existence de fichiers ou de répertoires dans l'ordre spécifié, et de servir le premier trouvé, ou de faire une redirection interne ou externe. Très puissant pour les applications monopages (SPA - Single Page Applications) ou les systèmes de gestion de contenu.
                  Ex: `try_files $uri $uri/ /index.html =404;`
                  (Tente de servir l'URI exacte, puis un répertoire avec cet URI, puis `index.html`, sinon renvoie 404).

                - **`limit_req_zone` / `limit_req`** :
                  Permet de limiter le taux de requêtes et de connexions, utile pour se protéger contre les attaques DDoS ou les abus.
                  Ex:
                  ```nginx
                  # Dans le bloc http
                  limit_req_zone $binary_remote_addr zone=mylimit:10m rate=1r/s;

                  # Dans un bloc location
                  location /api/ {
                      limit_req zone=mylimit burst=5 nodelay;
                      proxy_pass http://backend;
                  }
                  ```

                - **`limit_conn_zone` / `limit_conn`** :
                  Limite le nombre de connexions simultanées par IP.
                  Ex:
                  ```nginx
                  # Dans le bloc http
                  limit_conn_zone $binary_remote_addr zone=per_ip:10m;

                  # Dans un bloc server
                  server {
                      limit_conn per_ip 10; # Maximum 10 connexions par IP.
                      # ...
                  }
                  ```

                **Astuces Générales :**
                - **Tester la configuration :** Toujours exécuter `sudo nginx -t` après des modifications pour vérifier la syntaxe.
                - **Recharger Nginx :** Après une modification réussie, utilisez `sudo systemctl reload nginx` (ou `sudo service nginx reload`) pour appliquer les changements sans interrompre les connexions existantes.
                - **Organisation des fichiers :** Utilisez les répertoires `sites-available` et `sites-enabled` (sur Debian/Ubuntu) et des `include` pour une gestion propre de vos virtual hosts.
                - **Variables Nginx :** Nginx fournit de nombreuses variables intégrées (comme `$uri`, `$request_method`, `$remote_addr`, `$http_user_agent`, etc.) qui peuvent être utilisées dans les directives pour des comportements dynamiques.

                Comprendre ces directives avancées vous permettra d'exploiter pleinement la flexibilité et la puissance de Nginx pour vos besoins spécifiques.
                """
            }
        }

        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0) # Wider sidebar
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(len(self.nginx_sections), weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Nginx Explorer", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Buttons for each section
        self.section_buttons = []
        for i, section_name in enumerate(self.nginx_sections.keys()):
            button = ctk.CTkButton(self.sidebar_frame, text=section_name,
                                   command=lambda name=section_name: self.show_section(name),
                                   fg_color=("gray70", "gray25"), # Adjust button colors
                                   hover_color=("gray60", "gray35"))
            button.grid(row=i + 1, column=0, padx=20, pady=8, sticky="ew") # Adjust padding
            self.section_buttons.append(button)

        # Main content Frame
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25) # Adjust padding
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self.main_content_frame, text="", font=ctk.CTkFont(size=26, weight="bold")) # Larger font
        self.title_label.grid(row=0, column=0, padx=15, pady=(15, 25), sticky="ew") # Adjust padding

        self.text_area = ctk.CTkTextbox(self.main_content_frame, wrap="word", width=700, height=600, font=("Cascadia Code", 13), # Adjusted width and font
                                        activate_scrollbars=True)
        self.text_area.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        self.text_area.configure(state="disabled") # Make it read-only

        # Initial display
        self.show_section("Introduction")

    def show_section(self, section_name):
        section_data = self.nginx_sections.get(section_name)
        if section_data:
            self.title_label.configure(text=section_data["title"])
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", section_data["text"])
            self.text_area.configure(state="disabled")
            self.text_area.see("1.0") # Scroll to the top

            # Optional: Highlight the active button
            for btn in self.section_buttons:
                if btn.cget("text") == section_name:
                    btn.configure(fg_color=("gray60", "gray40")) # Active color
                else:
                    btn.configure(fg_color=("gray70", "gray25")) # Default color


if __name__ == "__main__":
    # ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    # ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
    app = NginxConfigExplainer()
    app.mainloop()