# database_management.py
# Database creation, opening, and selection utilities for SQL Desk.
# Author : Théo Giani — 2025

import os
import sqlite3
from tkinter import filedialog, simpledialog
import global_vars
from utils import save_recent_files, display_result
# from GUI_functions import refresh_db_file_menu


def menu_open_database(output_textbox, window=None, db_menu=None):
    """
    Open an existing SQLite database file and set it as the current one.

    Args:
        output_textbox : tkinter.Text
            Output area for displaying messages.
        window : tkinter.Tk, optional
            The main application window (used to update the title).
        db_menu : tkinter.Menu, optional
            The database menu widget, which can be refreshed by the caller.

    Returns: None
    """
    filepath = filedialog.askopenfilename(
        title="Open Database",
        filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
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
    Create a new SQLite database in a directory chosen by the user.

    The file is created empty, then immediately opened via choose_database().
    The GUI is expected to refresh the database menu afterwards.

    Args:
        output_textbox : tkinter.Text
            Output area for messages.
        window : tkinter.Tk, optional
            The main window.
        db_menu : tkinter.Menu, optional
            The database menu (not updated here).

    Returns: None
    """
    filepath = filedialog.asksaveasfilename(
        title="Create New Database",
        defaultextension=".db",
        filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
    )

    if not filepath:
        # User cancelled
        display_result(output_textbox, "Database creation cancelled.")
        return None

    # Create the empty file if it does not already exist
    try:
        with open(filepath, "w"):
            pass
    except Exception as e:
        display_result(output_textbox, f"Error creating file: {e}")
        return None

    # Open the newly created database immediately
    choose_database(
        filepath,
        output_textbox=output_textbox,
        window=window,
        db_menu=None  # GUI will refresh afterwards
    )

    # Add to the recent databases list
    global_vars.recent_db_files.insert(0, filepath)
    global_vars.recent_db_files = list(dict.fromkeys(global_vars.recent_db_files))[:10]
    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)

    # Display confirmation
    name = os.path.basename(filepath)
    display_result(output_textbox, f"Created and opened new database: {name}")
    return None


def choose_database(value, *, output_textbox=None, window=None, db_menu=None):
    """
    Close any existing connection and open a new one to the selected database.
    Updates both the UI and the recent databases list.

    Args:
        value : str
            Full path to the database file.
        output_textbox : tkinter.Text, optional
            Output area for messages.
        window : tkinter.Tk, optional
            The main window (to update the title).
        db_menu : tkinter.Menu, optional
            Not used directly; the GUI handles refreshing.

    Returns: None
    """
    if not os.path.exists(value):
        if output_textbox:
            display_result(output_textbox, f"File not found: {value}")
        if value in global_vars.recent_db_files:
            global_vars.recent_db_files.remove(value)
            save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
        return None

    # Close the current connection before opening another
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
        window.title(f"SQL Desk – {value}")

    add_recent_db_file(value)
    return None


def close_active_connection(commit_changes=True):
    """
    Safely close the active SQLite connection if one exists.

    Args:
        commit_changes : bool, default=True
            Whether to commit pending changes before closing.

    Returns: None
    """
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
    Add a database file to the recent list, avoiding duplicates and limiting its length.

    Args:
        filename : str
            Path to the database file.

    Returns: None
    """
    if filename in global_vars.recent_db_files:
        global_vars.recent_db_files.remove(filename)

    global_vars.recent_db_files.insert(0, filename)

    # Limit the number of entries
    max_recent = 10
    if len(global_vars.recent_db_files) > max_recent:
        global_vars.recent_db_files = global_vars.recent_db_files[:max_recent]

    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
    return None
