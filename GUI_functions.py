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
    load_recent_files, save_recent_files, make_pretty_table,
    highlight_keywords, colorize_keywords, insert_linebreaks_before_keywords,
    update_recent_sql_files
)
from tkinter import StringVar, OptionMenu, END, filedialog, messagebox, font
from database_management import menu_open_database, create_new_database, choose_database


def run_query(sql_textbox, output_textbox):
    '''Executes a single query after pretty-printing'''
    if not global_vars.current_database:
        display_result(output_textbox, "No database selected.\n")
        return None

    pretty_print_sql(sql_textbox)
    formatted_sql = sql_textbox.get("1.0", "end-1c")

    try:
        conn = sqlite3.connect(global_vars.current_database)
        cursor = conn.cursor()
        cursor.execute(formatted_sql)

        if formatted_sql.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            result = make_pretty_table(cursor.description, rows)
        else:
            conn.commit()
            result = "Query executed successfully."

        conn.close()

    except Exception as e:
        result = f"Error: {e}"

    display_result(output_textbox, result)
    return None


def run_sql(query, output_textbox):
    '''Executes SQL script with multiple statements'''
    result = ''
    try:
        with sqlite3.connect(global_vars.current_database) as db:
            cursor = db.cursor()
            statements = [s.strip() for s in query.strip().split(';') if s.strip()]
            for statement in statements:
                if statement.lower().startswith("select"):
                    cursor.execute(statement)
                    rows = cursor.fetchall()
                    result += make_pretty_table(cursor.description, rows) + '\n'
                else:
                    cursor.execute(statement)
                    db.commit()
                    result += f"Query executed: {statement[:30]}...\n"
    except Exception as e:
        result = f"ERROR: {e}"

    result = result.strip() + '\n\n'
    display_result(output_textbox, result)
    return None


def get_tables(output_textbox):
    '''Displays table names and columns in current DB'''
    db_path = global_vars.current_database
    output_textbox.config(state="normal")
    output_textbox.delete("1.0", "end")

    if not db_path:
        output_textbox.insert("1.0", "No database selected.")
        output_textbox.config(state="disabled")
        return None

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        if tables:
            output_textbox.insert("1.0", "Tables in current database:\n\n")
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                columns = [row[1] for row in cursor.fetchall()]
                col_list = ", ".join(columns)
                output_textbox.insert("end", f"• {table} ({col_list})\n")
        else:
            output_textbox.insert("1.0", "No tables found in the current database.")

        conn.close()

    except Exception as e:
        output_textbox.insert("1.0", f"Error retrieving tables:\n{e}")

    output_textbox.config(state="disabled")
    return None


def clear_output(output_box):
    '''Clears the output area'''
    output_box.config(state='normal')
    output_box.delete("1.0", END)
    output_box.config(state='disabled')
    return None


def display_result(output_box, text):
    '''Displays result text in output area'''
    output_box.config(state='normal')
    output_box.insert(END, text + "\n")
    output_box.config(state='disabled')
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


def open_sql_code(sql_textbox, filepath=None):
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
    except Exception as e:
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
    menu.add_command(label="Open SQL...", command=lambda: open_sql_code(textbox))
    menu.add_command(label="Save SQL...", command=lambda: save_sql_code(textbox, menu))
    menu.add_separator()

    for i, filepath in enumerate(global_vars.recent_sql_files, 1):
        short_name = os.path.basename(filepath)
        menu.add_command(
            label=f"{i}. {short_name}",
            command=lambda fp=filepath: open_sql_code(textbox, fp)
        )
    return None


def refresh_db_file_menu(db_menu, output_textbox, window=None):
    '''Refreshes Database menu with recent databases'''
    db_menu.delete(0, 'end')

    db_menu.add_command(label="Open Database...", command=lambda: menu_open_database(output_textbox, window))
    db_menu.add_command(label="Create New Database...", command=lambda: create_new_database(output_textbox, window))
    db_menu.add_separator()

    for i, filename in enumerate(global_vars.recent_db_files, start=1):
        db_menu.add_command(
            label=f"{i}. {os.path.basename(filename)}",
            command=lambda filename=filename: choose_database(filename, output_textbox=output_textbox, window=window)
        )
    return None


def pretty_print_sql(sql_textbox):
    '''Applies keyword capitalisation, linebreaks, and colouring'''
    raw_query = sql_textbox.get("1.0", "end-1c")
    formatted_query = insert_linebreaks_before_keywords(raw_query)
    formatted_query = highlight_keywords(formatted_query)
    sql_textbox.delete("1.0", "end")
    sql_textbox.insert("1.0", formatted_query)
    colorize_keywords(sql_textbox)
    return None


def run_sql_pretty(sql_textbox, output_textbox):
    '''Formats then runs SQL'''
    pretty_print_sql(sql_textbox)
    query = sql_textbox.get("1.0", "end-1c")
    run_sql(query, output_textbox)
    return None
