import customtkinter as ctk
import os

# --- Nginx Configuration String Generation Logic ---
def create_nginx_config_string(domain_name, root_path, server_type, error_pages, enable_ssl, ssl_type, cert_path="", key_path="",
                               redirects=None, allow_deny_rules=None, url_rewrites=None,
                               enable_rate_limiting=False, rate_limit_zone_name="", rate_limit_rate="", rate_limit_burst="",
                               block_user_agents=None, allowed_http_methods=None, block_file_types=None,
                               enable_hotlinking_protection=False, enable_security_headers=False,
                               url_filters=None): # New parameter for URL filters
    """
    Generates an Nginx configuration as a string based on server type, error pages, SSL settings,
    redirects, allow/deny rules, URL rewrites, and new filtering options.
    """
    if redirects is None:
        redirects = []
    if allow_deny_rules is None:
        allow_deny_rules = []
    if url_rewrites is None:
        url_rewrites = []
    if block_user_agents is None:
        block_user_agents = []
    if allowed_http_methods is None:
        allowed_http_methods = []
    if block_file_types is None:
        block_file_types = []
    if url_filters is None: # Initialize if None
        url_filters = []

    config_lines = []

    # --- Global Rate Limiting Zone (outside server block) ---
    # This part would ideally be in http {} block or a separate Nginx config file.
    # For simplicity, we'll put it at the very top of our generated file for now,
    # but the user should be aware of Nginx's hierarchical structure.
    if enable_rate_limiting and rate_limit_zone_name and rate_limit_rate:
        config_lines.append(f"""
# Rate Limiting Zone (consider moving to http {{}} block in nginx.conf)
limit_req_zone $binary_remote_addr zone={rate_limit_zone_name}:10m rate={rate_limit_rate};
""")


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
""")
    else:
        config_lines.append(f"    root {root_path};")

    # Add general security headers if enabled
    if enable_security_headers:
        config_lines.append("""
    # Additional Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "no-referrer-when-downgrade";
""")


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
        config_lines.append("\n    # Custom Redirections (using return)")
        for redirect in redirects:
            if redirect.get('source') and redirect.get('destination'):
                status_code = redirect.get('status', '301')
                config_lines.append(f"    location ~ ^{redirect['source']}$ {{ return {status_code} {redirect['destination']}; }}")

    # --- URL Filtering Rules ---
    if url_filters:
        config_lines.append("\n    # URL Specific Filtering")
        for f_rule in url_filters:
            if f_rule.get('url_pattern') and f_rule.get('filter_type'):
                pattern = f_rule['url_pattern']
                filter_type = f_rule['filter_type']
                target = f_rule.get('target', '').strip() # For redirects
                internal_ips = f_rule.get('internal_ips', '').strip() # For internal access

                config_lines.append(f"\n    location ~ ^{pattern}$ {{")
                if filter_type == "Redirection":
                    status_code = f_rule.get('status_code_redirect', '301')
                    config_lines.append(f"        return {status_code} {target};")
                elif filter_type == "Refus d'accès (403)":
                    config_lines.append(f"        deny all;")
                elif filter_type == "Accès Interne Uniquement":
                    # Define internal IPs
                    if internal_ips:
                        for ip in internal_ips.split(','):
                            ip = ip.strip()
                            if ip:
                                config_lines.append(f"        allow {ip};")
                    config_lines.append(f"        deny all;")
                config_lines.append(f"    }}")

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

    # --- Hotlinking Protection ---
    if enable_hotlinking_protection:
        config_lines.append(f"""
    # Hotlinking Protection
    location ~* \\.(jpg|jpeg|gif|png|webp|ico|svg|bmp)$ {{
        valid_referers none blocked ~.google. ~.bing. ~.yahoo. {domain_name} www.{domain_name};
        if ($invalid_referer) {{
            return 403; # Or return 404, or redirect to a placeholder image
        }}
    }}
""")

    # --- Block Specific File Types ---
    if block_file_types:
        extensions = "|".join([ext.strip().lstrip('.') for ext in block_file_types if ext.strip()])
        if extensions:
            config_lines.append(f"""
    # Block Specific File Types
    location ~* \\.({extensions})$ {{
        deny all;
    }}
""")

    # --- Server type specific configurations ---
    # We add common filters within the main location block if applicable
    common_filters_block = ""
    if block_user_agents:
        user_agent_regex = "|".join([ua.strip() for ua in block_user_agents if ua.strip()])
        if user_agent_regex:
            common_filters_block += f"""
        # Block User-Agents
        if ($http_user_agent ~* "{user_agent_regex}") {{
            return 403;
        }}
"""
    if allowed_http_methods:
        methods_regex = "|".join([m.strip() for m in allowed_http_methods if m.strip()])
        if methods_regex:
            common_filters_block += f"""
        # Restrict HTTP Methods
        if ($request_method !~ ^({methods_regex})$) {{
            return 405;
        }}
"""
    if enable_rate_limiting and rate_limit_zone_name:
        burst_setting = f" burst={rate_limit_burst}" if rate_limit_burst else ""
        common_filters_block += f"""
        # Apply Rate Limiting
        limit_req zone={rate_limit_zone_name}{burst_setting} nodelay;
"""


    if server_type == "Static HTML":
        config_lines.append(f"""
    index index.html index.htm;

    location / {{
{common_filters_block}
        try_files $uri $uri/ =404;
    }}
""")
    elif server_type == "PHP-FPM":
        config_lines.append(f"""
    index index.php index.html index.htm;

    location ~ \\.php$ {{
{common_filters_block}
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\\.php)(/.+)$;# Path to PHP-FPM socket
        fastcgi_pass unix:/var/run/php/php-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
    }}

    location / {{
{common_filters_block}
        try_files $uri $uri/ =404;
    }}
""")
    elif server_type == "Node.js/Proxy":
        config_lines.append(f"""
    location / {{
{common_filters_block}
        proxy_pass http://127.0.0.1:3000; # Default Node.js port, change if needed
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
""")

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
        self.geometry("900x800") # Start with a reasonable height, scrollbar will handle the rest
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Make the main scrollable frame expandable

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # --- Create a scrollable frame ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)


        # All existing frames will now be placed inside this scrollable frame
        # --- Input Frame ---
        self.input_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=0, pady=10, sticky="ew") # Removed outer padx/pady
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
        self.ssl_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        self.ssl_frame.grid(row=1, column=0, padx=0, pady=10, sticky="ew")
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
        self.url_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        self.url_frame.grid(row=2, column=0, padx=0, pady=10, sticky="ew")
        self.url_frame.grid_columnconfigure(0, weight=1) # Allow internal frames to expand

        ctk.CTkLabel(self.url_frame, text="URL Management:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        # --- Redirections (Global) ---
        self.redirect_frame = ctk.CTkFrame(self.url_frame, corner_radius=8)
        self.redirect_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.redirect_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.redirect_frame, text="Global Redirections (Return):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=7, padx=5, pady=(5, 2), sticky="w")

        self.redirects = [] # Store redirect entries
        self.redirect_rows = 0

        self.add_redirect_button = ctk.CTkButton(self.redirect_frame, text="Add Redirect", command=self.add_redirect_row)
        self.add_redirect_button.grid(row=1, column=6, padx=5, pady=5, sticky="e")
        self.add_redirect_row() # Add initial row

        # --- URL Rewrites ---
        self.rewrite_frame = ctk.CTkFrame(self.url_frame, corner_radius=8)
        self.rewrite_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.rewrite_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.rewrite_frame, text="URL Rewrites:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=7, padx=5, pady=(5, 2), sticky="w")

        self.url_rewrites = [] # Store rewrite entries
        self.rewrite_rows = 0

        self.add_rewrite_button = ctk.CTkButton(self.rewrite_frame, text="Add Rewrite", command=self.add_rewrite_row)
        self.add_rewrite_button.grid(row=1, column=6, padx=5, pady=5, sticky="e")
        self.add_rewrite_row() # Add initial row

        # --- Allow/Deny Rules ---
        self.access_frame = ctk.CTkFrame(self.url_frame, corner_radius=8)
        self.access_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.access_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.access_frame, text="Access Control (Allow/Deny IP):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=7, padx=5, pady=(5, 2), sticky="w")

        self.allow_deny_rules = [] # Store allow/deny entries
        self.allow_deny_rows = 0

        self.add_access_rule_button = ctk.CTkButton(self.access_frame, text="Add Rule", command=self.add_allow_deny_row)
        self.add_access_rule_button.grid(row=1, column=6, padx=5, pady=5, sticky="e")
        self.add_allow_deny_row() # Add initial row

        # --- URL Filtering (New Section) ---
        self.url_filter_frame = ctk.CTkFrame(self.url_frame, corner_radius=8)
        self.url_filter_frame.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.url_filter_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.url_filter_frame, text="URL Specific Filters:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=7, padx=5, pady=(5, 2), sticky="w")

        self.url_filters = [] # Store URL filter entries
        self.url_filter_rows = 0

        self.add_url_filter_button = ctk.CTkButton(self.url_filter_frame, text="Add URL Filter", command=self.add_url_filter_row)
        self.add_url_filter_button.grid(row=1, column=6, padx=5, pady=5, sticky="e")
        self.add_url_filter_row() # Add initial row


        # --- Security & Performance Filters Frame ---
        self.filters_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        self.filters_frame.grid(row=3, column=0, padx=0, pady=10, sticky="ew")
        self.filters_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.filters_frame, text="Security & Performance Filters:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        # --- Rate Limiting ---
        self.enable_rate_limit_var = ctk.BooleanVar(value=False)
        self.enable_rate_limit_checkbox = ctk.CTkCheckBox(self.filters_frame, text="Enable Rate Limiting (by IP)", variable=self.enable_rate_limit_var, command=self.toggle_rate_limit_options)
        self.enable_rate_limit_checkbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.rate_limit_zone_label = ctk.CTkLabel(self.filters_frame, text="Zone Name:")
        self.rate_limit_zone_label.grid(row=2, column=0, padx=10, pady=2, sticky="w")
        self.rate_limit_zone_entry = ctk.CTkEntry(self.filters_frame, placeholder_text="mylimit")
        self.rate_limit_zone_entry.grid(row=2, column=1, padx=10, pady=2, sticky="ew")
        self.rate_limit_zone_entry.insert(0, "mylimit")

        self.rate_limit_rate_label = ctk.CTkLabel(self.filters_frame, text="Rate (e.g., 5r/s or 30r/m):")
        self.rate_limit_rate_label.grid(row=3, column=0, padx=10, pady=2, sticky="w")
        self.rate_limit_rate_entry = ctk.CTkEntry(self.filters_frame, placeholder_text="5r/s")
        self.rate_limit_rate_entry.grid(row=3, column=1, padx=10, pady=2, sticky="ew")
        self.rate_limit_rate_entry.insert(0, "5r/s")

        self.rate_limit_burst_label = ctk.CTkLabel(self.filters_frame, text="Burst (optional):")
        self.rate_limit_burst_label.grid(row=4, column=0, padx=10, pady=2, sticky="w")
        self.rate_limit_burst_entry = ctk.CTkEntry(self.filters_frame, placeholder_text="10")
        self.rate_limit_burst_entry.grid(row=4, column=1, padx=10, pady=2, sticky="ew")

        self.toggle_rate_limit_options() # Initial state

        # --- Block User-Agents ---
        self.block_user_agents = [] # List to store entries for user-agent patterns
        self.user_agent_rows = 0
        self.user_agent_frame = ctk.CTkFrame(self.filters_frame, corner_radius=8)
        self.user_agent_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self.user_agent_frame, text="Block User-Agents (regex, e.g., .*bot.*):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 2), sticky="w")
        self.add_user_agent_button = ctk.CTkButton(self.user_agent_frame, text="Add User-Agent", command=self.add_user_agent_row)
        self.add_user_agent_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")
        self.add_user_agent_row() # Add initial row

        # --- Allowed HTTP Methods ---
        ctk.CTkLabel(self.filters_frame, text="Allowed HTTP Methods:", font=ctk.CTkFont(weight="bold")).grid(row=6, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        self.http_methods_frame = ctk.CTkFrame(self.filters_frame, corner_radius=8)
        self.http_methods_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.allowed_http_methods_vars = {}
        http_method_options = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
        for i, method in enumerate(http_method_options):
            var = ctk.BooleanVar(value=True if method in ["GET", "POST", "HEAD"] else False)
            checkbox = ctk.CTkCheckBox(self.http_methods_frame, text=method, variable=var)
            checkbox.grid(row=0, column=i, padx=5, pady=2, sticky="w")
            self.allowed_http_methods_vars[method] = var

        # --- Block Specific File Types ---
        ctk.CTkLabel(self.filters_frame, text="Block Specific File Types (comma-separated, e.g., zip,exe):", font=ctk.CTkFont(weight="bold")).grid(row=8, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        self.block_file_types_entry = ctk.CTkEntry(self.filters_frame, placeholder_text="zip, exe, rar, docx")
        self.block_file_types_entry.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # --- Hotlinking Protection ---
        self.enable_hotlinking_protection_var = ctk.BooleanVar(value=False)
        self.enable_hotlinking_protection_checkbox = ctk.CTkCheckBox(self.filters_frame, text="Enable Hotlinking Protection for Images", variable=self.enable_hotlinking_protection_var)
        self.enable_hotlinking_protection_checkbox.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # --- Additional Security Headers ---
        self.enable_security_headers_var = ctk.BooleanVar(value=False)
        self.enable_security_headers_checkbox = ctk.CTkCheckBox(self.filters_frame, text="Add More General Security Headers (X-Frame, X-Content, X-XSS, Referrer)", variable=self.enable_security_headers_var)
        self.enable_security_headers_checkbox.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="w")


        # --- Error Pages Frame ---
        self.error_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        self.error_frame.grid(row=4, column=0, padx=0, pady=10, sticky="ew")
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
        self.generate_button = ctk.CTkButton(self.scrollable_frame, text="Generate Nginx Config", command=self.generate_config)
        self.generate_button.grid(row=5, column=0, padx=0, pady=10, sticky="ew")

        # --- Output Textbox ---
        self.output_textbox = ctk.CTkTextbox(self.scrollable_frame, wrap="word", height=200) # Give it a fixed height for better scrolling
        self.output_textbox.grid(row=6, column=0, padx=0, pady=10, sticky="nsew")
        self.output_textbox.insert("end", "Click 'Generate Nginx Config' to see the output here.")
        self.output_textbox.configure(state="disabled")

        # --- Instructions Label ---
        self.instructions_label = ctk.CTkLabel(self.scrollable_frame, text="", wraplength=800, justify="left")
        self.instructions_label.grid(row=7, column=0, padx=0, pady=(0, 20), sticky="ew")

        # Make the output textbox expandable within the scrollable frame
        self.scrollable_frame.grid_rowconfigure(6, weight=1)


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

    def toggle_rate_limit_options(self):
        is_rate_limit_enabled = self.enable_rate_limit_var.get()
        if is_rate_limit_enabled:
            self.rate_limit_zone_label.grid()
            self.rate_limit_zone_entry.grid()
            self.rate_limit_rate_label.grid()
            self.rate_limit_rate_entry.grid()
            self.rate_limit_burst_label.grid()
            self.rate_limit_burst_entry.grid()
        else:
            self.rate_limit_zone_label.grid_remove()
            self.rate_limit_zone_entry.grid_remove()
            self.rate_limit_rate_label.grid_remove()
            self.rate_limit_rate_entry.grid_remove()
            self.rate_limit_burst_label.grid_remove()
            self.rate_limit_burst_entry.grid_remove()

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
        self.add_redirect_button.grid(row=self.redirect_rows + 1, column=6, padx=5, pady=5, sticky="e")


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
        self.add_rewrite_button.grid(row=self.rewrite_rows + 1, column=6, padx=5, pady=5, sticky="e")

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
        self.add_access_rule_button.grid(row=self.allow_deny_rows + 1, column=6, padx=5, pady=5, sticky="e")

    def add_user_agent_row(self):
        row_num = self.user_agent_rows + 1

        ctk.CTkLabel(self.user_agent_frame, text="Pattern:").grid(row=row_num, column=0, padx=5, pady=2, sticky="w")
        pattern_entry = ctk.CTkEntry(self.user_agent_frame, placeholder_text=".*crawler.*")
        pattern_entry.grid(row=row_num, column=1, padx=5, pady=2, sticky="ew")

        delete_button = ctk.CTkButton(self.user_agent_frame, text="X", width=20, fg_color="red", command=lambda r=row_num: self.remove_row(self.user_agent_frame, r, self.block_user_agents))
        delete_button.grid(row=row_num, column=2, padx=5, pady=2, sticky="e")

        self.block_user_agents.append({'pattern_entry': pattern_entry, 'row': row_num, 'delete_button': delete_button})
        self.user_agent_rows += 1
        self.add_user_agent_button.grid(row=self.user_agent_rows + 1, column=1, padx=5, pady=5, sticky="e")

    def add_url_filter_row(self):
        row_num = self.url_filter_rows + 1

        ctk.CTkLabel(self.url_filter_frame, text="URL Pattern (regex):").grid(row=row_num, column=0, padx=5, pady=2, sticky="w")
        url_pattern_entry = ctk.CTkEntry(self.url_filter_frame, placeholder_text="/private_data/.*")
        url_pattern_entry.grid(row=row_num, column=1, padx=5, pady=2, sticky="ew")

        ctk.CTkLabel(self.url_filter_frame, text="Filter Type:").grid(row=row_num, column=2, padx=5, pady=2, sticky="w")
        filter_type_options = ["Redirection", "Refus d'accès (403)", "Accès Interne Uniquement"]
        filter_type_var = ctk.StringVar(value=filter_type_options[0])

        # Fields for Redirection
        target_label = ctk.CTkLabel(self.url_filter_frame, text="Target URL:")
        target_entry = ctk.CTkEntry(self.url_filter_frame, placeholder_text="https://example.com/new-page")
        status_code_label = ctk.CTkLabel(self.url_filter_frame, text="Status Code:")
        status_code_options = ["301", "302"]
        status_code_redirect_var = ctk.StringVar(value=status_code_options[0])
        status_code_redirect_menu = ctk.CTkOptionMenu(self.url_filter_frame, values=status_code_options, variable=status_code_redirect_var, width=70)

        # Fields for Accès Interne Uniquement
        internal_ips_label = ctk.CTkLabel(self.url_filter_frame, text="Internal IPs (comma-separated):")
        internal_ips_entry = ctk.CTkEntry(self.url_filter_frame, placeholder_text="127.0.0.1, 192.168.1.0/24")

        delete_button = ctk.CTkButton(self.url_filter_frame, text="X", width=20, fg_color="red", command=lambda r=row_num: self.remove_row(self.url_filter_frame, r, self.url_filters))
        delete_button.grid(row=row_num, column=6, padx=5, pady=2, sticky="e")

        # Store widgets for later visibility control and data retrieval
        rule_widgets = {
            'url_pattern_entry': url_pattern_entry,
            'filter_type_var': filter_type_var,
            'target_label': target_label, 'target_entry': target_entry,
            'status_code_label': status_code_label, 'status_code_redirect_var': status_code_redirect_var, 'status_code_redirect_menu': status_code_redirect_menu,
            'internal_ips_label': internal_ips_label, 'internal_ips_entry': internal_ips_entry,
            'row': row_num,
            'delete_button': delete_button,
        }

        # The command needs to be set AFTER rule_widgets is populated
        filter_type_menu = ctk.CTkOptionMenu(self.url_filter_frame, values=filter_type_options, variable=filter_type_var, width=150,
                                              command=lambda *args, current_rule=rule_widgets: self.toggle_url_filter_options_new(current_rule))
        filter_type_menu.grid(row=row_num, column=3, padx=5, pady=2, sticky="w")
        rule_widgets['filter_type_menu'] = filter_type_menu # Store it after creation

        self.url_filters.append(rule_widgets)
        self.url_filter_rows += 1
        self.add_url_filter_button.grid(row=self.url_filter_rows + 1, column=6, padx=5, pady=5, sticky="e")

        # Initial visibility setup for the newly added row
        self.toggle_url_filter_options_new(rule_widgets)


    def toggle_url_filter_options_new(self, current_rule):
        row_num = current_rule['row']
        selected_type = current_rule['filter_type_var'].get()

        # Hide all specific options first
        for widget_key in ['target_label', 'target_entry', 'status_code_label', 'status_code_redirect_menu', 'internal_ips_label', 'internal_ips_entry']:
            if widget_key in current_rule and current_rule[widget_key].winfo_exists():
                current_rule[widget_key].grid_remove()

        # Place widgets based on selected type
        if selected_type == "Redirection":
            current_rule['target_label'].grid(row=row_num, column=4, padx=5, pady=2, sticky="w")
            current_rule['target_entry'].grid(row=row_num, column=5, padx=5, pady=2, sticky="ew")
            current_rule['status_code_label'].grid(row=row_num + 1, column=4, padx=5, pady=2, sticky="w")
            current_rule['status_code_redirect_menu'].grid(row=row_num + 1, column=5, padx=5, pady=2, sticky="w")
            current_rule['delete_button'].grid(row=row_num + 1, column=6, padx=5, pady=2, sticky="e") # Move delete button down
        elif selected_type == "Accès Interne Uniquement":
            current_rule['internal_ips_label'].grid(row=row_num, column=4, padx=5, pady=2, sticky="w")
            current_rule['internal_ips_entry'].grid(row=row_num, column=5, padx=5, pady=2, sticky="ew")
            current_rule['delete_button'].grid(row=row_num, column=6, padx=5, pady=2, sticky="e") # Keep on same row
        else: # Refus d'accès (403)
            current_rule['delete_button'].grid(row=row_num, column=6, padx=5, pady=2, sticky="e") # Keep on same row

        # Re-position all subsequent rows and the 'Add URL Filter' button
        self.reposition_url_filter_elements()


    def reposition_url_filter_elements(self):
        # This function recalculates the grid positions for all URL filter rows
        # after a change (add, remove, or type change).
        current_grid_row = 1 # Start after the "Add URL Filter" button's initial position

        for item in self.url_filters:
            item_row_start = current_grid_row
            # Update the stored row number for this item
            item['row'] = item_row_start

            # Grid URL pattern and filter type (always on the first line of the item)
            if item['url_pattern_entry'].winfo_exists():
                item['url_pattern_entry'].grid(row=item_row_start, column=1, padx=5, pady=2, sticky="ew")
            if item['filter_type_menu'].winfo_exists():
                item['filter_type_menu'].grid(row=item_row_start, column=3, padx=5, pady=2, sticky="w")

            selected_type = item['filter_type_var'].get()

            # Reposition type-specific widgets and the delete button
            # Hide all first
            for widget_key in ['target_label', 'target_entry', 'status_code_label', 'status_code_redirect_menu', 'internal_ips_label', 'internal_ips_entry']:
                if widget_key in item and item[widget_key].winfo_exists():
                    item[widget_key].grid_remove()

            # Show specific widgets and adjust delete button position
            if selected_type == "Redirection":
                if item['target_label'].winfo_exists():
                    item['target_label'].grid(row=item_row_start, column=4, padx=5, pady=2, sticky="w")
                if item['target_entry'].winfo_exists():
                    item['target_entry'].grid(row=item_row_start, column=5, padx=5, pady=2, sticky="ew")
                if item['status_code_label'].winfo_exists():
                    item['status_code_label'].grid(row=item_row_start + 1, column=4, padx=5, pady=2, sticky="w")
                if item['status_code_redirect_menu'].winfo_exists():
                    item['status_code_redirect_menu'].grid(row=item_row_start + 1, column=5, padx=5, pady=2, sticky="w")
                if item['delete_button'].winfo_exists():
                    item['delete_button'].grid(row=item_row_start + 1, column=6, padx=5, pady=2, sticky="e")
                current_grid_row += 2 # This rule takes 2 grid rows
            elif selected_type == "Accès Interne Uniquement":
                if item['internal_ips_label'].winfo_exists():
                    item['internal_ips_label'].grid(row=item_row_start, column=4, padx=5, pady=2, sticky="w")
                if item['internal_ips_entry'].winfo_exists():
                    item['internal_ips_entry'].grid(row=item_row_start, column=5, padx=5, pady=2, sticky="ew")
                if item['delete_button'].winfo_exists():
                    item['delete_button'].grid(row=item_row_start, column=6, padx=5, pady=2, sticky="e")
                current_grid_row += 1 # This rule takes 1 grid row
            else: # Refus d'accès (403)
                if item['delete_button'].winfo_exists():
                    item['delete_button'].grid(row=item_row_start, column=6, padx=5, pady=2, sticky="e")
                current_grid_row += 1 # This rule takes 1 grid row

            # Update delete button and menu commands with the new row number
            if 'delete_button' in item and item['delete_button'].winfo_exists():
                item['delete_button'].configure(command=lambda r=item['row']: self.remove_row(self.url_filter_frame, r, self.url_filters))
            if 'filter_type_menu' in item and item['filter_type_menu'].winfo_exists():
                item['filter_type_menu'].configure(command=lambda *args, current_rule=item: self.toggle_url_filter_options_new(current_rule))

        # Position the "Add URL Filter" button after all filter rows
        self.add_url_filter_button.grid(row=current_grid_row, column=6, padx=5, pady=5, sticky="e")


    def remove_row(self, frame, row_to_remove, data_list):
        # Find the item to remove
        item_to_remove = next((item for item in data_list if item['row'] == row_to_remove), None)
        if not item_to_remove:
            return

        # Determine how many grid rows this item occupied
        rows_occupied = 1
        if frame == self.url_filter_frame and item_to_remove.get('filter_type_var', ctk.StringVar()).get() == "Redirection":
            rows_occupied = 2

        # Destroy all widgets associated with the row to remove
        for widget_key, widget in item_to_remove.items():
            if isinstance(widget, (ctk.CTkEntry, ctk.CTkOptionMenu, ctk.CTkCheckBox, ctk.CTkButton, ctk.CTkLabel)):
                if widget.winfo_exists(): # Check if widget hasn't been destroyed by other means
                    widget.destroy()

        # Remove the item from the data list
        data_list[:] = [item for item in data_list if item['row'] != row_to_remove]

        # Adjust the row counter
        if frame == self.redirect_frame:
            self.redirect_rows -= 1
        elif frame == self.rewrite_frame:
            self.rewrite_rows -= 1
        elif frame == self.access_frame:
            self.allow_deny_rows -= 1
        elif frame == self.user_agent_frame:
            self.user_agent_rows -= 1
        elif frame == self.url_filter_frame:
            self.url_filter_rows -= 1

            # Re-position all URL filter elements after removal
            self.reposition_url_filter_elements()
            return # Exit early as reposition_url_filter_elements handles button and subsequent rows


        # For other frames (non-URL filters), re-grid remaining rows and update button
        for i, item in enumerate(data_list):
            current_row_in_list = item['row']
            if current_row_in_list > row_to_remove:
                new_row = current_row_in_list - rows_occupied # Shift up by the number of rows the removed item occupied

                for widget_key, widget in item.items():
                    if isinstance(widget, (ctk.CTkEntry, ctk.CTkOptionMenu, ctk.CTkCheckBox, ctk.CTkButton, ctk.CTkLabel)):
                        try:
                            grid_info = widget.grid_info()
                            offset = grid_info["row"] - current_row_in_list # Offset from the item's base row
                            widget.grid(row=new_row + offset, column=grid_info["column"],
                                        padx=grid_info["padx"],
                                        pady=grid_info["pady"],
                                        sticky=grid_info["sticky"])
                        except Exception:
                            pass # Widget might not have grid_info or already destroyed

                item['row'] = new_row
                # Update the command for the delete button
                if 'delete_button' in item and item['delete_button'].winfo_exists():
                    item['delete_button'].configure(command=lambda r=new_row: self.remove_row(frame, r, data_list))


        # Adjust the position of the "Add" button for non-URL filter frames
        if frame == self.redirect_frame:
            self.add_redirect_button.grid(row=self.redirect_rows + 1, column=6, padx=5, pady=5, sticky="e")
        elif frame == self.rewrite_frame:
            self.add_rewrite_button.grid(row=self.rewrite_rows + 1, column=6, padx=5, pady=5, sticky="e")
        elif frame == self.access_frame:
            self.add_access_rule_button.grid(row=self.allow_deny_rows + 1, column=6, padx=5, pady=5, sticky="e")
        elif frame == self.user_agent_frame:
            self.add_user_agent_button.grid(row=self.user_agent_rows + 1, column=1, padx=5, pady=5, sticky="e")


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

        # Collect URL filters
        collected_url_filters = []
        for uf_item in self.url_filters:
            url_pattern = uf_item['url_pattern_entry'].get().strip()
            filter_type = uf_item['filter_type_var'].get()
            rule_data = {'url_pattern': url_pattern, 'filter_type': filter_type}

            if filter_type == "Redirection":
                target = uf_item['target_entry'].get().strip()
                status_code_redirect = uf_item['status_code_redirect_var'].get()
                if url_pattern and target:
                    rule_data['target'] = target
                    rule_data['status_code_redirect'] = status_code_redirect
                    collected_url_filters.append(rule_data)
                elif url_pattern and not target:
                    self.update_output(f"URL Filter: Redirection for pattern '{url_pattern}' requires a target URL.", is_error=True)
                    return
            elif filter_type == "Accès Interne Uniquement":
                internal_ips = uf_item['internal_ips_entry'].get().strip()
                if url_pattern:
                    rule_data['internal_ips'] = internal_ips
                    collected_url_filters.append(rule_data)
                elif url_pattern and not internal_ips:
                    self.update_output(f"URL Filter: Internal access for pattern '{url_pattern}' should specify internal IPs (or 127.0.0.1 for server itself).", is_error=True)
                    return
            elif url_pattern and filter_type == "Refus d'accès (403)":
                collected_url_filters.append(rule_data)


        # Collect rate limiting info
        enable_rate_limiting = self.enable_rate_limit_var.get()
        rate_limit_zone_name = self.rate_limit_zone_entry.get().strip()
        rate_limit_rate = self.rate_limit_rate_entry.get().strip()
        rate_limit_burst = self.rate_limit_burst_entry.get().strip()

        # Collect blocked user agents
        collected_user_agents = []
        for ua_item in self.block_user_agents:
            pattern = ua_item['pattern_entry'].get().strip()
            if pattern:
                collected_user_agents.append(pattern)

        # Collect allowed HTTP methods
        collected_allowed_http_methods = [
            method for method, var in self.allowed_http_methods_vars.items() if var.get()
        ]

        # Collect blocked file types
        block_file_types_str = self.block_file_types_entry.get().strip()
        collected_block_file_types = [ext.strip() for ext in block_file_types_str.split(',') if ext.strip()]

        # Collect hotlinking and security headers flags
        enable_hotlinking_protection = self.enable_hotlinking_protection_var.get()
        enable_security_headers = self.enable_security_headers_var.get()


        if not domain or not root:
            self.update_output("Please enter both Domain Name and Website Root Path.", is_error=True)
            self.instructions_label.configure(text="")
            return

        if enable_ssl and ssl_type == "Manual Paths" and (not cert_path or not key_path):
            self.update_output("Please provide both Certificate Path and Private Key Path for Manual Paths SSL.", is_error=True)
            self.instructions_label.configure(text="")
            return

        if enable_rate_limiting and (not rate_limit_zone_name or not rate_limit_rate):
            self.update_output("Please provide both Zone Name and Rate for Rate Limiting.", is_error=True)
            self.instructions_label.configure(text="")
            return


        try:
            config_text = create_nginx_config_string(
                domain, root, server_type, error_pages, enable_ssl, ssl_type, cert_path, key_path,
                redirects=collected_redirects,
                allow_deny_rules=collected_allow_deny_rules,
                url_rewrites=collected_rewrites,
                enable_rate_limiting=enable_rate_limiting,
                rate_limit_zone_name=rate_limit_zone_name,
                rate_limit_rate=rate_limit_rate,
                rate_limit_burst=rate_limit_burst,
                block_user_agents=collected_user_agents,
                allowed_http_methods=collected_allowed_http_methods,
                block_file_types=collected_block_file_types,
                enable_hotlinking_protection=enable_hotlinking_protection,
                enable_security_headers=enable_security_headers,
                url_filters=collected_url_filters # Pass new URL filters
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

            if enable_rate_limiting:
                instructions += (
                    f"\n**Important for Rate Limiting:**\n  - The `limit_req_zone` directive is usually defined globally in the `http {{}}` block (e.g., in `/etc/nginx/nginx.conf`). The generated config places it at the top for simplicity, but you might need to move it.\n  - Ensure your `rate` and `burst` values suit your traffic. `nodelay` means no immediate delay, requests are rejected if the burst limit is reached.\n"
                )
            if collected_redirects:
                instructions += "\n**Important for Global Redirections:**\n  - Nginx `return` directives are processed early. Use these for simple, global URL redirects.\n  - Ensure your source paths use correct regex if desired (e.g., `^/old-path$`).\n"
            if collected_rewrites:
                instructions += "\n**Important for URL Rewrites:**\n  - Nginx `rewrite` rules are powerful but complex. Understand `last`, `break`, `redirect`, `permanent` flags.\n  - Rewrites are processed within a `location` block or `server` block depending on placement and can be used for internal path manipulation.\n"
            if collected_allow_deny_rules:
                instructions += "\n**Important for Access Control (IP):**\n  - `allow` and `deny` directives define IP access. Order matters.\n  - Global rules apply to the entire server; specific `location` rules override global ones for that location.\n"
            if collected_url_filters:
                instructions += "\n**Important for URL Specific Filters:**\n  - These rules create `location` blocks for specific URL patterns.\n  - **Redirection**: Uses `return` for external redirects. Specify a full target URL.\n  - **Refus d'accès (403)**: Blocks access to the URL pattern.\n  - **Accès Interne Uniquement**: Only allows specified IPs (e.g., `127.0.0.1` for the server itself, or your internal network IPs) to access the URL. All other IPs are denied.\n  - Ensure your URL patterns are correct regex.\n"
            if collected_user_agents:
                instructions += "\n**Important for User-Agent Blocking:**\n  - Blocking by User-Agent is effective for known bots but is easily spoofed.\n"
            if collected_allowed_http_methods:
                instructions += "\n**Important for HTTP Method Restriction:**\n  - This restricts which HTTP methods are allowed. Unauthorized methods will receive a 405 error.\n"
            if collected_block_file_types:
                instructions += "\n**Important for File Type Blocking:**\n  - This blocks direct access to files with specified extensions.\n"
            if enable_hotlinking_protection:
                instructions += "\n**Important for Hotlinking Protection:**\n  - Adjust `valid_referers` to include all legitimate domains that should be allowed to display your images.\n  - Currently returns 403 for unauthorized requests; you can change this to 404 or redirect to a placeholder image.\n"
            if enable_security_headers:
                instructions += "\n**Important for Security Headers:**\n  - These headers enhance security by instructing browsers on how to behave. Consider customizing `Content-Security-Policy` for advanced control.\n"


            instructions += (
                "\n**Final Steps:**\n"
                "9. Test your Nginx configuration: `sudo nginx -t`\n"
                "10. Reload Nginx to apply changes: `sudo systemctl reload nginx`"
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