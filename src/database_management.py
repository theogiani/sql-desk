# database_management.py
# Handles creation, opening, and selection of SQLite databases.
# Author: Théo Giani (2025)

import os
from tkinter import filedialog, simpledialog
import global_vars
from utils import save_recent_files, display_result


def menu_open_database(output_textbox, window=None, db_menu=None):
    """
    Opens a .db file and sets it as current database.
    Also updates the recent DBs menu immediately if db_menu is provided.
    """
    print(f"ici menu_open_database, db_menu = {db_menu}, {output_textbox}, {window}")
    filepath = filedialog.askopenfilename(
        title="Open Database",
        filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")]
    )
    if filepath:
        choose_database(filepath, output_textbox=output_textbox, window=window, db_menu=db_menu)
    return None


def create_new_database(output_textbox, window=None, db_menu=None):
    """
    Prompts user to name a new .db file and creates it.
    """
    name = simpledialog.askstring("New Database", "Enter name for new database (without .db):")
    if name:
        filename = f"{name}.db"
        with open(filename, "w"):
            pass

        global_vars.current_database = filename
        display_result(output_textbox, f"Created new database: {filename}")  
        # Add to recent DBs
        global_vars.recent_db_files.insert(0, filename)
        global_vars.recent_db_files = list(dict.fromkeys(global_vars.recent_db_files))[:10]
        save_recent_files("recent_db_files.txt", global_vars.recent_db_files)


        # Refresh menu if needed
        if db_menu is not None:
            refresh_db_file_menu(db_menu, output_textbox, window)
            
    return None


def choose_database(value, *, output_textbox=None, window=None, db_menu=None):
    """
    Sets current database, prints message, updates window title,
    updates recent DBs list, and refreshes the recent DB menu if provided.
    """
    print("Ici choose menu value, db_menu", value, db_menu)
    if not os.path.exists(value):
        if output_textbox:
            display_result(output_textbox, f"File not found: {value}")
        if value in global_vars.recent_db_files:
            global_vars.recent_db_files.remove(value)
            save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
        return None

    global_vars.current_database = value

    if output_textbox:
        name = os.path.basename(value)
        display_result(output_textbox, f"Database selected: {name}")  
    if window:
        window.title(f"Python Database Tool – {value}")

    # Update recent DBs
    global_vars.recent_db_files.insert(0, value)
    global_vars.recent_db_files = list(dict.fromkeys(global_vars.recent_db_files))[:10]
    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)

    # Refresh the recent DB menu if the menu is provided
    print("Ici refresh", db_menu)
    if db_menu: #and output_textbox and window:
        refresh_db_file_menu(db_menu, output_textbox, window)

    return None


# En bas de ??????
def refresh_db_file_menu(db_menu, output_textbox, window=None):
    from database_management import menu_open_database, create_new_database, choose_database

    db_menu.delete(0, 'end')

    db_menu.add_command(
        label="Open Database...",
        command=lambda: menu_open_database(output_textbox, window, db_menu)
    )
    db_menu.add_command(
        label="Create New Database...",
        command=lambda: create_new_database(output_textbox, window, db_menu)
    )
    db_menu.add_separator()

    for i, filename in enumerate(global_vars.recent_db_files, start=1):
        db_menu.add_command(
            label=f"{i}. {os.path.basename(filename)}",
            command=lambda filename=filename: choose_database(filename, output_textbox=output_textbox, window=window, db_menu=db_menu)
        )
    return None
