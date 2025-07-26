import customtkinter as ctk
from threading import Thread
import subprocess
import sys

class NmapCTKApp:
    def __init__(self, master):
        self.master = master
        master.title("Nmap Scanner Ultime")
        master.geometry("1000x700") # Adjusted window size for the side panel

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # --- Main Layout Frame (using grid for side-by-side organization) ---
        self.main_layout_frame = ctk.CTkFrame(master)
        self.main_layout_frame.pack(fill="both", expand=True, padx=10, pady=10) # Global padding
        
        # Configure columns for the main layout
        self.main_layout_frame.grid_columnconfigure(0, weight=0) # Left column (options) does not stretch
        self.main_layout_frame.grid_columnconfigure(1, weight=1) # Right column (target + results) stretches
        self.main_layout_frame.grid_rowconfigure(0, weight=1) # Main row stretches

        # --- Left Panel Frame for Scan Type List ---
        self.left_panel_frame = ctk.CTkFrame(self.main_layout_frame)
        self.left_panel_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0) # Padding to the right of the left frame
        
        self.scan_type_label = ctk.CTkLabel(self.left_panel_frame, text="Type de Scan Nmap :", font=ctk.CTkFont(size=14, weight="bold"))
        self.scan_type_label.pack(pady=(15, 5), padx=10, anchor="w") # Padding at top and left

        # Nmap scan options (extended and organized)
        self.scan_options = {
            "--- DÉCOUVERTE D'HÔTES ---": "",
            "Ping Scan simple (-sn)": "-sn",
            "Scan sans Ping (-Pn)": "-Pn",
            "Découverte ARP (réseau local)": "-PR",
            "Découverte SYN (-PS)": "-PS",
            "Découverte ACK (-PA)": "-PA",
            "Découverte ICMP Echo (-PE)": "-PE",
            "Découverte ICMP Timestamp (-PP)": "-PP",
            "Découverte ICMP Netmask (-PM)": "-PM",
            "Découverte complète (multi-sondages)": "-PR -PS -PA -PE -PP -PM",
            "List Scan (ne scanne pas, liste seulement)": "-sL",
            
            "--- SCAN DE PORTS (TCP) ---": "",
            "Scan Rapide (-F)": "-F",
            "Scan SYN (-sS) [Admin/Root]": "-sS",
            "Scan TCP Connect (-sT)": "-sT",
            "Scan Xmas (-sX)": "-sX",
            "Scan Null (-sN)": "-sN",
            "Scan Fin (-sF)": "-sF",
            "Scan ACK (-sA)": "-sA",
            "Scan Fenêtre (-sW)": "-sW",
            "Scan Maimon (-sM)": "-sM",
            "Scan Personnalisé (ex: -p 22,80,443)": "-p 22,80,443",
            "Tous les Ports TCP (-p-) [Très Long!]": "-p-",
            "Ports 1-1024 (-p 1-1024)": "-p 1-1024",

            "--- SCAN DE PORTS (UDP) ---": "",
            "Scan UDP (-sU)": "-sU",
            "Tous les Ports UDP (-p U:1-65535) [Très Long!]": "-p U:1-65535",
            
            "--- DÉTECTION DE SERVICES / OS ---": "",
            "Détection de Version (-sV)": "-sV",
            "Détection d'OS (-O) [Admin/Root]": "-O",
            "Scan Aggressif (-A) [Admin/Root]": "-A",
            "Scripts Nmap par Défaut (-sC)": "-sC",
            
            "--- COMBINAISONS COURANTES ---": "",
            "SYN + Version (-sS -sV) [Admin/Root]": "-sS -sV",
            "SYN + OS + Version (-sS -O -sV) [Admin/Root]": "-sS -O -sV",
            "Connect + Version (-sT -sV)": "-sT -sV",
            "UDP + Version (-sU -sV)": "-sU -sV",
            "Aggressif + Verbose (-A -v) [Admin/Root]": "-A -v",
            "Rapide + Version (-F -sV)": "-F -sV",

            "--- SCRIPTS NSE (Network Scripting Engine) ---": "",
            "Recherche de Vulnérabilités (--script vuln)": "--script vuln",
            "Enumération HTTP (--script http-enum)": "--script http-enum",
            "Scan de Brute Force FTP (--script ftp-brute)": "--script ftp-brute",
            "Détection de Vuln. SSL/TLS (--script ssl-enum-ciphers)": "--script ssl-enum-ciphers",
            "Détection de Vuln. Heartbleed (--script ssl-heartbleed)": "--script ssl-heartbleed",
            "Enumération SMB (--script smb-enum-shares)": "--script smb-enum-shares",
            "Détection de Vuln. EternalBlue (--script smb-vuln-ms17-010)": "--script smb-vuln-ms17-010",

            "--- PERFORMANCE & FURTIVITÉ ---": "",
            "Très Lent (-T0) - Pare-feu fort": "-T0",
            "Lent (-T1) - Éviter IDS/IPS": "-T1",
            "Normal (-T3)": "-T3",
            "Rapide (-T4)": "-T4",
            "Très Rapide (-T5) - Potentiellement bruyant": "-T5",
            "Fragmenter Paquets (-f)": "-f",
            "Données Aléatoires (--data-length 25)": "--data-length 25",
            "Délai Min. (ex: --scan-delay 1s)": "--scan-delay 1s",
            "Vitesse Min. (ex: --min-rate 100)": "--min-rate 100",
            
            "--- SORTIE & DIVERS ---": "",
            "Sortie Verbose (-v)": "-v",
            "Sortie Très Verbose (-vv)": "-vv",
            "Traceroute (--traceroute)": "--traceroute",
            "Afficher la Raison (--reason)": "--reason",
            "Afficher les Hôtes Ouverts (--open)": "--open",
            "Ne pas Résoudre DNS (-n)": "-n",
            "Mode Débogage (niveau 1) (-d1)": "-d1"
        }

        self.scan_type_var = ctk.StringVar(value=list(self.scan_options.keys())[1]) # Default to "Ping Scan simple"
        self.scan_type_optionmenu = ctk.CTkOptionMenu(self.left_panel_frame,
                                                      values=list(self.scan_options.keys()),
                                                      variable=self.scan_type_var,
                                                      width=300, # Fixed width for the side panel
                                                      height=30,
                                                      command=self.on_scan_option_selected)
        self.scan_type_optionmenu.pack(pady=5, padx=10, fill="x", expand=False) # Fill horizontally

        # --- Right Side Container Frame (for target input and results) ---
        self.right_side_container_frame = ctk.CTkFrame(self.main_layout_frame)
        self.right_side_container_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        # Configure rows within the right side container
        self.right_side_container_frame.grid_rowconfigure(0, weight=0) # Top row (target/button) does not stretch
        self.right_side_container_frame.grid_rowconfigure(1, weight=1) # Bottom row (results) stretches

        # --- Top Right Frame for Target and Scan Button ---
        self.right_top_frame = ctk.CTkFrame(self.right_side_container_frame)
        self.right_top_frame.grid(row=0, column=0, sticky="new", padx=0, pady=0)
        
        # Corrected: Initialize target_label and target_entry directly here
        self.target_label = ctk.CTkLabel(self.right_top_frame, text="Cible (IP/Hôte) :")
        self.target_label.pack(side="left", padx=(10, 0), pady=10)
        self.target_entry = ctk.CTkEntry(self.right_top_frame, width=250, placeholder_text="Ex: 192.168.1.1 ou google.com")
        self.target_entry.pack(side="left", padx=10, pady=10)
        self.target_entry.insert(0, "scanme.nmap.org") # Default value
        
        self.scan_button = ctk.CTkButton(self.right_top_frame, text="Lancer le Scan", command=self.start_nmap_scan)
        self.scan_button.pack(side="right", padx=10, pady=10)

        # --- Results Display Area (bottom right) ---
        self.results_frame = ctk.CTkFrame(self.right_side_container_frame)
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0) # Occupies the rest of the column

        self.results_label = ctk.CTkLabel(self.results_frame, text="Sortie de la commande Nmap :", font=ctk.CTkFont(size=14, weight="bold"))
        self.results_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.results_text = ctk.CTkTextbox(self.results_frame, wrap="word")
        self.results_text.pack(pady=(0, 10), padx=10, fill="both", expand=True)
        self.results_text.configure(state="disabled")

        # --- Status Bar ---
        self.status_bar = ctk.CTkLabel(master, text="Prêt", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=10)

    def on_scan_option_selected(self, choice):
        # This function is called when an option is selected.
        # It disables the button if a "category" is chosen.
        if choice.startswith("---"):
            self.scan_button.configure(state="disabled")
            self.update_status("Veuillez sélectionner un type de scan Nmap valide.", "orange")
        else:
            self.scan_button.configure(state="normal")
            self.update_status("Prêt à scanner.", "black")

    def start_nmap_scan(self):
        target = self.target_entry.get().strip() 
        if not target:
            self.update_status("Veuillez entrer une cible (IP ou hôte).", "red")
            return

        selected_option_text = self.scan_type_var.get()
        if selected_option_text.startswith("---"):
            self.update_status("Veuillez sélectionner un type de scan Nmap valide.", "red")
            self.results_text.configure(state="normal")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("end", "Erreur: Veuillez sélectionner un type de scan Nmap valide.\n")
            self.results_text.configure(state="disabled")
            return

        nmap_args_for_scan = self.scan_options.get(selected_option_text, "")

        nmap_command_parts = ['nmap']

        if nmap_args_for_scan:
            # WARNING: .split() does not handle arguments with spaces and quotes correctly.
            # For robust parsing of complex strings, using 'shlex.split()' (standard Python module)
            # is highly recommended if such arguments were necessary.
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
        """
        Executes the Nmap command via subprocess and displays the output in the interface.
        """
        try:
            result = subprocess.run(
                nmap_command_list,
                capture_output=True,
                text=True,
                check=False # We handle Nmap return codes manually
            )

            output = result.stdout
            if result.stderr:
                output += "\n--- Nmap Error Output (stderr) ---\n" + result.stderr
            
            if result.returncode != 0:
                output += f"\n--- Nmap command finished with error code: {result.returncode} ---"
                self.update_status("Error during Nmap scan (see results)", "red")
            else:
                self.update_status("Nmap scan completed successfully.", "green")

            self.update_results(output)

        except FileNotFoundError:
            error_message = f"Error: The 'nmap' command was not found.\n" \
                            "Please ensure Nmap is installed and its path is configured in your environment variables (PATH)."
            self.update_results(error_message)
            self.update_status("Error: Nmap not found", "red")
            print(error_message, file=sys.stderr)
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            self.update_results(error_message)
            self.update_status("Unexpected error", "red")
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