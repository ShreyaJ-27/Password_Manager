# crypto_utils.py

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from config import KDF_ITERATIONS


def generate_salt(length: int = 16) -> bytes:
    return os.urandom(length)


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 32-byte key from the master password using PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend(),
    )
    key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(key)


def get_fernet_from_password(password: str, salt: bytes) -> Fernet:
    key = derive_key(password, salt)
    return Fernet(key)


def encrypt_text(plain_text: str, fernet: Fernet) -> str:
    token = fernet.encrypt(plain_text.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_text(token: str, fernet: Fernet) -> str:
    plain = fernet.decrypt(token.encode("utf-8"))
    return plain.decode("utf-8")
