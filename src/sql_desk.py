# sql_desk.py

# SQL Desk – A lightweight SQL sandbox for teaching and learning
# Originally developed by Chris Roffey (2016) as a student practice tool
# Adapted and extended by Théo Giani (2025) for use in European Schools

# Features:
# - Query execution, recent file tracking, SQL script load/save
# - Syntax highlighting and query prettifier
# - Simple database creation and management
# - Tkinter GUI with dual-pane layout (Query / Output) and top menu

# Architecture:
# - GUI_functions.py: logic for queries, menus, file operations
# - database_management.py: DB creation and loading
# - utils.py: formatting tools, file I/O
# - global_vars.py: shared settings and state



from tkinter import *
from tkinter import font#, simpledialog, filedialog
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


# --- Main window setup ---
window = Tk()
window.title('SQL Desk')
window.configure(bg=global_vars.bg_main)


# --- Load recent files ---
load_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)
load_recent_files("recent_db_files.txt", global_vars.recent_db_files)


# --- Euro logo ---
try:
    euro_logo = PhotoImage(file='European_School_logoBR.png')
except:
    euro_logo = None
    

# --- Top frame: logo + menu buttons ---
frame_buttons = Frame(window, bg=global_vars.bg_main)
frame_buttons.grid(row=0, column=0, sticky="nsew")
frame_buttons.grid_rowconfigure(0, weight=0)
frame_buttons.grid_columnconfigure((0, 1, 2), weight=0)

frame_logo = Frame(window, bg=global_vars.bg_main)
frame_logo.grid(row=0, column=1, sticky="ne")
if euro_logo:
    Label(frame_logo, image=euro_logo, bg=global_vars.bg_main).grid(row=0, column=0, sticky="ne")
    

# --- Quit button ---
# Use the same close path as the window's [X] to ensure proper shutdown + saving recents
button_quit = Button(
    frame_buttons,
    text="Quit",
    width=10,
    bg=global_vars.bg_button,
    fg=global_vars.text_colour,
    command=lambda: on_closing(window, pre_close=lambda: close_active_connection(True))
)
button_quit.grid(row=0, column=2, padx=5, pady=10, sticky="n")




# --- SQL File Menu ---
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



# --- Main Paned layout (Query / Output) ---
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


# --- SQL Query Frame ---
Label(frame_query, text='SQL Shell :', bg=global_vars.bg_frame, fg=global_vars.text_colour).grid(row=0, column=0, sticky="nw")
sql_font = font.Font(family="Courier", size=global_vars.font_size_sql)

sql_textbox = ScrolledText(frame_query, width=60, height=10, background=global_vars.bg_textbox, font=sql_font)
sql_textbox.grid(row=1, column=0, sticky="nsew")

clean_recent_sql_files()
refresh_sql_file_menu(sql_file_menu, sql_textbox)


button_frame = Frame(frame_query, bg=global_vars.bg_frame)
button_frame.grid(row=2, column=0, sticky="nw", pady=2)
Button(button_frame, text="Run SQL", width=10, bg=global_vars.bg_button, fg=global_vars.text_colour,
       command=lambda: run_sql(sql_textbox, output_textbox)).pack(side=LEFT)
Button(button_frame, text="List Tables", width=12, bg=global_vars.bg_button, fg=global_vars.text_colour,
       command=lambda: get_tables(output_textbox)).pack(side=LEFT, padx=10)
Button(button_frame, text="Pretty Print", width=12, bg=global_vars.bg_button, fg=global_vars.text_colour,
       command=lambda: pretty_print_sql(sql_textbox)).pack(side=LEFT)
sql_font_size_var = StringVar()
sql_font_size_var.set(str(global_vars.font_size_sql))
OptionMenu(button_frame, sql_font_size_var, *[str(size) for size in range(8, 25, 2)],
           command=lambda sel: change_font_size(sel, sql_font, "sql")).pack(side=LEFT, padx=10)
frame_query.grid_rowconfigure(1, weight=1)
frame_query.grid_columnconfigure(0, weight=1)


# --- Output Frame ---
Label(frame_output, text='Output :', bg=global_vars.bg_frame, fg=global_vars.text_colour).grid(row=0, column=0, sticky="nw")
output_font = font.Font(family="Courier", size=global_vars.font_size_output)
output_textbox = ScrolledText(frame_output, width=75, height=20, background=global_vars.bg_textbox, font=output_font)
output_textbox.grid(row=1, column=0, sticky="nsew")
output_textbox.config(state='disabled')


# --- DB Menu (Open/Create + recent) ---
# Crée le bouton vide
db_button = Menubutton(frame_buttons, text="Database", bg=global_vars.bg_button,
                       fg=global_vars.text_colour, relief=RAISED)

# Crée le menu et l'attache immédiatement
db_menu = Menu(db_button, tearoff=0)
db_button.config(menu=db_menu)







# Entrée : Open Database
db_menu.add_command(
    label="Open Database...",
    command=lambda: open_and_refresh(db_menu, output_textbox, window, choose_database, menu_open_database)
)
##db_menu.add_command(
##    label="Open Database...",
##    command=lambda: (
##        menu_open_database(output_textbox, window, db_menu)
##    )
##)

# Entrée : Create New Database
db_menu.add_command(
    label="Create New Database...",
    command=lambda: create_and_refresh(db_menu, output_textbox, window, choose_database, create_new_database)
)
##db_menu.add_command(
##    label="Create New Database...",
##    command=lambda: (
##        create_new_database(output_textbox, window, db_menu)
##    )
##)


# Séparateur
db_menu.add_separator()

# Ajoute les bases récentes
refresh_db_file_menu(db_menu, output_textbox, window, select_database=choose_database)
clean_recent_db_files()

# Place le bouton sur l’interface
db_button.grid(row=0, column=0, padx=10, pady=10, sticky="n")


### --- DB Menu (Open/Create + recent) ---
##db_button = Menubutton(frame_buttons, text="Database",
##                       bg=global_vars.bg_button, fg=global_vars.text_colour, relief=RAISED)
##db_menu = Menu(db_button, tearoff=0)
##db_button.config(menu=db_menu)
##
### Entrées fixes
##db_menu.add_command(
##    label="Open Database...",
##    command=lambda: menu_open_database(output_textbox, window, db_menu)
##)
##db_menu.add_command(
##    label="Create New Database...",
##    command=lambda: create_new_database(output_textbox, window, db_menu)
##)
##db_menu.add_separator()
##
### Fichiers récents
##refresh_db_file_menu(db_menu, output_textbox, window)
##
### Nettoie les doublons / fichiers manquants
##clean_recent_db_files()
##
### Place le bouton sur l’interface
##db_button.grid(row=0, column=0, padx=10, pady=10, sticky="n")



button_frame_out = Frame(frame_output, bg=global_vars.bg_frame)
button_frame_out.grid(row=2, column=0, sticky="nw", pady=2)
Button(button_frame_out, text="Clear result box", bg=global_vars.bg_button, fg=global_vars.text_colour,
       command=lambda: clear_output(output_textbox)).pack(side=LEFT)
output_font_size_var = StringVar()
output_font_size_var.set(str(global_vars.font_size_output))
OptionMenu(button_frame_out, output_font_size_var, *[str(size) for size in range(8, 25, 2)],
           command=lambda sel: change_font_size(sel, output_font, "output")).pack(side=LEFT, padx=10)
frame_output.grid_rowconfigure(1, weight=1)
frame_output.grid_columnconfigure(0, weight=1)


# --- Quit + save recent ---
window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))


# --- Main loop ---
window.mainloop()
