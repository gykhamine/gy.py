import customtkinter as ctk
import platform
import subprocess
import os
import psutil
import datetime
import socket
import re
import json

# --- Imports spécifiques à la plateforme avec gestion robuste des erreurs ---
try:
    if platform.system() == "Windows":
        import wmi
        WMI_AVAILABLE = True
    else:
        WMI_AVAILABLE = False
except ImportError:
    wmi = None
    WMI_AVAILABLE = False
    print("ATTENTION: La bibliothèque WMI n'a pas été trouvée. Installez-la avec 'pip install wmi' pour un meilleur support de Windows.")
except Exception as e:
    wmi = None
    WMI_AVAILABLE = False
    print(f"ATTENTION: Erreur lors de l'import de WMI: {e}. Le support de Windows pourrait être limité.")


try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    cv2 = None
    OPENCV_AVAILABLE = False
    print("ATTENTION: OpenCV n'a pas été trouvé. Installez-le avec 'pip install opencv-python' pour la détection de caméra.")
except Exception as e:
    cv2 = None
    OPENCV_AVAILABLE = False
    print(f"ATTENTION: Erreur lors de l'import d'OpenCV: {e}. La détection de caméra sera désactivée.")


class DeviceScanner:
    def __init__(self):
        self.os_name = platform.system()
        self.wmi_c = wmi.WMI() if WMI_AVAILABLE and self.os_name == "Windows" else None

    def _run_command(self, command, requires_sudo=False, shell=False, check=False):
        try:
            full_command = ["sudo"] + command if requires_sudo and self.os_name == "Linux" else command
            
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                check=check,
                encoding="utf-8",
                errors="replace",
                shell=shell
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            return ""
        except Exception as e:
            return ""

    def get_cpu_info(self):
        cpu_details = {
            "Nom": "N/A",
            "Cœurs Physiques": psutil.cpu_count(logical=False),
            "Cœurs Logiques": psutil.cpu_count(logical=True),
            "Fréquence Actuelle": "N/A",
            "Fréquence Max": "N/A",
            "Architecture": platform.machine(),
            "Virtualisation Support": "Inconnu",
            "Fabricant": "N/A"
        }

        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            cpu_details["Fréquence Actuelle"] = f"{cpu_freq.current:.2f} MHz"
            cpu_details["Fréquence Max"] = f"{cpu_freq.max:.2f} MHz"

        if self.os_name == "Windows" and self.wmi_c:
            try:
                for proc in self.wmi_c.Win32_Processor():
                    cpu_details["Nom"] = proc.Name.strip()
                    cpu_details["Fabricant"] = proc.Manufacturer or "N/A"
                    break

                output = self._run_command(["wmic", "computersystem", "get", "HyperVisorPresent"])
                if "TRUE" in output.upper():
                    cpu_details["Virtualisation Support"] = "Oui (Hyper-V)"
                else:
                    cpu_details["Virtualisation Support"] = "Non (Hyper-V)"
            except Exception as e:
                pass

        elif self.os_name == "Linux":
            try:
                output = self._run_command(["lscpu"])
                for line in output.splitlines():
                    if "Model name:" in line:
                        cpu_details["Nom"] = line.split(":", 1)[1].strip()
                    elif "Vendor ID:" in line:
                        cpu_details["Fabricant"] = line.split(":", 1)[1].strip()
                    elif "Virtualization:" in line:
                        virt_info = line.split(":", 1)[1].strip()
                        if virt_info:
                            cpu_details["Virtualisation Support"] = f"Oui ({virt_info})"
                        else:
                            cpu_details["Virtualisation Support"] = "Non"

                if cpu_details["Virtualisation Support"] == "Inconnu":
                    cpu_output_raw = self._run_command(["cat", "/proc/cpuinfo"])
                    if "vmx" in cpu_output_raw or "svm" in cpu_output_raw:
                        cpu_details["Virtualisation Support"] = "Oui (VT-x/AMD-V)"
                    else:
                        cpu_details["Virtualisation Support"] = "Non (Pas de VT-x/AMD-V)"
            except Exception as e:
                pass
        return cpu_details

    def get_ram_info(self):
        total_ram_gb = psutil.virtual_memory().total / (1024**3)
        available_ram_gb = psutil.virtual_memory().available / (1024**3)
        ram_details = {
            "Total (GB)": f"{total_ram_gb:.2f}",
            "Disponible (GB)": f"{available_ram_gb:.2f}",
            "Utilisation (%)": psutil.virtual_memory().percent,
            "Type": "Inconnu",
            "Vitesse (MHz)": "N/A",
            "Slots Occupés": "N/A",
            "Slots Totaux": "N/A"
        }

        if self.os_name == "Windows" and self.wmi_c:
            try:
                mem_modules = self.wmi_c.Win32_PhysicalMemory()
                if mem_modules:
                    type_map = {
                        0: "Inconnu", 1: "Autre", 2: "DRAM", 3: "Synchronous DRAM", 4: "Cache DRAM",
                        5: "EDO", 6: "SDRAM", 7: "SRAM", 8: "RAM", 9: "ROM", 10: "Flash",
                        11: "EEPROM", 12: "FEPROM", 13: "EPROM", 14: "CDRAM", 15: "3DRAM",
                        16: "SDRAM (Synchronous)", 17: "SGRAM", 18: "RDRAM", 19: "DDR",
                        20: "DDR2", 21: "DDR2 FB-DIMM", 22: "DDR3", 23: "FBD2", 24: "DDR4", 25: "LPDDR3", 26: "LPDDR4",
                        27: "DDR5"
                    }
                    ram_details["Type"] = type_map.get(mem_modules[0].MemoryType, "Inconnu")
                    ram_details["Vitesse (MHz)"] = mem_modules[0].Speed or "N/A"
                    ram_details["Slots Occupés"] = len(mem_modules)
                
                for array in self.wmi_c.Win32_PhysicalMemoryArray():
                    ram_details["Slots Totaux"] = array.MemoryDevices
                    break
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                output = self._run_command(["sudo", "dmidecode", "--type", "memory"], requires_sudo=True)
                memory_blocks = re.findall(r'Memory Device\s+(.*?)(?=\nMemory Device|\Z)', output, re.DOTALL)
                
                occupied_slots = 0
                for block in memory_blocks:
                    if "Size: No Module Installed" not in block:
                        occupied_slots += 1
                    
                    if ram_details["Type"] == "Inconnu" and "Type:" in block:
                        type_match = re.search(r'Type:\s*(.*)', block)
                        if type_match: ram_details["Type"] = type_match.group(1).strip()
                    
                    if ram_details["Vitesse (MHz)"] == "N/A" and "Speed:" in block and "Unknown" not in block:
                        speed_match = re.search(r'Speed:\s*(\d+)', block)
                        if speed_match: ram_details["Vitesse (MHz)"] = speed_match.group(1).strip() + " MHz"
                
                ram_details["Slots Occupés"] = occupied_slots

                output_array = self._run_command(["sudo", "dmidecode", "--type", "16"], requires_sudo=True)
                match = re.search(r'Number Of Devices:\s*(\d+)', output_array)
                if match:
                    ram_details["Slots Totaux"] = match.group(1)
            except Exception as e:
                pass
        return ram_details

    def get_storage_info(self):
        drives = []
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for disk in self.wmi_c.Win32_DiskDrive():
                    drive_info = {
                        "Type": "Disque Physique",
                        "Modèle": disk.Model or "N/A",
                        "Fabricant": disk.Manufacturer or "N/A",
                        "Taille Totale (GB)": f"{int(disk.Size) / (1024**3):.2f}" if disk.Size else "N/A",
                        "Interface": disk.InterfaceType or "N/A",
                        "Numéro de Série": disk.SerialNumber or "N/A",
                        "Média Type": "SSD" if "SSD" in (disk.Caption or "").upper() or "SSD" in (disk.Model or "").upper() else "HDD/Autre"
                    }
                    drives.append(drive_info)

                partitions = psutil.disk_partitions()
                for p in partitions:
                    try:
                        usage = psutil.disk_usage(p.mountpoint)
                        drives.append({
                            "Type": "Partition Logique",
                            "Montage": p.mountpoint,
                            "Système de Fichiers": p.fstype,
                            "Total (GB)": f"{usage.total / (1024**3):.2f}",
                            "Utilisé (GB)": f"{usage.used / (1024**3):.2f}",
                            "Libre (GB)": f"{usage.free / (1024**3):.2f}",
                            "Pourcentage (%)": usage.percent,
                        })
                    except Exception:
                        pass
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                json_output = self._run_command(["lsblk", "-J", "-b"])
                if json_output:
                    lsblk_data = json.loads(json_output)
                    for block_device in lsblk_data.get("blockdevices", []):
                        if block_device.get("type") == "disk":
                            drive_info = {
                                "Type": "Disque Physique",
                                "Nom": block_device.get("name", "N/A"),
                                "Taille Totale (GB)": f"{int(block_device.get('size', 0)) / (1024**3):.2f}" if block_device.get("size") else "N/A",
                                "Modèle": block_device.get("model", "N/A"),
                                "Fabricant": block_device.get("vendor", "N/A"),
                                "Média Type": "SSD" if block_device.get("rota", "1") == "0" else "HDD/Autre",
                                "Statut": block_device.get("state", "N/A")
                            }
                            drives.append(drive_info)
                        
                        if "children" in block_device:
                            for partition in block_device["children"]:
                                if partition.get("type") == "part":
                                    partition_info = {
                                        "Type": "Partition Logique",
                                        "Nom": partition.get("name", "N/A"),
                                        "Montage": partition.get("mountpoint", "N/A"),
                                        "Système de Fichiers": partition.get("fstype", "N/A"),
                                        "Taille Totale (GB)": f"{int(partition.get('size', 0)) / (1024**3):.2f}" if partition.get("size") else "N/A",
                                        "Statut": partition.get("state", "N/A")
                                    }
                                    if partition_info["Montage"] != "N/A":
                                        try:
                                            usage = psutil.disk_usage(partition_info["Montage"])
                                            partition_info["Utilisé (GB)"] = f"{usage.used / (1024**3):.2f}"
                                            partition_info["Libre (GB)"] = f"{usage.free / (1024**3):.2f}"
                                            partition_info["Pourcentage (%)"] = usage.percent
                                        except Exception:
                                            pass
                                    drives.append(partition_info)
            except (json.JSONDecodeError, Exception) as e:
                pass
        return drives

    def get_gpu_info(self):
        gpus = []
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for controller in self.wmi_c.Win32_VideoController():
                    gpus.append({
                        "Nom": controller.Name or "N/A",
                        "Fabricant": controller.AdapterCompatibility or "N/A",
                        "Type": "GPU",
                        "Mémoire Vidéo (MB)": f"{controller.AdapterRAM / (1024**2):.0f}" if controller.AdapterRAM else "N/A",
                        "Résolution Actuelle": f"{controller.CurrentHorizontalResolution}x{controller.CurrentVerticalResolution}" if controller.CurrentHorizontalResolution else "N/A",
                        "Pilote Version": controller.DriverVersion or "N/A",
                        "Statut": controller.Status or "N/A"
                    })
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                output = self._run_command(["lspci", "-vmm"])
                for block in output.split("\n\n"):
                    if "VGA" in block or "3D controller" in block:
                        gpu_info = {"Type": "GPU", "Nom": "N/A", "Fabricant": "N/A", "Statut": "Détecté", "Mémoire Vidéo (MB)": "N/A"}
                        for line in block.splitlines():
                            if "Vendor:" in line:
                                gpu_info["Fabricant"] = line.split(":", 1)[1].strip()
                            elif "Device:" in line:
                                gpu_info["Nom"] = line.split(":", 1)[1].strip()
                            elif "Memory:" in line:
                                mem_match = re.search(r'\[size=(\d+)M\]', line)
                                if mem_match:
                                    gpu_info["Mémoire Vidéo (MB)"] = mem_match.group(1)
                        gpus.append(gpu_info)
            except Exception as e:
                pass
        return gpus

    def get_motherboard_info(self):
        mobo_info = {
            "Fabricant": "N/A",
            "Modèle": "N/A",
            "Version du Produit": "N/A",
            "Numéro de Série": "N/A",
            "BIOS Fabricant": "N/A",
            "BIOS Version": "N/A",
            "Date BIOS": "N/A",
            "Mode BIOS": "N/A"
        }
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for board in self.wmi_c.Win32_BaseBoard():
                    mobo_info["Fabricant"] = board.Manufacturer or "N/A"
                    mobo_info["Modèle"] = board.Product or "N/A"
                    mobo_info["Version du Produit"] = board.Version or "N/A"
                    mobo_info["Numéro de Série"] = board.SerialNumber or "N/A"
                    break
                for bios in self.wmi_c.Win32_BIOS():
                    mobo_info["BIOS Fabricant"] = bios.Manufacturer or "N/A"
                    mobo_info["BIOS Version"] = bios.SMBIOSBIOSVersion or "N/A"
                    mobo_info["Date BIOS"] = bios.ReleaseDate or "N/A"
                    
                    if hasattr(bios, 'SMBIOSMajorVersion') and bios.SMBIOSMajorVersion >= 2 and hasattr(bios, 'SMBIOSMinorVersion') and bios.SMBIOSMinorVersion >= 7:
                        mobo_info["Mode BIOS"] = "UEFI" if "UEFI" in (bios.Caption or "").upper() or "UEFI" in (bios.Description or "").upper() else "Legacy BIOS"
                    else:
                        mobo_info["Mode BIOS"] = "Legacy BIOS"
                    break
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                output_board = self._run_command(["sudo", "dmidecode", "--type", "baseboard"], requires_sudo=True)
                output_bios = self._run_command(["sudo", "dmidecode", "--type", "bios"], requires_sudo=True)

                for line in output_board.splitlines():
                    if "Manufacturer:" in line: mobo_info["Fabricant"] = line.split(":", 1)[1].strip()
                    elif "Product Name:" in line: mobo_info["Modèle"] = line.split(":", 1)[1].strip()
                    elif "Version:" in line: mobo_info["Version du Produit"] = line.split(":", 1)[1].strip()
                    elif "Serial Number:" in line: mobo_info["Numéro de Série"] = line.split(":", 1)[1].strip()

                for line in output_bios.splitlines():
                    if "Vendor:" in line: mobo_info["BIOS Fabricant"] = line.split(":", 1)[1].strip()
                    elif "Version:" in line: mobo_info["BIOS Version"] = line.split(":", 1)[1].strip()
                    elif "Release Date:" in line: mobo_info["Date BIOS"] = line.split(":", 1)[1].strip()
                
                if os.path.exists("/sys/firmware/efi"):
                    mobo_info["Mode BIOS"] = "UEFI"
                else:
                    mobo_info["Mode BIOS"] = "Legacy BIOS"
            except Exception as e:
                pass
        return mobo_info

    def get_input_devices(self):
        input_devices = []
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for keyboard in self.wmi_c.Win32_Keyboard():
                    input_devices.append({
                        "Type": "Clavier",
                        "Nom": keyboard.Name or "N/A",
                        "Fabricant": keyboard.Manufacturer or "N/A",
                        "Description": keyboard.Description or "N/A",
                        "Statut": keyboard.Status or "N/A"
                    })
                for mouse in self.wmi_c.Win32_PointingDevice():
                    input_devices.append({
                        "Type": "Souris / Périphérique de pointage",
                        "Nom": mouse.Name or "N/A",
                        "Fabricant": mouse.Manufacturer or "N/A",
                        "Description": mouse.Description or "N/A",
                        "Statut": mouse.Status or "N/A",
                        "Interface": mouse.HardwareType or "N/A"
                    })
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                output_lshw = self._run_command(["sudo", "lshw", "-json", "-class", "input"], requires_sudo=True)
                if output_lshw:
                    lshw_data = json.loads(output_lshw)
                    if not isinstance(lshw_data, list): lshw_data = [lshw_data]
                    for dev in lshw_data:
                        description = dev.get("description", "").lower()
                        if "keyboard" in description or "kbd" in dev.get("id", "").lower():
                            input_devices.append({
                                "Type": "Clavier",
                                "Nom": dev.get("product", "N/A"),
                                "Fabricant": dev.get("vendor", "N/A"),
                                "Description": description.capitalize(),
                                "Statut": "Détecté"
                            })
                        elif "mouse" in description or "pointer" in description or "touchpad" in description:
                            input_devices.append({
                                "Type": "Souris / Périphérique de pointage",
                                "Nom": dev.get("product", "N/A"),
                                "Fabricant": dev.get("vendor", "N/A"),
                                "Description": description.capitalize(),
                                "Statut": "Détecté"
                            })
            except (json.JSONDecodeError, Exception) as e:
                try:
                    output = self._run_command(["xinput", "--list"])
                    for line in output.splitlines():
                        if "keyboard" in line.lower() or "mouse" in line.lower() or "pointer" in line.lower() or "touchpad" in line.lower():
                            name_match = re.search(r'[^ ]+(?=\s+id=)', line)
                            id_match = re.search(r'id=(\d+)', line)
                            
                            name = name_match.group(0).strip() if name_match else "N/A"
                            id_val = id_match.group(1).strip() if id_match else "N/A"
                            
                            device_type = "Périphérique d'entrée"
                            if "keyboard" in line.lower(): device_type = "Clavier"
                            elif "mouse" in line.lower() or "pointer" in line.lower() or "touchpad" in line.lower(): device_type = "Souris / Périphérique de pointage"

                            input_devices.append({
                                "Type": device_type,
                                "Nom": name,
                                "Fabricant": "Inconnu (via XInput)",
                                "Statut": f"Présent (ID: {id_val})",
                                "Description": line.strip()
                            })
                except Exception as e:
                    pass
        return input_devices

    def get_usb_devices(self):
        devices = []
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for usb in self.wmi_c.Win32_PnPEntity():
                    if usb.DeviceID and "VID_" in usb.DeviceID and \
                       ("USB" in (usb.Name or "").upper() or "USB" in (usb.Description or "").upper()):
                        if not ("Host Controller" in (usb.Name or "") or "Root Hub" in (usb.Name or "")):
                            devices.append({
                                "Type": "Périphérique USB",
                                "Nom": usb.Name or "N/A",
                                "Fabricant": usb.Manufacturer or "N/A",
                                "Statut": "Activé" if usb.Status == "OK" else "Non fonctionnel",
                                "Description": usb.Description or "N/A",
                                "ID Périphérique": usb.DeviceID or "N/A"
                            })
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                output = self._run_command(["lsusb", "-v"])
                current_device = {}
                for line in output.splitlines():
                    line = line.strip()
                    if line.startswith("Bus") and line.endswith("Device"):
                        if current_device:
                            devices.append(current_device)
                        current_device = {
                            "Type": "Périphérique USB",
                            "Nom": "N/A",
                            "Fabricant": "N/A",
                            "Statut": "Présent",
                            "ID Périphérique": line
                        }
                    elif current_device:
                        if "iProduct" in line and current_device["Nom"] == "N/A":
                            current_device["Nom"] = line.split("iProduct", 1)[1].split(":")[1].strip()
                        elif "iManufacturer" in line and current_device["Fabricant"] == "N/A":
                            current_device["Fabricant"] = line.split("iManufacturer", 1)[1].split(":")[1].strip()
                        elif "ID" in line and "Bus" not in line and "Device" not in line and "ID Périphérique" in current_device:
                            current_device["ID Périphérique"] = line.replace("ID ", "").strip()
                if current_device:
                    devices.append(current_device)
            except Exception as e:
                pass
        return devices

    def get_network_adapters(self):
        devices = []
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for adapter in self.wmi_c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
                    net_adapter = {
                        "Type": "Adaptateur Réseau",
                        "Nom": adapter.Description or "N/A",
                        "Fabricant": adapter.Manufacturer or "N/A",
                        "Statut": "Activé" if adapter.IPEnabled else "Désactivé",
                        "Adresse MAC": adapter.MACAddress or "N/A",
                        "IP Adresses": ", ".join(adapter.IPAddress) if adapter.IPAddress else "N/A",
                        "Serveurs DNS": ", ".join(adapter.DNSServerSearchOrder) if adapter.DNSServerSearchOrder else "N/A",
                        "DHCP Activé": "Oui" if adapter.DHCPEnabled else "Non",
                        "Vitesse (Mbps)": f"{adapter.Speed / 1000000:.0f}" if adapter.Speed else "N/A",
                        "Duplex": "Full" if adapter.FullDuplex else "Half" if adapter.HalfDuplex else "N/A"
                    }
                    devices.append(net_adapter)
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                interfaces = psutil.net_if_stats()
                addrs = psutil.net_if_addrs()
                
                for name, stats in interfaces.items():
                    if stats.isup:
                        ip_addresses = []
                        dns_servers = []
                        mac_address = "N/A"
                        if name in addrs:
                            for addr in addrs[name]:
                                if addr.family == socket.AF_INET:
                                    ip_addresses.append(addr.address)
                                elif addr.family == psutil.AF_LINK:
                                    mac_address = addr.address
                        
                        try:
                            with open("/etc/resolv.conf", "r") as f:
                                for line in f:
                                    if line.strip().startswith("nameserver"):
                                        dns_servers.append(line.split()[1].strip())
                        except Exception:
                            pass

                        speed_mbps = "N/A"
                        duplex_info = "N/A"
                        ethtool_output = self._run_command(["sudo", "ethtool", name], requires_sudo=True)
                        if ethtool_output:
                            speed_match = re.search(r'Speed:\s*(\d+)\s*Mb/s', ethtool_output)
                            if speed_match:
                                speed_mbps = speed_match.group(1)
                            duplex_match = re.search(r'Duplex:\s*(Full|Half)', ethtool_output)
                            if duplex_match:
                                duplex_info = duplex_match.group(1)

                        devices.append({
                            "Type": "Adaptateur Réseau",
                            "Nom": name,
                            "Fabricant": "N/A (vérifier lspci -k)",
                            "Statut": "Activé",
                            "Adresse MAC": mac_address,
                            "IP Adresses": ", ".join(ip_addresses) if ip_addresses else "N/A",
                            "Serveurs DNS": ", ".join(dns_servers) if dns_servers else "N/A",
                            "Vitesse (Mbps)": speed_mbps,
                            "Duplex": duplex_info
                        })
            except Exception as e:
                pass
        return devices

    def get_audio_devices(self):
        devices = []
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for audio in self.wmi_c.Win32_SoundDevice():
                    devices.append({
                        "Type": "Appareil Audio",
                        "Nom": audio.Name or "N/A",
                        "Fabricant": audio.Manufacturer or "N/A",
                        "Statut": "Activé" if audio.Status == "OK" else "Non fonctionnel",
                        "Description": audio.Description or "N/A",
                        "Pilote Version": audio.DriverVersion or "N/A"
                    })
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                output_cards = self._run_command(["aplay", "-l"])
                if output_cards:
                    for line in output_cards.splitlines():
                        if "card" in line and "device" in line:
                            card_name_match = re.search(r'card \d+: (.*?) \[', line)
                            device_name_match = re.search(r'device \d+: (.*?) \[', line)
                            card_name = card_name_match.group(1).strip() if card_name_match else "N/A"
                            device_name = device_name_match.group(1).strip() if device_name_match else "N/A"
                            devices.append({
                                "Type": "Appareil Audio (Sortie)",
                                "Nom": f"{card_name} ({device_name})",
                                "Fabricant": "N/A (vérifier lspci -v)",
                                "Statut": "Présent",
                                "Description": line.strip()
                            })
                output_rec = self._run_command(["arecord", "-l"])
                if output_rec:
                    for line in output_rec.splitlines():
                        if "card" in line and "device" in line:
                            card_name_match = re.search(r'card \d+: (.*?) \[', line)
                            device_name_match = re.search(r'device \d+: (.*?) \[', line)
                            card_name = card_name_match.group(1).strip() if card_name_match else "N/A"
                            device_name = device_name_match.group(1).strip() if device_name_match else "N/A"
                            devices.append({
                                "Type": "Appareil Audio (Entrée)",
                                "Nom": f"{card_name} ({device_name})",
                                "Fabricant": "N/A (vérifier lspci -v)",
                                "Statut": "Présent",
                                "Description": line.strip()
                            })
            except Exception as e:
                pass
        return devices

    def get_cameras(self):
        devices = []
        if OPENCV_AVAILABLE:
            i = 0
            while True:
                # Suppress OpenCV warnings/errors to console for cleaner output
                # This is a common workaround, but doesn't fix the underlying camera access issue
                # It just makes the console less noisy.
                # For a true fix, user permissions or device drivers need to be checked.
                # You might need to add your user to the 'video' group on Linux: sudo usermod -a -G video $USER
                # And then log out and back in.
                
                # We won't redirect stderr directly in Python for the VideoCapture constructor
                # as it might break valid error reporting. Instead, rely on cap.isOpened()
                # and print a more user-friendly message if it fails.
                cap = cv2.VideoCapture(i)
                if not cap.isOpened():
                    # print(f"DEBUG: Could not open camera at index {i}. Trying next...")
                    if i == 0: # Only show this warning for the very first camera attempt
                        print("ATTENTION: Le script n'a pas pu accéder à la caméra. Assurez-vous d'avoir les permissions nécessaires (ex: ajouter votre utilisateur au groupe 'video' sur Linux).")
                    cap.release()
                    i += 1
                    if i > 5: # Limit scan to prevent infinite loop on systems with no cameras
                        break
                    continue
                
                ret, frame = cap.read()
                if ret:
                    backend_name = cap.getBackendName() if hasattr(cap, 'getBackendName') else "N/A"
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    
                    devices.append({
                        "Type": "Webcam",
                        "Nom": f"Caméra {i}",
                        "Fabricant": "N/A (via OpenCV)",
                        "Statut": "Connectée et accessible",
                        "Résolution par défaut": f"{width}x{height}",
                        "Backend": backend_name,
                        "Description": f"Périphérique de capture vidéo index {i}"
                    })
                cap.release()
                i += 1
        else:
            devices.append({
                "Type": "Webcam",
                "Nom": "N/A",
                "Fabricant": "N/A",
                "Statut": "Détection non disponible (OpenCV non installé)",
                "Description": "Installer 'opencv-python' pour la détection."
            })
        return devices

    def get_printers(self):
        devices = []
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for printer in self.wmi_c.Win32_Printer():
                    devices.append({
                        "Type": "Imprimante",
                        "Nom": printer.Name or "N/A",
                        "Fabricant": printer.Manufacturer or "N/A",
                        "Statut": "En ligne" if printer.PrinterStatus == 3 else "Hors ligne",
                        "Port": printer.PortName or "N/A",
                        "Pilote Nom": printer.DriverName or "N/A",
                        "Par défaut": "Oui" if printer.Default else "Non"
                    })
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                output = self._run_command(["lpstat", "-p"])
                for line in output.splitlines():
                    if line.startswith("printer"):
                        name_match = re.search(r'printer\s+(.*?)\s+is', line)
                        name = name_match.group(1).strip() if name_match else "N/A"
                        status = "En ligne" if "enabled" in line and "idle" in line else "Hors ligne/Occupée"
                        is_default = "is default" in line
                        devices.append({
                            "Type": "Imprimante",
                            "Nom": name,
                            "Fabricant": "N/A",
                            "Statut": status,
                            "Par défaut": "Oui" if is_default else "Non",
                            "Description": line
                        })
            except Exception as e:
                pass
        return devices

    def get_optical_drives(self):
        devices = []
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for drive in self.wmi_c.Win32_CDROMDrive():
                    devices.append({
                        "Type": "Lecteur Optique",
                        "Nom": drive.Name or "N/A",
                        "Fabricant": drive.Manufacturer or "N/A",
                        "Statut": "Activé" if drive.Status == "OK" else "Non fonctionnel",
                        "Lettre de lecteur": drive.Drive or "N/A"
                    })
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                output = self._run_command(["lsscsi", "-g"])
                for line in output.splitlines():
                    if "cd/dvd" in line.lower() or "rom" in line.lower():
                        name_match = re.search(r'\[\d+:\d+:\d+:\d+\]\s+disk\s+(.*?)\s+(/dev/\S+)', line)
                        name = name_match.group(1).strip() if name_match else "N/A"
                        path = name_match.group(2).strip() if name_match else "N/A"
                        devices.append({
                            "Type": "Lecteur Optique",
                            "Nom": name,
                            "Chemin Périphérique": path,
                            "Fabricant": "N/A",
                            "Statut": "Présent",
                            "Description": line
                        })
            except Exception as e:
                pass
        return devices
    
    def get_bluetooth_status(self):
        if self.os_name == "Windows" and self.wmi_c:
            try:
                for adapter in self.wmi_c.Win32_PnPEntity(Name="%Bluetooth%"):
                    if adapter.Status == "OK":
                        return True
                return False
            except Exception as e:
                return False
        elif self.os_name == "Linux":
            try:
                output = self._run_command(["systemctl", "is-active", "bluetooth"])
                return "active" in output
            except Exception as e:
                return False
        return False

    def get_firewall_status(self):
        if self.os_name == "Windows":
            try:
                output = self._run_command(['netsh', 'advfirewall', 'show', 'allprofiles', 'state'])
                return "State       ON" in output or "Activé" in output
            except Exception as e:
                return False
        elif self.os_name == "Linux":
            try:
                ufw_status = self._run_command(["sudo", "ufw", "status"], requires_sudo=True)
                if "Status: active" in ufw_status:
                    return True
                firewalld_status = self._run_command(["sudo", "systemctl", "is-active", "firewalld"], requires_sudo=True)
                if "active" in firewalld_status:
                    return True
            except Exception as e:
                pass
        return False

    def get_battery_status(self):
        battery = psutil.sensors_battery()
        if battery:
            return {
                "present": True,
                "percent": battery.percent,
                "power_plugged": battery.power_plugged,
                "secsleft": battery.secsleft
            }
        return {"present": False}

    def get_os_info(self):
        os_info = {
            "Nom": platform.system(),
            "Version": platform.version(),
            "Nom Complet": "N/A",
            "Architecture": platform.machine(),
            "Nom d'Hôte": socket.gethostname(),
            "Utilisateur Actuel": os.getlogin() if hasattr(os, 'getlogin') else os.getenv('USER') or os.getenv('USERNAME') or "N/A",
            "Démarrage depuis": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        }
        if self.os_name == "Windows":
            try:
                os_info["Nom Complet"] = platform.win32_edition() or platform.platform()
                output = self._run_command(["systeminfo"])
                match = re.search(r'OS Build:\s*(\d+)', output)
                if match:
                    os_info["Build OS"] = match.group(1)
            except Exception as e:
                pass
        elif self.os_name == "Linux":
            try:
                lsb_release = self._run_command(["lsb_release", "-ds"])
                if lsb_release:
                    os_info["Nom Complet"] = lsb_release
                else:
                    if os.path.exists("/etc/os-release"):
                        with open("/etc/os-release", "r") as f:
                            for line in f:
                                if line.startswith("PRETTY_NAME="):
                                    os_info["Nom Complet"] = line.split("=", 1)[1].strip().strip('"')
                                    break
            except Exception as e:
                pass
        return os_info

    def get_all_hardware_info(self):
        all_info = []

        all_info.append({"Type": "Système d'Exploitation", **self.get_os_info()})
        all_info.append({"Type": "CPU (Processeur)", **self.get_cpu_info()})
        all_info.append({"Type": "RAM (Mémoire Vive)", **self.get_ram_info()})
        all_info.append({"Type": "Carte Mère / BIOS", **self.get_motherboard_info()})
        all_info.extend(self.get_gpu_info()) 
        all_info.extend(self.get_storage_info())
        all_info.extend(self.get_input_devices())
        all_info.extend(self.get_usb_devices())
        all_info.extend(self.get_network_adapters())
        all_info.extend(self.get_audio_devices())
        all_info.extend(self.get_cameras())
        all_info.extend(self.get_printers())
        all_info.extend(self.get_optical_drives())

        if self.os_name == "Linux":
            pci_output = self._run_command(["lspci"])
            if pci_output:
                all_info.append({
                    "Type": "Périphériques PCI (détails bruts)",
                    "Détails": pci_output.splitlines()
                })
        
        all_info.append({
            "Type": "Processus en Cours",
            "Nombre Total": len(psutil.pids()),
            "Exemple": ", ".join([p.name() for p in psutil.process_iter(['name'])][:5]) + "..."
        })
        
        return all_info

    def calculate_power_score(self, hardware_info):
        score = 0
        max_possible_score = 100

        weights = {
            "cpu": 25,
            "ram": 15,
            "gpu": 30,
            "storage": 15,
            "network": 5,
            "other": 10
        }

        # --- Score CPU ---
        # Ensure default {} is always provided for next()
        cpu_info = next((d for d in hardware_info if d.get("Type") == "CPU (Processeur)"), {})
        cores = cpu_info.get("Cœurs Physiques", 1)
        freq_max_str = cpu_info.get("Fréquence Max", "0 MHz").replace(" MHz", "").replace(" GHz", "000")
        freq_max = float(freq_max_str.replace(",", ".")) if freq_max_str.replace('.', '', 1).replace(',', '', 1).isdigit() else 0

        cpu_subscore = 0
        if cores >= 16: cpu_subscore += 0.5
        elif cores >= 8: cpu_subscore += 0.4
        elif cores >= 4: cpu_subscore += 0.2
        elif cores >= 2: cpu_subscore += 0.1
        
        if freq_max >= 4500: cpu_subscore += 0.5
        elif freq_max >= 3500: cpu_subscore += 0.4
        elif freq_max >= 2500: cpu_subscore += 0.2
        elif freq_max >= 1500: cpu_subscore += 0.1
        
        if "64-bit" in cpu_info.get("Architecture", ""): cpu_subscore += 0.1
        if "Intel" in cpu_info.get("Fabricant", "").lower() or "amd" in cpu_info.get("Fabricant", "").lower(): cpu_subscore += 0.1
        
        score += min(cpu_subscore * weights["cpu"], weights["cpu"])

        # --- Score RAM ---
        ram_info = next((d for d in hardware_info if d.get("Type") == "RAM (Mémoire Vive)"), {})
        total_ram_gb_str = ram_info.get("Total (GB)", "0").replace(",", ".")
        total_ram_gb = float(total_ram_gb_str) if total_ram_gb_str.replace('.', '', 1).isdigit() else 0
        ram_type = ram_info.get("Type", "").upper()
        ram_speed_str = ram_info.get("Vitesse (MHz)", "0").replace(" MHz", "")
        ram_speed = int(ram_speed_str) if ram_speed_str.isdigit() else 0

        ram_subscore = 0
        if total_ram_gb >= 64: ram_subscore += 0.5
        elif total_ram_gb >= 32: ram_subscore += 0.4
        elif total_ram_gb >= 16: ram_subscore += 0.2
        elif total_ram_gb >= 8: ram_subscore += 0.1
        
        if "DDR5" in ram_type: ram_subscore += 0.3
        elif "DDR4" in ram_type: ram_subscore += 0.2
        elif "DDR3" in ram_type: ram_subscore += 0.1

        if ram_speed >= 4800: ram_subscore += 0.3
        elif ram_speed >= 3200: ram_subscore += 0.2
        elif ram_speed >= 2400: ram_subscore += 0.1

        score += min(ram_subscore * weights["ram"], weights["ram"])

        # --- Score GPU ---
        gpu_info_list = [d for d in hardware_info if d.get("Type") == "GPU"]
        gpu_subscore = 0
        if gpu_info_list:
            dedicated_gpu_found = False
            for gpu in gpu_info_list:
                if any(kwd in gpu.get("Fabricant", "").lower() for kwd in ["nvidia", "amd", "intel"]) and \
                   any(kwd in gpu.get("Nom", "").lower() for kwd in ["geforce", "radeon", "arc", "rtx", "rx", "quadro", "firepro"]):
                    dedicated_gpu_found = True
                    vram_mb_str = str(gpu.get("Mémoire Vidéo (MB)", "0")).replace(",", ".")
                    vram_mb = int(float(vram_mb_str)) if vram_mb_str.replace('.', '', 1).isdigit() else 0

                    if vram_mb >= 16384: gpu_subscore += 0.6
                    elif vram_mb >= 8192: gpu_subscore += 0.4
                    elif vram_mb >= 4096: gpu_subscore += 0.2
                    break

            if dedicated_gpu_found: gpu_subscore += 0.4
            else: gpu_subscore += 0.1
        
        score += min(gpu_subscore * weights["gpu"], weights["gpu"])

        # --- Score Stockage ---
        storage_subscore = 0
        total_ssd_capacity_gb = 0
        total_hdd_capacity_gb = 0

        for drive in hardware_info:
            if drive.get("Type") == "Disque Physique":
                total_size_gb_str = drive.get("Taille Totale (GB)", "0").replace(",", ".")
                total_size_gb = float(total_size_gb_str) if total_size_gb_str.replace('.', '', 1).isdigit() else 0

                if drive.get("Média Type") == "SSD":
                    storage_subscore += 0.5
                    total_ssd_capacity_gb += total_size_gb
                elif drive.get("Média Type") == "HDD/Autre":
                    storage_subscore += 0.1
                    total_hdd_capacity_gb += total_size_gb
        
        if total_ssd_capacity_gb >= 2000: storage_subscore += 0.4
        elif total_ssd_capacity_gb >= 1000: storage_subscore += 0.3
        elif total_ssd_capacity_gb >= 500: storage_subscore += 0.2
        elif total_ssd_capacity_gb >= 250: storage_subscore += 0.1

        if total_hdd_capacity_gb >= 4000: storage_subscore += 0.1
        elif total_hdd_capacity_gb >= 2000: storage_subscore += 0.05

        score += min(storage_subscore * weights["storage"], weights["storage"])

        # --- Score Réseau ---
        network_subscore = 0
        for net_adapter in hardware_info:
            if net_adapter.get("Type") == "Adaptateur Réseau" and net_adapter.get("Statut") == "Activé":
                speed_str = net_adapter.get("Vitesse (Mbps)", "0")
                speed_mbps = int(speed_str) if str(speed_str).isdigit() else 0
                if speed_mbps >= 10000:
                    network_subscore += 0.5
                elif speed_mbps >= 2500:
                    network_subscore += 0.3
                elif speed_mbps >= 1000:
                    network_subscore += 0.2
                break
        score += min(network_subscore * weights["network"], weights["network"])

        # --- Autres Facteurs (OS, Pare-feu, Batterie, etc.) ---
        other_subscore = 0
        
        # Ensure default [ {} ] is always provided for next() on a list comprehension
        os_info = next((d for d in hardware_info if d.get("Type") == "Système d'Exploitation"), {}) 
        if "64-bit" in os_info.get("Architecture", ""): other_subscore += 0.1
        
        if self.get_firewall_status(): other_subscore += 0.1
        
        battery_info = self.get_battery_status()
        if battery_info["present"]: other_subscore += 0.1
        if battery_info["present"] and battery_info["percent"] > 20: other_subscore += 0.05

        if any(d.get('Type') == "Webcam" and "accessible" in d.get('Statut', '') for d in hardware_info): other_subscore += 0.05
        if any(d.get('Type') == "Appareil Audio (Entrée)" and "Présent" in d.get('Statut', '') for d in hardware_info): other_subscore += 0.05
        if any(d.get('Type') == "Appareil Audio (Sortie)" and "Présent" in d.get('Statut', '') for d in hardware_info): other_subscore += 0.05
        if any(d.get('Type') == "Imprimante" and "En ligne" in d.get('Statut', '') for d in hardware_info): other_subscore += 0.05
        if any(d.get('Type') == "Lecteur Optique" and "Présent" in d.get('Statut', '') for d in hardware_info): other_subscore += 0.02
        if self.get_bluetooth_status(): other_subscore += 0.05
        
        score += min(other_subscore * weights["other"], weights["other"])

        final_score = int(max(0, min(score, max_possible_score)))
        return final_score


class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tableau de Bord Détaillé du Matériel et Score de Puissance")
        self.geometry("1500x950")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self, text="État et Capacités Détaillés du Matériel Système", font=ctk.CTkFont(size=30, weight="bold")).grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.top_info_frame = ctk.CTkFrame(self, corner_radius=10)
        self.top_info_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.top_info_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.cap_labels = {}
        capabilities_definitions = [
            ("Voir (Webcam)", "Non détecté"),
            ("Entendre (Micro)", "Non détecté"),
            ("Parler (Audio Sortie)", "Non détecté"),
            ("Communiquer (Réseau)", "Non détecté"),
            ("Impression", "Non détecté"),
            ("Lecture Optique", "Non détecté"),
            ("Stockage Suffisant", "Non"),
            ("Multitâche Efficace", "Non"),
            ("Graphismes Avancés", "Non détecté"),
            ("Connectivité Bluetooth", "Non"),
            ("Virtualisation", "Non"),
            ("Protection par Pare-feu", "Non"),
            ("Alimentation Portable", "Non"),
            ("Saisie Clavier", "Non détecté"),
            ("Saisie Souris/Pad", "Non détecté")
        ]

        ctk.CTkLabel(self.top_info_frame, text="Capacités Actuelles:", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        
        col_count = 4
        for i, (cap_name, default_status) in enumerate(capabilities_definitions):
            row = (i // col_count) + 1
            col = i % col_count
            label_text = f"**{cap_name}**: {default_status}"
            label = ctk.CTkLabel(self.top_info_frame, text=label_text, font=ctk.CTkFont(size=14))
            label.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            self.cap_labels[cap_name] = label

        self.power_score_label = ctk.CTkLabel(self.top_info_frame, text="Score de Puissance du PC (0-100): N/A", font=ctk.CTkFont(size=20, weight="bold"), text_color="yellow")
        self.power_score_label.grid(row= (len(capabilities_definitions) // col_count) + 2, column=0, columnspan=4, padx=10, pady=15, sticky="w")

        self.device_list_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.device_list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.device_list_frame.grid_columnconfigure(0, weight=1)

        self.last_scan_label = ctk.CTkLabel(self, text="Dernière analyse: N/A", font=ctk.CTkFont(size=12))
        self.last_scan_label.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="e")

        self.refresh_button = ctk.CTkButton(self, text="Rafraîchir les informations", command=self.update_dashboard)
        self.refresh_button.grid(row=4, column=0, padx=20, pady=10)

        self.scanner = DeviceScanner()
        self.device_widgets = []

        self.update_dashboard()

    def update_dashboard(self):
        for widget in self.device_widgets:
            widget.destroy()
        self.device_widgets.clear()

        all_hardware_info = self.scanner.get_all_hardware_info()

        current_capabilities = {cap_name: False for cap_name in self.cap_labels.keys()}
        
        # Ensure default {} is always provided for next()
        os_info = next((d for d in all_hardware_info if d.get("Type") == "Système d'Exploitation"), {})
        cpu_info = next((d for d in all_hardware_info if d.get("Type") == "CPU (Processeur)"), {})
        
        total_free_gb = sum(
            float(d.get("Libre (GB)", "0").replace(",", "."))
            for d in all_hardware_info if d.get("Type") == "Partition Logique"
            and (d.get("Libre (GB)", "0").replace('.', '', 1).replace(',', '', 1).isdigit())
        )
        if total_free_gb > 20:
             current_capabilities["Stockage Suffisant"] = True
        current_capabilities["Stockage Suffisant"] = f"{total_free_gb:.2f} GB total libre" if not current_capabilities["Stockage Suffisant"] else "Oui"

        cpu_cores = cpu_info.get("Cœurs Physiques", 0)
        cpu_freq_max_str = cpu_info.get("Fréquence Max", "0 MHz").replace(" MHz", "").replace(" GHz", "000")
        cpu_freq_max = float(cpu_freq_max_str.replace(",", ".")) if cpu_freq_max_str.replace('.', '', 1).replace(',', '', 1).isdigit() else 0

        if cpu_cores >= 4 and cpu_freq_max >= 2500:
            current_capabilities["Multitâche Efficace"] = True

        if "Oui" in cpu_info.get("Virtualisation Support", ""):
            current_capabilities["Virtualisation"] = True

        current_capabilities["Connectivité Bluetooth"] = self.scanner.get_bluetooth_status()

        current_capabilities["Protection par Pare-feu"] = self.scanner.get_firewall_status()

        battery_info = self.scanner.get_battery_status()
        if battery_info["present"]:
            battery_status_text = f"Oui ({battery_info['percent']:.0f}%, "
            if battery_info['power_plugged']:
                battery_status_text += "Branché)"
            elif battery_info['secsleft'] is not None and battery_info['secsleft'] != psutil.POWER_TIME_UNKNOWN:
                minutes = battery_info['secsleft'] // 60
                hours = minutes // 60
                minutes = minutes % 60
                battery_status_text += f"Reste: {hours}h {minutes}min)"
            else:
                battery_status_text += "Autonomie inconnue)"
            current_capabilities["Alimentation Portable"] = battery_status_text
        else:
             current_capabilities["Alimentation Portable"] = "Non (Pas de batterie)"

        for device_info in all_hardware_info:
            device_type = device_info.get('Type')
            device_status = device_info.get('Statut', '').lower()

            if device_type == "Webcam" and "accessible" in device_status:
                current_capabilities["Voir (Webcam)"] = True
            if device_type == "Appareil Audio (Entrée)" and "présent" in device_status:
                current_capabilities["Entendre (Micro)"] = True
            if device_type == "Appareil Audio (Sortie)" and "présent" in device_status:
                current_capabilities["Parler (Audio Sortie)"] = True
            if device_type == "Adaptateur Réseau" and "activé" in device_status:
                current_capabilities["Communiquer (Réseau)"] = True
            if device_type == "Imprimante" and "en ligne" in device_status:
                current_capabilities["Impression"] = True
            if device_type == "Lecteur Optique" and "présent" in device_status:
                current_capabilities["Lecture Optique"] = True
            if device_type == "GPU" and "détecté" in device_status:
                current_capabilities["Graphismes Avancés"] = True
            if device_type == "Clavier" and ("présent" in device_status or "activé" in device_status):
                current_capabilities["Saisie Clavier"] = True
            if device_type == "Souris / Périphérique de pointage" and ("présent" in device_status or "activé" in device_status):
                current_capabilities["Saisie Souris/Pad"] = True


        row_idx = 0
        if not all_hardware_info:
            no_devices_label = ctk.CTkLabel(self.device_list_frame, text="Aucune information matérielle détectée ou accès limité. Exécutez en tant qu'administrateur/root.", wraplength=1400)
            no_devices_label.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            self.device_widgets.append(no_devices_label)
            row_idx += 1
        else:
            for device_info in all_hardware_info:
                info_parts = []
                header_type = device_info.pop('Type', "Périphérique Inconnu")
                info_parts.append(f"**Type**: {header_type}")
                
                sorted_keys = sorted(device_info.keys(), key=lambda k: (k != "Nom", k != "Modèle", k))
                
                for key in sorted_keys:
                    value = device_info.get(key)
                    if value is not None:
                        if isinstance(value, list):
                            info_parts.append(f"**{key}**: " + ", ".join(map(str, value[:5])) + ("..." if len(value) > 5 else ""))
                        else:
                            info_parts.append(f"**{key}**: {value}")
                
                info_text = "\n".join(info_parts)

                device_label = ctk.CTkLabel(
                    self.device_list_frame,
                    text=info_text,
                    justify="left",
                    wraplength=1400,
                    corner_radius=8,
                    fg_color=("gray80", "gray20"),
                    pady=10, padx=10
                )
                device_label.grid(row=row_idx, column=0, padx=10, pady=5, sticky="ew")
                self.device_widgets.append(device_label)
                row_idx += 1

        for cap_name, label_widget in self.cap_labels.items():
            status_value = current_capabilities.get(cap_name, "Non détecté")
            if isinstance(status_value, bool):
                status_text = "Oui" if status_value else "Non"
            else:
                status_text = str(status_value)
            label_widget.configure(text=f"**{cap_name}**: {status_text}")
        
        power_score = self.scanner.calculate_power_score(all_hardware_info)
        self.power_score_label.configure(text=f"Score de Puissance du PC (0-100): {power_score}",
                                        text_color="green" if power_score >= 75 else "orange" if power_score >= 40 else "red")

        self.last_scan_label.configure(text=f"Dernière analyse: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = DashboardApp()
    app.mainloop()