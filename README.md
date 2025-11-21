# Password_Manager
🔐 Advanced Password Manager (Modular Python Project)

This is a secure, terminal-based Password Manager built with Python and designed using a modular architecture.
It supports encrypted password storage, password strength checking, password generation, multi-user vaults, auto-lock, and file integrity verification.

The project is built using 7 separate Python modules for clean structure and maintainability.

⭐ Features
Security Features

- Strong Encryption (PBKDF2 + Fernet)
Your master password derives a cryptographic key using PBKDF2, ensuring industry-grade protection.

- Password Strength Checker
Evaluates password strength (Weak, Medium, Strong) before saving.

- Password Generator
Automatically generate strong random passwords with length and symbol options.

- Master Password Verification
The master password is never stored — only a secure PBKDF2 hash is saved.

- Auto-Lock After Inactivity
If the user is idle (default: 120 seconds), the vault auto-locks and requires re-authentication.

- Multiple Users / Multiple Vaults
Each username gets their own encrypted vault file inside .vaults/.

- File Integrity Check (HMAC)
Detects if the vault file was tampered with or corrupted.

📁 Folder Structure
password_manager/
│
├── main.py              # Entry point of the application (run this)
├── crypto_utils.py      # Key derivation, hashing, encryption/decryption
├── user_manager.py      # Login, vault creation, auto-lock logic
├── vault_manager.py     # Store/retrieve passwords, manage vault
├── integrity.py         # HMAC-based file integrity verification
├── password_utils.py    # Password generator + strength checker
├── config.py            # Config constants (vault dir, timings, iterations)
└── .vaults/             # Auto-created folder containing encrypted vaults


Each file handles a specific responsibility, making the project scalable and easy to maintain.

🛠 Installation
1. Clone or download the project

Place the folder anywhere on your system.

Example:

Desktop/
└── Password_Manager/

2. Install dependencies

Make sure Python 3.8+ is installed.

In your terminal or command prompt:

pip install cryptography

▶️ How to Start the Project
Step 1 — Navigate to your project folder

Example:

cd C:\Users\YourName\Desktop\Password_Manager

Verify files:
dir   

You should see:

main.py
crypto_utils.py
user_manager.py
vault_manager.py
integrity.py
password_utils.py
config.py

Step 2 — Run the application
python main.py


🚀 First Run Experience
1. You will be asked for a username:
Enter username: arpit

2. If this is a new user, the manager will:

Create a salt

Ask you to set a master password

Create your encrypted vault inside .vaults/arpit.json

You will see:

Vault created successfully.

3. Main Menu
MENU
1. Add new password
2. Retrieve password
3. Generate + Store strong password
4. List services
5. Exit


Everything is encrypted inside your vault file.

🔒 Vault Location

Every user gets their own vault file:

.password_manager/.vaults/
│
└── arpit.json


This file contains:

Encrypted passwords

Salt

Master password hash

HMAC integrity tag

Your actual passwords are never stored in plain text.

🔥 Important Security Behavior
❌ If the user forgets their master password:

Data cannot be recovered.

This is intentional and correct — no backdoors exist.

💡 Future Improvements (Optional)

You can extend this project with:

Recovery keys

Biometric unlock (desktop)

Cloud-encrypted sync

GUI using Tkinter or PyQt

Export/import backup vaults

Browser extension integration
