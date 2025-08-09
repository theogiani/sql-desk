# SQL Desk – Updated Call Map

## GUI_functions.py

### `change_font_size(selection, target_font, font_type)`
- **Doc:** Updates font size in SQL or output box
- **Calls:** int, target_font.configure
- **Called by:** (none)

### `get_tables(output_textbox)`
- **Doc:** Displays table names and columns in current DB
- **Calls:** conn.close, conn.cursor, cursor.execute, cursor.fetchall, display_result, join, lines.append, output_textbox.config, sqlite3.connect
- **Called by:** (none)

### `open_sql_code(sql_textbox, filepath, menu)`
- **Doc:** Opens SQL file and inserts it into editor
- **Calls:** f.read, filedialog.askopenfilename, messagebox.showerror, open, pretty_print_sql, refresh_sql_file_menu, sql_textbox.after, sql_textbox.delete, sql_textbox.insert, update_recent_sql_files
- **Called by:** GUI_functions.py.refresh_sql_file_menu

### `pretty_print_sql(sql_textbox)`
- **Doc:** Applies keyword capitalisation, linebreaks, and colouring
- **Calls:** colorize_keywords, highlight_keywords, insert_linebreaks_before_keywords, re.sub, sql_textbox.delete, sql_textbox.get, sql_textbox.insert
- **Called by:** GUI_functions.py.open_sql_code, GUI_functions.py.run_sql

### `refresh_sql_file_menu(menu, textbox)`
- **Doc:** Refreshes SQL file menu with recent files
- **Calls:** enumerate, menu.add_command, menu.add_separator, menu.delete, open_sql_code, os.path.basename, save_sql_code
- **Called by:** GUI_functions.py.open_sql_code, GUI_functions.py.save_sql_code

### `run_sql(sql_textbox, output_textbox)`
- **Doc:** Execute the selected SQL (if any) or the whole editor content.
- **Calls:** conn.commit, conn.cursor, conn.execute, cur.execute, cur.fetchall, display_result, enumerate, make_pretty_table, pretty_print_sql, split_sql_statements, sql_textbox.get, sql_textbox.tag_ranges, sqlite3.connect, strip
- **Called by:** (none)

### `save_sql_code(sql_textbox, menu)`
- **Doc:** Saves formatted SQL to file
- **Calls:** f.write, filedialog.asksaveasfilename, highlight_keywords, open, print, refresh_sql_file_menu, sql_textbox.get, update_recent_sql_files
- **Called by:** GUI_functions.py.refresh_sql_file_menu

### `split_sql_statements(sql_code)`
- **Doc:** Split SQL code into complete statements using sqlite3.complete_statement(),
- **Calls:** buffer.strip, sqlite3.complete_statement, statements.append
- **Called by:** GUI_functions.py.run_sql


## database_management.py

### `choose_database(value, output_textbox, window, db_menu)`
- **Doc:** Sets current database, prints message, updates window title,
- **Calls:** dict.fromkeys, display_result, global_vars.recent_db_files.insert, global_vars.recent_db_files.remove, list, os.path.basename, os.path.exists, refresh_db_file_menu, save_recent_files, window.title
- **Called by:** database_management.py.menu_open_database, database_management.py.refresh_db_file_menu

### `create_new_database(output_textbox, window, db_menu)`
- **Doc:** Prompts user to name a new .db file and creates it.
- **Calls:** dict.fromkeys, display_result, global_vars.recent_db_files.insert, list, open, refresh_db_file_menu, save_recent_files, simpledialog.askstring
- **Called by:** database_management.py.refresh_db_file_menu

### `menu_open_database(output_textbox, window, db_menu)`
- **Doc:** Opens a .db file and sets it as current database.
- **Calls:** choose_database, filedialog.askopenfilename
- **Called by:** database_management.py.refresh_db_file_menu

### `refresh_db_file_menu(db_menu, output_textbox, window)`
- **Calls:** choose_database, create_new_database, db_menu.add_command, db_menu.add_separator, db_menu.delete, enumerate, menu_open_database, os.path.basename
- **Called by:** database_management.py.choose_database, database_management.py.create_new_database


## utils.py

### `clean_recent_db_files()`
- **Doc:** Removes non-existing .db files from recent_db_files.
- **Calls:** os.path.exists, save_recent_files
- **Called by:** (none)

### `clean_recent_sql_files()`
- **Doc:** Removes non-existing .sql files from recent_sql_files.
- **Calls:** os.path.exists, save_recent_files
- **Called by:** (none)

### `clear_output(output_box)`
- **Doc:** Clears the output area
- **Calls:** output_box.config, output_box.delete
- **Called by:** (none)

### `colorize_keywords(text_widget)`
- **Doc:** Applies colour tag to SQL keywords in Text widget.
- **Calls:** enumerate, match.group, match.span, re.finditer, split, text_widget.get, text_widget.tag_add, text_widget.tag_configure, text_widget.tag_remove, word.upper
- **Called by:** GUI_functions.py.pretty_print_sql

### `display_result(output_box, text)`
- **Doc:** Displays result text in output area
- **Calls:** output_box.config, output_box.insert, output_box.see, text.rstrip
- **Called by:** GUI_functions.py.get_tables, GUI_functions.py.run_sql, database_management.py.choose_database, database_management.py.create_new_database

### `highlight_keywords(query)`
- **Doc:** Converts known SQL keywords to uppercase.
- **Calls:** match.group, match.span, re.finditer, word.upper
- **Called by:** GUI_functions.py.pretty_print_sql, GUI_functions.py.save_sql_code

### `insert_linebreaks_before_keywords(sql_code)`
- **Doc:** Inserts newlines before key SQL keywords (from LINEBREAK_KEYWORDS),
- **Calls:** formatted.strip, re.escape, re.sub, sorted
- **Called by:** GUI_functions.py.pretty_print_sql

### `load_recent_files(file_path, target_list, max_items)`
- **Doc:** Loads recent files into the target list.
- **Calls:** line.strip, open, os.path.exists, print, target_list.clear, target_list.extend
- **Called by:** (none)

### `make_pretty_table(info, body)`
- **Doc:** Returns a Markdown-style table from query result.
- **Calls:** join, len, max, range, str
- **Called by:** GUI_functions.py.run_sql

### `on_closing(window)`
- **Doc:** Saves recent files and closes window.
- **Calls:** save_recent_files, window.destroy
- **Called by:** (none)

### `save_recent_files(file_path, source_list)`
- **Doc:** Saves list of recent files to disk.
- **Calls:** f.write, open, print
- **Called by:** database_management.py.choose_database, database_management.py.create_new_database, utils.py.clean_recent_db_files, utils.py.clean_recent_sql_files, utils.py.on_closing, utils.py.update_recent_sql_files

### `update_recent_sql_files(filepath, max_items)`
- **Calls:** global_vars.recent_sql_files.insert, global_vars.recent_sql_files.remove, save_recent_files
- **Called by:** GUI_functions.py.open_sql_code, GUI_functions.py.save_sql_code

