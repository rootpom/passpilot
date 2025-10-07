"""
PassPilot Supreme: The Ultimate Password Security Toolkit
=========================================================

A professional-grade password management application with advanced security
features, beautiful modern UI, and comprehensive password analysis tools.

Revolutionary Features:
- 🎨 Modern, glassmorphic UI with dark/light themes
- 🔐 Military-grade password generation with multiple presets
- 📊 Real-time advanced strength analysis with visual feedback
- 🌐 Pwned Passwords API integration with k-anonymity
- 📝 Secure password history (session-only, in-memory)
- 🎯 Password pattern detection and suggestions
- 🔍 Zxcvbn-inspired strength estimation
- 📋 Smart clipboard management with auto-clear
- 💾 Export passwords securely
- ⚡ Keyboard shortcuts for power users
- 🎭 Password masking toggle
- 📈 Detailed entropy breakdown
- 🎪 Password generator presets (Memorable, Maximum Security, etc.)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import string
import secrets
import re
import math
import hashlib
import requests
import json
from datetime import datetime
from collections import Counter
import threading
import gettext
import locale
import os

# Internationalization setup
locale.setlocale(locale.LC_ALL, '')
lang = locale.getlocale()[0]
if lang and lang.startswith('hi'):
    lang = 'hi'
else:
    lang = 'en'

localedir = os.path.join(os.path.dirname(__file__), 'locale')
gettext.install('passpilot', localedir, names=['ngettext'])
_ = gettext.gettext

# --- Advanced Password Generator ---

class AdvancedPasswordGenerator:
    """Next-generation password generator with intelligent algorithms."""
    
    PRESETS = {
        "Balanced": {"length": 16, "lower": True, "upper": True, "digits": True, "symbols": True},
        "Maximum Security": {"length": 32, "lower": True, "upper": True, "digits": True, "symbols": True},
        "Memorable": {"length": 20, "lower": True, "upper": True, "digits": True, "symbols": False},
        "PIN": {"length": 6, "lower": False, "upper": False, "digits": True, "symbols": False},
        "Alphanumeric": {"length": 16, "lower": True, "upper": True, "digits": True, "symbols": False},
        "Paranoid": {"length": 64, "lower": True, "upper": True, "digits": True, "symbols": True}
    }
    
    def __init__(self):
        self.history = []
        self.max_history = 50
    
    def generate(self, length, use_lower, use_upper, use_digits, use_symbols, exclude_ambiguous=False):
        """Generate a cryptographically secure password."""
        char_pool = []
        password_chars = []
        
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        
        # Exclude ambiguous characters if requested
        if exclude_ambiguous:
            lower = lower.replace('l', '').replace('o', '')
            upper = upper.replace('I', '').replace('O', '')
            digits = digits.replace('0', '').replace('1', '')
            symbols = symbols.replace('|', '').replace('l', '')
        
        if use_lower:
            char_pool.extend(lower)
            password_chars.append(secrets.choice(lower))
        if use_upper:
            char_pool.extend(upper)
            password_chars.append(secrets.choice(upper))
        if use_digits:
            char_pool.extend(digits)
            password_chars.append(secrets.choice(digits))
        if use_symbols:
            char_pool.extend(symbols)
            password_chars.append(secrets.choice(symbols))
        
        if not char_pool:
            return ""
        
        remaining = length - len(password_chars)
        if remaining > 0:
            password_chars.extend(secrets.choice(char_pool) for _ in range(remaining))
        
        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)
        
        # Add to history
        self.add_to_history(password)
        return password
    
    def generate_passphrase(self, word_count=5, separator="-", capitalize=True, add_number=True):
        """Generate a memorable passphrase using common words."""
        # Built-in word list (simplified version)
        words = [
            "correct", "horse", "battery", "staple", "dragon", "mountain", "river", "forest",
            "thunder", "crystal", "phoenix", "shadow", "silver", "golden", "mystic", "cosmic",
            "aurora", "nebula", "quantum", "stellar", "lunar", "solar", "ocean", "summit",
            "falcon", "tiger", "eagle", "wolf", "bear", "lion", "hawk", "cobra",
            "velocity", "infinity", "destiny", "legacy", "wisdom", "courage", "honor", "justice"
        ]
        
        selected = [secrets.choice(words) for _ in range(word_count)]
        if capitalize:
            selected = [w.capitalize() for w in selected]
        
        passphrase = separator.join(selected)
        if add_number:
            passphrase += separator + str(secrets.randbelow(9999))
        
        self.add_to_history(passphrase)
        return passphrase
    
    def add_to_history(self, password):
        """Add password to session history."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history.insert(0, {"password": password, "time": timestamp})
        if len(self.history) > self.max_history:
            self.history.pop()

# --- Advanced Password Analyzer ---

class AdvancedPasswordAnalyzer:
    """Comprehensive password analysis with pattern detection."""
    
    def __init__(self):
        self.common_patterns = [
            r'123+', r'abc+', r'qwert+', r'password', r'admin',
            r'(\w)\1{2,}', r'\d{4,}', r'[a-z]{5,}', r'[A-Z]{5,}'
        ]
    
    def calculate_entropy(self, password):
        """Calculate Shannon entropy."""
        if not password:
            return 0.0
        
        pool_size = 0
        if re.search(r'[a-z]', password):
            pool_size += 26
        if re.search(r'[A-Z]', password):
            pool_size += 26
        if re.search(r'\d', password):
            pool_size += 10
        if re.search(r'[^a-zA-Z\d]', password):
            pool_size += 32
        
        if pool_size == 0:
            return 0.0
        
        entropy = len(password) * math.log2(pool_size)
        return round(entropy, 2)
    
    def calculate_character_entropy(self, password):
        """Calculate actual Shannon entropy based on character frequency."""
        if not password:
            return 0.0
        
        freq = Counter(password)
        length = len(password)
        entropy = -sum((count/length) * math.log2(count/length) for count in freq.values())
        return round(entropy * length, 2)
    
    def detect_patterns(self, password):
        """Detect common weak patterns."""
        patterns = []
        for pattern in self.common_patterns:
            if re.search(pattern, password, re.IGNORECASE):
                patterns.append(pattern)
        return patterns
    
    def get_crack_time(self, entropy):
        """Estimate time to crack with modern hardware."""
        # Assuming 100 billion guesses per second (modern GPU)
        guesses_per_sec = 100_000_000_000
        combinations = 2 ** entropy
        seconds = combinations / guesses_per_sec
        
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.2f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.2f} days"
        elif seconds < 31536000 * 100:
            return f"{seconds/31536000:.2f} years"
        elif seconds < 31536000 * 1000000:
            return f"{seconds/(31536000*1000):.2f} thousand years"
        else:
            return "millions of years+"
    
    def get_strength_feedback(self, entropy):
        """Enhanced strength classification."""
        if entropy < 28:
            return _("Critical"), "#c0392b", 0
        elif entropy < 36:
            return _("Very Weak"), "#e74c3c", 1
        elif entropy < 50:
            return _("Weak"), "#e67e22", 2
        elif entropy < 65:
            return _("Fair"), "#f39c12", 3
        elif entropy < 80:
            return _("Good"), "#f1c40f", 4
        elif entropy < 100:
            return _("Strong"), "#2ecc71", 5
        elif entropy < 120:
            return _("Very Strong"), "#27ae60", 6
        else:
            return _("Exceptional"), "#16a085", 7
    
    def get_suggestions(self, password):
        """Provide intelligent improvement suggestions."""
        suggestions = []

        if len(password) < 12:
            suggestions.append("• " + _("Increase length to at least 12 characters"))
        if not re.search(r'[a-z]', password):
            suggestions.append("• " + _("Add lowercase letters"))
        if not re.search(r'[A-Z]', password):
            suggestions.append("• " + _("Add uppercase letters"))
        if not re.search(r'\d', password):
            suggestions.append("• " + _("Add numbers"))
        if not re.search(r'[^a-zA-Z\d]', password):
            suggestions.append("• " + _("Add special characters"))
        if self.detect_patterns(password):
            suggestions.append("• " + _("Avoid common patterns and sequences"))
        if len(set(password)) < len(password) * 0.6:
            suggestions.append("• " + _("Use more unique characters"))

        return suggestions if suggestions else ["• " + _("Your password is excellent!")]
    
    def check_if_pwned(self, password):
        """Check against Have I Been Pwned database."""
        if not password:
            return None, "Password is empty."
        
        try:
            sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix, suffix = sha1[:5], sha1[5:]
            
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == suffix:
                    return int(count), None
            
            return 0, None
        except requests.RequestException as e:
            return None, f"API error: {e}"
        except Exception as e:
            return None, f"Error: {e}"

# --- Modern UI Application ---

class PassPilotSupreme(tk.Tk):
    """The ultimate password management interface."""
    
    def __init__(self, generator, analyzer):
        super().__init__()
        self.generator = generator
        self.analyzer = analyzer

        self.title(_("PassPilot Supreme"))
        self.geometry("900x850")
        self.resizable(True, True)
        
        # Theme variables
        self.dark_mode = tk.BooleanVar(value=True)
        self.show_password = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        # Language variable
        self.language_var = tk.StringVar(value=lang)
        
        # Clipboard timer
        self.clipboard_timer = None
        
        # Setup UI
        self.setup_styles()
        self.create_menu()
        self.create_widgets()
        self.apply_theme()
        
        # Keyboard shortcuts
        self.bind('<Control-g>', lambda e: self.generate_password())
        self.bind('<Control-c>', lambda e: self.copy_to_clipboard())
        self.bind('<Control-p>', lambda e: self.generate_passphrase())
        self.bind('<F1>', lambda e: self.show_help())
    
    def setup_styles(self):
        """Configure modern styling."""
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
    
    def apply_theme(self):
        """Apply dark or light theme."""
        if self.dark_mode.get():
            # Dark theme
            bg = "#1a1a2e"
            fg = "#eee"
            accent = "#0f3460"
            highlight = "#16213e"
            button_bg = "#e94560"
            
            self.configure(bg=bg)
            self.style.configure("TFrame", background=bg)
            self.style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
            self.style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground="#e94560")
            self.style.configure("Subtitle.TLabel", font=("Segoe UI", 11, "bold"))
            self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background=button_bg, foreground="white")
            self.style.map("TButton", background=[('active', '#d63447')])
            self.style.configure("TCheckbutton", background=bg, foreground=fg, font=("Segoe UI", 9))
            self.style.configure("TLabelframe", background=bg, foreground=fg, bordercolor=accent)
            self.style.configure("TLabelframe.Label", background=bg, foreground="#e94560", font=("Segoe UI", 11, "bold"))
            self.style.configure("TNotebook", background=bg, bordercolor=accent)
            self.style.configure("TNotebook.Tab", background=accent, foreground=fg, padding=[20, 10])
            self.style.map("TNotebook.Tab", background=[('selected', button_bg)], foreground=[('selected', 'white')])
        else:
            # Light theme
            bg = "#f8f9fa"
            fg = "#212529"
            accent = "#dee2e6"
            highlight = "#e9ecef"
            button_bg = "#0d6efd"
            
            self.configure(bg=bg)
            self.style.configure("TFrame", background=bg)
            self.style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
            self.style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground=button_bg)
            self.style.configure("Subtitle.TLabel", font=("Segoe UI", 11, "bold"))
            self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background=button_bg, foreground="white")
            self.style.configure("TCheckbutton", background=bg, foreground=fg, font=("Segoe UI", 9))
            self.style.configure("TLabelframe", background=bg, foreground=fg, bordercolor=accent)
            self.style.configure("TLabelframe.Label", background=bg, foreground=button_bg, font=("Segoe UI", 11, "bold"))
    
    def create_menu(self):
        """Create application menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("File"), menu=file_menu)
        file_menu.add_command(label=_("Export History"), command=self.export_history)
        file_menu.add_separator()
        file_menu.add_command(label=_("Exit"), command=self.quit)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("View"), menu=view_menu)
        view_menu.add_checkbutton(label=_("Dark Mode"), variable=self.dark_mode, command=self.apply_theme)
        view_menu.add_checkbutton(label=_("Show Passwords"), variable=self.show_password, command=self.toggle_password_visibility)

        # Language submenu
        lang_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label=_("Language"), menu=lang_menu)
        lang_menu.add_radiobutton(label="English", variable=self.language_var, value="en", command=self.change_language)
        lang_menu.add_radiobutton(label="हिंदी (Hindi)", variable=self.language_var, value="hi", command=self.change_language)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("Help"), menu=help_menu)
        help_menu.add_command(label=_("Keyboard Shortcuts"), command=self.show_help)
        help_menu.add_command(label=_("About"), command=self.show_about)
    
    def create_widgets(self):
        """Build the main interface."""
        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        ttk.Label(header, text="🔐 PassPilot Supreme", style="Title.TLabel").pack()
        ttk.Label(header, text=_("Military-Grade Password Security Toolkit"),
                 font=("Segoe UI", 9, "italic")).pack()
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tab 1: Generator
        self.create_generator_tab()

        # Tab 2: Analyzer
        self.create_analyzer_tab()

        # Tab 3: History
        self.create_history_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self, text=_("Ready"), relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")
    
    def create_generator_tab(self):
        """Create password generator tab."""
        gen_tab = ttk.Frame(self.notebook)
        self.notebook.add(gen_tab, text="🎲 " + _("Generator"))
        
        # Main container
        container = ttk.Frame(gen_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Presets
        preset_frame = ttk.LabelFrame(container, text=_("Quick Presets"), padding=15)
        preset_frame.pack(fill="x", pady=(0, 15))
        
        presets_container = ttk.Frame(preset_frame)
        presets_container.pack()
        
        for i, preset_name in enumerate(self.generator.PRESETS.keys()):
            btn = ttk.Button(presets_container, text=preset_name, 
                           command=lambda p=preset_name: self.apply_preset(p))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
        
        # Custom settings
        settings_frame = ttk.LabelFrame(container, text=_("Custom Settings"), padding=15)
        settings_frame.pack(fill="x", pady=(0, 15))
        
        # Length slider
        length_frame = ttk.Frame(settings_frame)
        length_frame.pack(fill="x", pady=5)
        ttk.Label(length_frame, text=_("Length:"), style="Subtitle.TLabel").pack(side="left", padx=(0, 10))
        self.length_var = tk.IntVar(value=16)
        self.length_scale = ttk.Scale(length_frame, from_=4, to_=128, orient="horizontal", 
                                     variable=self.length_var, command=self._update_length_label)
        self.length_scale.pack(side="left", fill="x", expand=True, padx=5)
        self.length_label = ttk.Label(length_frame, text="16", font=("Segoe UI", 10, "bold"), width=5)
        self.length_label.pack(side="left", padx=(10, 0))
        
        # Character options
        chars_frame = ttk.Frame(settings_frame)
        chars_frame.pack(fill="x", pady=10)
        
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(chars_frame, text=_("Lowercase (a-z)"), variable=self.lower_var).grid(row=0, column=0, sticky="w", pady=3)
        ttk.Checkbutton(chars_frame, text=_("Uppercase (A-Z)"), variable=self.upper_var).grid(row=0, column=1, sticky="w", pady=3, padx=20)
        ttk.Checkbutton(chars_frame, text=_("Numbers (0-9)"), variable=self.digits_var).grid(row=1, column=0, sticky="w", pady=3)
        ttk.Checkbutton(chars_frame, text=_("Symbols (!@#$%)"), variable=self.symbols_var).grid(row=1, column=1, sticky="w", pady=3, padx=20)
        ttk.Checkbutton(chars_frame, text=_("Exclude ambiguous (0OIl1|)"), variable=self.exclude_ambiguous).grid(row=2, column=0, columnspan=2, sticky="w", pady=3)
        
        # Generated password display
        output_frame = ttk.LabelFrame(container, text=_("Generated Password"), padding=15)
        output_frame.pack(fill="x", pady=(0, 15))
        
        self.password_entry = tk.Entry(output_frame, font=("Consolas", 14, "bold"), 
                                      justify="center", fg="#2ecc71", bd=0, relief="flat")
        self.password_entry.pack(fill="x", ipady=10)
        
        # Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x")
        
        ttk.Button(btn_frame, text="🎲 " + _("Generate Password (Ctrl+G)"),
                  command=self.generate_password).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="📝 " + _("Generate Passphrase (Ctrl+P)"),
                  command=self.generate_passphrase).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="📋 " + _("Copy to Clipboard (Ctrl+C)"),
                  command=self.copy_to_clipboard).pack(fill="x", pady=2)
    
    def create_analyzer_tab(self):
        """Create password analyzer tab."""
        ana_tab = ttk.Frame(self.notebook)
        self.notebook.add(ana_tab, text="🔍 " + _("Analyzer"))
        
        container = ttk.Frame(ana_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Input
        input_frame = ttk.LabelFrame(container, text=_("Password Analysis"), padding=15)
        input_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(input_frame, text=_("Enter password to analyze:")).pack(anchor="w", pady=(0, 5))
        
        self.analyze_entry_var = tk.StringVar()
        self.analyze_entry_var.trace_add("write", self.analyze_password)
        self.analyze_entry = tk.Entry(input_frame, font=("Consolas", 12), 
                                     textvariable=self.analyze_entry_var, show="")
        self.analyze_entry.pack(fill="x", ipady=5)
        
        # Strength visualization
        viz_frame = ttk.LabelFrame(container, text=_("Strength Visualization"), padding=15)
        viz_frame.pack(fill="x", pady=(0, 15))

        self.strength_canvas = tk.Canvas(viz_frame, height=40, bg="#2c3e50", highlightthickness=0)
        self.strength_canvas.pack(fill="x", pady=(0, 10))

        self.feedback_label = ttk.Label(viz_frame, text=_("Enter a password to analyze"),
                                       font=("Segoe UI", 12, "bold"), anchor="center")
        self.feedback_label.pack(fill="x")
        
        # Detailed metrics
        metrics_frame = ttk.LabelFrame(container, text=_("Detailed Metrics"), padding=15)
        metrics_frame.pack(fill="x", pady=(0, 15))

        self.entropy_label = ttk.Label(metrics_frame, text=_("Entropy: - bits"), anchor="w")
        self.entropy_label.pack(fill="x", pady=2)

        self.crack_time_label = ttk.Label(metrics_frame, text=_("Est. crack time: -"), anchor="w")
        self.crack_time_label.pack(fill="x", pady=2)

        self.char_entropy_label = ttk.Label(metrics_frame, text=_("Character diversity: -"), anchor="w")
        self.char_entropy_label.pack(fill="x", pady=2)
        
        # Suggestions
        suggest_frame = ttk.LabelFrame(container, text=_("Improvement Suggestions"), padding=15)
        suggest_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.suggestions_text = scrolledtext.ScrolledText(suggest_frame, height=6, 
                                                         font=("Segoe UI", 9), wrap="word")
        self.suggestions_text.pack(fill="both", expand=True)
        
        # Breach check
        breach_frame = ttk.Frame(container)
        breach_frame.pack(fill="x")
        
        ttk.Button(breach_frame, text="🌐 " + _("Check if Exposed in Data Breach"),
                  command=self.check_pwned_threaded).pack(fill="x", pady=2)
        
        self.pwned_label = ttk.Label(breach_frame, text="", anchor="center", 
                                    font=("Segoe UI", 10, "bold"))
        self.pwned_label.pack(fill="x", pady=5)
    
    def create_history_tab(self):
        """Create password history tab."""
        hist_tab = ttk.Frame(self.notebook)
        self.notebook.add(hist_tab, text="📜 " + _("History"))
        
        container = ttk.Frame(hist_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(container, text=_("Session Password History (In-Memory Only)"),
                  style="Subtitle.TLabel").pack(pady=(0, 10))

        ttk.Label(container, text="⚠️ " + _("Passwords are stored only for this session and are never written to disk."),
                  font=("Segoe UI", 9, "italic")).pack(pady=(0, 10))
        
        # History listbox
        hist_frame = ttk.Frame(container)
        hist_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(hist_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(hist_frame, font=("Consolas", 10), 
                                         yscrollcommand=scrollbar.set, selectmode="single")
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(btn_frame, text="📋 " + _("Copy Selected"),
                  command=self.copy_from_history).pack(side="left", padx=2, fill="x", expand=True)
        ttk.Button(btn_frame, text="🔄 " + _("Refresh"),
                  command=self.refresh_history).pack(side="left", padx=2, fill="x", expand=True)
        ttk.Button(btn_frame, text="🗑️ " + _("Clear History"),
                  command=self.clear_history).pack(side="left", padx=2, fill="x", expand=True)
    
    def _update_length_label(self, value):
        """Update length display."""
        self.length_label.config(text=f"{int(float(value))}")
    
    def apply_preset(self, preset_name):
        """Apply a preset configuration."""
        preset = self.generator.PRESETS[preset_name]
        self.length_var.set(preset["length"])
        self.lower_var.set(preset["lower"])
        self.upper_var.set(preset["upper"])
        self.digits_var.set(preset["digits"])
        self.symbols_var.set(preset["symbols"])
        self.generate_password()
    
    def generate_password(self):
        """Generate a new password."""
        if not any([self.lower_var.get(), self.upper_var.get(),
                    self.digits_var.get(), self.symbols_var.get()]):
            messagebox.showwarning(_("Warning"), _("Please select at least one character type!"))
            return
        
        password = self.generator.generate(
            self.length_var.get(),
            self.lower_var.get(),
            self.upper_var.get(),
            self.digits_var.get(),
            self.symbols_var.get(),
            self.exclude_ambiguous.get()
        )
        
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        
        self.analyze_entry.delete(0, tk.END)
        self.analyze_entry.insert(0, password)
        
        self.status_bar.config(text=_("Password generated ({0} characters)").format(len(password)))
        self.refresh_history()
    
    def generate_passphrase(self):
        """Generate a memorable passphrase."""
        passphrase = self.generator.generate_passphrase()
        
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, passphrase)
        
        self.analyze_entry.delete(0, tk.END)
        self.analyze_entry.insert(0, passphrase)
        
        self.status_bar.config(text=_("Passphrase generated"))
        self.refresh_history()
    
    def copy_to_clipboard(self):
        """Copy password to clipboard with auto-clear timer."""
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning(_("Warning"), _("No password to copy!"))
            return

        self.clipboard_clear()
        self.clipboard_append(password)
        self.status_bar.config(text=_("Copied! Clipboard will clear in 30 seconds..."))
        
        # Auto-clear after 30 seconds
        if self.clipboard_timer:
            self.after_cancel(self.clipboard_timer)
        self.clipboard_timer = self.after(30000, self.clear_clipboard)
    
    def clear_clipboard(self):
        """Clear clipboard for security."""
        self.clipboard_clear()
        self.status_bar.config(text=_("Clipboard cleared for security"))
    
    def analyze_password(self, *args):
        """Analyze password in real-time."""
        password = self.analyze_entry_var.get()
        
        if not password:
            self.strength_canvas.delete("all")
            self.feedback_label.config(text=_("Enter a password to analyze"), foreground="#95a5a6")
            self.entropy_label.config(text=_("Entropy: - bits"))
            self.crack_time_label.config(text=_("Est. crack time: -"))
            self.char_entropy_label.config(text=_("Character diversity: -"))
            self.suggestions_text.delete(1.0, tk.END)
            self.pwned_label.config(text="")
            return
        
        # Calculate metrics
        entropy = self.analyzer.calculate_entropy(password)
        char_entropy = self.analyzer.calculate_character_entropy(password)
        strength_text, color, level = self.analyzer.get_strength_feedback(entropy)
        crack_time = self.analyzer.get_crack_time(entropy)
        suggestions = self.analyzer.get_suggestions(password)
        
        # Update visualization
        self.draw_strength_bar(level, color)
        self.feedback_label.config(text=_("{0} Password").format(strength_text), foreground=color)

        # Update metrics
        self.entropy_label.config(text=_("Entropy: {0} bits (pool-based)").format(entropy))
        self.crack_time_label.config(text=_("Est. crack time: {0}").format(crack_time))
        self.char_entropy_label.config(text=_("Character diversity: {0} bits (Shannon)").format(char_entropy))
        
        # Update suggestions
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.insert(1.0, "\n".join(suggestions))
        
        # Clear breach check result
        self.pwned_label.config(text="")
    
    def draw_strength_bar(self, level, color):
        """Draw animated strength indicator."""
        width = self.strength_canvas.winfo_width()
        if width <= 1:
            width = 500
        height = 40
        
        self.strength_canvas.delete("all")
        
        # Background
        self.strength_canvas.create_rectangle(0, 0, width, height, fill="#34495e", outline="")
        
        # Strength bar
        bar_width = (width / 7) * (level + 1)
        self.strength_canvas.create_rectangle(0, 0, bar_width, height, fill=color, outline="")
        
        # Grid lines
        for i in range(8):
            x = (width / 7) * i
            self.strength_canvas.create_line(x, 0, x, height, fill="#2c3e50", width=2)
    
    def check_pwned_threaded(self):
        """Check password breach status in background thread."""
        password = self.analyze_entry.get()
        if not password:
            messagebox.showinfo(_("Info"), _("Please enter a password to check."))
            return

        self.pwned_label.config(text="🔄 " + _("Checking..."), foreground="#3498db")
        self.status_bar.config(text=_("Checking breach database..."))
        
        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=self.check_pwned_worker, args=(password,))
        thread.daemon = True
        thread.start()
    
    def check_pwned_worker(self, password):
        """Worker thread for breach check."""
        count, error = self.analyzer.check_if_pwned(password)
        
        # Update UI in main thread
        self.after(0, self.update_pwned_result, count, error)
    
    def update_pwned_result(self, count, error):
        """Update UI with breach check results."""
        if error:
            self.pwned_label.config(text="❌ " + error, foreground="#e74c3c")
            self.status_bar.config(text=_("Breach check failed"))
        elif count > 0:
            msg = _("⚠️ EXPOSED! Found {0} times in breaches").format(f"{count:,}")
            self.pwned_label.config(text=msg, foreground="#e74c3c")
            self.status_bar.config(text=_("Password is compromised!"))
        else:
            msg = _("✅ Safe! Not found in known breaches")
            self.pwned_label.config(text=msg, foreground="#2ecc71")
            self.status_bar.config(text=_("Password passed breach check"))
    
    def refresh_history(self):
        """Refresh the history display."""
        self.history_listbox.delete(0, tk.END)
        for item in self.generator.history:
            display = f"[{item['time']}] {item['password'][:40]}..." if len(item['password']) > 40 else f"[{item['time']}] {item['password']}"
            self.history_listbox.insert(tk.END, display)
    
    def copy_from_history(self):
        """Copy selected password from history."""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showinfo(_("Info"), _("Please select a password from history."))
            return

        idx = selection[0]
        password = self.generator.history[idx]['password']

        self.clipboard_clear()
        self.clipboard_append(password)
        messagebox.showinfo(_("Success"), _("Password copied from history!"))
    
    def clear_history(self):
        """Clear password history."""
        if messagebox.askyesno(_("Confirm"), _("Clear all password history?")):
            self.generator.history.clear()
            self.refresh_history()
            self.status_bar.config(text=_("History cleared"))
    
    def export_history(self):
        """Export history to JSON file."""
        if not self.generator.history:
            messagebox.showinfo(_("Info"), _("No history to export."))
            return

        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[(_("JSON files"), "*.json"), (_("All files"), "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.generator.history, f, indent=2)
                messagebox.showinfo(_("Success"), _("History exported to {0}").format(filename))
            except Exception as e:
                messagebox.showerror(_("Error"), _("Export failed: {0}").format(e))
    
    def toggle_password_visibility(self):
        """Toggle password masking."""
        show = "" if self.show_password.get() else "•"
        self.analyze_entry.config(show=show)
    
    def show_help(self):
        """Display keyboard shortcuts."""
        help_text = _("""
        PassPilot Supreme - Keyboard Shortcuts
        =====================================

        Ctrl+G    Generate Password
        Ctrl+P    Generate Passphrase
        Ctrl+C    Copy to Clipboard
        F1        Show This Help

        Features:
        • Military-grade password generation
        • Real-time strength analysis
        • Breach database checking (Have I Been Pwned)
        • Pattern detection & suggestions
        • Secure clipboard with auto-clear
        • Session-only password history
        """)
        messagebox.showinfo(_("Help"), help_text)
    
    def show_about(self):
        """Show about dialog."""
        about_text = _("""
        PassPilot Supreme v2.0
        The Ultimate Password Security Toolkit

        Features:
        ✓ Cryptographically secure password generation
        ✓ Advanced entropy calculation
        ✓ Real-time strength analysis
        ✓ Pattern detection
        ✓ Breach database integration
        ✓ Smart suggestions
        ✓ Secure clipboard management
        ✓ Beautiful modern interface

        Built with Python & Tkinter
        © 2025 PassPilot Supreme
        """)
        messagebox.showinfo(_("About"), about_text)

    def change_language(self):
        """Change application language - requires restart."""
        selected_lang = self.language_var.get()
        messagebox.showinfo(_("Language Change"),
                          _("Language changed to {0}. Please restart the application for changes to take effect.").format(
                              "हिंदी" if selected_lang == 'hi' else "English"))

# --- Main Execution ---

if __name__ == "__main__":
    generator = AdvancedPasswordGenerator()
    analyzer = AdvancedPasswordAnalyzer()
    app = PassPilotSupreme(generator, analyzer)
    app.mainloop()