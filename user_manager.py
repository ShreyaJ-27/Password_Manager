# user_manager.py

import json
import os
from getpass import getpass
import base64

from rich.console import Console
from rich.prompt import Prompt, Confirm

from config import USER_DB_FILE
from crypto_utils import generate_salt, derive_key, get_fernet_from_password

console = Console()


def _load_users() -> dict:
    if not os.path.exists(USER_DB_FILE):
        return {}
    with open(USER_DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_users(users: dict) -> None:
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def _create_user(username: str):
    console.print(f"[cyan]Creating new user:[/cyan] {username}")
    while True:
        master_password = getpass("Create a master password: ")
        confirm = getpass("Confirm master password: ")
        if master_password != confirm:
            console.print("[red]Passwords do not match. Try again.[/red]")
            continue
        if len(master_password) < 6:
            console.print("[yellow]Master password is short. Consider using 6+ characters.[/yellow]")
        break

    salt = generate_salt()
    derived_key = derive_key(master_password, salt)
    master_hash = base64.b64encode(derived_key).decode("utf-8")  # store hash safely
    salt_b64 = base64.b64encode(salt).decode("utf-8")

    users = _load_users()
    users[username] = {
        "salt": salt_b64,
        "master_hash": master_hash,
    }
    _save_users(users)

    console.print("[green]User created successfully![/green]")
    fernet = get_fernet_from_password(master_password, salt)
    return username, fernet


def login_or_register() -> tuple[str, object]:
    """
    Login or register a user.
    Returns: (username, fernet)
    """
    users = _load_users()
    username = Prompt.ask("Enter username").strip()

    if username not in users:
        create = Confirm.ask(f"User '{username}' not found. Do you want to create it?", default=True)
        if not create:
            raise SystemExit("Exiting.")
        return _create_user(username)

    # Existing user - authenticate
    record = users[username]
    salt = base64.b64decode(record["salt"])
    stored_hash = record["master_hash"]

    for _ in range(3):
        master_password = getpass("Enter master password: ")
        derived_key = derive_key(master_password, salt)
        candidate_hash = base64.b64encode(derived_key).decode("utf-8")
        if candidate_hash == stored_hash:
            console.print("[green]Login successful![/green]")
            fernet = get_fernet_from_password(master_password, salt)
            return username, fernet
        else:
            console.print("[red]Incorrect master password.[/red]")

    raise SystemExit("Too many failed attempts. Exiting.")
