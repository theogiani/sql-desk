# GUI_functions.py

# Core GUI logic for SQL Desk – a lightweight SQL sandbox tool

# Dependencies:
# - Uses sqlite3 for database access
# - Tkinter widgets and filedialog for GUI interaction
# - Relies on helper functions in: utils.py, database_management.py, global_vars.py



import sqlite3
import os
import global_vars
from utils import (
    make_pretty_table, highlight_keywords, colorize_keywords,
    insert_linebreaks_before_keywords, update_recent_sql_files, display_result
)
from tkinter import filedialog, messagebox



def run_sql(sql_textbox, output_textbox):
    """
    Execute the selected SQL (if any) or the whole editor content.
    Supports multiple statements (via sqlite3.complete_statement).
    Pretty-print is applied after execution only when no selection is used.
    """
    if not global_vars.current_database:
        display_result(output_textbox, "No database selected.")
        return None

    # 1) Récupérer soit la sélection, soit tout le contenu
    if sql_textbox.tag_ranges("sel"):
        sql_code = sql_textbox.get("sel.first", "sel.last").strip()
        do_pretty_after = False  # on ne reformate pas pour ne pas casser la sélection
    else:
        sql_code = sql_textbox.get("1.0", "end-1c").strip()
        do_pretty_after = True   # on reformate le buffer complet après exécution

    if not sql_code:
        display_result(output_textbox, "(Nothing to execute.)")
        return None

    # 2) Découper en statements complets
    statements = split_sql_statements(sql_code)
    if not statements:
        display_result(output_textbox, "(No complete SQL statement found.)")
        return None

    # 3) Exécuter chaque statement
    try:
        with sqlite3.connect(global_vars.current_database) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cur = conn.cursor()

            for idx, stmt in enumerate(statements, 1):
                try:
                    cur.execute(stmt)
                    if stmt.strip().lower().startswith("select"):
                        rows = cur.fetchall()
                        result = make_pretty_table(cur.description, rows)
                    else:
                        conn.commit()
                        result = "OK."
                    display_result(output_textbox, result)
                except Exception as e:
                    display_result(output_textbox, f"Error in statement {idx}: {e}")

    except Exception as e:
        display_result(output_textbox, f"Connection error: {e}")

    # 4) Pretty print uniquement si on n'avait PAS de sélection
    if do_pretty_after:
        pretty_print_sql(sql_textbox)

    return None



def split_sql_statements(sql_code):
    """
    Split SQL code into complete statements.
    Uses sqlite3.complete_statement() to safely detect the end of each statement,
    avoiding naive splitting on ';'. Handles multi-line statements correctly.
    Args:
        sql_code (str): SQL code, possibly containing multiple statements.

    Returns:
        list[str]: Complete SQL statements without surrounding whitespace.
    """
    buffer = ""
    statements = []

    for line in sql_code.splitlines():
        buffer += line + "\n"
        if sqlite3.complete_statement(buffer):
            statements.append(buffer.strip())
            buffer = ""
    return statements


def get_tables(output_textbox):
    '''Displays table names and columns in current DB'''
    db_path = global_vars.current_database
    output_textbox.config(state="normal")

    if not db_path:
        display_result(output_textbox, "No database selected.")
        return None

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        if tables:
            lines = ["Tables in current database:"]
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                columns = [row[1] for row in cursor.fetchall()]
                col_list = ", ".join(columns)
                lines.append(f"• {table} ({col_list})")
            result = "\n".join(lines)
        else:
            result = "No tables found in the current database."

        conn.close()

    except Exception as e:
        result = f"Error retrieving tables:\n{e}"

    display_result(output_textbox, result)
    return None


def save_sql_code(sql_textbox, menu=None):
    '''Saves formatted SQL to file'''
    raw_sql = sql_textbox.get("1.0", "end-1c")
    formatted_sql = highlight_keywords(raw_sql)

    filepath = filedialog.asksaveasfilename(
        defaultextension=".sql",
        filetypes=[("SQL Files", "*.sql"), ("All Files", "*.*")]
    )

    if filepath:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(formatted_sql)

            update_recent_sql_files(filepath)
            if menu:
                refresh_sql_file_menu(menu, sql_textbox)

        except Exception as e:
            print(f"Error saving file: {e}")
    return None


def open_sql_code(sql_textbox, filepath=None, menu=None):
    '''Opens SQL file and inserts it into editor'''
    if not filepath:
        filepath = filedialog.askopenfilename(
            title="Open SQL File",
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
    if not filepath:
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        sql_textbox.delete("1.0", "end")
        sql_textbox.insert("1.0", content)
        pretty_print_sql(sql_textbox)
        update_recent_sql_files(filepath)
        
        if menu:
            # Rafraîchissement différé pour éviter problème d'affichage
            sql_textbox.after(50, lambda: refresh_sql_file_menu(menu, sql_textbox))
        
    except Exception as e:
        # Voir plus tard comment gérer les messages d'erreur
        messagebox.showerror("Error", f"Failed to open file:\n{e}")
    return None


def change_font_size(selection, target_font, font_type):
    '''Updates font size in SQL or output box'''
    size = int(selection)

    if font_type == "sql":
        global_vars.font_size_sql = size
    elif font_type == "output":
        global_vars.font_size_output = size

    target_font.configure(size=size)
    return None


def refresh_sql_file_menu(menu, textbox):
    '''Refreshes SQL file menu with recent files'''
    menu.delete(0, 'end')
    menu.add_command(label="Open SQL...", command=lambda: open_sql_code(textbox, menu=menu))
    menu.add_command(label="Save SQL...", command=lambda: save_sql_code(textbox, menu=menu))
    menu.add_separator()

    for i, filepath in enumerate(global_vars.recent_sql_files, 1):
        short_name = os.path.basename(filepath)
        menu.add_command(
            label=f"{i}. {short_name}",
            command=lambda fp=filepath: open_sql_code(textbox, fp, menu=menu)
        )
    return None


def pretty_print_sql(sql_textbox):
    '''Applies keyword capitalisation, linebreaks, and colouring'''
    import re  # local import pour éviter d'ajouter d'import en haut
    raw_query = sql_textbox.get("1.0", "end-1c")

    # 1) Line breaks avant les mots-clés
    formatted_query = insert_linebreaks_before_keywords(raw_query)

    # 2) Ligne vide après chaque instruction terminée par ';' (sans doubler)
    #    - agit seulement quand le ';' est suivi d'un \n
    #    - n'ajoute rien en fin de fichier si pas de \n après ';'
    formatted_query = re.sub(r';[ \t]*\n(?!\n)', ';\n\n', formatted_query)

    # 3) Capitalisation des mots-clés
    formatted_query = highlight_keywords(formatted_query)

    # 4) Injecter + recoloriser
    sql_textbox.delete("1.0", "end")
    sql_textbox.insert("1.0", formatted_query)
    colorize_keywords(sql_textbox)
    return None







