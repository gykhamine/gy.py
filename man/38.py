# --- Bibliothèques Nécessaires ---
import customtkinter as ctk
import threading
import queue
import subprocess
import re
import os
import socket

# --- Définition de l'Application Principale ---
class NetworkAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Analyseur Réseau en Temps Réel (tcpdump)")
        self.master.geometry("1400x750") # Taille ajustée car plus d'onglets

        # --- Variables d'État de l'Application ---
        self.packet_queue = queue.Queue()
        self.sniffing = False
        self.packet_count = 0
        self.tcpdump_process = None
        self.local_ip = None # Pour IPv4
        self.local_ipv6 = None # Pour IPv6

        # --- Éléments de l'Interface Utilisateur (UI) ---

        # Cadre supérieur pour les contrôles et le statut
        self.top_frame = ctk.CTkFrame(master)
        self.top_frame.pack(pady=10, padx=10, fill="x")

        # Configuration des colonnes pour aligner les éléments du haut
        self.top_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        # 1. Section de Sélection d'Interface
        self.interface_label = ctk.CTkLabel(self.top_frame, text="Interface:")
        self.interface_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.available_interfaces = self.get_available_interfaces()
        self.interface_combobox = ctk.CTkComboBox(self.top_frame, values=self.available_interfaces, width=120)
        if self.available_interfaces:
            self.interface_combobox.set(self.available_interfaces[0])
        else:
            self.interface_combobox.set("Aucune interface trouvée")
            self.interface_combobox.configure(state="disabled")
        self.interface_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # 2. Section des Filtres tcpdump (par type)
        # Filtre par Hôte
        self.host_filter_label = ctk.CTkLabel(self.top_frame, text="Hôte:")
        self.host_filter_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.host_filter_entry = ctk.CTkEntry(self.top_frame, width=120, placeholder_text="ex: 192.168.1.1 ou google.com")
        self.host_filter_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Filtre par Port
        self.port_filter_label = ctk.CTkLabel(self.top_frame, text="Port:")
        self.port_filter_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.port_filter_entry = ctk.CTkEntry(self.top_frame, width=80, placeholder_text="ex: 80 ou 443")
        self.port_filter_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        # Filtre par Protocole
        self.protocol_filter_label = ctk.CTkLabel(self.top_frame, text="Protocole:")
        self.protocol_filter_label.grid(row=0, column=6, padx=5, pady=5, sticky="w")
        self.protocol_filter_entry = ctk.CTkEntry(self.top_frame, width=80, placeholder_text="ex: tcp, udp, icmp")
        self.protocol_filter_entry.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

        # Boutons de Contrôle
        self.start_button = ctk.CTkButton(self.top_frame, text="Démarrer", command=self.start_sniffing)
        self.start_button.grid(row=0, column=8, padx=10, pady=5, sticky="e")

        self.stop_button = ctk.CTkButton(self.top_frame, text="Arrêter", command=self.stop_sniffing, state="disabled")
        self.stop_button.grid(row=0, column=9, padx=10, pady=5, sticky="e")

        # Libellé d'État (placé sous les contrôles)
        self.status_label = ctk.CTkLabel(self.top_frame, text="Statut: Inactif")
        self.status_label.grid(row=1, column=0, columnspan=10, padx=10, pady=5, sticky="w")


        # Cadre principal pour les deux zones de texte (entrant/sortant)
        self.main_display_frame = ctk.CTkFrame(master)
        self.main_display_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.main_display_frame.grid_columnconfigure(0, weight=1)
        self.main_display_frame.grid_columnconfigure(1, weight=1)
        self.main_display_frame.grid_rowconfigure(0, weight=1)

        # --- Cadre pour les paquets ENTRANTS ---
        self.incoming_frame = ctk.CTkFrame(self.main_display_frame)
        self.incoming_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.incoming_frame.grid_rowconfigure(1, weight=1)
        self.incoming_frame.grid_columnconfigure(0, weight=1)

        self.incoming_label = ctk.CTkLabel(self.incoming_frame, text="Paquets Entrants", font=ctk.CTkFont(size=14, weight="bold"))
        self.incoming_label.grid(row=0, column=0, pady=5)
        self.incoming_textbox = ctk.CTkTextbox(self.incoming_frame, width=650, height=500, font=("Cascadia Mono", 10))
        self.incoming_textbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # --- Cadre pour les paquets SORTANTS ---
        self.outgoing_frame = ctk.CTkFrame(self.main_display_frame)
        self.outgoing_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.outgoing_frame.grid_rowconfigure(1, weight=1)
        self.outgoing_frame.grid_columnconfigure(0, weight=1)

        self.outgoing_label = ctk.CTkLabel(self.outgoing_frame, text="Paquets Sortants", font=ctk.CTkFont(size=14, weight="bold"))
        self.outgoing_label.grid(row=0, column=0, pady=5)
        self.outgoing_textbox = ctk.CTkTextbox(self.outgoing_frame, width=650, height=500, font=("Cascadia Mono", 10))
        self.outgoing_textbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")


        # --- Boucle de Mise à Jour de l'Interface ---
        self.master.after(100, self.update_ui)

        # --- Expressions Régulières pour l'Analyse des Paquets ---
        # Regex principale pour les paquets IP standard (avec ou sans port), gère IPv4 et IPv6
        self.packet_standard_regex = re.compile(
            r'(\d{2}:\d{2}:\d{2}\.\d{6})\s+'      # Groupe 1: Horodatage
            r'(?:IP|IP6)?\s*'                     # Non-capturant: "IP" ou "IP6" (peut être absent)
            r'([\w\d\.-]+(?::\d+)?)\s+>\s+'       # Groupe 2: Source (IP/nom de domaine, avec port optionnel)
            r'([\w\d\.-]+(?::\d+)?):\s+'          # Groupe 3: Destination (IP/nom de domaine, avec port optionnel)
            r'([\w\d]+)'                         # Groupe 4: Protocole (e.g., TCP, UDP, ICMP, etc.)
        )
        
        # Regex pour les paquets Ethertype IPv4 détaillés (incluant les adresses MAC et l'IP)
        # Capture l'horodatage, MAC Src, MAC Dst, IP Src, IP Dst, et TOUT LE RESTE DE LA LIGNE comme 'full_details_raw'
        self.eth_ipv4_detailed_regex = re.compile(
            r'(\d{2}:\d{2}:\d{2}\.\d{6})\s+'                   # 1: Horodatage
            r'([0-9a-fA-F:]+)\s+>\s+([0-9a-fA-F:]+),\s+'      # 2: MAC Src, 3: MAC Dst
            r'ethertype\s+IPv4\s+\(0x0800\),\s+length\s+\d+:\s+' # Assure Ethertype IPv4
            r'([\d\.]+)(?::\d+)?\s*>\s*([\d\.]+)(?::\d+)?(?:,\s*\S+)?:\s*' # 4: IP Src, 5: IP Dst, (?:,\s*\S+)? pour consommer le protocole éventuel entre IP et :)
            r'(.*)'                                           # 6: TOUT LE RESTE DE LA LIGNE (sera analysé pour le protocole et les détails)
        )

        # Regex pour les paquets Ethertype IPv6 détaillés (incluant les adresses MAC et l'IPv6)
        # Capture l'horodatage, MAC Src, MAC Dst, IPv6 Src, IPv6 Dst, et TOUT LE RESTE DE LA LIGNE comme 'full_details_raw'
        self.eth_ipv6_detailed_regex = re.compile(
            r'(\d{2}:\d{2}:\d{2}\.\d{6})\s+'                  # 1: Horodatage
            r'([0-9a-fA-F:]+)\s+>\s+([0-9a-fA-F:]+),\s+'     # 2: MAC Src, 3: MAC Dst
            r'ethertype\s+IPv6\s+\(0x86dd\),\s+length\s+\d+:\s+' # Assure Ethertype IPv6
            r'(?:.*?)\s*'                                     # Non-capturant: Informations IPv6 intermédiaires (flowlabel, hlim, etc.)
            r'([\w\d\.:]+)\s*>\s*([\w\d\.:]+)(?:,\s*\S+)?:\s*' # 4: IP Src, 5: IP Dst, (?:,\s*\S+)? pour consommer le protocole éventuel entre IP et :)
            r'(.*)'                                          # 6: TOUT LE RESTE DE LA LIGNE (sera analysé pour le protocole et les détails)
        )

        # Regex pour détecter le début d'une nouvelle trame dans la sortie tcpdump -x
        self.new_frame_start_regex = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{6})\s+(.*)')
        # Regex pour les lignes de données hexadécimales (offset et hex/ASCII)
        self.hex_data_line_regex = re.compile(r'^\s*0x([0-9a-f]+)\:\s+([0-9a-f\s]{2,})\s+(.*)$')


    # ---
    # ### Méthodes Utilitaires (Interaction Système et Parsing)
    # ---

    def get_available_interfaces(self):
        interfaces = []
        try:
            process = subprocess.run(['sudo', 'tcpdump', '-D'],
                                     capture_output=True, text=True, check=True, timeout=5)
            for line in process.stdout.splitlines():
                if line.strip() and not line.startswith('tcpdump:'):
                    parts = line.split('.')
                    if len(parts) > 1:
                        interface_name = parts[1].split(' ')[0]
                        interfaces.append(interface_name)
        except FileNotFoundError:
            print("Erreur: La commande 'tcpdump' est introuvable. Impossible de lister les interfaces.")
            return ["eth0", "wlan0", "lo"]
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'appel à tcpdump -D (vérifiez les permissions sudo): {e.stderr}")
            return ["eth0", "wlan0", "lo"]
        except Exception as e:
            print(f"Une erreur inattendue est survenue lors de la récupération des interfaces: {e}")
            return ["eth0", "wlan0", "lo"]

        return sorted(list(set(interfaces)))

    def get_local_ips(self, interface):
        """
        Tente d'obtenir les adresses IP locales (IPv4 et IPv6) de l'interface spécifiée.
        """
        local_ipv4 = None
        local_ipv6 = None
        try:
            # Essai avec socket pour IPv4
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) # Connecte à une IP publique pour obtenir l'IP de sortie
            local_ipv4 = s.getsockname()[0]
            s.close()
        except socket.error:
            pass # On continue pour essayer 'ip address'

        try:
            # Essai avec 'ip address' pour toutes les IPs
            result = subprocess.run(['ip', '-o', 'address', 'show', interface], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    ipv4_match = re.search(r'inet\s+([\d.]+)/\d+', line)
                    if ipv4_match:
                        local_ipv4 = ipv4_match.group(1)
                    ipv6_match = re.search(r'inet6\s+([0-9a-fA-F:]+)/\d+', line)
                    # Ignore les adresses link-local (fe80::) sauf si c'est la seule
                    if ipv6_match and not ipv6_match.group(1).lower().startswith('fe80:'):
                        local_ipv6 = ipv6_match.group(1).split('%')[0] # Enlève le scope ID
                    elif ipv6_match and not local_ipv6: # Si c'est la seule IPv6, prends même fe80
                        local_ipv6 = ipv6_match.group(1).split('%')[0] # Enlève le scope ID
        except Exception as e:
            print(f"Erreur lors de la récupération des IPs locales avec 'ip address': {e}")

        # Fallback pour des valeurs par défaut si rien n'est trouvé
        if not local_ipv4:
            local_ipv4 = "127.0.0.1"
        if not local_ipv6:
            local_ipv6 = "::1" # Loopback IPv6 par défaut

        return local_ipv4, local_ipv6

    def parse_packet_header(self, line):
        """
        Analyse une ligne d'en-tête de paquet et extrait les informations principales.
        Retourne le type de paquet, les infos parsées (dict) et le type de flux.
        """
        # --- 1. Tentative de parsing pour les paquets Ethertype IPv4 détaillés ---
        eth_ipv4_match = self.eth_ipv4_detailed_regex.search(line)
        if eth_ipv4_match:
            timestamp, mac_src, mac_dst, ip_src, ip_dst, full_details_raw = eth_ipv4_match.groups()
            
            protocol = "Inconnu"
            details = full_details_raw.strip()
            if details:
                if details.startswith('[') and ']' in details:
                    parts_after_bracket = details.split(']', 1)
                    if len(parts_after_bracket) > 1:
                        details_after_bracket = parts_after_bracket[1].strip()
                        if details_after_bracket:
                            protocol = details_after_bracket.split(' ')[0].strip().replace(',', '')
                            details = details_after_bracket
                else:
                    protocol = details.split(' ')[0].strip().replace(',', '')
            
            protocol = re.sub(r':\d+|^\d+$', '', protocol).strip()
            if not protocol:
                protocol = "Inconnu"

            flow_type = "UNKNOWN"
            if self.local_ip:
                if ip_src == self.local_ip:
                    flow_type = "PACKET_OUT"
                elif ip_dst == self.local_ip:
                    flow_type = "PACKET_IN"

            parsed_info = {
                "Horodatage": timestamp,
                "MAC Source": mac_src,
                "MAC Destination": mac_dst,
                "EtherType": "IPv4",
                "IP Source": ip_src,
                "IP Destination": ip_dst,
                "Protocole": protocol,
                "Détails": details,
                "HexData": [] # Initialisation de la liste pour les données hex
            }
            return ("PACKET_DETAILED_IPV4", parsed_info, flow_type)

        # --- 2. Tentative de parsing pour les paquets Ethertype IPv6 détaillés ---
        eth_ipv6_match = self.eth_ipv6_detailed_regex.search(line)
        if eth_ipv6_match:
            timestamp, mac_src, mac_dst, ip_src, ip_dst, full_details_raw = eth_ipv6_match.groups()

            protocol = "Inconnu"
            details = full_details_raw.strip()
            if details:
                if details.startswith('[') and ']' in details:
                    parts_after_bracket = details.split(']', 1)
                    if len(parts_after_bracket) > 1:
                        details_after_bracket = parts_after_bracket[1].strip()
                        if details_after_bracket:
                            protocol = details_after_bracket.split(' ')[0].strip().replace(',', '')
                            details = details_after_bracket
                    else:
                        protocol = details.split(' ')[0].strip().replace(',', '')
                
                protocol = re.sub(r':\d+|^\d+$', '', protocol).strip()
                if not protocol:
                    protocol = "Inconnu"

            flow_type = "UNKNOWN"
            if self.local_ipv6:
                if not ip_src.lower().startswith("ff") and self.local_ipv6 and ip_src.startswith(self.local_ipv6):
                    flow_type = "PACKET_OUT"
                elif not ip_dst.lower().startswith("ff") and self.local_ipv6 and ip_dst.startswith(self.local_ipv6):
                    flow_type = "PACKET_IN"
                else:
                    flow_type = "PACKET_OTHER"

            parsed_info = {
                "Horodatage": timestamp,
                "MAC Source": mac_src,
                "MAC Destination": mac_dst,
                "EtherType": "IPv6",
                "IP Source": ip_src,
                "IP Destination": ip_dst,
                "Protocole": protocol,
                "Détails": details,
                "HexData": [] # Initialisation de la liste pour les données hex
            }
            return ("PACKET_DETAILED_IPV6", parsed_info, flow_type)

        # --- 3. Tentative de parsing avec la regex principale (IP, TCP/UDP/ICMP) ---
        standard_match = self.packet_standard_regex.search(line)
        if standard_match:
            timestamp, src_addr, dst_addr, protocol = standard_match.groups()
            flow_type = "UNKNOWN"

            src_ip_only = src_addr.split(':')[0]
            dst_ip_only = dst_addr.split(':')[0]

            if '.' in src_ip_only and self.local_ip:
                if src_ip_only == self.local_ip:
                    flow_type = "PACKET_OUT"
                elif dst_ip_only == self.local_ip:
                    flow_type = "PACKET_IN"
            elif ':' in src_ip_only and self.local_ipv6:
                if not src_ip_only.lower().startswith("ff") and self.local_ipv6 and src_ip_only.startswith(self.local_ipv6):
                    flow_type = "PACKET_OUT"
                elif not dst_ip_only.lower().startswith("ff") and self.local_ipv6 and dst_ip_only.startswith(self.local_ipv6):
                    flow_type = "PACKET_IN"
                else:
                    flow_type = "PACKET_OTHER"

            parsed_info = {
                "Horodatage": timestamp,
                "Source": src_addr,
                "Destination": dst_addr,
                "Protocole": protocol,
                "HexData": [] # Initialisation de la liste pour les données hex
            }
            return ("PACKET_STANDARD", parsed_info, flow_type)

        return ("UNPARSED_HEADER", None, None) # Si ce n'est pas un en-tête de paquet reconnu


    # ---
    # ### Logique de Capture Réseau (Threadée)
    # ---

    def run_tcpdump(self, interface):
        self.local_ip, self.local_ipv6 = self.get_local_ips(interface)
        local_ip_str = self.local_ip if self.local_ip and self.local_ip != "127.0.0.1" else "non détectée ou loopback"
        local_ipv6_str = self.local_ipv6 if self.local_ipv6 and self.local_ipv6 != "::1" else "non détectée ou loopback"
        self.packet_queue.put(("STATUS", f"IPs locales détectées sur {interface}: IPv4={local_ip_str}, IPv6={local_ipv6_str}. (utilisées pour différencier les flux)"))

        filters = []
        host_filter = self.host_filter_entry.get().strip()
        port_filter = self.port_filter_entry.get().strip()
        protocol_filter = self.protocol_filter_entry.get().strip()

        if host_filter:
            filters.append(f"host {host_filter}")
        if port_filter:
            filters.append(f"port {port_filter}")
        if protocol_filter:
            filters.append(f"proto {protocol_filter}")

        # --- IMPORTANT : Ajout de -x pour la vue hexadécimale ---
        command = ['sudo', 'tcpdump', '-l', '-n', '-e', '-i', interface, '-s', '0', '-vv', '-x']
        if filters:
            full_filter_expression = " and ".join(filters)
            command.extend(full_filter_expression.split())
            self.packet_queue.put(("STATUS", f"Filtres appliqués: '{full_filter_expression}'"))
        else:
            self.packet_queue.put(("STATUS", "Aucun filtre spécifié. Capture de tout le trafic."))


        try:
            self.tcpdump_process = subprocess.Popen(command,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    text=True,
                                                    bufsize=1)
            self.packet_queue.put(("STATUS", f"Démarrage de tcpdump sur {interface}..."))

            current_packet_data = None # Pour stocker les détails du paquet en cours de traitement
            
            for line in self.tcpdump_process.stdout:
                if not self.sniffing:
                    break

                # --- Détection de début de nouveau paquet ---
                new_frame_start_match = self.new_frame_start_regex.match(line)
                
                if new_frame_start_match:
                    # Si nous traitions déjà un paquet, le mettre dans la queue avant de commencer le nouveau
                    if current_packet_data:
                        self.packet_queue.put(current_packet_data)
                        self.packet_count += 1
                    
                    # Tenter de parser l'en-tête du nouveau paquet
                    packet_type, parsed_info, flow_type = self.parse_packet_header(line)
                    if parsed_info: # Si c'est un en-tête de paquet reconnu
                        current_packet_data = (packet_type, parsed_info, flow_type)
                    else: # Ligne d'en-tête non parsée (ex: ARP, IPv6 non pris en charge)
                        # Pour les paquets non parsés, on stocke la ligne brute et une liste HexData vide
                        current_packet_data = ("RAW_PACKET_HEADER", {"RawLine": line.strip(), "HexData": []}, "UNKNOWN")
                        
                else:
                    # --- Si ce n'est pas le début d'un nouveau paquet, vérifie si c'est une ligne hex ---
                    hex_data_match = self.hex_data_line_regex.match(line)
                    if hex_data_match:
                        if current_packet_data and "HexData" in current_packet_data[1]: # Assurez-vous que nous avons un paquet en cours et une place pour l'hex
                            current_packet_data[1]["HexData"].append(line.strip())
                        # else: Ligne hexadécimale sans en-tête précédent connu, on l'ignore.
                    elif line.strip(): # Si la ligne n'est pas vide et n'est ni en-tête ni hex
                        # Cela pourrait être des lignes de détails supplémentaires sous l'en-tête
                        # dans un format que tcpdump -vv -x ne met pas sur la ligne d'en-tête.
                        # Pour l'instant, nous ignorons ces lignes "intermédiaires" si elles ne sont pas hex.
                        pass


            # Après la boucle, si un paquet est en cours, il faut l'ajouter à la queue
            if current_packet_data:
                self.packet_queue.put(current_packet_data)
                self.packet_count += 1

            stderr_output = self.tcpdump_process.stderr.read()
            if stderr_output:
                self.packet_queue.put(("ERROR", f"Erreur tcpdump: {stderr_output.strip()}"))

        except FileNotFoundError:
            self.packet_queue.put(("ERROR", "Erreur: La commande 'tcpdump' est introuvable. Veuillez l'installer."))
        except Exception as e:
            self.packet_queue.put(("ERROR", f"Erreur lors de l'exécution de tcpdump: {e}"))
        finally:
            if self.tcpdump_process:
                self.tcpdump_process.terminate()
                self.tcpdump_process.wait()
            self.sniffing = False
            self.packet_queue.put(("STATUS", "Processus tcpdump terminé."))


    # ---
    # ### Gestion des Actions Utilisateur (Boutons)
    # ---

    def start_sniffing(self):
        if not self.sniffing:
            interface = self.interface_combobox.get().strip()
            if not interface or interface == "Aucune interface trouvée":
                self.status_label.configure(text="Erreur: Veuillez sélectionner une interface valide.")
                return

            self.sniffing = True
            self.packet_count = 0
            self.incoming_textbox.delete("1.0", "end")
            self.outgoing_textbox.delete("1.0", "end")
            self.status_label.configure(text=f"Statut: Capture en cours sur {interface}...")

            self.start_button.configure(state="disabled")
            self.interface_combobox.configure(state="disabled")
            self.host_filter_entry.configure(state="disabled")
            self.port_filter_entry.configure(state="disabled")
            self.protocol_filter_entry.configure(state="disabled")
            self.stop_button.configure(state="normal")

            self.sniff_thread = threading.Thread(
                target=self.run_tcpdump,
                args=(interface,),
                daemon=True
            )
            self.sniff_thread.start()

    def stop_sniffing(self):
        self.sniffing = False
        self.status_label.configure(text="Statut: Arrêté")

        self.start_button.configure(state="normal")
        self.interface_combobox.configure(state="normal")
        self.host_filter_entry.configure(state="normal")
        self.port_filter_entry.configure(state="normal")
        self.protocol_filter_entry.configure(state="normal")
        self.stop_button.configure(state="disabled")


    # ---
    # ### Boucle de Mise à Jour de l'Interface Utilisateur (UI)
    # ---

    def update_ui(self):
        while not self.packet_queue.empty():
            item = self.packet_queue.get()
            item_type = item[0]
            display_text = ""
            target_textbox = None

            if item_type in ["PACKET_STANDARD", "PACKET_DETAILED_IPV4", "PACKET_DETAILED_IPV6"]:
                parsed_details, flow_type = item[1], item[2]
                
                # Formatage des détails du paquet
                if item_type == "PACKET_STANDARD":
                    display_text = (
                        f"--- [Paquet Standard] ---\n"
                        f"  Horodatage  : {parsed_details['Horodatage']}\n"
                        f"  Protocole   : {parsed_details['Protocole']}\n"
                        f"  Source      : {parsed_details['Source']}\n"
                        f"  Destination : {parsed_details['Destination']}"
                    )
                else: # Detailed IPv4/IPv6
                    display_text = (
                        f"--- [Paquet {parsed_details['EtherType']} Détaillé] ---\n"
                        f"  Horodatage  : {parsed_details['Horodatage']}\n"
                        f"  MAC Source  : {parsed_details['MAC Source']}\n"
                        f"  MAC Dest.   : {parsed_details['MAC Destination']}\n"
                        f"  IP Source   : {parsed_details['IP Source']}\n"
                        f"  IP Dest.    : {parsed_details['IP Destination']}\n"
                        f"  Protocole   : {parsed_details['Protocole']}\n"
                        f"  Détails     : {parsed_details['Détails']}"
                    )
                
                # Ajout des données hexadécimales brutes
                if parsed_details["HexData"]:
                    display_text += "\n--- HEX ---"
                    # Affiche chaque ligne hex sur une nouvelle ligne, avec un préfixe d'indentation
                    for hex_line in parsed_details["HexData"]:
                        display_text += f"\n  {hex_line}"
                else:
                    display_text += "\n--- HEX --- [Non disponible]"
                display_text += "\n\n" # Deux sauts de ligne pour séparer les paquets

                if flow_type == "PACKET_IN":
                    target_textbox = self.incoming_textbox
                elif flow_type == "PACKET_OUT":
                    target_textbox = self.outgoing_textbox
                else:
                    target_textbox = self.incoming_textbox # Par défaut, met les "Autres" dans Entrants


            elif item_type == "RAW_PACKET_HEADER": # Pour les paquets non parsés par nos regex d'en-tête
                parsed_details, flow_type = item[1], item[2] # current_packet_data = ("RAW_PACKET_HEADER", {"RawLine": line.strip(), "HexData": []}, "UNKNOWN")
                raw_line = parsed_details["RawLine"]
                hex_data_list = parsed_details["HexData"]

                display_text = f"--- [Paquet Brut Non Parsé] ---\n  {raw_line}"
                if hex_data_list:
                    display_text += "\n--- HEX ---"
                    for hex_line in hex_data_list:
                        display_text += f"\n  {hex_line}"
                else:
                    display_text += "\n--- HEX --- [Non disponible]"
                display_text += "\n\n"

                target_textbox = self.incoming_textbox # Les mettre dans les entrants par défaut

            elif item_type == "STATUS":
                display_text = f"[INFO] {item[1]}\n\n"
                self.incoming_textbox.insert("end", display_text)
                self.incoming_textbox.see("end")
                self.outgoing_textbox.insert("end", display_text)
                self.outgoing_textbox.see("end")
                continue

            elif item_type == "ERROR":
                display_text = f"[ERREUR] {item[1]}\n\n"
                self.incoming_textbox.insert("end", display_text)
                self.incoming_textbox.see("end")
                self.outgoing_textbox.insert("end", display_text)
                self.outgoing_textbox.see("end")
                continue

            # "UNPARSED_HEADER" est géré directement dans run_tcpdump

            if target_textbox:
                target_textbox.insert("end", display_text)
                target_textbox.see("end")


        self.status_label.configure(
            text=f"Statut: {'Capture en cours' if self.sniffing else 'Arrêté'} | Paquets: {self.packet_count}"
        )

        self.master.after(100, self.update_ui)

# --- Point d'Entrée Principal de l'Application ---
if __name__ == "__main__":
    print("Démarrage de l'application. Assurez-vous que 'tcpdump' est installé et que vous disposez des permissions nécessaires (par ex. en l'exécutant avec 'sudo').")
    print("La détermination des flux entrants/sortants est basée sur la détection de l'IP locale de l'interface.")
    print("La vue hexadécimale est maintenant intégrée aux vues des paquets Entrants/Sortants.")

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = NetworkAnalyzerApp(root)
    root.mainloop()