# database_management.py
# Database creation, opening, and selection utilities for SQL Desk.
# Author: Théo Giani (2025)

import os, sqlite3

from tkinter import filedialog, simpledialog

import global_vars
from utils import save_recent_files, display_result
#from GUI_functions import refresh_db_file_menu



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


##def create_new_database(output_textbox, window=None, db_menu=None):
##    """
##    Prompt the user for a new database name and create the corresponding
##    '.db' file in the working directory.
##    """
##    name = simpledialog.askstring(
##        "New Database", "Enter name for new database (without .db):"
##    )
##    if name:
##        filename = f"{name}.db"
##        with open(filename, "w"):
##            # Touch the file to create an empty SQLite container.
##            # The file will be initialised by sqlite3 on first connection.
##            pass
##
##        global_vars.current_database = filename
##        display_result(output_textbox, f"Created new database: {filename}")
##
##        # Add to the recent DB list (deduplicated and trimmed to 10 items).
##        recent = global_vars.recent_db_files
##        recent.insert(0, filename)
##        recent = list(dict.fromkeys(recent))[:10]
##        global_vars.recent_db_files = recent
##        save_recent_files("recent_db_files.txt", recent)
##
##        # Optionally refresh the menu in the UI.
##        if db_menu is not None:
##            refresh_db_file_menu(db_menu, output_textbox, window)
##
##    return None


##def create_new_database(output_textbox, window=None, db_menu=None):
##    """
##    Prompt for a new database name, create the .db file, then select and open it.
##    No GUI refresh here; the GUI will refresh the menu after calling this.
##    """
##    name = simpledialog.askstring(
##        "New Database", "Enter name for new database (without .db):"
##    )
##    if not name:
##        return None
##
##    filename = f"{name}.db"
##    with open(filename, "w"):
##        # Touch the file; sqlite will initialize it on first connection.
##        pass
##
##    # Open immediately via the single-connection flow.
##    # choose_database will:
##    # - close any existing connection,
##    # - open the new one,
##    # - set global_vars.current_database/current_connection,
##    # - update recent_db_files and save them,
##    # - update the window title (if provided).
##    choose_database(
##        filename,
##        output_textbox=output_textbox,
##        window=window,
##        db_menu=None  # GUI will refresh the menu afterwards
##    )
##    return None

def create_new_database(output_textbox, window=None, db_menu=None):
    """
    Create a new SQLite database in a user-chosen directory.
    The file is created empty, then opened immediately via choose_database().
    The GUI is responsible for refreshing the menu afterwards.
    """
    filepath = filedialog.asksaveasfilename(
        title="Create New Database",
        defaultextension=".db",
        filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
    )

    if not filepath:
        # User cancelled the dialog
        display_result(output_textbox, "Database creation cancelled.")
        return None

    # Create the file if it does not exist yet
    try:
        with open(filepath, "w"):
            pass
    except Exception as e:
        display_result(output_textbox, f"Error creating file: {e}")
        return None

    # Open immediately using the unified connection flow
    choose_database(
        filepath,
        output_textbox=output_textbox,
        window=window,
        db_menu=None  # GUI will refresh afterwards
    )

    # Add to recent list (handled again inside choose_database, but kept safe)
    global_vars.recent_db_files.insert(0, filepath)
    global_vars.recent_db_files = list(dict.fromkeys(global_vars.recent_db_files))[:10]
    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)

    # Display confirmation
    name = os.path.basename(filepath)
    display_result(output_textbox, f"✅ Created and opened new database: {name}")
    return None


def choose_database(value, *, output_textbox=None, window=None, db_menu=None):
    """
    Close the current connection, open a new one to the selected database,
    update the UI and the recent databases list.
    """
    if not os.path.exists(value):
        if output_textbox:
            display_result(output_textbox, f"File not found: {value}")
        if value in global_vars.recent_db_files:
            global_vars.recent_db_files.remove(value)
            save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
        return None

    close_active_connection(commit_changes=True)

    conn = sqlite3.connect(value)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
    except Exception:
        pass
    global_vars.current_connection = conn
    global_vars.current_database = value

    if output_textbox:
        name = os.path.basename(value)
        display_result(output_textbox, f"Database selected: {name}")
    if window:
        window.title(f"SQL Desk - {value}")

    add_recent_db_file(value)

##    if db_menu is not None:
##        refresh_db_file_menu(db_menu, output_textbox, window)

    return None



def close_active_connection(commit_changes=True):
    """Ferme proprement la connexion unique si elle existe."""
    conn = global_vars.current_connection
    if not conn:
        return None
    try:
        if getattr(conn, "in_transaction", False):
            if commit_changes:
                try:
                    conn.commit()
                except Exception:
                    try:
                        conn.rollback()
                    except Exception:
                        pass
            else:
                try:
                    conn.rollback()
                except Exception:
                    pass
    finally:
        try:
            conn.close()
        except Exception:
            pass
        global_vars.current_connection = None
    return None


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

