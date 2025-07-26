import subprocess
import os
import re

def get_local_ip_address():
    """
    Executes 'hostname -I' to get the local IP address(es) and returns the first one.
    Returns None if no IP address is found or an error occurs.
    """
    try:
        # Execute 'hostname -I' command
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True, check=True)
        ip_addresses = result.stdout.strip().split()

        if ip_addresses:
            # Return the first IP address found
            return ip_addresses[0]
        else:
            print("Aucune adresse IP trouvée par 'hostname -I'.")
            return None
    except FileNotFoundError:
        print("Erreur: La commande 'hostname' est introuvable. Assurez-vous qu'elle est installée et dans votre PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de 'hostname -I': {e.stderr.strip()}")
        return None
    except Exception as e:
        print(f"Une erreur inattendue est survenue lors de la récupération de l'IP: {e}")
        return None

def update_etc_hosts(target_hostname, new_ip):
    """
    Reads /etc/hosts, updates the line containing target_hostname with new_ip,
    and writes the changes back to the file.
    """
    hosts_file_path = '/etc/hosts'
    updated_lines = []
    line_found = False

    if not new_ip:
        print("Erreur: Nouvelle adresse IP non fournie. Impossible de mettre à jour /etc/hosts.")
        return False

    if not os.path.exists(hosts_file_path):
        print(f"Erreur: Le fichier '{hosts_file_path}' n'existe pas.")
        return False

    # Check for root permissions
    if os.geteuid() != 0:
        print(f"Erreur: Permissions insuffisantes. Ce script doit être exécuté avec 'sudo' pour modifier '{hosts_file_path}'.")
        return False

    try:
        with open(hosts_file_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            # Use regex to find lines that start with an IP and contain the target hostname
            # This regex looks for:
            # ^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+  (start of line, optional whitespace, IP address, one or more spaces)
            # (.*\s+)?                                 (optional any characters, one or more spaces before hostname)
            # (?:[a-zA-Z0-9\-\.]+\s+)* (optional hostnames followed by space)
            # (gykhamine\.cg)                          (our target hostname, captured in group 1)
            # (.*)$                                    (any remaining characters to the end of the line, captured in group 2)
            match = re.match(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+(?:[a-zA-Z0-9\-\.]+\s+)*?(" + re.escape(target_hostname) + r")(\s+.*)?$", line)

            if target_hostname in line and re.match(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line):
                # This line contains the target hostname and starts with an IP.
                # Replace the entire IP part of the line with the new IP
                # We also want to keep any other hostnames on the same line.
                parts = line.split()
                if parts and len(parts) > 1: # Ensure there's at least an IP and a hostname
                    # Find where target_hostname is, and reconstruct the line
                    # Preserve existing hostnames/aliases after the target_hostname
                    aliases = [p for p in parts[1:] if p != target_hostname]
                    
                    # Ensure target_hostname is always present after the IP
                    if target_hostname not in aliases:
                        aliases.insert(0, target_hostname)
                    else:
                        # Move target_hostname to be the first after IP if it's there
                        aliases.remove(target_hostname)
                        aliases.insert(0, target_hostname)

                    new_line = f"{new_ip}\t{' '.join(aliases)}\n"
                    updated_lines.append(new_line)
                    line_found = True
                    print(f"Ligne trouvée et modifiée pour '{target_hostname}': {line.strip()} -> {new_line.strip()}")
                else:
                    # If the line structure is unexpected but contains the hostname,
                    # just replace the IP part. This might be less robust for complex lines.
                    new_line = f"{new_ip}\t{target_hostname}\n" # Simplified replacement
                    updated_lines.append(new_line)
                    line_found = True
                    print(f"Ligne trouvée et modifiée pour '{target_hostname}' (simplifié): {line.strip()} -> {new_line.strip()}")
            else:
                updated_lines.append(line)

        if not line_found:
            print(f"Avertissement: La ligne contenant '{target_hostname}' avec une adresse IP n'a pas été trouvée dans '{hosts_file_path}'. Aucune modification effectuée.")
            # If you want to add the line if not found, uncomment the next two lines:
            # new_line_to_add = f"{new_ip}\t{target_hostname}\n"
            # updated_lines.append(new_line_to_add)
            # print(f"Ajout de la nouvelle ligne: {new_line_to_add.strip()}")
            # line_found = True # Set to True if you decided to add

        # Write the updated content back to /etc/hosts
        with open(hosts_file_path, 'w') as f:
            f.writelines(updated_lines)
        
        if line_found:
            print(f"Le fichier '{hosts_file_path}' a été mis à jour avec succès.")
            return True
        else:
            print(f"Le fichier '{hosts_file_path}' n'a pas été modifié car la ligne n'a pas été trouvée.")
            return False

    except IOError as e:
        print(f"Erreur d'accès au fichier '{hosts_file_path}': {e}")
        return False
    except Exception as e:
        print(f"Une erreur inattendue est survenue lors de la mise à jour de /etc/hosts: {e}")
        return False

if __name__ == "__main__":
    target_hostname_to_find = "gykhamine.cg"

    # 1. Get the current local IP address
    current_ip = get_local_ip_address()

    if current_ip:
        print(f"Adresse IP locale actuelle détectée: {current_ip}")
        # 2. Update the /etc/hosts file
        success = update_etc_hosts(target_hostname_to_find, current_ip)
        if success:
            print("Opération terminée.")
        else:
            print("L'opération de mise à jour de /etc/hosts n'a pas été entièrement réussie.")
    else:
        print("Impossible de récupérer l'adresse IP locale. La mise à jour de /etc/hosts est annulée.")