# password_utils.py

import string
import random
import threading
import time

import pyperclip
from rich.console import Console

from config import CLIPBOARD_TIMEOUT_SECONDS

console = Console()


def check_strength(password: str) -> tuple[str, int, list[str]]:
    """
    Returns (label, score, reasons)
    Score 0-5
    """
    score = 0
    reasons = []

    length = len(password)
    if length >= 12:
        score += 1
    else:
        reasons.append("Length < 12")

    if any(c.islower() for c in password):
        score += 1
    else:
        reasons.append("No lowercase letters")

    if any(c.isupper() for c in password):
        score += 1
    else:
        reasons.append("No uppercase letters")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        reasons.append("No digits")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        reasons.append("No symbols")

    if score <= 2:
        label = "Weak"
    elif score == 3 or score == 4:
        label = "Medium"
    else:
        label = "Strong"

    return label, score, reasons


def generate_password(
    length: int = 16,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    chars = ""
    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation

    if not chars:
        raise ValueError("At least one character set must be enabled")

    return "".join(random.choice(chars) for _ in range(length))


def _clear_clipboard_later(delay: int):
    time.sleep(delay)
    pyperclip.copy("")


def copy_to_clipboard_temporarily(text: str, seconds: int = CLIPBOARD_TIMEOUT_SECONDS):
    pyperclip.copy(text)
    console.print(f"[green]Password copied to clipboard for {seconds} seconds.[/green]")
    t = threading.Thread(target=_clear_clipboard_later, args=(seconds,), daemon=True)
    t.start()
