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



def run_query(sql_textbox, output_textbox):
    '''Executes a single query after pretty-printing'''

    if not global_vars.current_database:
        display_result(output_textbox, "No database selected.\n")
        return None

    # Sauvegarder la sélection si elle existe
    selection = None
    if sql_textbox.tag_ranges("sel"):
        selection = (sql_textbox.index("sel.first"), sql_textbox.index("sel.last"))

    # Restaurer la sélection si elle existait
    if selection:
        sql_textbox.tag_add("sel", selection[0], selection[1])

    # Récupérer la sélection ou tout le contenu
    if sql_textbox.tag_ranges("sel"):
        formatted_sql = sql_textbox.get("sel.first", "sel.last")
    else:
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
    # Pretty print (modifie le contenu, donc fait perdre la sélection)
    pretty_print_sql(sql_textbox)
    return None




##
##
##def run_sql(sql_textbox, output_textbox):
##    # Récupérer la sélection si elle existe, sinon tout le contenu
##    print(f'Avant recherche sel')
##    if sql_textbox.tag_ranges("sel"):
##        query = sql_textbox.get("sel.first", "sel.last")
##        print(query)
##    else:
##        query = sql_textbox.get("1.0", "end-1c")
##
##    # Debug : afficher la requête brute récupérée
##    print(f"Raw query to execute:\n{query}\n---")
##
##    # Séparer le script en instructions SQL individuelles
##    statements = [s.strip() for s in query.strip().split(';') if s.strip()]
##
##    # Afficher dans la zone de sortie la liste des instructions détectées
##    display_result(output_textbox, f"Statements to execute ({len(statements)}):\n" + "\n".join(statements) + "\n\n")
##
##    result = ''
##    try:
##        with sqlite3.connect(global_vars.current_database) as db:
##            cursor = db.cursor()
##            print("Statements found:")
##            for i, stmt in enumerate(statements):
##                print(f"{i+1}: {repr(stmt)}")
##
##            for statement in statements:
##                if statement.lower().startswith("select"):
##                    cursor.execute(statement)
##                    rows = cursor.fetchall()
##                    result += make_pretty_table(cursor.description, rows) + '\n'
##                else:
##                    cursor.execute(statement)
##                    db.commit()
##                    result += f"Query executed: {statement[:30]}...\n"
##
##    except Exception as e:
##        result = f"ERROR: {e}"
##
##    result = result.strip() + '\n\n'
##    display_result(output_textbox, result)
    return None




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
    raw_query = sql_textbox.get("1.0", "end-1c")
    formatted_query = insert_linebreaks_before_keywords(raw_query)
    formatted_query = highlight_keywords(formatted_query)
    sql_textbox.delete("1.0", "end")
    sql_textbox.insert("1.0", formatted_query)
    colorize_keywords(sql_textbox)
    return None







