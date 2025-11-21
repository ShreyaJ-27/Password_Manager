# vault_manager.py

import json
import os
from datetime import datetime

from rich.console import Console

from config import VAULT_DIR
from integrity import write_integrity, verify_integrity

console = Console()


def _vault_path(username: str) -> str:
    os.makedirs(VAULT_DIR, exist_ok=True)
    return os.path.join(VAULT_DIR, f"{username}.json")


def load_vault(username: str) -> dict:
    path = _vault_path(username)
    if not os.path.exists(path):
        return {"version": 1, "entries": []}

    verify_integrity(path)

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            console.print("[red]Vault file is corrupted. Starting with an empty vault.[/red]")
            return {"version": 1, "entries": []}

    if "entries" not in data:
        data["entries"] = []
    return data


def save_vault(username: str, vault: dict) -> None:
    path = _vault_path(username)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(vault, f, indent=2)
    write_integrity(path)


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def find_entry(vault: dict, service_name: str) -> dict | None:
    target = service_name.lower()
    for entry in vault.get("entries", []):
        if entry.get("service", "").lower() == target:
            return entry
    return None


def search_entries(vault: dict, query: str) -> list[dict]:
    q = query.lower()
    return [e for e in vault.get("entries", []) if q in e.get("service", "").lower()]


def add_entry(vault: dict, service: str, enc_password: str, category: str | None, username_for_service: str | None):
    existing = find_entry(vault, service)
    if existing:
        raise ValueError("Service already exists. Use edit options instead.")

    entry = {
        "service": service,
        "username": username_for_service or "",
        "category": category or "Other",
        "password": enc_password,
        "created_at": _now(),
        "updated_at": _now(),
    }
    vault["entries"].append(entry)


def update_password(vault: dict, service: str, enc_password: str):
    entry = find_entry(vault, service)
    if not entry:
        raise KeyError("Service not found")
    entry["password"] = enc_password
    entry["updated_at"] = _now()


def rename_service(vault: dict, old_service: str, new_service: str):
    entry = find_entry(vault, old_service)
    if not entry:
        raise KeyError("Service not found")
    entry["service"] = new_service
    entry["updated_at"] = _now()


def update_category(vault: dict, service: str, category: str):
    entry = find_entry(vault, service)
    if not entry:
        raise KeyError("Service not found")
    entry["category"] = category
    entry["updated_at"] = _now()


def delete_entry(vault: dict, service: str):
    entries = vault.get("entries", [])
    target = service.lower()
    new_entries = [e for e in entries if e.get("service", "").lower() != target]
    if len(new_entries) == len(entries):
        raise KeyError("Service not found")
    vault["entries"] = new_entries


def group_by_category(vault: dict) -> dict[str, list[dict]]:
    grouped = {}
    for e in vault.get("entries", []):
        cat = e.get("category") or "Other"
        grouped.setdefault(cat, []).append(e)
    return grouped
