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
    Execute the selected SQL (if any) or the whole editor content using the
    single active SQLite connection (global_vars.current_connection).
    Commits after non-SELECT statements; pretty-prints as before.
    """
    # 0) Require an active connection (mono-connection model)
    conn = global_vars.current_connection
    if conn is None:
        display_result(output_textbox, "No database connected. Use Database -> Open...")
        return None

    # 1) Retrieve either the selection or the whole buffer
    if sql_textbox.tag_ranges("sel"):
        sql_code = sql_textbox.get("sel.first", "sel.last").strip()
        do_pretty_after = True
    else:
        sql_code = sql_textbox.get("1.0", "end-1c").strip()
        do_pretty_after = True

    if not sql_code:
        display_result(output_textbox, "(Nothing to execute.)")
        return None

    # 2) Split into complete SQL statements
    statements = split_sql_statements(sql_code)
    if not statements:
        display_result(output_textbox, "(No complete SQL statement found.)")
        return None

    # 3) Execute each statement on the active connection
    cur = conn.cursor()
    for idx, stmt in enumerate(statements, 1):
        try:
            before = conn.total_changes
            cur.execute(stmt)
            is_select = (cur.description is not None)

            if is_select:
                rows = cur.fetchall()
                headers = [d[0] for d in cur.description]
                # make_pretty_table expects (columns, rows)
                result = make_pretty_table(headers, rows)
            else:
                affected = conn.total_changes - before
                if affected < 0:
                    affected = 0
                # commit after write statements
                if conn.in_transaction:
                    try:
                        conn.commit()
                    except Exception:
                        try:
                            conn.rollback()
                        except Exception:
                            pass
                        raise
                result = f"OK - {affected} row(s) affected."

            display_result(output_textbox, result)
            display_result(output_textbox, "")
            try:
                output_textbox.see("end")
            except Exception:
                pass

        except Exception as e:
            # rollback if the statement left a transaction open
            if conn.in_transaction:
                try:
                    conn.rollback()
                except Exception:
                    pass
            display_result(output_textbox, f"Error in statement {idx}: {e}")

    # 4) Pretty print only when requested
    if do_pretty_after:
        pretty_print_sql(sql_textbox)

    return None





def split_sql_statements(sql_code):
    """
    Split SQL code into complete statements using sqlite3.complete_statement(),
    works even when multiple statements share the same line (e.g. '...;INSERT ...').
    """
    statements = []
    buffer = ""

    for ch in sql_code:
        buffer += ch
        if sqlite3.complete_statement(buffer):
            stmt = buffer.strip()
            if stmt:
                statements.append(stmt)
            buffer = ""

    # S'il reste des miettes non vides (sans ';'), on les exécute aussi.
    tail = buffer.strip()
    if tail:
        statements.append(tail)

    return statements



def get_tables(output_textbox):
    """Display table names and columns from the current DB using the active connection."""
    conn = global_vars.current_connection
    if conn is None:
        display_result(output_textbox, "No database connected.")
        return None

    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [row[0] for row in cur.fetchall()]

        if tables:
            lines = ["Tables in current database:"]
            for table in tables:
                # Escape single quotes in table name for PRAGMA
                safe = table.replace("'", "''")
                cur.execute(f"PRAGMA table_info('{safe}');")
                cols = [row[1] for row in cur.fetchall()]
                col_list = ", ".join(cols) if cols else "(no columns)"
                lines.append(f"- {table} ({col_list})")
            result = "\n".join(lines)
        else:
            result = "No tables found in the current database."
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
    import re  # local import pour eviter d'ajouter d'import en haut

    # --- NEW: save cursor/selection/scroll state ---
    insert_idx = sql_textbox.index("insert")
    try:
        sel_start = sql_textbox.index("sel.first")
        sel_end   = sql_textbox.index("sel.last")
        had_sel = True
    except Exception:
        had_sel = False
        sel_start = sel_end = None
    top_frac = sql_textbox.yview()[0]
    try:
        x_frac = sql_textbox.xview()[0]
    except Exception:
        x_frac = 0.0

    raw_query = sql_textbox.get("1.0", "end-1c")

    # 1) Line breaks avant les mots-cles
    formatted_query = insert_linebreaks_before_keywords(raw_query)

    # 2) Ligne vide apres chaque instruction + eventuels commentaires
    #    - detecte un ';', puis des commentaires eventuels '-- ...'
    #    - insere la ligne vide apres ces commentaires
    pattern = r'(;[^\n]*(?:\n--[^\n]*)*)(?=\n(?!\n))'
    formatted_query = re.sub(pattern, r'\1\n', formatted_query)

    # 3) Capitalisation des mots-cles
    formatted_query = highlight_keywords(formatted_query)

    # (optionnel) marquer une separatrice d'undo pour que tout soit une seule action
    try:
        sql_textbox.edit_separator()
    except Exception:
        pass

    # 4) Injecter + recoloriser (ta logique d'origine)
    sql_textbox.delete("1.0", "end")
    sql_textbox.insert("1.0", formatted_query)
    colorize_keywords(sql_textbox)

    # --- NEW: restore cursor/selection/scroll state ---
    sql_textbox.mark_set("insert", insert_idx)
    if had_sel:
        sql_textbox.tag_remove("sel", "1.0", "end")
        sql_textbox.tag_add("sel", sel_start, sel_end)
    # d'abord le viewport, puis s'assurer que le curseur est visible
    sql_textbox.yview_moveto(top_frac)
    try:
        sql_textbox.xview_moveto(x_frac)
    except Exception:
        pass
    sql_textbox.see("insert")
    sql_textbox.focus_set()

    # (optionnel) separatrice d'undo apres
    try:
        sql_textbox.edit_separator()
    except Exception:
        pass

    return None






# --- dans GUI_functions.py ---

def refresh_db_file_menu(menu, output_textbox, window=None, *, select_database):
    """
    Rebuild only the dynamic 'Recent databases' section.
    `select_database` is a callable (e.g. database_management.choose_database).
    """
    import os
    import global_vars

    menu.delete(3, 'end')  # 0=Open, 1=Create, 2=separator
    for i, filepath in enumerate(global_vars.recent_db_files, 1):
        short = os.path.basename(filepath)
        menu.add_command(
            label=f"{i}. {short}",
            command=lambda fp=filepath: choose_recent_db(
                fp, menu, output_textbox, window, select_database
            )
        )
    return None


# =========================
# WRAPPERS (GUI callbacks)
# =========================

def choose_recent_db(filepath, menu, output_textbox, window, select_database):
    """Open the selected recent DB, then refresh the submenu."""
    select_database(filepath, output_textbox=output_textbox, window=window, db_menu=None)
    refresh_db_file_menu(menu, output_textbox, window, select_database=select_database)
    return None

def open_and_refresh(menu, output_textbox, window, select_database, open_db_func):
    """Open DB via dialog, then refresh 'Recent'."""
    open_db_func(output_textbox, window, db_menu=None)
    refresh_db_file_menu(menu, output_textbox, window, select_database=select_database)
    return None

def create_and_refresh(menu, output_textbox, window, select_database, create_db_func):
    """Create DB, then refresh 'Recent'."""
    create_db_func(output_textbox, window, db_menu=None)
    refresh_db_file_menu(menu, output_textbox, window, select_database=select_database)
    return None







