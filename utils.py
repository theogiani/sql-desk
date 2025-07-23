# utils.py
# Utility functions for SQL Desk (formatting, recent files, syntax styling)
# Author: Théo Giani (2025)

import os
import re
import global_vars
from tkinter import Tk, END

SQL_KEYWORDS = {
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE", "SET",
    "DELETE", "CREATE", "TABLE", "DROP", "ALTER", "ADD", "RENAME",
    "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "OUTER", "CROSS", "NATURAL",
    "ON", "AS", "AND", "OR", "NOT", "IS", "NULL", "IN", "LIKE", "BETWEEN",
    "ORDER", "BY", "GROUP", "HAVING", "DISTINCT", "LIMIT", "OFFSET",
    "UNION", "ALL", "EXISTS", "CASE", "WHEN", "THEN", "ELSE", "END",
    "ASC", "DESC", "UNIQUE", "IF",
    "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "CHECK", "DEFAULT", "CONSTRAINT",
    "INTEGER", "TEXT", "REAL", "NUMERIC", "BLOB", "BOOLEAN",
    "CASCADE", "RESTRICT", "NO", "ACTION", "SET",
    "VIEW", "TRIGGER", "BEFORE", "AFTER", "INSTEAD", "OF", "BEGIN", "COMMIT", "ROLLBACK", "TRANSACTION"
}


LINEBREAK_KEYWORDS = {
    "SELECT", "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT", "OFFSET",
    "UNION", "VALUES", "INSERT INTO", "UPDATE", "SET", "DELETE FROM",
    "CREATE TABLE", "ALTER TABLE", "DROP TABLE",
    "JOIN", "INNER JOIN", "LEFT JOIN", "CROSS JOIN", "NATURAL JOIN", "ON"
}

##def add_linebreaks(sql_code):
##    formatted = sql_code
##    for keyword in sorted(LINEBREAK_KEYWORDS, key=len, reverse=True):  # longest first
##        pattern = rf"\b{re.escape(keyword)}\b"
##        formatted = re.sub(pattern, rf"\n{keyword}", formatted, flags=re.IGNORECASE)
##    # Nettoyage : supprime les \n en double ou les espaces inutiles
##    formatted = re.sub(r"\n\s*", "\n", formatted)
##    return formatted.strip()
##

SQL_KEYWORDS = SQL_KEYWORDS.union(LINEBREAK_KEYWORDS)


def make_pretty_table(info, body):
    """
    Returns a Markdown-style table from query result.
    """
    if not info:
        return "\n| (No data returned) |\n"

    headings = [col[0] for col in info]
    num_cols = len(headings)
    column_widths = [len(h) for h in headings]

    for row in body:
        for i in range(num_cols):
            column_widths[i] = max(column_widths[i], len(str(row[i])))

    result = '\n'
    result += '| ' + ' | '.join(f'{headings[i]:<{column_widths[i]}}' for i in range(num_cols)) + ' |\n'
    result += '|-' + '-|-'.join('-' * column_widths[i] for i in range(num_cols)) + '-|\n'

    for row in body:
        result += '| ' + ' | '.join(f'{str(row[i]):<{column_widths[i]}}' for i in range(num_cols)) + ' |\n'

    return result



def save_recent_files(file_path, source_list):
    """
    Saves list of recent files to disk.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in source_list:
                f.write(line + '\n')
    except Exception as e:
        print(f"Error saving recent files to {file_path}: {e}")

    return None


def highlight_keywords(query: str) -> str:
    """
    Converts known SQL keywords to uppercase.
    """
    matches = re.finditer(r'\b\w+\b', query)
    result = ''
    last_end = 0

    for match in matches:
        start, end = match.span()
        word = match.group(0)
        result += query[last_end:start]
        result += word.upper() if word.upper() in SQL_KEYWORDS else word
        last_end = end

    result += query[last_end:]
    return result


def colorize_keywords(text_widget):
    """
    Applies colour tag to SQL keywords in Text widget.
    """
    text_widget.tag_remove("sql_keyword", "1.0", "end")
    text_widget.tag_configure("sql_keyword", foreground="#4A637D")

    lines = text_widget.get("1.0", "end-1c").split("\n")

    for i, line in enumerate(lines):
        for match in re.finditer(r'\b\w+\b', line):
            word = match.group(0)
            if word.upper() in SQL_KEYWORDS:
                start_col, end_col = match.span()
                start = f"{i + 1}.{start_col}"
                end = f"{i + 1}.{end_col}"
                text_widget.tag_add("sql_keyword", start, end)
    return None


##def insert_linebreaks_before_keywords(sql_code: str) -> str:
##    """
##    Inserts newlines before key SQL keywords.
##    """
##    pattern = r"(?<!\n)\b(" + "|".join(LINEBREAK_KEYWORDS) + r")\b"
##    return re.sub(pattern, prepend_newline_to_keyword, sql_code, flags=re.IGNORECASE)
##import re

def insert_linebreaks_before_keywords(sql_code: str) -> str:
    """
    Inserts newlines before key SQL keywords (from LINEBREAK_KEYWORDS),
    in an idempotent way: no duplicate newlines on repeated runs.
    """
    formatted = sql_code
    for keyword in sorted(LINEBREAK_KEYWORDS, key=len, reverse=True):
        pattern = rf"\b{re.escape(keyword)}\b"
        formatted = re.sub(pattern, rf"\n{keyword}", formatted, flags=re.IGNORECASE)
    # Remove redundant newlines and whitespace
    formatted = re.sub(r'\n\s*', '\n', formatted)
    return formatted.strip()


def prepend_newline_to_keyword(match: re.Match) -> str:
    """
    Adds newline before a SQL keyword.
    """
    return f"\n{match.group(1)}"


def on_closing(window: Tk):
    """
    Saves recent files and closes window.
    """
    from utils import save_recent_files
    save_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)
    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
    window.destroy()
    return None

def update_recent_sql_files(filepath, max_items=10):
    if filepath in global_vars.recent_sql_files:
        global_vars.recent_sql_files.remove(filepath)

    global_vars.recent_sql_files.insert(0, filepath)
    global_vars.recent_sql_files = global_vars.recent_sql_files[:max_items]

    # Sauvegarder la liste mise à jour
    save_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)

##def update_recent_sql_files(filepath, max_items=10):
##    """
##    Adds file to recent list (deduplicated, capped).
##    """
##    if filepath in global_vars.recent_sql_files:
##        global_vars.recent_sql_files.remove(filepath)
##
##    global_vars.recent_sql_files.insert(0, filepath)
##    global_vars.recent_sql_files = global_vars.recent_sql_files[:max_items]
##    return None

def load_recent_files(file_path, target_list, max_items=8):
    """
    Loads recent files into the target list.
    """
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            target_list.clear()
            target_list.extend(lines[:max_items])
    except Exception as e:
        print(f"Error loading recent files from {file_path}: {e}")

    return None


def clean_recent_db_files():
    """
    Removes non-existing .db files from recent_db_files.
    """
    global_vars.recent_db_files = [
        f for f in global_vars.recent_db_files if os.path.exists(f)
    ]
    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
    return None

def clean_recent_sql_files():
    """
    Removes non-existing .sql files from recent_sql_files.
    """
    global_vars.recent_sql_files = [
        f for f in global_vars.recent_sql_files if os.path.exists(f)
    ]
    save_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)
    return None



def display_result(output_box, text):
    '''Displays result text in output area'''
    output_box.config(state='normal')
    output_box.insert(END, text.rstrip() + "\n\n")
    output_box.see(END)
    output_box.config(state='disabled')
    return None


def clear_output(output_box):
    '''Clears the output area'''
    output_box.config(state='normal')
    output_box.delete("1.0", END)
    output_box.config(state='disabled')
    return None
