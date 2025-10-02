"""
PassPilot Pro: The Greatest Password Toolkit
=============================================

This application is an evolution of the original PassPilot script,
transforming it into a full-featured, secure, and user-friendly GUI
application built with tkinter.

Key Upgrades:
1.  Graphical User Interface (GUI): Replaced the command-line menu with an
    intuitive and clean interface using Python's standard tkinter library.
2.  Live Password Strength Analysis: The password strength checker now
    updates in real-time as you type, providing immediate feedback.
3.  Entropy Calculation: Measures password strength using bits of entropy,
    a more accurate and standard metric than a simple score.
4.  "Pwned" Password Check: Integrates with the 'Have I Been Pwned?' API
    to securely check if a password has been exposed in a known data breach.
    This is a critical modern security feature.
5.  Clipboard Integration: Easily copy generated passwords to the clipboard
    with a single click.
6.  Object-Oriented Structure: The code is refactored into classes for
    better organization, maintainability, and scalability.
7.  Improved Password Generation: Uses a more robust method to ensure all
    selected character types are included in the generated password.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets
import re
import math
import hashlib
import requests # Required for the Pwned Passwords API check

# --- Core Logic Classes ---

class PasswordGenerator:
    """Handles the logic for generating secure passwords."""

    def generate(self, length, use_lower, use_upper, use_digits, use_symbols):
        """Generates a password ensuring all selected character types are included."""
        char_pool = []
        password_chars = []

        if use_lower:
            char_pool.extend(string.ascii_lowercase)
            password_chars.append(secrets.choice(string.ascii_lowercase))
        if use_upper:
            char_pool.extend(string.ascii_uppercase)
            password_chars.append(secrets.choice(string.ascii_uppercase))
        if use_digits:
            char_pool.extend(string.digits)
            password_chars.append(secrets.choice(string.digits))
        if use_symbols:
            # Using a curated list of common, non-problematic symbols
            symbols = "!@#$%^&*()-_=+"
            char_pool.extend(symbols)
            password_chars.append(secrets.choice(symbols))

        if not char_pool:
            return "" # Return empty if no character sets are selected

        # Fill the rest of the password length
        remaining_length = length - len(password_chars)
        if remaining_length > 0:
            password_chars.extend(secrets.choice(char_pool) for _ in range(remaining_length))

        # Shuffle the list to ensure character positions are random
        secrets.SystemRandom().shuffle(password_chars)

        return "".join(password_chars)

class PasswordAnalyzer:
    """Analyzes password strength and checks for breaches."""

    def calculate_entropy(self, password):
        """Calculates the entropy of a password in bits."""
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
            pool_size += 32 # Common estimate for symbols
        
        if pool_size == 0:
            return 0.0
            
        entropy = len(password) * math.log2(pool_size)
        return round(entropy, 2)

    def get_strength_feedback(self, entropy):
        """Provides a qualitative strength level and color based on entropy."""
        if entropy < 40:
            return "Very Weak", "#e74c3c" # Red
        elif entropy < 60:
            return "Weak", "#f39c12" # Orange
        elif entropy < 80:
            return "Moderate", "#f1c40f" # Yellow
        elif entropy < 100:
            return "Strong", "#27ae60" # Green
        else:
            return "Very Strong", "#2ecc71" # Darker Green

    def check_if_pwned(self, password):
        """
        Checks the password against the 'Have I Been Pwned' database using k-Anonymity.
        The full password is NOT sent over the internet.
        """
        if not password:
            return None, "Password is empty."

        try:
            # 1. Hash the password using SHA-1 (as required by the API)
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix, suffix = sha1_hash[:5], sha1_hash[5:]

            # 2. Query the Pwned Passwords API with the first 5 characters of the hash
            api_url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(api_url, timeout=5)
            response.raise_for_status() # Raise an exception for bad status codes

            # 3. Check the response for the rest of the hash
            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == suffix:
                    return int(count), None # Found a match
            
            return 0, None # No match found
        except requests.RequestException as e:
            return None, f"API request error: {e}"
        except Exception as e:
            return None, f"An unexpected error occurred: {e}"

# --- GUI Application Class ---

class PassPilotApp(tk.Tk):
    """The main application window and GUI logic."""

    def __init__(self, generator, analyzer):
        super().__init__()
        self.generator = generator
        self.analyzer = analyzer

        self.title("PassPilot Pro")
        self.geometry("600x650")
        self.resizable(False, False)

        # Style configuration
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configure(bg="#2c3e50")
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 10))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=10, foreground="#2c3e50")
        self.style.configure("TCheckbutton", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 10))
        self.style.map("TCheckbutton",
            background=[('active', '#34495e')],
            indicatorcolor=[('selected', '#27ae60'), ('!selected', '#bdc3c7')])
        self.style.configure("Generated.TEntry", foreground="#2ecc71", font=("Courier", 12, "bold"))
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        # --- Generator Section ---
        gen_frame = ttk.LabelFrame(main_frame, text="Password Generator", padding="15")
        gen_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(gen_frame, text="Length:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.length_var = tk.IntVar(value=16)
        self.length_scale = ttk.Scale(gen_frame, from_=8, to_=64, orient="horizontal", variable=self.length_var, command=self._update_length_label)
        self.length_scale.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5)
        self.length_label = ttk.Label(gen_frame, text="16", font=("Arial", 10, "bold"))
        self.length_label.grid(row=0, column=3, padx=5)

        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(gen_frame, text="Lowercase (a-z)", variable=self.lower_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        ttk.Checkbutton(gen_frame, text="Uppercase (A-Z)", variable=self.upper_var).grid(row=2, column=0, columnspan=2, sticky="w", pady=5)
        ttk.Checkbutton(gen_frame, text="Numbers (0-9)", variable=self.digits_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=5)
        ttk.Checkbutton(gen_frame, text="Symbols (!@#$%)", variable=self.symbols_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=5)

        self.password_entry = ttk.Entry(gen_frame, font=("Courier", 12), justify="center", style="Generated.TEntry")
        self.password_entry.grid(row=5, column=0, columnspan=4, sticky="ew", pady=10)

        generate_btn = ttk.Button(gen_frame, text="Generate Password", command=self.generate_password_action)
        generate_btn.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5, padx=(0,5))
        copy_btn = ttk.Button(gen_frame, text="Copy to Clipboard", command=self.copy_to_clipboard_action)
        copy_btn.grid(row=6, column=2, columnspan=2, sticky="ew", pady=5, padx=(5,0))

        # --- Analyzer Section ---
        analyzer_frame = ttk.LabelFrame(main_frame, text="Password Strength Analyzer", padding="15")
        analyzer_frame.pack(fill="x", expand=True)

        ttk.Label(analyzer_frame, text="Enter password to analyze:").pack(fill="x", pady=(0, 5))
        self.analyze_entry_var = tk.StringVar()
        self.analyze_entry_var.trace_add("write", self.analyze_password_action)
        self.analyze_entry = ttk.Entry(analyzer_frame, font=("Courier", 12), textvariable=self.analyze_entry_var)
        self.analyze_entry.pack(fill="x", pady=5)
        
        self.strength_bar = ttk.Progressbar(analyzer_frame, orient="horizontal", length=300, mode="determinate")
        self.strength_bar.pack(fill="x", pady=10)
        self.strength_bar_style = ttk.Style()
        self.strength_bar_style.layout("TProgressbar",
            [('Horizontal.Progressbar.trough',
            {'children': [('Horizontal.Progressbar.pbar',
                            {'side': 'left', 'sticky': 'ns'})],
            'sticky': 'nswe'})])
        
        self.feedback_label = ttk.Label(analyzer_frame, text="Enter a password to see feedback.", justify="center", font=("Arial", 11, "bold"))
        self.feedback_label.pack(fill="x", pady=5)

        self.entropy_label = ttk.Label(analyzer_frame, text="Entropy: 0 bits", justify="center")
        self.entropy_label.pack(fill="x", pady=5)
        
        self.pwned_button = ttk.Button(analyzer_frame, text="Check if Exposed in Breach", command=self.check_pwned_action)
        self.pwned_button.pack(fill="x", pady=10)
        self.pwned_result_label = ttk.Label(analyzer_frame, text="", justify="center")
        self.pwned_result_label.pack(fill="x", pady=5)

    def _update_length_label(self, value):
        self.length_label.config(text=f"{int(float(value))}")

    def generate_password_action(self):
        length = self.length_var.get()
        use_lower = self.lower_var.get()
        use_upper = self.upper_var.get()
        use_digits = self.digits_var.get()
        use_symbols = self.symbols_var.get()

        if not any([use_lower, use_upper, use_digits, use_symbols]):
            messagebox.showwarning("Warning", "Please select at least one character set.")
            return

        password = self.generator.generate(length, use_lower, use_upper, use_digits, use_symbols)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        # Also update the analyzer with the new password
        self.analyze_entry.delete(0, tk.END)
        self.analyze_entry.insert(0, password)

    def copy_to_clipboard_action(self):
        password = self.password_entry.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Nothing to copy. Please generate a password first.")

    def analyze_password_action(self, *args):
        password = self.analyze_entry_var.get()
        entropy = self.analyzer.calculate_entropy(password)
        strength_text, color = self.analyzer.get_strength_feedback(entropy)

        self.feedback_label.config(text=strength_text, foreground=color)
        self.entropy_label.config(text=f"Entropy: {entropy} bits")
        
        # Update progress bar
        self.strength_bar['value'] = min(entropy, 120) # Cap at 120 for visual representation
        self.strength_bar_style.configure("TProgressbar", background=color)

        # Clear pwned result on new input
        self.pwned_result_label.config(text="")

    def check_pwned_action(self):
        password = self.analyze_entry.get()
        if not password:
            messagebox.showwarning("Input Needed", "Please enter a password to check.")
            return
            
        self.pwned_result_label.config(text="Checking...", foreground="#ecf0f1")
        self.update_idletasks() # Force UI update

        count, error = self.analyzer.check_if_pwned(password)

        if error:
            self.pwned_result_label.config(text=f"Error: {error}", foreground="#e74c3c")
        elif count > 0:
            msg = f"Oh no! This password was found {count:,} times in data breaches. It is NOT secure!"
            self.pwned_result_label.config(text=msg, foreground="#e74c3c")
        else:
            msg = "Good news! This password was not found in any known data breaches."
            self.pwned_result_label.config(text=msg, foreground="#2ecc71")

# --- Main Execution ---

if __name__ == "__main__":
    password_generator = PasswordGenerator()
    password_analyzer = PasswordAnalyzer()
    app = PassPilotApp(password_generator, password_analyzer)
    app.mainloop()
