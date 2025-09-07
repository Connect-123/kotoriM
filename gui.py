"""
gui.py - GUI interface for Ninjemail
Provides the graphical user interface for email account creation
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
from datetime import datetime
import ninjemail as nm  # Import our ninjemail module


class NinjemailGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🥷 Ninjemail - Email Account Creator")
        self.root.geometry("950x750")

        # Set theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#4CAF50"
        self.error_color = "#f44336"
        self.warning_color = "#FF9800"

        self.root.configure(bg=self.bg_color)

        # Account creator instance
        self.account_creator = nm.AccountCreator()

        # Configure styles
        self.setup_styles()

        # Create UI
        self.create_widgets()

        # Load saved configuration
        self.load_config()

    def setup_styles(self):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure dark theme styles
        style.configure("Title.TLabel",
                        background=self.bg_color,
                        foreground=self.accent_color,
                        font=('Arial', 18, 'bold'))

        style.configure("Heading.TLabel",
                        background=self.bg_color,
                        foreground=self.fg_color,
                        font=('Arial', 12, 'bold'))

        style.configure("Dark.TFrame", background=self.bg_color)
        style.configure("Dark.TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("Dark.TCheckbutton", background=self.bg_color, foreground=self.fg_color)

    def create_widgets(self):
        """Create all GUI widgets"""
        # Title with emoji
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=15)

        title_label = ttk.Label(title_frame, text="🥷 Ninjemail Account Creator",
                                style="Title.TLabel")
        title_label.pack()

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create tabs
        self.create_main_tab()
        self.create_sms_tab()
        self.create_proxy_tab()
        self.create_accounts_tab()
        self.create_logs_tab()

        # Status bar
        self.create_status_bar()

    def create_main_tab(self):
        """Create the main configuration tab"""
        main_frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(main_frame, text="📧 Main Configuration")

        # Provider selection
        provider_frame = ttk.LabelFrame(main_frame, text="Email Provider", style="Dark.TFrame")
        provider_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(provider_frame, text="Provider:", style="Dark.TLabel").grid(row=0, column=0, padx=5, pady=8,
                                                                              sticky="w")

        self.provider_var = tk.StringVar(value="gmail")
        providers = ["gmail", "outlook", "yahoo"]
        self.provider_combo = ttk.Combobox(provider_frame, textvariable=self.provider_var,
                                           values=providers, state="readonly", width=20)
        self.provider_combo.grid(row=0, column=1, padx=5, pady=8)

        # Account details with auto-generate buttons
        details_frame = ttk.LabelFrame(main_frame, text="Account Details", style="Dark.TFrame")
        details_frame.pack(fill=tk.X, padx=10, pady=10)

        # Username
        ttk.Label(details_frame, text="Username:", style="Dark.TLabel").grid(row=0, column=0, padx=5, pady=8,
                                                                             sticky="w")
        self.username_entry = ttk.Entry(details_frame, width=25)
        self.username_entry.grid(row=0, column=1, padx=5, pady=8)

        tk.Button(details_frame, text="🎲 Auto Generate",
                  bg="#2196F3", fg="white", font=('Arial', 9),
                  command=self.generate_username).grid(row=0, column=2, padx=5, pady=8)

        # Password
        ttk.Label(details_frame, text="Password:", style="Dark.TLabel").grid(row=1, column=0, padx=5, pady=8,
                                                                             sticky="w")
        self.password_entry = ttk.Entry(details_frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=8)

        tk.Button(details_frame, text="🔐 Generate Strong",
                  bg="#2196F3", fg="white", font=('Arial', 9),
                  command=self.generate_password).grid(row=1, column=2, padx=5, pady=8)

        self.show_password_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(details_frame, text="Show", variable=self.show_password_var,
                        style="Dark.TCheckbutton",
                        command=self.toggle_password_visibility).grid(row=1, column=3, padx=5, pady=8)

        # First name
        ttk.Label(details_frame, text="First Name:", style="Dark.TLabel").grid(row=2, column=0, padx=5, pady=8,
                                                                               sticky="w")
        self.firstname_entry = ttk.Entry(details_frame, width=25)
        self.firstname_entry.grid(row=2, column=1, padx=5, pady=8)

        tk.Button(details_frame, text="👤 Auto Generate",
                  bg="#2196F3", fg="white", font=('Arial', 9),
                  command=self.generate_firstname).grid(row=2, column=2, padx=5, pady=8)

        # Last name
        ttk.Label(details_frame, text="Last Name:", style="Dark.TLabel").grid(row=3, column=0, padx=5, pady=8,
                                                                              sticky="w")
        self.lastname_entry = ttk.Entry(details_frame, width=25)
        self.lastname_entry.grid(row=3, column=1, padx=5, pady=8)

        tk.Button(details_frame, text="👤 Auto Generate",
                  bg="#2196F3", fg="white", font=('Arial', 9),
                  command=self.generate_lastname).grid(row=3, column=2, padx=5, pady=8)

        # Birth date
        ttk.Label(details_frame, text="Birth Date:", style="Dark.TLabel").grid(row=4, column=0, padx=5, pady=8,
                                                                               sticky="w")
        self.birthdate_entry = ttk.Entry(details_frame, width=25)
        self.birthdate_entry.grid(row=4, column=1, padx=5, pady=8)
        self.birthdate_entry.insert(0, "YYYY-MM-DD")

        tk.Button(details_frame, text="📅 Auto Generate",
                  bg="#2196F3", fg="white", font=('Arial', 9),
                  command=self.generate_birthdate).grid(row=4, column=2, padx=5, pady=8)

        # Age range for birthday generation
        age_frame = tk.Frame(details_frame, bg=self.bg_color)
        age_frame.grid(row=4, column=3, padx=5, pady=8)

        ttk.Label(age_frame, text="Age:", style="Dark.TLabel").pack(side=tk.LEFT)
        self.min_age = tk.Spinbox(age_frame, from_=18, to=90, width=3, value=18)
        self.min_age.pack(side=tk.LEFT, padx=2)
        ttk.Label(age_frame, text="-", style="Dark.TLabel").pack(side=tk.LEFT)
        self.max_age = tk.Spinbox(age_frame, from_=18, to=90, width=3, value=65)
        self.max_age.pack(side=tk.LEFT, padx=2)

        # Country
        ttk.Label(details_frame, text="Country:", style="Dark.TLabel").grid(row=5, column=0, padx=5, pady=8, sticky="w")
        self.country_entry = ttk.Entry(details_frame, width=25)
        self.country_entry.grid(row=5, column=1, padx=5, pady=8)

        tk.Button(details_frame, text="🌍 Auto Select",
                  bg="#2196F3", fg="white", font=('Arial', 9),
                  command=self.generate_country).grid(row=5, column=2, padx=5, pady=8)

        # Auto-generate all button
        tk.Button(details_frame, text="🎲 Generate All Fields",
                  bg="#9C27B0", fg="white", font=('Arial', 10, 'bold'),
                  command=self.generate_all_fields).grid(row=6, column=1, columnspan=2, padx=5, pady=15)

        # Browser settings
        browser_frame = ttk.LabelFrame(main_frame, text="Browser Settings", style="Dark.TFrame")
        browser_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(browser_frame, text="Browser:", style="Dark.TLabel").grid(row=0, column=0, padx=5, pady=8, sticky="w")

        self.browser_var = tk.StringVar(value="chrome")
        browsers = ["chrome", "firefox", "undetected-chrome"]
        self.browser_combo = ttk.Combobox(browser_frame, textvariable=self.browser_var,
                                          values=browsers, state="readonly", width=20)
        self.browser_combo.grid(row=0, column=1, padx=5, pady=8)

        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(browser_frame, text="Headless Mode (No GUI)",
                        variable=self.headless_var,
                        style="Dark.TCheckbutton").grid(row=0, column=2, padx=20, pady=8)

        # Action buttons
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=20)

        self.create_button = tk.Button(button_frame, text="✨ Create Account",
                                       bg=self.accent_color, fg="white",
                                       font=('Arial', 12, 'bold'),
                                       padx=20, pady=12,
                                       command=self.create_account)
        self.create_button.pack(side=tk.LEFT, padx=10)

        # Batch creation frame
        batch_frame = tk.Frame(button_frame, bg=self.bg_color)
        batch_frame.pack(side=tk.LEFT, padx=10)

        self.batch_button = tk.Button(batch_frame, text="📦 Batch Create",
                                      bg="#FF5722", fg="white",
                                      font=('Arial', 12, 'bold'),
                                      padx=20, pady=12,
                                      command=self.batch_create)
        self.batch_button.pack(side=tk.LEFT)

        count_frame = tk.Frame(batch_frame, bg=self.bg_color)
        count_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(count_frame, text="Count:", bg=self.bg_color, fg=self.fg_color,
                 font=('Arial', 10)).pack()

        self.batch_count = tk.Spinbox(count_frame, from_=1, to=100, width=5, value=5)
        self.batch_count.pack()

    def create_sms_tab(self):
        """Create SMS service configuration tab"""
        sms_frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(sms_frame, text="📱 SMS Services")

        ttk.Label(sms_frame, text="SMS Verification Services",
                  style="Heading.TLabel").pack(pady=20)

        # Service selection
        service_frame = tk.Frame(sms_frame, bg=self.bg_color)
        service_frame.pack(pady=10)

        ttk.Label(service_frame, text="Service:", style="Dark.TLabel").pack(side=tk.LEFT, padx=5)

        self.sms_service_var = tk.StringVar(value="none")
        services = ["none", "getsmscode", "smspool", "5sim"]
        self.sms_combo = ttk.Combobox(service_frame, textvariable=self.sms_service_var,
                                      values=services, state="readonly", width=20)
        self.sms_combo.pack(side=tk.LEFT, padx=5)
        self.sms_combo.bind("<<ComboboxSelected>>", self.on_sms_change)

        # Credentials frame
        self.sms_creds_frame = ttk.LabelFrame(sms_frame, text="Service Credentials", style="Dark.TFrame")
        self.sms_creds_frame.pack(fill=tk.X, padx=10, pady=20)

        # GetSMSCode
        self.getsmscode_frame = tk.Frame(self.sms_creds_frame, bg=self.bg_color)
        ttk.Label(self.getsmscode_frame, text="Username:", style="Dark.TLabel").grid(row=0, column=0, padx=5, pady=5)
        self.getsmscode_user = ttk.Entry(self.getsmscode_frame, width=30)
        self.getsmscode_user.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.getsmscode_frame, text="Token:", style="Dark.TLabel").grid(row=1, column=0, padx=5, pady=5)
        self.getsmscode_token = ttk.Entry(self.getsmscode_frame, width=30, show="*")
        self.getsmscode_token.grid(row=1, column=1, padx=5, pady=5)

        # SMSPool
        self.smspool_frame = tk.Frame(self.sms_creds_frame, bg=self.bg_color)
        ttk.Label(self.smspool_frame, text="API Token:", style="Dark.TLabel").grid(row=0, column=0, padx=5, pady=5)
        self.smspool_token = ttk.Entry(self.smspool_frame, width=30, show="*")
        self.smspool_token.grid(row=0, column=1, padx=5, pady=5)

        # 5sim
        self.fivesim_frame = tk.Frame(self.sms_creds_frame, bg=self.bg_color)
        ttk.Label(self.fivesim_frame, text="API Token:", style="Dark.TLabel").grid(row=0, column=0, padx=5, pady=5)
        self.fivesim_token = ttk.Entry(self.fivesim_frame, width=30, show="*")
        self.fivesim_token.grid(row=0, column=1, padx=5, pady=5)

        # Initially hide all
        self.on_sms_change()

    def create_proxy_tab(self):
        """Create proxy configuration tab"""
        proxy_frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(proxy_frame, text="🔒 Proxy Settings")

        ttk.Label(proxy_frame, text="Proxy Configuration",
                  style="Heading.TLabel").pack(pady=20)

        # Proxy options
        options_frame = tk.Frame(proxy_frame, bg=self.bg_color)
        options_frame.pack(pady=10)

        self.use_proxy_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Use Proxy",
                        variable=self.use_proxy_var,
                        style="Dark.TCheckbutton",
                        command=self.toggle_proxy).pack(side=tk.LEFT, padx=5)

        self.auto_proxy_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Auto-fetch Free Proxies",
                        variable=self.auto_proxy_var,
                        style="Dark.TCheckbutton").pack(side=tk.LEFT, padx=5)

        # Proxy list
        proxy_list_frame = ttk.LabelFrame(proxy_frame, text="Proxy List (one per line)", style="Dark.TFrame")
        proxy_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.proxy_text = scrolledtext.ScrolledText(proxy_list_frame,
                                                    height=8, width=60,
                                                    bg="#2b2b2b", fg=self.fg_color,
                                                    insertbackground=self.fg_color)
        self.proxy_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Format info
        info_text = """Format Examples:
        • http://ip:port
        • http://username:password@ip:port
        • socks5://ip:port"""

        tk.Label(proxy_frame, text=info_text, bg=self.bg_color, fg="#888888",
                 justify=tk.LEFT, font=('Courier', 9)).pack(padx=10, pady=5, anchor="w")

        self.toggle_proxy()

    def create_accounts_tab(self):
        """Create tab to display created accounts"""
        accounts_frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(accounts_frame, text="✅ Created Accounts")

        ttk.Label(accounts_frame, text="Successfully Created Accounts",
                  style="Heading.TLabel").pack(pady=15)

        # Buttons
        button_frame = tk.Frame(accounts_frame, bg=self.bg_color)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="💾 Export to File",
                  bg="#FF9800", fg="white", font=('Arial', 10),
                  command=self.export_accounts).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="📋 Copy Selected",
                  bg="#00BCD4", fg="white", font=('Arial', 10),
                  command=self.copy_selected).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="🗑️ Clear List",
                  bg=self.error_color, fg="white", font=('Arial', 10),
                  command=self.clear_accounts).pack(side=tk.LEFT, padx=5)

        # Treeview
        columns = ("Provider", "Username", "Password", "Name", "Birthday", "Created")
        self.accounts_tree = ttk.Treeview(accounts_frame, columns=columns,
                                          show="tree headings", height=15)

        # Configure columns
        self.accounts_tree.heading("#0", text="ID")
        self.accounts_tree.column("#0", width=50)

        widths = [80, 150, 150, 150, 100, 150]
        for col, width in zip(columns, widths):
            self.accounts_tree.heading(col, text=col)
            self.accounts_tree.column(col, width=width)

        self.accounts_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.accounts_tree, orient="vertical",
                                  command=self.accounts_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.accounts_tree.configure(yscrollcommand=scrollbar.set)

    def create_logs_tab(self):
        """Create logs tab"""
        logs_frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(logs_frame, text="📝 Logs")

        ttk.Label(logs_frame, text="Operation Logs",
                  style="Heading.TLabel").pack(pady=15)

        # Buttons
        button_frame = tk.Frame(logs_frame, bg=self.bg_color)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="🧹 Clear Logs",
                  bg="#607D8B", fg="white", font=('Arial', 10),
                  command=self.clear_logs).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="💾 Save Logs",
                  bg="#795548", fg="white", font=('Arial', 10),
                  command=self.save_logs).pack(side=tk.LEFT, padx=5)

        # Log text area
        self.log_text = scrolledtext.ScrolledText(logs_frame,
                                                  height=18, width=85,
                                                  bg="#1a1a1a", fg="#00FF00",
                                                  insertbackground="#00FF00",
                                                  font=('Consolas', 10))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Configure tags for colored text
        self.log_text.tag_config("error", foreground="#FF5252")
        self.log_text.tag_config("success", foreground="#69F0AE")
        self.log_text.tag_config("warning", foreground="#FFD740")
        self.log_text.tag_config("info", foreground="#40C4FF")

    def create_status_bar(self):
        """Create status bar"""
        self.status_frame = tk.Frame(self.root, bg="#333333", height=35)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(self.status_frame,
                                     text="✅ Ready",
                                     bg="#333333", fg=self.fg_color,
                                     font=('Arial', 10), anchor="w")
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.accounts_count_label = tk.Label(self.status_frame,
                                             text="📊 Accounts: 0",
                                             bg="#333333", fg=self.fg_color,
                                             font=('Arial', 10), anchor="e")
        self.accounts_count_label.pack(side=tk.RIGHT, padx=10)

    # Auto-generate functions
    def generate_username(self):
        """Generate and insert username"""
        firstname = self.firstname_entry.get() if self.firstname_entry.get() else None
        lastname = self.lastname_entry.get() if self.lastname_entry.get() else None
        username = nm.DataGenerator.generate_username(firstname, lastname)
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)
        self.log(f"Generated username: {username}", "INFO")

    def generate_password(self):
        """Generate and insert password"""
        password = nm.DataGenerator.generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.log(f"Generated password: {'*' * len(password)}", "INFO")

    def generate_firstname(self):
        """Generate and insert first name"""
        firstname = nm.DataGenerator.generate_first_name()
        self.firstname_entry.delete(0, tk.END)
        self.firstname_entry.insert(0, firstname)
        self.log(f"Generated first name: {firstname}", "INFO")

    def generate_lastname(self):
        """Generate and insert last name"""
        lastname = nm.DataGenerator.generate_last_name()
        self.lastname_entry.delete(0, tk.END)
        self.lastname_entry.insert(0, lastname)
        self.log(f"Generated last name: {lastname}", "INFO")

    def generate_birthdate(self):
        """Generate and insert birthdate"""
        min_age = int(self.min_age.get())
        max_age = int(self.max_age.get())
        birthdate = nm.DataGenerator.generate_birthday(min_age, max_age)
        self.birthdate_entry.delete(0, tk.END)
        self.birthdate_entry.insert(0, birthdate)
        self.log(f"Generated birthdate: {birthdate}", "INFO")

    def generate_country(self):
        """Generate and insert country"""
        country = nm.DataGenerator.generate_country()
        self.country_entry.delete(0, tk.END)
        self.country_entry.insert(0, country)
        self.log(f"Generated country: {country}", "INFO")

    def generate_all_fields(self):
        """Generate all fields at once"""
        self.generate_firstname()
        self.generate_lastname()
        self.generate_username()
        self.generate_password()
        self.generate_birthdate()
        self.generate_country()
        self.log("Generated all fields", "SUCCESS")

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def toggle_proxy(self):
        """Toggle proxy text area"""
        if self.use_proxy_var.get():
            self.proxy_text.config(state="normal")
        else:
            self.proxy_text.config(state="disabled")

    def on_sms_change(self, event=None):
        """Handle SMS service change"""
        for frame in [self.getsmscode_frame, self.smspool_frame, self.fivesim_frame]:
            frame.pack_forget()

        service = self.sms_service_var.get()
        if service == "getsmscode":
            self.getsmscode_frame.pack(fill=tk.X, padx=5, pady=5)
        elif service == "smspool":
            self.smspool_frame.pack(fill=tk.X, padx=5, pady=5)
        elif service == "5sim":
            self.fivesim_frame.pack(fill=tk.X, padx=5, pady=5)

    def log(self, message, level="INFO"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Map levels to tags
        tag_map = {
            "ERROR": "error",
            "SUCCESS": "success",
            "WARNING": "warning",
            "INFO": "info"
        }
        tag = tag_map.get(level, "info")

        log_message = f"[{timestamp}] [{level}] {message}\n"
        self.log_text.insert(tk.END, log_message, tag)
        self.log_text.see(tk.END)

        # Update status
        status_icons = {
            "ERROR": "❌",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "INFO": "ℹ️"
        }
        icon = status_icons.get(level, "ℹ️")
        self.status_label.config(text=f"{icon} {message[:50]}...")

    def get_sms_config(self):
        """Get SMS configuration"""
        service = self.sms_service_var.get()

        if service == "none":
            return None, None
        elif service == "getsmscode":
            username = self.getsmscode_user.get()
            token = self.getsmscode_token.get()
            if username and token:
                return service, {"username": username, "token": token}
        elif service == "smspool":
            token = self.smspool_token.get()
            if token:
                return service, {"token": token}
        elif service == "5sim":
            token = self.fivesim_token.get()
            if token:
                return service, {"token": token}

        return None, None

    def get_proxy_list(self):
        """Get proxy list"""
        if not self.use_proxy_var.get():
            return None

        proxy_text = self.proxy_text.get("1.0", tk.END).strip()
        if not proxy_text:
            return None

        proxies = [p.strip() for p in proxy_text.split("\n") if p.strip()]
        return proxies if proxies else None

    def create_account(self):
        """Create single account"""
        self.create_button.config(state="disabled", text="⏳ Creating...")

        thread = threading.Thread(target=self._create_account_thread)
        thread.daemon = True
        thread.start()

    def _create_account_thread(self):
        """Thread for account creation"""
        try:
            self.log("Starting account creation...")

            # Get all values
            provider = self.provider_var.get()
            browser = self.browser_var.get()
            headless = self.headless_var.get()

            username = self.username_entry.get() or None
            password = self.password_entry.get() or None
            firstname = self.firstname_entry.get() or None
            lastname = self.lastname_entry.get() or None
            birthdate = self.birthdate_entry.get()
            if birthdate == "YYYY-MM-DD":
                birthdate = None
            country = self.country_entry.get() or None

            sms_service, sms_config = self.get_sms_config()
            proxies = self.get_proxy_list()
            auto_proxy = self.auto_proxy_var.get() if self.use_proxy_var.get() else False

            # Kick off creation
            account = self.account_creator.create_account(
                provider=provider,
                browser=browser,
                headless=headless,
                username=username,
                password=password,
                firstname=firstname,
                lastname=lastname,
                birthdate=birthdate,
                country=country,
                sms_service=sms_service,
                sms_config=sms_config,
                proxies=proxies,
                auto_proxy=auto_proxy,
                auto_generate=True
            )

            if account:
                self.root.after(0, self._on_account_created, account)
                self.log(f"Account created: {account['username']}", "SUCCESS")
            else:
                self.log("Account creation failed.", "ERROR")

        except Exception as e:
            self.log(f"Error creating account: {e}", "ERROR")
        finally:
            self.root.after(0, lambda: self.create_button.config(state="normal", text="✨ Create Account"))

    def _on_account_created(self, account):
        """UI updates when a single account is created"""
        self._add_account_to_tree(account)
        self._update_account_count()

    def _add_account_to_tree(self, account):
        """Insert a created account into the treeview"""
        idx = len(self.accounts_tree.get_children()) + 1
        name = f"{account.get('firstname', '')} {account.get('lastname', '')}".strip()
        created = account.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.accounts_tree.insert(
            "",
            "end",
            text=str(idx),
            values=(
                account.get("provider", ""),
                account.get("username", ""),
                account.get("password", ""),
                name,
                account.get("birthdate", ""),
                created
            )
        )

    def _update_account_count(self):
        """Refresh status bar account count"""
        count = len(self.account_creator.created_accounts)
        self.accounts_count_label.config(text=f"📊 Accounts: {count}")

    # ---------- Batch creation ----------
    def batch_create(self):
        """Start batch creation in a thread"""
        try:
            count = int(self.batch_count.get())
        except ValueError:
            messagebox.showerror("Invalid count", "Please enter a valid number of accounts to create.")
            return

        self.batch_button.config(state="disabled", text="⏳ Creating batch...")
        thread = threading.Thread(target=self._batch_create_thread, args=(count,))
        thread.daemon = True
        thread.start()

    def _batch_create_thread(self, count):
        """Thread worker for batch creation"""
        try:
            self.log(f"Starting batch creation: {count} account(s)...", "INFO")

            # Collect shared settings
            provider = self.provider_var.get()
            browser = self.browser_var.get()
            headless = self.headless_var.get()

            # Individual fields can be left blank so each account autogenerates
            username = self.username_entry.get() or None
            password = self.password_entry.get() or None
            firstname = self.firstname_entry.get() or None
            lastname = self.lastname_entry.get() or None
            birthdate = self.birthdate_entry.get()
            if birthdate == "YYYY-MM-DD":
                birthdate = None
            country = self.country_entry.get() or None

            sms_service, sms_config = self.get_sms_config()
            proxies = self.get_proxy_list()
            auto_proxy = self.auto_proxy_var.get() if self.use_proxy_var.get() else False

            accounts = self.account_creator.batch_create(
                count=count,
                provider=provider,
                browser=browser,
                headless=headless,
                username=username,
                password=password,
                firstname=firstname,
                lastname=lastname,
                birthdate=birthdate,
                country=country,
                sms_service=sms_service,
                sms_config=sms_config,
                proxies=proxies,
                auto_proxy=auto_proxy,
                auto_generate=True
            )

            if accounts:
                self.log(f"Batch created {len(accounts)} account(s).", "SUCCESS")
                self.root.after(0, self._on_batch_created, accounts)
            else:
                self.log("No accounts were created in batch.", "WARNING")

        except Exception as e:
            self.log(f"Batch creation error: {e}", "ERROR")
        finally:
            self.root.after(0, lambda: self.batch_button.config(state="normal", text="📦 Batch Create"))

    def _on_batch_created(self, accounts):
        """UI updates when batch completes"""
        for acct in accounts:
            self._add_account_to_tree(acct)
        self._update_account_count()

    # ---------- Accounts tab actions ----------
    def export_accounts(self):
        """Export created accounts to a file"""
        if not self.account_creator.created_accounts:
            messagebox.showinfo("Nothing to export", "No accounts have been created yet.")
            return

        filetypes = [("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        filename = filedialog.asksaveasfilename(
            title="Export Accounts",
            defaultextension=".txt",
            filetypes=filetypes,
            initialfile="accounts.txt"
        )
        if not filename:
            return

        fmt = "json" if filename.lower().endswith(".json") else "txt"
        ok = self.account_creator.export_accounts(filename, fmt)
        if ok:
            self.log(f"Exported accounts to {filename}", "SUCCESS")
            messagebox.showinfo("Exported", f"Accounts exported to:\n{filename}")
        else:
            self.log("Export failed.", "ERROR")
            messagebox.showerror("Export failed", "Failed to export accounts.")

    def copy_selected(self):
        """Copy selected rows to clipboard"""
        items = self.accounts_tree.selection()
        if not items:
            messagebox.showinfo("No selection", "Select one or more rows first.")
            return

        lines = []
        headers = ["ID", "Provider", "Username", "Password", "Name", "Birthday", "Created"]
        lines.append("\t".join(headers))
        for item in items:
            id_text = self.accounts_tree.item(item, "text")
            vals = self.accounts_tree.item(item, "values")
            line = [id_text] + list(vals)
            lines.append("\t".join(str(x) for x in line))

        text = "\n".join(lines)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.log("Copied selected rows to clipboard.", "SUCCESS")

    def clear_accounts(self):
        """Clear the tree and internal list"""
        if not self.account_creator.created_accounts:
            return
        if not messagebox.askyesno("Clear accounts", "Remove all displayed accounts?"):
            return

        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)
        self.account_creator.created_accounts.clear()
        self._update_account_count()
        self.log("Cleared account list.", "INFO")

    # ---------- Logs tab actions ----------
    def clear_logs(self):
        self.log_text.delete("1.0", tk.END)
        self.status_label.config(text="✅ Ready")

    def save_logs(self):
        filename = filedialog.asksaveasfilename(
            title="Save Logs",
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filename:
            return
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.log_text.get("1.0", tk.END))
            self.log(f"Saved logs to {filename}", "SUCCESS")
        except Exception as e:
            self.log(f"Failed to save logs: {e}", "ERROR")

    # ---------- Config persistence ----------
    def save_config(self):
        """Persist a minimal config snapshot using AccountCreator helper"""
        cfg = {
            "provider": self.provider_var.get(),
            "browser": self.browser_var.get(),
            "headless": self.headless_var.get(),
            "username": self.username_entry.get(),
            "password": self.password_entry.get(),
            "firstname": self.firstname_entry.get(),
            "lastname": self.lastname_entry.get(),
            "birthdate": self.birthdate_entry.get(),
            "country": self.country_entry.get(),
            "sms_service": self.sms_service_var.get(),
            "getsmscode_user": self.getsmscode_user.get(),
            "getsmscode_token": self.getsmscode_token.get(),
            "smspool_token": self.smspool_token.get(),
            "fivesim_token": self.fivesim_token.get(),
            "use_proxy": self.use_proxy_var.get(),
            "auto_proxy": self.auto_proxy_var.get(),
            "proxies": self.proxy_text.get("1.0", tk.END)
        }
        ok = self.account_creator.save_config(cfg, filename="ninjemail_config.json")
        if ok:
            self.log("Configuration saved.", "SUCCESS")
        else:
            self.log("Failed to save configuration.", "ERROR")

    def load_config(self):
        """Load prior config (if any) and apply to UI"""
        cfg = self.account_creator.load_config(filename="ninjemail_config.json")
        if not cfg:
            return
        try:
            self.provider_var.set(cfg.get("provider", "gmail"))
            self.browser_var.set(cfg.get("browser", "chrome"))
            self.headless_var.set(bool(cfg.get("headless", False)))

            # Text fields
            self.username_entry.delete(0, tk.END);
            self.username_entry.insert(0, cfg.get("username", ""))
            self.password_entry.delete(0, tk.END);
            self.password_entry.insert(0, cfg.get("password", ""))
            self.firstname_entry.delete(0, tk.END);
            self.firstname_entry.insert(0, cfg.get("firstname", ""))
            self.lastname_entry.delete(0, tk.END);
            self.lastname_entry.insert(0, cfg.get("lastname", ""))
            self.birthdate_entry.delete(0, tk.END);
            self.birthdate_entry.insert(0, cfg.get("birthdate", "YYYY-MM-DD"))
            self.country_entry.delete(0, tk.END);
            self.country_entry.insert(0, cfg.get("country", ""))

            # SMS
            self.sms_service_var.set(cfg.get("sms_service", "none"))
            self.on_sms_change()
            self.getsmscode_user.delete(0, tk.END);
            self.getsmscode_user.insert(0, cfg.get("getsmscode_user", ""))
            self.getsmscode_token.delete(0, tk.END);
            self.getsmscode_token.insert(0, cfg.get("getsmscode_token", ""))
            self.smspool_token.delete(0, tk.END);
            self.smspool_token.insert(0, cfg.get("smspool_token", ""))
            self.fivesim_token.delete(0, tk.END);
            self.fivesim_token.insert(0, cfg.get("fivesim_token", ""))

            # Proxy
            self.use_proxy_var.set(bool(cfg.get("use_proxy", False)))
            self.auto_proxy_var.set(bool(cfg.get("auto_proxy", False)))
            self.proxy_text.config(state="normal")
            self.proxy_text.delete("1.0", tk.END)
            self.proxy_text.insert("1.0", cfg.get("proxies", ""))
            self.toggle_proxy()

            self.log("Configuration loaded.", "INFO")
        except Exception as e:
            self.log(f"Failed to load configuration: {e}", "ERROR")


def run_gui():
    """Launch the Ninjemail GUI"""
    root = tk.Tk()
    app = NinjemailGUI(root)

    # Add a simple menu for Save Config / Exit
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Save Configuration", command=app.save_config)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
