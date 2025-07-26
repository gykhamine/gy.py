import customtkinter as ctk
from threading import Thread
import subprocess
import sys

class NmapCTKApp:
    def __init__(self, master):
        self.master = master
        master.title("Nmap Scanner Ultime (250+ Options)")
        master.geometry("1100x780") # Taille de fenêtre ajustée pour la longue liste

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # --- Cadre Principal (utilisation de grid pour le layout) ---
        self.main_layout_frame = ctk.CTkFrame(master)
        self.main_layout_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configuration des colonnes
        self.main_layout_frame.grid_columnconfigure(0, weight=0) # Colonne gauche (options) ne s'étire pas
        self.main_layout_frame.grid_columnconfigure(1, weight=1) # Colonne droite (cible + résultats) s'étire
        self.main_layout_frame.grid_rowconfigure(0, weight=1) # La ligne principale s'étire

        # --- Cadre Gauche pour la Liste Défilante des Types de Scan ---
        self.left_panel_frame = ctk.CTkFrame(self.main_layout_frame)
        self.left_panel_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        self.scan_type_label = ctk.CTkLabel(self.left_panel_frame, text="Types de Scan Nmap (250+) :", font=ctk.CTkFont(size=16, weight="bold"))
        self.scan_type_label.pack(pady=(15, 5), padx=10, anchor="w")

        # Utilisation de CTkScrollableFrame pour contenir toutes les options
        self.options_scroll_frame = ctk.CTkScrollableFrame(self.left_panel_frame, width=320, height=600) # Largeur fixe, hauteur ajustable
        self.options_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # --- Dictionnaire FINAL des options de scan Nmap (très étendu) ---
        # Note: Les catégories sont des clés spéciales commençant par "---" et ayant une valeur vide.
        # Les options sont générées dynamiquement ci-dessous pour atteindre le nombre souhaité.
        self.scan_options = {}

        # --- Base Scan Types ---
        base_scan_types = {
            "Default (Top 1000 Ports)": "",
            "SYN Scan (-sS)": "-sS",
            "TCP Connect Scan (-sT)": "-sT",
            "UDP Scan (-sU)": "-sU",
            "Fast Scan (-F)": "-F",
            "Ping Scan (-sn)": "-sn",
            "No Ping (-Pn)": "-Pn",
        }

        # --- Detection Types ---
        detection_types = {
            "Version (-sV)": "-sV",
            "OS (-O)": "-O",
            "Default Scripts (-sC)": "-sC",
            "Aggressive (-A)": "-A", # Includes -O, -sV, -sC, --traceroute
        }

        # --- Timing Templates ---
        timing_types = {
            "Very Slow (-T0)": "-T0",
            "Slow (-T1)": "-T1",
            "Normal (-T3)": "-T3",
            "Fast (-T4)": "-T4",
            "Insane (-T5)": "-T5",
        }

        # --- Verbosity/Output Types ---
        output_types = {
            "Verbose (-v)": "-v",
            "Very Verbose (-vv)": "-vv",
            "Reason (--reason)": "--reason",
            "Open Ports Only (--open)": "--open",
            "Debug 1 (-d1)": "-d1",
        }

        # --- Port Options ---
        port_options = {
            "Common Ports (22,80,443)": "-p 22,80,443",
            "All TCP Ports (-p-)": "-p-",
            "All UDP Ports (-p U:1-65535)": "-p U:1-65535",
            "Top 2000 Ports": "--top-ports 2000",
            "Specific Ports (80,443,8080)": "-p 80,443,8080",
        }

        # --- NSE Script Examples ---
        nse_scripts = {
            "Vuln Script (--script vuln)": "--script vuln",
            "HTTP Enum (--script http-enum)": "--script http-enum",
            "SMB Enum (--script smb-enum-shares)": "--script smb-enum-shares",
            "FTP Brute (--script ftp-brute)": "--script ftp-brute",
            "SSL Ciphers (--script ssl-enum-ciphers)": "--script ssl-enum-ciphers",
            "Heartbleed (--script ssl-heartbleed)": "--script ssl-heartbleed",
            "DNS Brute (--script dns-brute)": "--script dns-brute",
        }
        
        # --- Populate scan_options with categories and combinations ---
        
        # CATEGORY: DISCOVERY
        self.scan_options["--- DÉCOUVERTE D'HÔTES ---"] = ""
        self.scan_options.update({
            "Ping Scan simple (-sn)": "-sn",
            "Scan sans Ping (-Pn)": "-Pn",
            "Découverte ARP (-PR)": "-PR",
            "Découverte SYN (-PS)": "-PS",
            "Découverte ACK (-PA)": "-PA",
            "Découverte ICMP Echo (-PE)": "-PE",
            "Découverte ICMP Timestamp (-PP)": "-PP",
            "Découverte ICMP Netmask (-PM)": "-PM",
            "Découverte complète (multi-sondages)": "-PR -PS -PA -PE -PP -PM",
            "List Scan (ne scanne pas)": "-sL",
            "Traceroute + Ping Scan": "--traceroute -sn",
        })

        # CATEGORY: BASIC PORT SCANS
        self.scan_options["--- SCANS DE PORTS (BASIQUE) ---"] = ""
        self.scan_options.update({
            "Default Scan (Top 1000 TCP)": "",
            "Scan Rapide (-F)": "-F",
            "Scan SYN (-sS) [Admin/Root]": "-sS",
            "Scan TCP Connect (-sT)": "-sT",
            "Scan Xmas (-sX)": "-sX",
            "Scan Null (-sN)": "-sN",
            "Scan Fin (-sF)": "-sF",
            "Scan ACK (-sA)": "-sA",
            "Scan Fenêtre (-sW)": "-sW",
            "Scan Maimon (-sM)": "-sM",
            "Scan UDP (-sU)": "-sU",
            "Tous les Ports TCP (-p-) [Très Long!]": "-p-",
            "Tous les Ports UDP (-p U:1-65535) [Très Long!]": "-p U:1-65535",
            "Ports courants (22,80,443)": "-p 22,80,443",
            "Top 2000 Ports TCP": "--top-ports 2000",
        })

        # CATEGORY: DETECTION (Service, OS)
        self.scan_options["--- DÉTECTION (SERVICES & OS) ---"] = ""
        self.scan_options.update({
            "Détection de Version (-sV)": "-sV",
            "Détection d'OS (-O) [Admin/Root]": "-O",
            "Scripts Nmap par Défaut (-sC)": "-sC",
            "Scan Aggressif (-A) [Admin/Root]": "-A",
            "Détection de version légère (--version-light)": "--version-light",
            "Détection de version agressive (--version-all)": "--version-all",
        })

        # CATEGORY: COMMON COMBINATIONS
        self.scan_options["--- COMBINAISONS COURANTES ---"] = ""
        generated_count = 0
        for b_name, b_cmd in base_scan_types.items():
            if b_name.startswith("Ping") or b_name.startswith("No Ping"): continue
            for d_name, d_cmd in detection_types.items():
                if d_name.startswith("Aggressive") and b_name != "Default (Top 1000 Ports)": continue # Avoid redundancy
                if not b_cmd and not d_cmd: continue # Skip empty combo
                
                cmd_str = f"{b_cmd} {d_cmd}".strip()
                name_str = f"{b_name} + {d_name}".replace(" + ", " ").strip()
                name_str = name_str.replace("Default (Top 1000 Ports)", "Default")

                if cmd_str and cmd_str not in self.scan_options.values():
                    self.scan_options[name_str] = cmd_str
                    generated_count += 1
                
                # Add a timing
                for t_name, t_cmd in timing_types.items():
                    if not t_cmd: continue
                    cmd_timing = f"{cmd_str} {t_cmd}".strip()
                    name_timing = f"{name_str} ({t_name})"
                    if cmd_timing and cmd_timing not in self.scan_options.values():
                        self.scan_options[name_timing] = cmd_timing
                        generated_count += 1
                    
                    # Add verbosity
                    for v_name, v_cmd in output_types.items():
                        if not v_cmd or v_name.startswith("Open Ports"): continue # Avoid too many combinations with specific output
                        cmd_verb = f"{cmd_timing} {v_cmd}".strip()
                        name_verb = f"{name_timing} ({v_name})"
                        if cmd_verb and cmd_verb not in self.scan_options.values():
                            self.scan_options[name_verb] = cmd_verb
                            generated_count += 1

        # CATEGORY: SCRIPTS NSE
        self.scan_options["--- SCRIPTS NSE (Network Scripting Engine) ---"] = ""
        for s_name, s_cmd in nse_scripts.items():
            self.scan_options[s_name] = s_cmd
            # Add with common scan types and verbosity
            for b_name, b_cmd in {"SYN": "-sS", "Connect": "-sT", "Default": ""}.items():
                if not b_cmd and not s_cmd: continue
                cmd_script_base = f"{b_cmd} {s_cmd}".strip()
                name_script_base = f"{b_name} + {s_name}"
                if cmd_script_base and cmd_script_base not in self.scan_options.values():
                    self.scan_options[name_script_base] = cmd_script_base
                    generated_count += 1
                
                cmd_script_verbose = f"{cmd_script_base} -vv".strip()
                name_script_verbose = f"{name_script_base} (Très Verbose)"
                if cmd_script_verbose and cmd_script_verbose not in self.scan_options.values():
                    self.scan_options[name_script_verbose] = cmd_script_verbose
                    generated_count += 1
        
        # CATEGORY: PERFORMANCE & EVASION
        self.scan_options["--- PERFORMANCE & FURTIVITÉ ---"] = ""
        self.scan_options.update({
            "Très Lent (-T0) - Pare-feu fort": "-T0",
            "Lent (-T1) - Éviter IDS/IPS": "-T1",
            "Normal (-T3)": "-T3",
            "Rapide (-T4)": "-T4",
            "Très Rapide (-T5) - Potentiellement bruyant": "-T5",
            "Fragmenter Paquets (-f)": "-f",
            "MTU Personnalisé (--mtu 24)": "--mtu 24",
            "Données Aléatoires (--data-length 25)": "--data-length 25",
            "Délai Min. (ex: --scan-delay 1s)": "--scan-delay 1s",
            "Vitesse Min. (ex: --min-rate 100)": "--min-rate 100",
            "Délai Max. (ex: --max-scan-delay 100ms)": "--max-scan-delay 100ms",
            "Hôtes Décoy (ex: --decoys 192.168.1.1,ME)": "--decoys 192.168.1.1,ME",
            "Source IP Fausse (ex: -S 10.0.0.1) [Admin/Root]": "-S 10.0.0.1",
            "Source Port Fausse (--source-port 53)": "--source-port 53",
            "Utiliser des proxies (ex: --proxies http://1.2.3.4:8080)": "--proxies http://1.2.3.4:8080",
            "Sans Résolution DNS (-n)": "-n",
            "Résolution DNS inverse (-R)": "-R",
            "Exclure Hôtes (ex: --exclude 192.168.1.2)": "--exclude 192.168.1.2",
            "Exclure Fichier (ex: --excludefile exclude.txt)": "--excludefile exclude.txt",
        })

        # CATEGORY: OUTPUT & DEBUG
        self.scan_options["--- SORTIE & DÉBOGAGE ---"] = ""
        self.scan_options.update({
            "Sortie Verbose (-v)": "-v",
            "Sortie Très Verbose (-vv)": "-vv",
            "Afficher la Raison (--reason)": "--reason",
            "Afficher les Hôtes Ouverts (--open)": "--open",
            "Mode Débogage (niveau 1) (-d1)": "-d1",
            "Mode Débogage (niveau 9) (-d9)": "-d9",
            "XML Output (-oX output.xml)": "-oX output.xml",
            "Grepable Output (-oG output.gnmap)": "-oG output.gnmap",
            "Normal Output (-oN output.nmap)": "-oN output.nmap",
            "All Output Formats (-oA all_output)": "-oA all_output",
            "Append Output (--append-output)": "--append-output",
            "Packet Trace (--packet-trace)": "--packet-trace",
        })
        
        # CATEGORY: Advanced & Specific Combos
        self.scan_options["--- COMBINAISONS AVANCÉES ---"] = ""
        self.scan_options.update({
            "Full TCP Scan + Aggressive + Insane Speed": "-p- -A -T5",
            "Full UDP Scan + Version Detection + Very Slow": "-p U:1-65535 -sU -sV -T0",
            "SYN Scan + Version + All TCP Ports + Verbose": "-sS -sV -p- -v",
            "Connect Scan + OS Detection + Default Scripts + Fast Speed": "-sT -O -sC -T4",
            "Ping Scan + Traceroute + Verbose": "-sn --traceroute -v",
            "No Ping + SYN Scan + Common Web Ports + Reason": "-Pn -sS -p 80,443 --reason",
            "Aggressive Scan + All TCP Ports + Very Verbose": "-A -p- -vv",
            "Default Scan + All Output Formats": "-oA all_output",
            "SYN Scan + Script Vuln + Aggressive Timing": "-sS --script vuln -T4",
            "UDP Scan + DNS Brute Script + Debug": "-sU --script dns-brute -d1",
            "Fragmented SYN Scan + OS Detection": "-sS -f -O",
            "Scan with Min Rate 1000 + Max Scan Delay 50ms": "--min-rate 1000 --max-scan-delay 50ms",
            "Comprehensive Scan (SYN, UDP, Version, OS, Scripts, Aggressive, Fast, Verbose)": "-sS -sU -sV -O -sC -A -T4 -vv",
        })


        # Create labels for each option in the scrollable frame
        self.selected_scan_option = ctk.StringVar(value="") # Variable to store the selected option's arguments
        self.selected_label_widget = None # Reference to the currently selected label widget

        for i, (text, args) in enumerate(self.scan_options.items()):
            if text.startswith("---"): # It's a category title
                category_label = ctk.CTkLabel(self.options_scroll_frame, text=text, font=ctk.CTkFont(size=13, weight="bold"), text_color="gray")
                category_label.pack(pady=(10, 2), padx=5, anchor="w")
            else: # It's a scan option
                option_label = ctk.CTkLabel(self.options_scroll_frame, text=text,
                                            font=ctk.CTkFont(size=12), fg_color="transparent",
                                            corner_radius=5, padx=5, pady=2, anchor="w")
                option_label.pack(fill="x", pady=1, padx=5)
                # Bind a click event to each option label
                option_label.bind("<Button-1>", lambda event, args=args, label=option_label: self.on_option_label_click(event, args, label))

        # --- Right Side Container Frame (for target input and results) ---
        self.right_side_container_frame = ctk.CTkFrame(self.main_layout_frame)
        self.right_side_container_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        # Configure rows within the right side container
        self.right_side_container_frame.grid_rowconfigure(0, weight=0) # Top row (target/button) does not stretch
        self.right_side_container_frame.grid_rowconfigure(1, weight=1) # Bottom row (results) stretches

        # --- Top Right Frame for Target and Scan Button ---
        self.right_top_frame = ctk.CTkFrame(self.right_side_container_frame)
        self.right_top_frame.grid(row=0, column=0, sticky="new", padx=0, pady=0)
        
        self.target_label = ctk.CTkLabel(self.right_top_frame, text="Cible (IP/Hôte) :", font=ctk.CTkFont(size=14, weight="bold"))
        self.target_label.pack(side="left", padx=(10, 0), pady=10)
        self.target_entry = ctk.CTkEntry(self.right_top_frame, width=280, placeholder_text="Ex: 192.168.1.1 ou google.com")
        self.target_entry.pack(side="left", padx=10, pady=10)
        self.target_entry.insert(0, "scanme.nmap.org")
        
        self.scan_button = ctk.CTkButton(self.right_top_frame, text="Lancer le Scan", command=self.start_nmap_scan, state="disabled") # Disabled by default
        self.scan_button.pack(side="right", padx=10, pady=10)

        # --- Results Display Area (bottom right) ---
        self.results_frame = ctk.CTkFrame(self.right_side_container_frame)
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        self.results_label = ctk.CTkLabel(self.results_frame, text="Sortie de la commande Nmap :", font=ctk.CTkFont(size=14, weight="bold"))
        self.results_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.results_text = ctk.CTkTextbox(self.results_frame, wrap="word")
        self.results_text.pack(pady=(0, 10), padx=10, fill="both", expand=True)
        self.results_text.configure(state="disabled")

        # --- Status Bar ---
        self.status_bar = ctk.CTkLabel(master, text="Prêt (Sélectionnez un scan)", anchor="w", font=ctk.CTkFont(size=12))
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=10)

    def on_option_label_click(self, event, args, label):
        """
        Handles the click on a scan option label.
        Highlights the selected option and updates the scan argument.
        """
        # Reset color of previously selected label
        if self.selected_label_widget:
            self.selected_label_widget.configure(fg_color="transparent")
        
        # Update selected label and its color
        self.selected_label_widget = label
        self.selected_label_widget.configure(fg_color=ctk.ThemeManager.theme["CTkOptionMenu"]["button_color"]) # Use CTk button color for highlight
        
        self.selected_scan_option.set(args) # Store the actual scan arguments
        self.update_status(f"Option sélectionnée : {label.cget('text')} - Prêt à scanner.", "black")
        self.scan_button.configure(state="normal") # Enable the scan button

    def start_nmap_scan(self):
        target = self.target_entry.get().strip()
        if not target:
            self.update_status("Veuillez entrer une cible (IP ou hôte).", "red")
            return

        nmap_args_for_scan = self.selected_scan_option.get()
        if not nmap_args_for_scan: # Ensure an option has been selected
            self.update_status("Veuillez sélectionner un type de scan Nmap.", "red")
            self.results_text.configure(state="normal")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("end", "Erreur: Aucun type de scan Nmap sélectionné.\n")
            self.results_text.configure(state="disabled")
            return

        nmap_command_parts = ['nmap']

        # Split arguments by space. (Still note: does not handle complex quoted arguments like --script "my script" perfectly)
        nmap_command_parts.extend(nmap_args_for_scan.split())

        nmap_command_parts.append(target)

        full_command_str = ' '.join(nmap_command_parts)
        self.update_status(f"Exécution de : {full_command_str}...", "blue")
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("end", f"Exécution : {full_command_str}\n\n")
        self.results_text.configure(state="disabled")

        command_thread = Thread(target=self._run_nmap_subprocess, args=(nmap_command_parts,))
        command_thread.start()

    def _run_nmap_subprocess(self, nmap_command_list):
        try:
            result = subprocess.run(
                nmap_command_list,
                capture_output=True,
                text=True,
                check=False
            )

            output = result.stdout
            if result.stderr:
                output += "\n--- Sortie Erreur Nmap (stderr) ---\n" + result.stderr
            
            if result.returncode != 0:
                output += f"\n--- Commande Nmap terminée avec un code de retour d'erreur : {result.returncode} ---"
                self.update_status("Erreur lors du scan Nmap (voir les résultats)", "red")
            else:
                self.update_status("Scan Nmap terminé avec succès.", "green")

            self.update_results(output)

        except FileNotFoundError:
            error_message = f"Erreur : La commande 'nmap' n'a pas été trouvée.\n" \
                            "Veuillez vous assurer que Nmap est installé et que son chemin d'accès est configuré dans les variables d'environnement (PATH)."
            self.update_results(error_message)
            self.update_status("Erreur : Nmap non trouvé", "red")
            print(error_message, file=sys.stderr)
        except Exception as e:
            error_message = f"Une erreur inattendue est survenue : {e}"
            self.update_results(error_message)
            self.update_status("Erreur inattendue", "red")
            print(error_message, file=sys.stderr)

    def update_results(self, text):
        self.results_text.configure(state="normal")
        self.results_text.insert("end", text)
        self.results_text.configure(state="disabled")
        self.results_text.see("end")

    def update_status(self, message, color="black"):
        self.status_bar.configure(text=message, text_color=color)

if __name__ == "__main__":
    root = ctk.CTk()
    app = NmapCTKApp(root)
    root.mainloop()