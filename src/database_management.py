# database_management.py
# Database creation, opening, and selection utilities for SQL Desk.
# Author: Théo Giani (2025)

import os
from tkinter import filedialog, simpledialog

import global_vars
from utils import save_recent_files, display_result
from GUI_functions import refresh_db_file_menu



def menu_open_database(output_textbox, window=None, db_menu=None):
    """
    Open an existing SQLite database file and set it as the current database.
    If a menu widget is supplied, the 'Recent Databases' section can be
    refreshed immediately by the caller.
    """
    filepath = filedialog.askopenfilename(
        title="Open Database",
        filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")],
    )
    if filepath:
        choose_database(
            filepath,
            output_textbox=output_textbox,
            window=window,
            db_menu=db_menu,
        )
    return None


def create_new_database(output_textbox, window=None, db_menu=None):
    """
    Prompt the user for a new database name and create the corresponding
    '.db' file in the working directory.
    """
    name = simpledialog.askstring(
        "New Database", "Enter name for new database (without .db):"
    )
    if name:
        filename = f"{name}.db"
        with open(filename, "w"):
            # Touch the file to create an empty SQLite container.
            # The file will be initialised by sqlite3 on first connection.
            pass

        global_vars.current_database = filename
        display_result(output_textbox, f"Created new database: {filename}")

        # Add to the recent DB list (deduplicated and trimmed to 10 items).
        recent = global_vars.recent_db_files
        recent.insert(0, filename)
        recent = list(dict.fromkeys(recent))[:10]
        global_vars.recent_db_files = recent
        save_recent_files("recent_db_files.txt", recent)

        # Optionally refresh the menu in the UI.
        if db_menu is not None:
            refresh_db_file_menu(db_menu, output_textbox, window)

    return None


def choose_database(value, *, output_textbox=None, window=None, db_menu=None):
    """
    Select an existing database file, update window title, notify the user,
    and update the recent database list. If a menu is provided, its 'Recent
    Databases' section is refreshed as well.
    """
    if not os.path.exists(value):
        if output_textbox:
            display_result(output_textbox, f"File not found: {value}")
        if value in global_vars.recent_db_files:
            global_vars.recent_db_files.remove(value)
            save_recent_files(
                "recent_db_files.txt", global_vars.recent_db_files
            )
        return None

    global_vars.current_database = value

    if output_textbox:
        name = os.path.basename(value)
        display_result(output_textbox, f"Database selected: {name}")
    if window:
        window.title(f"SQL Desk – {value}")

    # Update the recent DB list (deduplicated and trimmed to 10 items).
    recent = global_vars.recent_db_files
    recent.insert(0, value)
    recent = list(dict.fromkeys(recent))[:10]
    global_vars.recent_db_files = recent
    save_recent_files("recent_db_files.txt", recent)

    # Optionally refresh the 'Recent Databases' menu section.
    if db_menu is not None:
        refresh_db_file_menu(db_menu, output_textbox, window)

    return None


##def refresh_db_file_menu(db_menu, output_textbox, window=None):
##    """
##    Rebuild the Database menu, including static entries and the list of recent
##    databases. Note: this function currently wires UI callbacks (lambdas) and
##    will be refactored to keep UI concerns in sql_desk.py.
##    """
##    db_menu.delete(0, "end")
##
##    db_menu.add_command(
##        label="Open Database...",
##        command=lambda: menu_open_database(
##            output_textbox, window, db_menu
##        ),
##    )
##    db_menu.add_command(
##        label="Create New Database...",
##        command=lambda: create_new_database(
##            output_textbox, window, db_menu
##        ),
##    )
##    db_menu.add_separator()
##
##    for i, filename in enumerate(global_vars.recent_db_files, start=1):
##        short = os.path.basename(filename)
##        db_menu.add_command(
##            label=f"{i}. {short}",
##            command=lambda filename=filename: choose_database(
##                filename,
##                output_textbox=output_textbox,
##                window=window,
##                db_menu=db_menu,
##            ),
##        )
##    return None

# --- Recent DB files logic (no UI here) ---

def add_recent_db_file(filename: str):
    """
    Add a database file to the recent list, avoiding duplicates and
    keeping a maximum of N entries. Also updates the saved file list.
    """
    if filename in global_vars.recent_db_files:
        global_vars.recent_db_files.remove(filename)

    global_vars.recent_db_files.insert(0, filename)

    # Limit size of the recent list
    max_recent = 10
    if len(global_vars.recent_db_files) > max_recent:
        global_vars.recent_db_files = global_vars.recent_db_files[:max_recent]

    # Save to text file
    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
    return None

