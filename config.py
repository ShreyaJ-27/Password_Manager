import os

# Where user vaults will be stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.join(BASE_DIR, "vaults")

# File that stores user info (salt + master hash)
USER_DB_FILE = os.path.join(BASE_DIR, "users.json")

# Clipboard timeout (seconds) for auto-copy
CLIPBOARD_TIMEOUT_SECONDS = 15

# PBKDF2 iterations for key derivation
KDF_ITERATIONS = 390_000