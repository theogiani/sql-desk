# GUI_functions.py
#
# Core GUI logic for SQL Desk – a lightweight educational SQL sandbox.
#
# Responsibilities :
# - Execute SQL code using the active SQLite connection
# - Manage recent SQL files and databases
# - Provide pretty-printing and keyword colouring
# - Serve as the link between GUI buttons and underlying functions
#
# Dependencies :
# - sqlite3 for database access
# - Tkinter widgets and filedialog for user interaction
# - Helper modules : utils.py, database_management.py, global_vars.py

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
    Execute the selected SQL code (if any) or the entire buffer using
    the current SQLite connection (mono-connection model).

    Behaviour :
        - SELECT statements : fetch and pretty-print results.
        - Other statements  : commit automatically and show rows affected.
        - Each statement is executed in sequence.

    Args:
        sql_textbox : tkinter.Text
            The SQL editor widget.
        output_textbox : tkinter.Text
            The output area for displaying results.

    Returns:
        None
    """
    conn = global_vars.current_connection
    if conn is None:
        display_result(output_textbox, "No database connected. Use Database → Open…")
        return None

    # Retrieve either the selection or the whole content
    if sql_textbox.tag_ranges("sel"):
        sql_code = sql_textbox.get("sel.first", "sel.last").strip()
        do_pretty_after = True
    else:
        sql_code = sql_textbox.get("1.0", "end-1c").strip()
        do_pretty_after = True

    if not sql_code:
        display_result(output_textbox, "(Nothing to execute.)")
        return None

    # Split into complete SQL statements
    statements = split_sql_statements(sql_code)
    if not statements:
        display_result(output_textbox, "(No complete SQL statement found.)")
        return None

    cur = conn.cursor()
    for idx, stmt in enumerate(statements, 1):
        try:
            before = conn.total_changes
            cur.execute(stmt)
            is_select = (cur.description is not None)

            if is_select:
                rows = cur.fetchall()
                headers = [d[0] for d in cur.description]
                result = make_pretty_table(headers, rows)
            else:
                affected = max(conn.total_changes - before, 0)
                if conn.in_transaction:
                    try:
                        conn.commit()
                    except Exception:
                        try:
                            conn.rollback()
                        except Exception:
                            pass
                        raise
                result = f"OK – {affected} row(s) affected."

            display_result(output_textbox, result)
            display_result(output_textbox, "")
            try:
                output_textbox.see("end")
            except Exception:
                pass

        except Exception as e:
            if conn.in_transaction:
                try:
                    conn.rollback()
                except Exception:
                    pass
            display_result(output_textbox, f"Error in statement {idx}: {e}")

    # Pretty-print SQL after execution for visual consistency
    if do_pretty_after:
        pretty_print_sql(sql_textbox)

    return None


def split_sql_statements(sql_code):
    """
    Split SQL code into complete statements, using
    sqlite3.complete_statement() to ensure correctness.

    Handles cases where multiple statements share a single line.

    Args:
        sql_code : str
            Raw SQL text from the editor.

    Returns:
        list[str] : List of individual SQL statements.
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

    # Handle trailing content without a final semicolon
    tail = buffer.strip()
    if tail:
        statements.append(tail)

    return statements


def get_tables(output_textbox):
    """
    Display the list of tables in the current database,
    including their columns, primary keys, and foreign keys.

    Primary keys are shown in red (tag 'pk'),
    and foreign keys are marked with a '#' character.

    Args:
        output_textbox : tkinter.Text
            Output widget for displaying table structures.

    Returns:
        None
    """
    conn = global_vars.current_connection
    if conn is None:
        display_result(output_textbox, "No database connected.")
        return None

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
        )
        tables = [row[0] for row in cur.fetchall()]

        if not tables:
            display_result(output_textbox, "No tables found in the current database.")
            return None

        output_textbox.config(state="normal")
        output_textbox.insert("end", "Tables in current database:\n\n", "tbl")

        for table in tables:
            safe = table.replace("'", "''")

            # Column definitions and PK
            cur.execute(f"PRAGMA table_info('{safe}');")
            table_info = cur.fetchall()  # (cid, name, type, notnull, dflt, pk)
            pk_cols = {row[1] for row in table_info if row[5] != 0}

            # Foreign keys
            cur.execute(f"PRAGMA foreign_key_list('{safe}');")
            fk_info = cur.fetchall()      # (id, seq, table, from, to, on_update, on_delete, match)
            fk_cols = {row[3] for row in fk_info}

            output_textbox.insert("end", f"- {table} (", "tbl")
            for i, row in enumerate(table_info):
                col = row[1]

                if col in pk_cols:
                    output_textbox.insert("end", col, "pk")
                else:
                    output_textbox.insert("end", col)

                if col in fk_cols:
                    output_textbox.insert("end", "#")

                if i < len(table_info) - 1:
                    output_textbox.insert("end", ", ", "comma")
            output_textbox.insert("end", ")\n")

        output_textbox.insert("end", "\n")
        output_textbox.config(state="disabled")

    except Exception as e:
        display_result(output_textbox, f"Error retrieving tables:\n{e}")

    return None


def save_sql_code(sql_textbox, menu=None):
    """Save the current SQL editor content (with highlighted keywords) to a file."""
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
    """Open an SQL file and load its content into the editor."""
    if not filepath:
        filepath = filedialog.askopenfilename(
            title="Open SQL File",
            filetypes=[("SQL Files", "*.sql"), ("All Files", "*.*")]
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
            sql_textbox.after(50, lambda: refresh_sql_file_menu(menu, sql_textbox))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file:\n{e}")
    return None


def change_font_size(selection, target_font, font_type):
    """Adjust the font size in either the SQL or output text box."""
    size = int(selection)

    if font_type == "sql":
        global_vars.font_size_sql = size
    elif font_type == "output":
        global_vars.font_size_output = size

    target_font.configure(size=size)
    return None


def refresh_sql_file_menu(menu, textbox):
    """Rebuild the SQL File menu with updated recent entries."""
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
    """
    Apply SQL formatting :
        - Insert line breaks before key SQL words.
        - Ensure blank lines after semicolons and comments.
        - Capitalise recognised keywords.
        - Restore cursor and scroll position.

    The aim is to make SQL code visually consistent and easier to read.
    """
    import re

    insert_idx = sql_textbox.index("insert")
    try:
        sel_start = sql_textbox.index("sel.first")
        sel_end = sql_textbox.index("sel.last")
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

    formatted_query = insert_linebreaks_before_keywords(raw_query)

    pattern = r'(;[^\n]*(?:\n--[^\n]*)*)(?=\n(?!\n))'
    formatted_query = re.sub(pattern, r'\1\n', formatted_query)

    formatted_query = highlight_keywords(formatted_query)

    try:
        sql_textbox.edit_separator()
    except Exception:
        pass

    sql_textbox.delete("1.0", "end")
    sql_textbox.insert("1.0", formatted_query)
    colorize_keywords(sql_textbox)

    sql_textbox.mark_set("insert", insert_idx)
    if had_sel:
        sql_textbox.tag_remove("sel", "1.0", "end")
        sql_textbox.tag_add("sel", sel_start, sel_end)
    sql_textbox.yview_moveto(top_frac)
    try:
        sql_textbox.xview_moveto(x_frac)
    except Exception:
        pass
    sql_textbox.see("insert")
    sql_textbox.focus_set()

    try:
        sql_textbox.edit_separator()
    except Exception:
        pass

    return None


def refresh_db_file_menu(menu, output_textbox, window=None, *, select_database):
    """
    Rebuild the 'Recent Databases' section of the Database menu.

    Args:
        menu : tkinter.Menu
            The database menu widget.
        output_textbox : tkinter.Text
            Output area for feedback.
        window : tkinter.Tk, optional
            Main application window.
        select_database : callable
            Function that handles the actual database selection.

    Returns:
        None
    """
    menu.delete(3, 'end')
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
# GUI CALLBACK WRAPPERS
# =========================

def choose_recent_db(filepath, menu, output_textbox, window, select_database):
    """Open a recent database and refresh the menu list."""
    select_database(filepath, output_textbox=output_textbox, window=window, db_menu=None)
    refresh_db_file_menu(menu, output_textbox, window, select_database=select_database)
    return None


def open_and_refresh(menu, output_textbox, window, select_database, open_db_func):
    """Open a database via dialogue, then refresh the 'Recent' section."""
    open_db_func(output_textbox, window, db_menu=None)
    refresh_db_file_menu(menu, output_textbox, window, select_database=select_database)
    return None


def create_and_refresh(menu, output_textbox, window, select_database, create_db_func):
    """Create a new database and refresh the 'Recent' section."""
    create_db_func(output_textbox, window, db_menu=None)
    refresh_db_file_menu(menu, output_textbox, window, select_database=select_database)
    return None
