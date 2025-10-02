# 🔐 PassPilot 

### The Ultimate Password Security Toolkit

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional-grade password management application featuring military-grade password generation, advanced security analysis, and a beautiful modern UI with dark/light themes[web:7][web:10].

![PassPilot  Demo](docs/demo.gif)
*Screenshot placeholder - Add actual screenshots here*

---

## ✨ Features

### 🎲 Advanced Password Generation
- **Cryptographically secure** password generation using Python's `secrets` module
- **6 intelligent presets**: Balanced, Maximum Security, Memorable, PIN, Alphanumeric, and Paranoid
- **Passphrase generator** with customizable word count and separators
- **Exclude ambiguous characters** option (0, O, I, l, 1, |)
- Length range from 4 to 128 characters

### 🔍 Real-Time Analysis
- **Shannon entropy calculation** with pool-based and character-frequency metrics
- **Advanced strength visualization** with 8-level color-coded progress bar
- **Pattern detection** for common weak sequences (123, abc, qwerty, etc.)
- **Crack time estimation** using modern GPU attack rates (100B guesses/sec)
- **Intelligent suggestions** for password improvement

### 🌐 Security Features
- **Have I Been Pwned integration** using k-anonymity API (no full password sent)
- **Secure clipboard management** with 30-second auto-clear
- **Session-only password history** (never written to disk)
- **Password masking toggle** for privacy

### 🎨 Modern Interface
- **Glassmorphic UI design** with smooth animations
- **Dark and light themes** with instant switching
- **Tabbed interface**: Generator, Analyzer, and History
- **Responsive layout** with keyboard shortcuts for power users

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Usage](#-usage)
- [Keyboard Shortcuts](#%EF%B8%8F-keyboard-shortcuts)
- [Dependencies](#-dependencies)
- [Security Considerations](#-security-considerations)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Steps

1. **Clone the repository**
```

git clone https://github.com/rootpom/passpilot.git
cd passpilot

```

2. **Install required dependencies**
```

pip install -r requirements.txt

```

3. **Run the application**
```

python passpilot.py

```

### Alternative: Create a Virtual Environment (Recommended)

```


# Create virtual environment

python -m venv venv

# Activate it

# On Windows:

venv\Scripts\activate

# On macOS/Linux:

source venv/bin/activate

# Install dependencies

pip install -r requirements.txt

# Run the application

python passpilot.py

```

---

## 💻 Usage

### Quick Start

1. **Generate a Password**
   - Select a preset or customize character options
   - Adjust length using the slider (4-128 characters)
   - Click "Generate Password" or press `Ctrl+G`

2. **Analyze Password Strength**
   - Switch to the "Analyzer" tab
   - Enter or paste any password
   - View real-time strength metrics, entropy, and suggestions
   - Click "Check if Exposed in Data Breach" to verify against HIBP database

3. **View History**
   - Access the "History" tab to see all generated passwords in current session
   - Copy any previous password to clipboard
   - Export history to JSON for backup

### Example: Generate Maximum Security Password

```


# The application uses this logic internally:

from passpilot import AdvancedPasswordGenerator

generator = AdvancedPasswordGenerator()
password = generator.generate(
length=32,
use_lower=True,
use_upper=True,
use_digits=True,
use_symbols=True,
exclude_ambiguous=False
)
print(password)

# Output: 'K9\$mP2\#xL@nV4wQ8*zR7\&hT5!yU3^dF1'

```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+G` | Generate new password |
| `Ctrl+P` | Generate passphrase |
| `Ctrl+C` | Copy password to clipboard |
| `F1` | Show help dialog |

---

## 📦 Dependencies

Create a `requirements.txt` file with:

```

requests>=2.31.0

```

**Built-in modules used:**
- `tkinter` (included with Python)
- `secrets` (cryptographically secure random generation)
- `hashlib` (SHA-1 hashing for HIBP API)
- `threading` (non-blocking API calls)

---

## 🔒 Security Considerations

### What We Do
✅ Use `secrets` module for cryptographically secure random generation  
✅ Implement k-anonymity when checking Have I Been Pwned (only first 5 chars of hash sent)  
✅ Store passwords in memory only (never written to disk)  
✅ Auto-clear clipboard after 30 seconds  
✅ Calculate true Shannon entropy for strength assessment  

### What We Don't Do
❌ Never store passwords permanently  
❌ Never send full passwords over the network  
❌ Never log sensitive information  
❌ No telemetry or analytics  

### Best Practices for Users
- Use generated passwords with **at least 16 characters**
- Enable **Maximum Security** preset for critical accounts
- Always check if password has been **exposed in breaches**
- Use a **password manager** to store generated passwords securely
- Never reuse passwords across different services

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Setup

```


# Clone your fork

git clone https://github.com/rootpom/passpilot.git

# Install development dependencies

pip install -r requirements-dev.txt

# Run tests (if available)

python -m pytest tests/

# Format code

black passpilot.py

```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Have I Been Pwned API** by Troy Hunt for breach checking
- **Zxcvbn** algorithm inspiration for strength estimation
- Python **Tkinter** community for UI guidance
- **XKCD #936** for passphrase generation concepts

---

## 📞 Contact & Support

- **Author**: Rupam Ghosh
- **GitHub**: [@rootpom](https://github.com/rootpom)
- **Issues**: [Report a bug](https://github.com/rootpom/passpilot/issues)
- **Email**: your.email@example.com

---

## 🗺️ Roadmap

- [ ] Add password strength history tracking
- [ ] Implement password policy checker
- [ ] Add multi-language support
- [ ] Create browser extension version
- [ ] Add password manager integration (1Password, Bitwarden)
- [ ] Implement two-factor authentication code generator

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/rootpom/passpilot?style=social)
![GitHub forks](https://img.shields.io/github/forks/rootpom/passpilot?style=social)
![GitHub issues](https://img.shields.io/github/issues/rootpom/passpilot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/rootpom/passpilot)

---

<p align="center">Made with ❤️ and Python | © 2025 PassPilot </p>