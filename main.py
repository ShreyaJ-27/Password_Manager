# main.py

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

from user_manager import login_or_register
from vault_manager import (
    load_vault,
    save_vault,
    add_entry,
    search_entries,
    find_entry,
    delete_entry,
    rename_service,
    update_password,
    group_by_category,
    update_category,
)
from crypto_utils import encrypt_text, decrypt_text
from password_utils import check_strength, generate_password, copy_to_clipboard_temporarily

console = Console()


CATEGORIES = ["Social", "Email", "Banking", "Work", "Other"]


def choose_category() -> str:
    console.print("\n[bold]Choose a category:[/bold]")
    for i, c in enumerate(CATEGORIES, start=1):
        console.print(f"{i}. {c}")
    console.print(f"{len(CATEGORIES) + 1}. Custom")
    choice = IntPrompt.ask("Enter choice", default=5)
    if 1 <= choice <= len(CATEGORIES):
        return CATEGORIES[choice - 1]
    else:
        return Prompt.ask("Enter custom category").strip() or "Other"


def show_entries_table(entries: list[dict]):
    if not entries:
        console.print("[yellow]No entries to show.[/yellow]")
        return
    table = Table(title="Saved Passwords", show_lines=True)
    table.add_column("#", justify="right")
    table.add_column("Service")
    table.add_column("Username")
    table.add_column("Category")
    table.add_column("Created")
    table.add_column("Updated")

    for idx, e in enumerate(entries, start=1):
        table.add_row(
            str(idx),
            e.get("service", ""),
            e.get("username", ""),
            e.get("category", "Other"),
            e.get("created_at", ""),
            e.get("updated_at", ""),
        )

    console.print(table)


def handle_add_password(vault, fernet):
    console.print(Panel.fit("Add New Password", style="bold green"))

    # Ask for service name
    service = Prompt.ask("Service name (e.g., Gmail, Facebook)").strip()
    if not service:
        console.print("[red]Service name cannot be empty.[/red]")
        return

    # Username/email for the service (optional)
    username_for_service = Prompt.ask(
        "Username/email for this service (optional)", 
        default=""
    ).strip()

    # --- CHOICE: Generate or manually enter ---
    console.print("\n[bold]Choose password entry method:[/bold]")
    console.print("1. Generate a strong password")
    console.print("2. Manually enter a password")

    choice = Prompt.ask(
        "Enter choice (1/2)", 
        choices=["1", "2"], 
        default="1"
    )

    if choice == "1":
        # Generate password automatically
        length = IntPrompt.ask("Password length", default=16)
        password = generate_password(length=length)
        console.print(f"[cyan]Generated password:[/cyan] {password}")

    else:
        # Manual entry with masking
        from getpass import getpass
        password = getpass("Enter password: ")

    # --- Strength Check ---
    label, score, reasons = check_strength(password)
    console.print(f"\nPassword Strength: [bold]{label}[/bold] (score: {score}/5)")
    if reasons:
        console.print("[yellow]Issues: [/yellow]" + ", ".join(reasons))

    # --- Choose Category ---
    category = choose_category()

    # --- Encrypt and Save ---
    enc_password = encrypt_text(password, fernet)

    try:
        add_entry(
            vault,
            service,
            enc_password,
            category,
            username_for_service
        )
        console.print("[green]Password stored successfully![/green]")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        return


def handle_search(vault):
    console.print(Panel.fit("Search Passwords", style="bold cyan"))
    query = Prompt.ask("Search by service name").strip()
    matches = search_entries(vault, query)

    # No results
    if not matches:
        console.print("[yellow]No matching services found.[/yellow]")
        return None

    # Auto-select when exactly one match
    if len(matches) == 1:
        console.print("[green]Only one match found. Auto-selecting it.[/green]")
        return matches[0]

    # Multiple results → show table + ask user to choose
    show_entries_table(matches)
    idx = IntPrompt.ask(
        "Enter # of service to select (0 to cancel)",
        default=0,
    )

    if idx == 0:
        return None

    if 1 <= idx <= len(matches):
        return matches[idx - 1]

    console.print("[red]Invalid selection.[/red]")
    return None

def handle_retrieve_password(vault, fernet):
    console.print(Panel.fit("Retrieve Password", style="bold magenta"))
    entry = handle_search(vault)
    if not entry:
        return
    token = entry.get("password")
    try:
        plain = decrypt_text(token, fernet)
    except Exception:
        console.print("[red]Failed to decrypt password. Wrong key or corrupted data.[/red]")
        return

    # Auto-copy to clipboard instead of printing
    copy_to_clipboard_temporarily(plain)


def handle_edit_password(vault, fernet):
    console.print(Panel.fit("Edit Password", style="bold blue"))
    entry = handle_search(vault)
    if not entry:
        return
    service = entry["service"]

    from getpass import getpass
    new_password = getpass("Enter new password: ")
    label, score, reasons = check_strength(new_password)
    console.print(f"Password Strength: [bold]{label}[/bold] (score: {score}/5)")
    if reasons:
        console.print("Issues: " + ", ".join(reasons))

    enc_password = encrypt_text(new_password, fernet)
    update_password(vault, service, enc_password)
    console.print("[green]Password updated successfully.[/green]")


def handle_rename_service(vault):
    console.print(Panel.fit("Rename Service", style="bold blue"))
    entry = handle_search(vault)
    if not entry:
        return
    old_name = entry["service"]
    new_name = Prompt.ask(f"Enter new name for service '{old_name}'").strip()
    if not new_name:
        console.print("[yellow]Name cannot be empty.[/yellow]")
        return
    try:
        rename_service(vault, old_name, new_name)
        console.print("[green]Service renamed successfully.[/green]")
    except KeyError as e:
        console.print(f"[red]{e}[/red]")


def handle_delete_entry(vault):
    console.print(Panel.fit("Delete Password", style="bold red"))
    entry = handle_search(vault)
    if not entry:
        return
    service = entry["service"]
    from rich.prompt import Confirm
    confirm = Confirm.ask(f"Are you sure you want to delete '{service}'?", default=False)
    if not confirm:
        console.print("[yellow]Deletion cancelled.[/yellow]")
        return
    try:
        delete_entry(vault, service)
        console.print("[green]Entry deleted.[/green]")
    except KeyError as e:
        console.print(f"[red]{e}[/red]")


def handle_list_by_category(vault):
    console.print(Panel.fit("Passwords by Category", style="bold cyan"))
    grouped = group_by_category(vault)
    if not grouped:
        console.print("[yellow]No passwords saved yet.[/yellow]")
        return
    for category, entries in grouped.items():
        console.print(Panel.fit(f"Category: [bold]{category}[/bold]", style="bold"))
        show_entries_table(entries)


def main_menu():
    console.print(Panel.fit("Simple Password Manager", style="bold green"))
    console.print("1. Add new password")
    console.print("2. Retrieve password")
    console.print("3. Search passwords")
    console.print("4. List passwords by category")
    console.print("5. Edit password")
    console.print("6. Rename service")
    console.print("7. Delete password")
    console.print("8. Exit")

    choice = Prompt.ask("Enter choice", choices=[str(i) for i in range(1, 9)], default="8")
    return choice


def main():
    username, fernet = login_or_register()
    vault = load_vault(username)

    while True:
        choice = main_menu()
        if choice == "1":
            handle_add_password(vault, fernet)
        elif choice == "2":
            handle_retrieve_password(vault, fernet)
        elif choice == "3":
            handle_search(vault)  # just search; retrieval/edit uses this too
        elif choice == "4":
            handle_list_by_category(vault)
        elif choice == "5":
            handle_edit_password(vault, fernet)
        elif choice == "6":
            handle_rename_service(vault)
        elif choice == "7":
            handle_delete_entry(vault)
        elif choice == "8":
            console.print("[cyan]Goodbye![/cyan]")
            break

        save_vault(username, vault)


if __name__ == "__main__":
    main()