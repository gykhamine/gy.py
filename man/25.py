import customtkinter as ctk
import os

# --- Nginx Configuration String Generation Logic ---
def create_nginx_config_string(domain_name, root_path, server_type, error_pages, enable_ssl, ssl_type, cert_path="", key_path="",
                               redirects=None, allow_deny_rules=None, url_rewrites=None):
    """
    Generates an Nginx configuration as a string based on server type, error pages, SSL settings,
    redirects, allow/deny rules, and URL rewrites.
    """
    if redirects is None:
        redirects = []
    if allow_deny_rules is None:
        allow_deny_rules = []
    if url_rewrites is None:
        url_rewrites = []

    config_lines = []

    # HTTP Block (for redirection to HTTPS or initial setup)
    config_lines.append(f"""
# Nginx configuration for {domain_name}
server {{
    listen 80;
    server_name {domain_name} www.{domain_name};
""")

    if enable_ssl:
        config_lines.append(f"""
    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}}

server {{
    listen 443 ssl;
    server_name {domain_name} www.{domain_name};

    root {root_path};
""")
        if ssl_type == "Certbot (Let's Encrypt)":
            config_lines.append(f"""
    # SSL configuration for Certbot (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/{domain_name}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain_name}/privkey.pem;
""")
        elif ssl_type == "Manual Paths":
            if cert_path and key_path:
                config_lines.append(f"""
    # Manual SSL certificate paths
    ssl_certificate {cert_path};
    ssl_certificate_key {key_path};
""")
            else:
                raise ValueError("SSL certificate and key paths are required for Manual Paths SSL type.")

        config_lines.append("""
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_stapling on;
    ssl_stapling_verify on;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
""")
    else:
        config_lines.append(f"    root {root_path};")

    # Add error page handling
    for code, path in error_pages.items():
        if path: # Only add if a path is provided
            # Extract basename for the error_page directive
            error_page_basename = os.path.basename(path)
            config_lines.append(f"    error_page {code} /{error_page_basename};")
            # Add internal location for the error page
            config_lines.append(f"""    location /{error_page_basename} {{
        internal;
    }}""")

    # --- URL Rewrites ---
    if url_rewrites:
        config_lines.append("\n    # URL Rewrites")
        for rewrite in url_rewrites:
            if rewrite.get('source') and rewrite.get('destination'):
                flag = f" {rewrite['flag']}" if rewrite.get('flag') else ""
                config_lines.append(f"    rewrite {rewrite['source']} {rewrite['destination']}{flag};")

    # --- Redirections (before server type specific config to ensure they take precedence) ---
    if redirects:
        config_lines.append("\n    # Custom Redirections")
        for redirect in redirects:
            if redirect.get('source') and redirect.get('destination'):
                status_code = redirect.get('status', '301')
                config_lines.append(f"    location ~ ^{redirect['source']}$ {{ return {status_code} {redirect['destination']}; }}")

    # --- Server type specific configurations ---
    if server_type == "Static HTML":
        config_lines.append("""
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
""")
    elif server_type == "PHP-FPM":
        config_lines.append("""
    index index.php index.html index.htm;

    location ~ \\.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\\.php)(/.+)$;# Path to PHP-FPM socket
        fastcgi_pass unix:/var/run/php/php-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
    }

    location / {
        try_files $uri $uri/ =404;
    }
""")
    elif server_type == "Node.js/Proxy":
        config_lines.append("""
    location / {
        proxy_pass http://127.0.0.1:3000; # Default Node.js port, change if needed
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
""")

    # --- Allow/Deny Rules (typically in location blocks or server level for global) ---
    if allow_deny_rules:
        config_lines.append("\n    # Allow/Deny Rules")
        for rule in allow_deny_rules:
            if rule.get('action') and rule.get('ip'):
                # Apply globally or within a specific location if provided
                location_path = rule.get('location', '/')
                if location_path == '/':
                    config_lines.append(f"    {rule['action']} {rule['ip']};")
                else:
                    # This is a simplified approach. For multiple rules in specific locations,
                    # you'd need a more complex structure to group location blocks.
                    # For now, it will add a new location block for each specific rule.
                    config_lines.append(f"""
    location {location_path} {{
        {rule['action']} {rule['ip']};
    }}""")


    # Basic logging
    config_lines.append(f"""
    access_log /var/log/nginx/{domain_name}_access.log;
    error_log /var/log/nginx/{domain_name}_error.log;
}}
""")
    # Join all lines and remove leading/trailing whitespace from the whole block
    return "\n".join(config_lines).strip()

# --- CustomTkinter GUI Application ---
class NginxConfigApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nginx Config Generator")
        self.geometry("850x1050") # Increased size to accommodate new options
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1) # Make the textbox expandable

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # --- Input Frame ---
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Domain Name
        ctk.CTkLabel(self.input_frame, text="Domain Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.domain_entry = ctk.CTkEntry(self.input_frame, placeholder_text="example.com")
        self.domain_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.domain_entry.insert(0, "your-domain.com")

        # Website Root Path
        ctk.CTkLabel(self.input_frame, text="Website Root Path:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.root_entry = ctk.CTkEntry(self.input_frame, placeholder_text="/var/www/your_site")
        self.root_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.root_entry.insert(0, "/var/www/your_website")

        # Server Type Selection
        ctk.CTkLabel(self.input_frame, text="Server Type:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.server_type_options = ["Static HTML", "PHP-FPM", "Node.js/Proxy"]
        self.server_type_var = ctk.StringVar(value=self.server_type_options[0]) # Default value
        self.server_type_menu = ctk.CTkOptionMenu(self.input_frame, values=self.server_type_options,
                                                 variable=self.server_type_var)
        self.server_type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # --- SSL Configuration Frame ---
        self.ssl_frame = ctk.CTkFrame(self, corner_radius=10)
        self.ssl_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.ssl_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.ssl_frame, text="SSL Certificate (HTTPS):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        self.enable_ssl_var = ctk.BooleanVar(value=False)
        self.enable_ssl_checkbox = ctk.CTkCheckBox(self.ssl_frame, text="Enable HTTPS (SSL)", variable=self.enable_ssl_var, command=self.toggle_ssl_options)
        self.enable_ssl_checkbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.ssl_type_label = ctk.CTkLabel(self.ssl_frame, text="SSL Type:")
        self.ssl_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ssl_type_options = ["Certbot (Let's Encrypt)", "Manual Paths"]
        self.ssl_type_var = ctk.StringVar(value=self.ssl_type_options[0])
        self.ssl_type_menu = ctk.CTkOptionMenu(self.ssl_frame, values=self.ssl_type_options, variable=self.ssl_type_var, command=self.toggle_ssl_paths)
        self.ssl_type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.cert_path_label = ctk.CTkLabel(self.ssl_frame, text="Certificate Path:")
        self.cert_path_label.grid(row=3, column=0, padx=10, pady=2, sticky="w")
        self.cert_path_entry = ctk.CTkEntry(self.ssl_frame, placeholder_text="/etc/ssl/certs/your_domain.crt")
        self.cert_path_entry.grid(row=3, column=1, padx=10, pady=2, sticky="ew")

        self.key_path_label = ctk.CTkLabel(self.ssl_frame, text="Private Key Path:")
        self.key_path_label.grid(row=4, column=0, padx=10, pady=2, sticky="w")
        self.key_path_entry = ctk.CTkEntry(self.ssl_frame, placeholder_text="/etc/ssl/private/your_domain.key")
        self.key_path_entry.grid(row=4, column=1, padx=10, pady=2, sticky="ew")

        # Initially hide SSL path entries
        self.toggle_ssl_options()


        # --- URL Management Frame ---
        self.url_frame = ctk.CTkFrame(self, corner_radius=10)
        self.url_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.url_frame.grid_columnconfigure(0, weight=1) # Allow internal frames to expand

        ctk.CTkLabel(self.url_frame, text="URL Management:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        # --- Redirections ---
        self.redirect_frame = ctk.CTkFrame(self.url_frame, corner_radius=8)
        self.redirect_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.redirect_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.redirect_frame, text="Redirections:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 2), sticky="w")

        self.redirects = [] # Store redirect entries
        self.redirect_rows = 0

        self.add_redirect_button = ctk.CTkButton(self.redirect_frame, text="Add Redirect", command=self.add_redirect_row)
        self.add_redirect_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.add_redirect_row() # Add initial row

        # --- URL Rewrites ---
        self.rewrite_frame = ctk.CTkFrame(self.url_frame, corner_radius=8)
        self.rewrite_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.rewrite_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.rewrite_frame, text="URL Rewrites:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, padx=5, pady=(5, 2), sticky="w")

        self.url_rewrites = [] # Store rewrite entries
        self.rewrite_rows = 0

        self.add_rewrite_button = ctk.CTkButton(self.rewrite_frame, text="Add Rewrite", command=self.add_rewrite_row)
        self.add_rewrite_button.grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.add_rewrite_row() # Add initial row

        # --- Allow/Deny Rules ---
        self.access_frame = ctk.CTkFrame(self.url_frame, corner_radius=8)
        self.access_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.access_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.access_frame, text="Access Control (Allow/Deny):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, padx=5, pady=(5, 2), sticky="w")

        self.allow_deny_rules = [] # Store allow/deny entries
        self.allow_deny_rows = 0

        self.add_access_rule_button = ctk.CTkButton(self.access_frame, text="Add Rule", command=self.add_allow_deny_row)
        self.add_access_rule_button.grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.add_allow_deny_row() # Add initial row


        # --- Error Pages Frame ---
        self.error_frame = ctk.CTkFrame(self, corner_radius=10)
        self.error_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.error_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.error_frame, text="Custom Error Pages (e.g., /error_pages/404.html):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        self.error_entries = {}
        error_codes = ["403", "404", "500", "502", "503", "504"]
        for i, code in enumerate(error_codes):
            ctk.CTkLabel(self.error_frame, text=f"{code} Page:").grid(row=i+1, column=0, padx=10, pady=2, sticky="w")
            entry = ctk.CTkEntry(self.error_frame, placeholder_text=f"/error_pages/{code}.html")
            entry.grid(row=i+1, column=1, padx=10, pady=2, sticky="ew")
            self.error_entries[code] = entry

        # --- Generate Button ---
        self.generate_button = ctk.CTkButton(self, text="Generate Nginx Config", command=self.generate_config)
        self.generate_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        # --- Output Textbox ---
        self.output_textbox = ctk.CTkTextbox(self, wrap="word")
        self.output_textbox.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")
        self.output_textbox.insert("end", "Click 'Generate Nginx Config' to see the output here.")
        self.output_textbox.configure(state="disabled")

        # --- Instructions Label ---
        self.instructions_label = ctk.CTkLabel(self, text="", wraplength=800, justify="left")
        self.instructions_label.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")


    def toggle_ssl_options(self):
        is_ssl_enabled = self.enable_ssl_var.get()
        if is_ssl_enabled:
            self.ssl_type_label.grid()
            self.ssl_type_menu.grid()
            self.toggle_ssl_paths() # Adjust visibility based on current SSL type
        else:
            self.ssl_type_label.grid_remove()
            self.ssl_type_menu.grid_remove()
            self.cert_path_label.grid_remove()
            self.cert_path_entry.grid_remove()
            self.key_path_label.grid_remove()
            self.key_path_entry.grid_remove()

    def toggle_ssl_paths(self, *args): # *args to accept event argument from option menu
        ssl_type = self.ssl_type_var.get()
        if ssl_type == "Manual Paths" and self.enable_ssl_var.get():
            self.cert_path_label.grid()
            self.cert_path_entry.grid()
            self.key_path_label.grid()
            self.key_path_entry.grid()
        else:
            self.cert_path_label.grid_remove()
            self.cert_path_entry.grid_remove()
            self.key_path_label.grid_remove()
            self.key_path_entry.grid_remove()

    def add_redirect_row(self):
        row_num = self.redirect_rows + 1 # Start from 1 for content rows
        
        ctk.CTkLabel(self.redirect_frame, text="Source Path (regex):").grid(row=row_num, column=0, padx=5, pady=2, sticky="w")
        source_entry = ctk.CTkEntry(self.redirect_frame, placeholder_text="/old-path")
        source_entry.grid(row=row_num, column=1, padx=5, pady=2, sticky="ew")

        ctk.CTkLabel(self.redirect_frame, text="Destination URL:").grid(row=row_num, column=2, padx=5, pady=2, sticky="w")
        dest_entry = ctk.CTkEntry(self.redirect_frame, placeholder_text="https://new.example.com/new-path")
        dest_entry.grid(row=row_num, column=3, padx=5, pady=2, sticky="ew")

        ctk.CTkLabel(self.redirect_frame, text="Status Code:").grid(row=row_num, column=4, padx=5, pady=2, sticky="w")
        status_options = ["301", "302", "307", "308"]
        status_var = ctk.StringVar(value=status_options[0])
        status_menu = ctk.CTkOptionMenu(self.redirect_frame, values=status_options, variable=status_var, width=70)
        status_menu.grid(row=row_num, column=5, padx=5, pady=2, sticky="w")

        delete_button = ctk.CTkButton(self.redirect_frame, text="X", width=20, fg_color="red", command=lambda r=row_num: self.remove_row(self.redirect_frame, r, self.redirects))
        delete_button.grid(row=row_num, column=6, padx=5, pady=2, sticky="e")

        self.redirects.append({'source_entry': source_entry, 'dest_entry': dest_entry, 'status_var': status_var, 'row': row_num, 'delete_button': delete_button})
        self.redirect_rows += 1
        # Move "Add Redirect" button to the new last row
        self.add_redirect_button.grid(row=self.redirect_rows + 1, column=2, padx=5, pady=5, sticky="e")


    def add_rewrite_row(self):
        row_num = self.rewrite_rows + 1

        ctk.CTkLabel(self.rewrite_frame, text="Source Pattern (regex):").grid(row=row_num, column=0, padx=5, pady=2, sticky="w")
        source_entry = ctk.CTkEntry(self.rewrite_frame, placeholder_text="^/old/(.*)$")
        source_entry.grid(row=row_num, column=1, padx=5, pady=2, sticky="ew")

        ctk.CTkLabel(self.rewrite_frame, text="Destination URL:").grid(row=row_num, column=2, padx=5, pady=2, sticky="w")
        dest_entry = ctk.CTkEntry(self.rewrite_frame, placeholder_text="/new/$1")
        dest_entry.grid(row=row_num, column=3, padx=5, pady=2, sticky="ew")

        ctk.CTkLabel(self.rewrite_frame, text="Flag:").grid(row=row_num, column=4, padx=5, pady=2, sticky="w")
        flag_options = ["", "last", "break", "redirect", "permanent"]
        flag_var = ctk.StringVar(value=flag_options[0])
        flag_menu = ctk.CTkOptionMenu(self.rewrite_frame, values=flag_options, variable=flag_var, width=70)
        flag_menu.grid(row=row_num, column=5, padx=5, pady=2, sticky="w")

        delete_button = ctk.CTkButton(self.rewrite_frame, text="X", width=20, fg_color="red", command=lambda r=row_num: self.remove_row(self.rewrite_frame, r, self.url_rewrites))
        delete_button.grid(row=row_num, column=6, padx=5, pady=2, sticky="e")

        self.url_rewrites.append({'source_entry': source_entry, 'dest_entry': dest_entry, 'flag_var': flag_var, 'row': row_num, 'delete_button': delete_button})
        self.rewrite_rows += 1
        self.add_rewrite_button.grid(row=self.rewrite_rows + 1, column=3, padx=5, pady=5, sticky="e")

    def add_allow_deny_row(self):
        row_num = self.allow_deny_rows + 1

        ctk.CTkLabel(self.access_frame, text="Action:").grid(row=row_num, column=0, padx=5, pady=2, sticky="w")
        action_options = ["allow", "deny"]
        action_var = ctk.StringVar(value=action_options[0])
        action_menu = ctk.CTkOptionMenu(self.access_frame, values=action_options, variable=action_var, width=70)
        action_menu.grid(row=row_num, column=1, padx=5, pady=2, sticky="w")

        ctk.CTkLabel(self.access_frame, text="IP/CIDR:").grid(row=row_num, column=2, padx=5, pady=2, sticky="w")
        ip_entry = ctk.CTkEntry(self.access_frame, placeholder_text="192.168.1.1 or 10.0.0.0/24")
        ip_entry.grid(row=row_num, column=3, padx=5, pady=2, sticky="ew")

        ctk.CTkLabel(self.access_frame, text="Location (optional):").grid(row=row_num, column=4, padx=5, pady=2, sticky="w")
        location_entry = ctk.CTkEntry(self.access_frame, placeholder_text="/admin/ (leave blank for global)")
        location_entry.grid(row=row_num, column=5, padx=5, pady=2, sticky="ew")

        delete_button = ctk.CTkButton(self.access_frame, text="X", width=20, fg_color="red", command=lambda r=row_num: self.remove_row(self.access_frame, r, self.allow_deny_rules))
        delete_button.grid(row=row_num, column=6, padx=5, pady=2, sticky="e")

        self.allow_deny_rules.append({'action_var': action_var, 'ip_entry': ip_entry, 'location_entry': location_entry, 'row': row_num, 'delete_button': delete_button})
        self.allow_deny_rows += 1
        self.add_access_rule_button.grid(row=self.allow_deny_rows + 1, column=3, padx=5, pady=5, sticky="e")

    def remove_row(self, frame, row_to_remove, data_list):
        # Destroy all widgets in the specified row
        for widget in frame.winfo_children():
            if int(widget.grid_info()["row"]) == row_to_remove:
                widget.destroy()

        # Remove the item from the data list
        data_list[:] = [item for item in data_list if item['row'] != row_to_remove]

        # Re-grid remaining rows and update their row numbers
        for i, item in enumerate(data_list):
            current_row = item['row']
            if current_row > row_to_remove:
                new_row = current_row - 1
                for widget_key in ['source_entry', 'dest_entry', 'status_var', 'flag_var', 'action_var', 'ip_entry', 'location_entry', 'delete_button']:
                    if widget_key in item and isinstance(item[widget_key], ctk.CTkBaseClass): # Check if it's a CTk widget
                         item[widget_key].grid(row=new_row, column=item[widget_key].grid_info()["column"], padx=item[widget_key].grid_info()["padx"], pady=item[widget_key].grid_info()["pady"], sticky=item[widget_key].grid_info()["sticky"])
                # Also update the label, if it exists for this item
                for widget in frame.winfo_children():
                    if int(widget.grid_info()["row"]) == current_row and isinstance(widget, ctk.CTkLabel):
                         widget.grid(row=new_row, column=widget.grid_info()["column"], padx=widget.grid_info()["padx"], pady=widget.grid_info()["pady"], sticky=widget.grid_info()["sticky"])
                item['row'] = new_row
                # Update the command for the delete button
                if 'delete_button' in item:
                    item['delete_button'].configure(command=lambda r=new_row: self.remove_row(frame, r, data_list))


        # Adjust the row counter
        if frame == self.redirect_frame:
            self.redirect_rows -= 1
            self.add_redirect_button.grid(row=self.redirect_rows + 1, column=2, padx=5, pady=5, sticky="e")
        elif frame == self.rewrite_frame:
            self.rewrite_rows -= 1
            self.add_rewrite_button.grid(row=self.rewrite_rows + 1, column=3, padx=5, pady=5, sticky="e")
        elif frame == self.access_frame:
            self.allow_deny_rows -= 1
            self.add_access_rule_button.grid(row=self.allow_deny_rows + 1, column=3, padx=5, pady=5, sticky="e")


    def generate_config(self):
        domain = self.domain_entry.get()
        root = self.root_entry.get()
        server_type = self.server_type_var.get()
        enable_ssl = self.enable_ssl_var.get()
        ssl_type = self.ssl_type_var.get()
        cert_path = self.cert_path_entry.get()
        key_path = self.key_path_entry.get()

        error_pages = {code: entry.get() for code, entry in self.error_entries.items()}

        # Collect redirects
        collected_redirects = []
        for r_item in self.redirects:
            source = r_item['source_entry'].get().strip()
            destination = r_item['dest_entry'].get().strip()
            status = r_item['status_var'].get()
            if source and destination:
                collected_redirects.append({'source': source, 'destination': destination, 'status': status})

        # Collect URL rewrites
        collected_rewrites = []
        for rw_item in self.url_rewrites:
            source = rw_item['source_entry'].get().strip()
            destination = rw_item['dest_entry'].get().strip()
            flag = rw_item['flag_var'].get().strip()
            if source and destination:
                rewrite_data = {'source': source, 'destination': destination}
                if flag:
                    rewrite_data['flag'] = flag
                collected_rewrites.append(rewrite_data)

        # Collect allow/deny rules
        collected_allow_deny_rules = []
        for ad_item in self.allow_deny_rules:
            action = ad_item['action_var'].get()
            ip = ad_item['ip_entry'].get().strip()
            location = ad_item['location_entry'].get().strip()
            if ip:
                rule_data = {'action': action, 'ip': ip}
                if location:
                    rule_data['location'] = location
                collected_allow_deny_rules.append(rule_data)

        if not domain or not root:
            self.update_output("Please enter both Domain Name and Website Root Path.", is_error=True)
            self.instructions_label.configure(text="")
            return

        if enable_ssl and ssl_type == "Manual Paths" and (not cert_path or not key_path):
            self.update_output("Please provide both Certificate Path and Private Key Path for Manual Paths SSL.", is_error=True)
            self.instructions_label.configure(text="")
            return

        try:
            config_text = create_nginx_config_string(
                domain, root, server_type, error_pages, enable_ssl, ssl_type, cert_path, key_path,
                redirects=collected_redirects,
                allow_deny_rules=collected_allow_deny_rules,
                url_rewrites=collected_rewrites
            )

            self.update_output(config_text)

            instructions = (
                f"1. Save this content to a file, e.g., `/etc/nginx/sites-available/{domain}.conf`\n"
                f"2. Create a symbolic link: `sudo ln -s /etc/nginx/sites-available/{domain}.conf /etc/nginx/sites-enabled/`\n"
                "3. Ensure your custom error pages exist at the specified paths within your website's root.\n"
            )
            if enable_ssl:
                if ssl_type == "Certbot (Let's Encrypt)":
                    instructions += (
                        "4. Install Certbot if you haven't: `sudo apt update && sudo apt install certbot python3-certbot-nginx`\n"
                        f"5. Obtain and install SSL certificate using Certbot: `sudo certbot --nginx -d {domain} -d www.{domain}`\n"
                        "6. Certbot automatically configures Nginx for SSL. You may need to adjust the generated config to match this one if there are conflicts.\n"
                    )
                elif ssl_type == "Manual Paths":
                    instructions += (
                        "4. Ensure your SSL certificate and private key files are correctly placed at the specified paths.\n"
                    )
            
            if collected_redirects:
                instructions += "\nImportant for Redirections:\n  - Nginx redirects (`return`) are processed before `try_files`.\n  - Ensure your source paths use correct regex if desired (e.g., `^/old-path$`).\n"
            if collected_rewrites:
                instructions += "\nImportant for Rewrites:\n  - Nginx `rewrite` rules are powerful but complex. Understand `last`, `break`, `redirect`, `permanent` flags.\n  - Rewrites are processed within a `location` block or `server` block depending on placement.\n"
            if collected_allow_deny_rules:
                instructions += "\nImportant for Access Control:\n  - `allow` and `deny` directives define IP access. Order matters.\n  - Global rules apply to the entire server; specific location rules override global ones for that location.\n"


            instructions += (
                "7. Test your Nginx configuration: `sudo nginx -t`\n"
                "8. Reload Nginx to apply changes: `sudo systemctl reload nginx`"
            )

            self.instructions_label.configure(text=instructions)

        except Exception as e:
            self.update_output(f"An error occurred: {e}", is_error=True)
            self.instructions_label.configure(text="Error generating configuration.")

    def update_output(self, text, is_error=False):
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("end", text)
        self.output_textbox.configure(state="disabled")
        if is_error:
            self.output_textbox.configure(text_color="red")
        else:
            self.output_textbox.configure(text_color="white" if ctk.get_appearance_mode() == "Dark" else "black")


if __name__ == "__main__":
    app = NginxConfigApp()
    app.mainloop()