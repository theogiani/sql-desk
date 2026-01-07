# utils.py
# Utility functions for SQL Desk: formatting, recent files, and SQL syntax highlighting.
# Author : Théo Giani — 2025

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

SQL_KEYWORDS = SQL_KEYWORDS.union(LINEBREAK_KEYWORDS)


def make_pretty_table(info, body):
    """
    Build a Markdown-style table from a query result.

    Args:
        info : list or cursor.description
            Column headers (list of strings or cursor description tuples).
        body : list of tuples
            Data rows to include in the table.

    Returns:
        str : Formatted table as a string.
    """
    if not info:
        return "\n| (No data returned) |\n"

    # If 'info' is a list of strings, use it directly;
    # otherwise, extract the first element of each tuple.
    if isinstance(info[0], str):
        headings = list(info)
    else:
        headings = [col[0] for col in info]

    num_cols = len(headings)
    column_widths = [len(h) for h in headings]

    for row in body:
        for i in range(num_cols):
            val = "" if row[i] is None else str(row[i])
            column_widths[i] = max(column_widths[i], len(val))

    result = '\n'
    result += '| ' + ' | '.join(f'{headings[i]:<{column_widths[i]}}' for i in range(num_cols)) + ' |\n'
    result += '|-' + '-|-'.join('-' * column_widths[i] for i in range(num_cols)) + '-|\n'

    for row in body:
        result += '| ' + ' | '.join(
            f'{("" if row[i] is None else str(row[i])):<{column_widths[i]}}' for i in range(num_cols)
        ) + ' |\n'

    return result


def save_recent_files(file_path, source_list):
    """
    Save a list of recent files to disk.

    Args:
        file_path : str
            Path to the text file where the list will be written.
        source_list : list
            List of file paths as strings.

    Returns:
        None
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
    Convert recognised SQL keywords in a string to uppercase.

    Args:
        query : str
            SQL code to format.

    Returns:
        str : Query with SQL keywords uppercased.
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


##def colorize_keywords(text_widget):
##    """
##    Apply colour tags to SQL keywords inside a Tkinter Text widget.
##
##    Args:
##        text_widget : tkinter.Text
##            The text area to be colourised.
##
##    Returns:
##        None
##    """
####    text_widget.tag_remove("sql_keyword", "1.0", "end")
####    
####    text_widget.tag_configure("sql_keyword", foreground="#4A637D")
####    text_widget.tag_configure("sql_comment_line", foreground="#2F4F4F")
####    text_widget.tag_configure("sql_comment_block", foreground="#2F4F4F")
####
####
####    lines = text_widget.get("1.0", "end-1c").split("\n")
####
####    for i, line in enumerate(lines):
####        for match in re.finditer(r'\b\w+\b', line):
####            word = match.group(0)
####            if word.upper() in SQL_KEYWORDS:
####                start_col, end_col = match.span()
####                start = f"{i + 1}.{start_col}"
####                end = f"{i + 1}.{end_col}"
####                text_widget.tag_add("sql_keyword", start, end)
####    return None
##
##
##    text_widget.tag_remove("sql_keyword", "1.0", "end")
##    text_widget.tag_remove("sql_comment_line", "1.0", "end")
##
##    text_widget.tag_configure("sql_keyword", foreground="#3B5C8A")
##    text_widget.tag_configure("sql_comment_line", foreground="#4F7F6F")
##    text_widget.tag_configure("sql_comment_block", foreground="#4F7F6F")
##
##    lines = text_widget.get("1.0", "end-1c").split("\n")
##
##        # --- Block comments /* ... */ ---
##    text = text_widget.get("1.0", "end-1c")
##
##    start_idx = 0
##    while True:
##        start = text.find("/*", start_idx)
##        if start == -1:
##            break
##
##        end = text.find("*/", start + 2)
##        if end == -1:
##            end = len(text) - 1
##        else:
##            end += 2
##
##        start_pos = text_widget.index(f"1.0+{start}c")
##        end_pos = text_widget.index(f"1.0+{end}c")
##
##        text_widget.tag_add("sql_comment_block", start_pos, end_pos)
##
##        start_idx = end
##
##    for i, line in enumerate(lines):
##        comment_start = line.find("--")
##        if comment_start != -1:
##            start = f"{i + 1}.{comment_start}"
##            end = f"{i + 1}.end"
##            text_widget.tag_add("sql_comment_line", start, end)
##            scan_line = line[:comment_start]
##        else:
##            scan_line = line
##
##        for match in re.finditer(r"\b\w+\b", scan_line):
##            word = match.group(0)
##            if word.upper() in SQL_KEYWORDS:
##                start_col, end_col = match.span()
##                start = f"{i + 1}.{start_col}"
##                end = f"{i + 1}.{end_col}"
##                text_widget.tag_add("sql_keyword", start, end)
##
##    return None

def colorize_keywords(text_widget):
    """
    Apply colour tags to SQL keywords inside a Tkinter Text widget.

    Args:
        text_widget : tkinter.Text
            The text area to be colourised.

    Returns:
        None
    """
    # Clear existing tags
    text_widget.tag_remove("sql_keyword", "1.0", "end")
    text_widget.tag_remove("sql_comment_line", "1.0", "end")
    text_widget.tag_remove("sql_comment_block", "1.0", "end")

    # Configure styles
    text_widget.tag_configure("sql_keyword", foreground="#3B5C8A")
    text_widget.tag_configure("sql_comment_line", foreground="#4F7F6F")
    text_widget.tag_configure("sql_comment_block", foreground="#4F7F6F")

    text = text_widget.get("1.0", "end-1c")

    # --- Pass 1 : block comments /* ... */ (multi-line) ---
    for m in re.finditer(r"/\*.*?\*/", text, flags=re.DOTALL):
        start = text_widget.index(f"1.0+{m.start()}c")
        end = text_widget.index(f"1.0+{m.end()}c")
        text_widget.tag_add("sql_comment_block", start, end)

    # --- Pass 2 : line comments -- ... (single line) ---
    lines = text.split("\n")
    for i, line in enumerate(lines):
        col = line.find("--")
        if col != -1:
            start = f"{i + 1}.{col}"
            end = f"{i + 1}.end"
            text_widget.tag_add("sql_comment_line", start, end)

    # --- Pass 3 : keywords (only outside comments) ---
    for i, line in enumerate(lines):
        for match in re.finditer(r"\b\w+\b", line):
            word = match.group(0)
            if word.upper() not in SQL_KEYWORDS:
                continue

            start_col, end_col = match.span()
            start = f"{i + 1}.{start_col}"
            end = f"{i + 1}.{end_col}"

            # Skip if inside any comment
            if text_widget.tag_nextrange("sql_comment_line", start, end):
                continue
            if text_widget.tag_nextrange("sql_comment_block", start, end):
                continue

            text_widget.tag_add("sql_keyword", start, end)

    # Ensure comments stay on top visually
    text_widget.tag_raise("sql_comment_block")
    text_widget.tag_raise("sql_comment_line")

    return None


def insert_linebreaks_before_keywords(sql_code: str) -> str:
    """
    Insert newlines before key SQL keywords (from LINEBREAK_KEYWORDS)
    in an idempotent way: repeated calls will not add redundant line breaks.
    """
    formatted = sql_code

    for keyword in sorted(LINEBREAK_KEYWORDS, key=len, reverse=True):
        formatted = re.sub(
            rf"(?<!\n)\b{re.escape(keyword)}\b",
            rf"\n{keyword}",
            formatted,
            flags=re.IGNORECASE
        )

    # Remove trailing spaces before newline (safe)
    formatted = re.sub(r"[ \t]+\n", "\n", formatted)

    # Keep up to 2 empty lines max:
    # 3+ empty lines -> exactly 2 empty lines (i.e. 3 consecutive '\n')
    formatted = re.sub(r"\n{4,}", "\n\n\n", formatted)

    return formatted.rstrip()




def on_closing(window, pre_close=None):
    """
    Save recent files, execute an optional pre-close hook, and close the window.

    Args:
        window : tkinter.Tk
            The main window to close.
        pre_close : callable or None
            Optional function to run before closing.

    Returns:
        None
    """
    save_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)
    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)

    if callable(pre_close):
        try:
            pre_close()
        except Exception:
            pass

    window.destroy()
    return None


def update_recent_sql_files(filepath, max_items=10):
    """
    Update the list of recent SQL files, ensuring no duplicates
    and enforcing a maximum number of entries.

    Args:
        filepath : str
            Path of the file to move to the top of the list.
        max_items : int
            Maximum number of entries to keep.

    Returns:
        None
    """
    if filepath in global_vars.recent_sql_files:
        global_vars.recent_sql_files.remove(filepath)

    global_vars.recent_sql_files.insert(0, filepath)
    global_vars.recent_sql_files = global_vars.recent_sql_files[:max_items]

    save_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)
    return None


def load_recent_files(file_path, target_list, max_items=8):
    """
    Load a list of recent file paths from disk into a target list.

    Args:
        file_path : str
            Path to the text file on disk.
        target_list : list
            The in-memory list to overwrite.
        max_items : int
            Maximum number of entries to load.

    Returns:
        None
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
    Remove paths from recent_db_files that no longer exist on disk.

    Returns:
        None
    """
    global_vars.recent_db_files = [
        f for f in global_vars.recent_db_files if os.path.exists(f)
    ]
    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
    return None


def clean_recent_sql_files():
    """
    Remove paths from recent_sql_files that no longer exist on disk.

    Returns:
        None
    """
    global_vars.recent_sql_files = [
        f for f in global_vars.recent_sql_files if os.path.exists(f)
    ]
    save_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)
    return None


def display_result(output_box, text=None, chunks=None):
    """
    Display plain or styled result text in the output area.

    Args:
        output_box : tkinter.Text
            The output widget.
        text : str or None
            Plain text to display (mutually exclusive with 'chunks').
        chunks : list[tuple[str, str or None]] or None
            Styled mode: each element is a (string, tagname) pair.

    Returns:
        None
    """
    output_box.config(state='normal')

    if chunks is not None:
        for s, tag in chunks:
            if tag:
                output_box.insert("end", s, (tag,))
            else:
                output_box.insert("end", s)
        output_box.insert("end", "\n\n")
    elif text is not None:
        output_box.insert("end", text.rstrip() + "\n\n")

    output_box.see("end")
    output_box.config(state='disabled')
    return None


def clear_output(output_box):
    """
    Clear the entire output area.

    Args:
        output_box : tkinter.Text
            The output widget to clear.

    Returns:
        None
    """
    output_box.config(state='normal')
    output_box.delete("1.0", END)
    output_box.config(state='disabled')
    return None
