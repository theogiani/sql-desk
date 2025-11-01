# sql_desk.py
#
# SQL Desk – A lightweight SQL sandbox for teaching and learning
# Originally developed by Chris Roffey (2016) as a student practice tool
# Adapted and extended by Théo Giani (2025) for use in European Schools
#
# Features:
# - Execute SQL queries and display results
# - Track recent databases and recent SQL files
# - Create and open SQLite databases via the GUI
# - Syntax highlighting and Pretty Print for SQL code
# - Minimal, classroom-friendly Tkinter interface:
#   left pane = SQL editor, right pane = output console
#
# Project structure (design choice):
# - This file focuses on interface layout and widget wiring only.
#   It should not implement application logic beyond simple callbacks.
# - GUI_functions.py        : actions triggered by buttons/menus
# - database_management.py  : opening / creating / switching databases
# - utils.py                : formatting, output helpers, housekeeping
# - global_vars.py          : shared colours, fonts, state, etc.


from tkinter import *
from tkinter import font, simpledialog, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os, global_vars


from GUI_functions import (
    run_sql, get_tables, save_sql_code,
    open_sql_code, change_font_size, refresh_sql_file_menu,
    pretty_print_sql, refresh_db_file_menu, open_and_refresh, create_and_refresh
)

from utils import (load_recent_files, clear_output,
                    clean_recent_db_files, clean_recent_sql_files, on_closing)

from database_management import (
    create_new_database, choose_database, menu_open_database, close_active_connection
)

from tkinter import Button


# --- Main window setup ---
# Create the main application window, apply base colour theme and title.
window = Tk()
window.title('SQL Desk')
window.configure(bg=global_vars.bg_main)


# --- Load recent file lists on startup ---
# These files record the most recently used SQL scripts and database files.
load_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)
load_recent_files("recent_db_files.txt", global_vars.recent_db_files)


# --- Application logo (European Schools brushed aluminium style) ---
# We try to load the logo; if not found, we simply continue without failing.
try:
    euro_logo = PhotoImage(file='European_School_logoBR.png')
except:
    euro_logo = None
    

# --- Top row: left = Database menu button, middle = Quit button, right = logo ---
frame_buttons = Frame(window, bg=global_vars.bg_main)
frame_buttons.grid(row=0, column=0, sticky="nsew")
frame_buttons.grid_rowconfigure(0, weight=0)
frame_buttons.grid_columnconfigure((0, 1, 2), weight=0)

frame_logo = Frame(window, bg=global_vars.bg_main)
frame_logo.grid(row=0, column=1, sticky="ne")
if euro_logo:
    Label(frame_logo, image=euro_logo, bg=global_vars.bg_main).grid(row=0, column=0, sticky="ne")
    

# --- Quit button ---
# Uses the same shutdown path as clicking the [X] of the window:
# - saves recent files
# - closes any active DB connection
# - destroys the window cleanly
button_quit = Button(
    frame_buttons,
    text="Quit",
    width=10,
    bg=global_vars.bg_button,
    fg=global_vars.text_colour,
    command=lambda: on_closing(window, pre_close=lambda: close_active_connection(True))
)
button_quit.grid(row=0, column=2, padx=5, pady=10, sticky="n")


# --- SQL File menu (Open / Save / Recents) ---
# Menubutton instead of a traditional menubar: easier for students, obvious to click.
sql_file_button = Menubutton(frame_buttons, text="SQL File", bg=global_vars.bg_button, fg=global_vars.text_colour, relief=RAISED)
sql_file_menu = Menu(sql_file_button, tearoff=0)
sql_file_menu.add_command(label="Open SQL...", command=lambda: open_sql_code(sql_textbox, menu=sql_file_menu))
sql_file_menu.add_command(label="Save SQL...", command=lambda: save_sql_code(sql_textbox, sql_file_menu))
sql_file_menu.add_separator()
for i, filename in enumerate(global_vars.recent_sql_files, start=1):
    sql_file_menu.add_command(
        label=f"{i}. {os.path.basename(filename)}",
        command=lambda f=filename: [open_sql_code(sql_textbox, f), refresh_sql_file_menu(sql_file_menu, sql_textbox)]
    )
sql_file_button.config(menu=sql_file_menu)
sql_file_button.grid(row=0, column=3, padx=5, pady=10, sticky="n")


# --- Main layout: a vertical PanedWindow containing a horizontal PanedWindow ---
# Top row (row=0) is buttons/logo.
# Row=1 is a resizable split pane: left = SQL editor, right = output console.
main_paned = PanedWindow(window, orient=VERTICAL)
main_paned.grid(row=1, column=0, columnspan=2, sticky="nsew")

horizontal_paned = PanedWindow(main_paned, orient=HORIZONTAL)

frame_query = Frame(bg=global_vars.bg_frame)
frame_output = Frame(bg=global_vars.bg_frame)

horizontal_paned.add(frame_query)
horizontal_paned.add(frame_output)
main_paned.add(horizontal_paned)

main_paned.paneconfigure(horizontal_paned, stretch="always")
horizontal_paned.paneconfigure(frame_query, stretch="always")
horizontal_paned.paneconfigure(frame_output, stretch="always")

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)


# --- SQL Query frame ---
# Left-hand pane: an SQL "shell" text area + action buttons.
Label(frame_query, text='SQL Shell :', bg=global_vars.bg_frame, fg=global_vars.text_colour).grid(row=0, column=0, sticky="nw")
sql_font = font.Font(family="Courier", size=global_vars.font_size_sql)

sql_textbox = ScrolledText(frame_query, width=60, height=10, background=global_vars.bg_textbox, font=sql_font)
sql_textbox.grid(row=1, column=0, sticky="nsew")


# --- Keyboard shortcuts (Ctrl+...) on the SQL editor ---
# - Ctrl+Z / Ctrl+Y (and Ctrl+Shift+Z): undo / redo
# - Ctrl+S: save SQL to file
# The text widget has undo buffering enabled so pupils can safely experiment.
sql_textbox.config(undo=True, maxundo=2000, autoseparators=True)
window.bind("<Control-z>", lambda e: (sql_textbox.event_generate("<<Undo>>"), "break")[1])
window.bind("<Control-y>", lambda e: (sql_textbox.event_generate("<<Redo>>"), "break")[1])
window.bind("<Control-Shift-Z>", lambda e: (sql_textbox.event_generate("<<Redo>>"), "break")[1])
window.bind("<Control-s>", lambda e: (save_sql_code(sql_textbox, sql_file_menu), "break")[1])


# Refresh the “recent SQL files” menu now that the widget exists.
clean_recent_sql_files()
refresh_sql_file_menu(sql_file_menu, sql_textbox)


# --- Buttons below the SQL editor (Run / List Tables / Pretty Print / Font size) ---
button_frame = Frame(frame_query, bg=global_vars.bg_frame)
button_frame.grid(row=2, column=0, sticky="nw", pady=2)

Button(
    button_frame,
    text="Run SQL",
    width=10,
    bg=global_vars.bg_button,
    fg=global_vars.text_colour,
    command=lambda: run_sql(sql_textbox, output_textbox)
).pack(side=LEFT)

Button(
    button_frame,
    text="List Tables",
    width=12,
    bg=global_vars.bg_button,
    fg=global_vars.text_colour,
    command=lambda: get_tables(output_textbox)
).pack(side=LEFT, padx=10)

Button(
    button_frame,
    text="Pretty Print",
    width=12,
    bg=global_vars.bg_button,
    fg=global_vars.text_colour,
    command=lambda: pretty_print_sql(sql_textbox)
).pack(side=LEFT)

sql_font_size_var = StringVar()
sql_font_size_var.set(str(global_vars.font_size_sql))
OptionMenu(
    button_frame,
    sql_font_size_var,
    *[str(size) for size in range(8, 25, 2)],
    command=lambda sel: change_font_size(sel, sql_font, "sql")
).pack(side=LEFT, padx=10)

frame_query.grid_rowconfigure(1, weight=1)
frame_query.grid_columnconfigure(0, weight=1)


# --- Output frame ---
# Right-hand pane: read-only console style output.
# Used to show query results, table listings, status messages, etc.
Label(frame_output, text='Output :', bg=global_vars.bg_frame, fg=global_vars.text_colour).grid(row=0, column=0, sticky="nw")
output_font = font.Font(family="Courier", size=global_vars.font_size_output)

output_textbox = ScrolledText(frame_output, width=75, height=20, background=global_vars.bg_textbox, font=output_font)
output_textbox.grid(row=1, column=0, sticky="nsew")
output_textbox.config(state='disabled')

# Styling tags for structured output:
# - "pk"     : primary keys in red
# - "tbl"    : table names in bold
# - "comma"  : commas in light grey for readability
output_textbox.tag_config("pk", foreground="red")
output_textbox.tag_config("tbl", font=("Courier", global_vars.font_size_output, "bold"))
output_textbox.tag_config("comma", foreground="#888888")


# --- Database menu button ---
# This replaces the old-style menubar.
# It groups:
#   - "Connect to a Database..."  (open existing .db)
#   - "Create New Database..."    (new .db via Save-As)
#   - recently opened databases
# The menu is refreshed live so the list stays current.
db_button = Menubutton(
    frame_buttons,
    text="Database",
    bg=global_vars.bg_button,
    fg=global_vars.text_colour,
    relief=RAISED
)

db_menu = Menu(db_button, tearoff=0)
db_button.config(menu=db_menu)


# Entry: connect to an existing database file
db_menu.add_command(
    label="Connect to a Database...",
    command=lambda: open_and_refresh(db_menu, output_textbox, window, choose_database, menu_open_database)
)

# Entry: create a brand new database file, then connect to it
db_menu.add_command(
    label="Create New Database...",
    command=lambda: create_and_refresh(db_menu, output_textbox, window, choose_database, create_new_database)
)

# Separator between actions and recent files
db_menu.add_separator()

# Populate the list of recent databases (and clean broken paths)
refresh_db_file_menu(db_menu, output_textbox, window, select_database=choose_database)
clean_recent_db_files()

# Place the Database menu button in the top bar (left side)
db_button.grid(row=0, column=0, padx=10, pady=10, sticky="n")


# --- Output frame controls (Clear output, Output font size) ---
button_frame_out = Frame(frame_output, bg=global_vars.bg_frame)
button_frame_out.grid(row=2, column=0, sticky="nw", pady=2)

Button(
    button_frame_out,
    text="Clear result box",
    bg=global_vars.bg_button,
    fg=global_vars.text_colour,
    command=lambda: clear_output(output_textbox)
).pack(side=LEFT)

output_font_size_var = StringVar()
output_font_size_var.set(str(global_vars.font_size_output))
OptionMenu(
    button_frame_out,
    output_font_size_var,
    *[str(size) for size in range(8, 25, 2)],
    command=lambda sel: change_font_size(sel, output_font, "output")
).pack(side=LEFT, padx=10)

frame_output.grid_rowconfigure(1, weight=1)
frame_output.grid_columnconfigure(0, weight=1)


# --- Window close behaviour ---
# Clicking the window's [X] should:
# - save recent file lists
# - (optionally) close DB connection
# - exit cleanly
window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))


# --- Main loop ---
window.mainloop()
