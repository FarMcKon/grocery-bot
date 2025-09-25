#!/usr/bin/env python3
"""
Storage Module Test Tool for Grocery Bot
Small CLI to sanity-check `storage.py` types and Database wiring
without touching any unfinished SQLite code.
"""

import uuid
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Import the storage module we want to test
from storage import Database  # , UserType, ListType, SmsTransaction

console = Console()


def _show_header():
    console.print("-" * 60)


@click.group()
def cli():
    """Storage Test Tool for Grocery Bot"""
    console.print(Panel.fit("📦 Grocery Bot Storage Tester", style="bold blue"))


@cli.command()
@click.option(
    "--db_file", "-f", default="grocery_bot_tinydb.json", help="Tiny DB file to work on"
)
@click.option("--ugrade", "-u", default=False, help="Upgrade, don't create new DB")
@click.option("--create", "-c", default=False, help="CReate a new DB")
@click.option(
    "--force", "-f", default=False, help="Force create or upgrade (dangerous)"
)
def db_init(db_file, ugrade, create, force=False):
    """Initialize or upgrade the database."""
    _show_header()
    console.print("[bold]Database Init[/bold]")
    try:
        db = Database(db_path=db_file, db_type="tiny_db")
    #     console.print("Initialized Database(db_type='tiny_db') ✓")
    #     console.print(f"db_path: {db.db_path}")
    except Exception as e:
        console.print(f"[red]Failed to initialize Database:[/red] {e}")


@cli.command()
@click.option("--name", "-n", default="John Doe", help="New User Name")
@click.option("--phone", "-p", default="+15551234567", help="New User Phone Number")
@click.option("--email", "-e", default="user@example.com", help="New User Email")
def create_user(name, phone, email):
    """Create a new user."""
    db_file = "grocery_bot_tinydb.json"
    _show_header()
    console.print("[bold]Create User[/bold]")
    try:
        db = Database(db_path=db_file, db_type="tiny_db")
        user_payload = {"name": name, "phone_number": phone, "email": email}
        db.upsert_user(user_payload)
    except Exception as e:
        console.print(f"[red]Failed to create user:[/red] {e}")


@cli.command()
@click.option(
    "--phone",
    "-p",
    default="+15551234567",
    help="User to create the list for, by Phone Number",
)
@click.option("--list_name", "-l", default="Groceries", help="New List Name")
def upsert_list(phone, list_name):
    """Create a list for a user by phone number."""
    db_file = "grocery_bot_tinydb.json"
    user_id = None
    _show_header()
    console.print("[bold]Create User[/bold]")

    # get our user's ID
    try:
        db = Database(db_path=db_file, db_type="tiny_db")
        search_by = {"phone_number": phone}
        user_id = db.get_user_id(search_by)
    except Exception as e:
        console.print(f"[red]Failed to find user:[/red] {e}")

    # create our list
    try:
        list_payload = {"name": list_name, "owner_id": user_id}
        db.upsert_list(list_payload)
    except Exception as e:
        console.print(f"[red]Failed to create list:[/red] {e}")


@cli.command()
@click.option(
    "--phone",
    "-p",
    default="+15551234567",
    help="User to create the list for, by Phone Number",
)
# @click.option('--list_name', '-l', default='Groceries', help='New List Name')
@click.option(
    "--item", "-i", default="Milk", help="Text of item to add to the default List"
)
def add_item(phone, item):
    """Add an item to a list for a user by phone number."""
    db_file = "grocery_bot_tinydb.json"
    list_name = "Groceries"
    user_id = None
    _show_header()
    console.print("[bold]Add to List[/bold]")

    # get our user's ID
    try:
        db = Database(db_path=db_file, db_type="tiny_db")
        search_by = {"phone_number": phone}
        user_id = db.get_user_id(search_by)
    except Exception as e:
        console.print(f"[red]Failed to find user:[/red] {e}")

    # fetch default / active list
    try:
        list_payload = {"name": list_name, "owner_id": user_id}
        list_dict = db.get_list(list_payload)
    except Exception as e:
        console.print(f"[red]Failed to find list:[/red] {e}")

    ## add item to the the litems list in the list object
    import pdb

    pdb.set_trace()
    if list_dict.get("items"):
        list_dict["items"].append(item)
    else:
        list_dict["items"] = [item]

    try:
        db.upsert_list(list_dict)
    except Exception as e:
        console.print(f"[red]Failed to create list:[/red] {e}")


@cli.command()
@click.option("--phone", "-p", default="+15551234567", help="New User Phone Number")
@click.option(
    "--list_name", "-n", default="Groceries", help="Name of the list to clear"
)
def clear(phone, list_name):
    """Clear a list of all items"""
    # FUTURE: Make this an archive action
    db_file = "grocery_bot_tinydb.json"
    user_id = None
    _show_header()
    console.print(f"[bold]Clear List {list_name} [/bold]")

    # get our user's ID
    try:
        db = Database(db_path=db_file, db_type="tiny_db")
        search_by = {"phone_number": phone}
        user_id = db.get_user_id(search_by)
    except Exception as e:
        console.print(f"[red]Failed to find user:[/red] {e}")

    # fetch default / active list
    try:
        list_payload = {"name": list_name, "owner_id": user_id}
        list_dict = db.get_list(list_payload)
    except Exception as e:
        console.print(f"[red]Failed to find list:[/red] {e}")

    ## add item to the the litems list in the list object
    list_clone_dict = list_dict.copy()
    list_dict["archived_on"] = datetime.now().isoformat()
    line_clone["items"] = None
    import pdb

    pdb.set_trace()
    try:
        # save the 'empty' clone, mark the old list as archived
        db.upsert_list(list_dict)
        db.upsert_list(list_clone_dict)
    except Exception as e:
        console.print(f"[red]Failed to clear (and archive old) list:[/red] {e}")


# @cli.command()
# def status():
#     """Show basic storage module status."""
#     _show_header()
#     console.print("[bold]Import & Types[/bold]")
#     table = Table(title="Storage Types", show_header=True, header_style="bold magenta")
#     table.add_column("Type", style="cyan", no_wrap=True)
#     table.add_column("OK?", style="green")

#     try:
#         _ = UserType("user_1", "+15551234567", "user@example.com", "Test User", datetime.now().isoformat())
#         table.add_row("UserType", "✓")
#     except Exception as e:
#         table.add_row("UserType", f"❌ {e}")

#     try:
#         lt = ListType("list_1", "My List", "user_1")
#         lt.add_item("apples")
#         table.add_row("ListType", "✓")
#     except Exception as e:
#         table.add_row("ListType", f"❌ {e}")

#     try:
#         _ = SmsTransaction(
#             transaction_id="txn_1",
#             user_id="user_1",
#             phone_number="+15551234567",
#             message_content="hello",
#             direction="inbound",
#             timestamp=datetime.now().isoformat(),
#             processed=False,
#             list_id="list_1",
#         )
#         table.add_row("SmsTransaction", "✓")
#     except Exception as e:
#         table.add_row("SmsTransaction", f"❌ {e}")

#     console.print(table)

#     _show_header()
#     console.print("[bold]Database Init[/bold]")
#     try:
#         db = Database(db_path="grocery_bot.json", db_type="tiny_db")
#         console.print("Initialized Database(db_type='tiny_db') ✓")
#         console.print(f"db_path: {db.db_path}")
#     except Exception as e:
#         console.print(f"[red]Failed to initialize Database:[/red] {e}")


# @cli.command()
# def smoke():
#     """Run a lightweight smoke test of the storage layer."""
#     _show_header()
#     console.print("[bold]Construct example objects[/bold]")

#     user_id = f"user_{uuid.uuid4().hex[:8]}"
#     list_id = f"list_{uuid.uuid4().hex[:8]}"
#     txn_id = f"txn_{uuid.uuid4().hex[:8]}"

#     try:
#         user = UserType(
#             user_id=user_id,
#             phone_number="+15550001111",
#             email="demo@example.com",
#             name="Demo User",
#             last_active=datetime.now().isoformat(),
#         )
#         console.print(f"UserType: id={user.user_id} phone={user.phone_number}")
#     except Exception as e:
#         console.print(f"[red]UserType creation failed:[/red] {e}")

#     try:
#         glist = ListType(list_id=list_id, name="Demo List", owner_id=user_id)
#         glist.add_item("milk")
#         glist.add_item("bread")
#         console.print(f"ListType: id={glist.list_id} name={glist.name} entries={glist.entries}")
#     except Exception as e:
#         console.print(f"[red]ListType creation failed:[/red] {e}")

#     try:
#         txn = SmsTransaction(
#             transaction_id=txn_id,
#             user_id=user_id,
#             phone_number="+15550001111",
#             message_content="add eggs",
#             direction="inbound",
#             timestamp=datetime.now().isoformat(),
#             processed=False,
#             list_id=list_id,
#         )
#         console.print(
#             f"SmsTransaction: id={txn.transaction_id} dir={txn.direction} phone={txn.phone_number} msg='{txn.message_content}'"
#         )
#     except Exception as e:
#         console.print(f"[red]SmsTransaction creation failed:[/red] {e}")

#     _hr()
#     console.print("[bold]Database smoke[/bold]")
#     try:
#         db = Database(db_path="grocery_bot.json", db_type="tiny_db")
#         console.print("Database object created ✓ (tiny_db mode)")
#     except Exception as e:
#         console.print(f"[red]Database init failed:[/red] {e}")


if __name__ == "__main__":
    cli()
