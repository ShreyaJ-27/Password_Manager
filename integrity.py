# integrity.py

import hashlib
import os

from rich.console import Console

console = Console()


def _sig_path(path: str) -> str:
    return path + ".sig"


def write_integrity(path: str) -> None:
    if not os.path.exists(path):
        return
    with open(path, "rb") as f:
        data = f.read()
    digest = hashlib.sha256(data).hexdigest()
    with open(_sig_path(path), "w", encoding="utf-8") as f:
        f.write(digest)


def verify_integrity(path: str) -> bool:
    if not os.path.exists(path) or not os.path.exists(_sig_path(path)):
        return True  # Nothing to verify yet
    with open(path, "rb") as f:
        data = f.read()
    actual = hashlib.sha256(data).hexdigest()
    with open(_sig_path(path), "r", encoding="utf-8") as f:
        stored = f.read().strip()
    ok = (actual == stored)
    if not ok:
        console.print("[red]Warning: vault integrity check failed. File may be tampered or corrupted.[/red]")
    return ok
