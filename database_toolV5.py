#### database_toolV4.py
# A teaching tool for students studying IGCSE to help them practice
# making SQL queries required in the database section of the syllabus.
# Author - Chris Roffey 2016, adapted and redesigned by Théo Giani 2025

from tkinter import *
from tkinter import font, simpledialog, filedialog
from tkinter.scrolledtext import ScrolledText
import global_vars
from GUI_functions import (
    run_query, get_tables, build_database,
    choose_database, clear_output, save_sql_code,
    open_sql_code, change_font_size, refresh_sql_file_menu,
    refresh_db_file_menu
)
from utils import load_recent_files, save_recent_files


# ------------------------#### database_toolV4.py
# A teaching tool for students studying IGCSE to help them practice
# making SQL queries required in the database section of the syllabus.
# Author - Chris Roffey 2016, adapted and redesigned by Théo Giani 2025

from tkinter import *
from tkinter import font, simpledialog, filedialog
from tkinter.scrolledtext import ScrolledText
import global_vars
from GUI_functions import (
    run_query, get_tables, build_database,
    choose_database, clear_output, save_sql_code,
    open_sql_code, change_font_size
)


# Ouvrir une base existante
def menu_open_database():
    filepath = filedialog.askopenfilename(
        title="Open Database",
        filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")]
    )
    if filepath:
        global_vars.current_database = filepath
        output_textbox.config(state='normal')
        output_textbox.insert(END, f"Opened database: {filepath}\n")
        output_textbox.config(state='disabled')

# Créer une nouvelle base de données
def create_new_database():
    name = simpledialog.askstring("New Database", "Enter name for new database (without .db):")
    if name:
        filename = f"{name}.db"
        with open(filename, "w"):  # crée un fichier vide
            pass
        global_vars.current_database = filename
        output_textbox.config(state='normal')
        output_textbox.insert(END, f"Created new database: {filename}\n")
        output_textbox.config(state='disabled')



# ------------------------
# Couleurs harmonisées avec logo metal brossé
# ------------------------
bg_main = '#b9b9b4'  # Mise à jour selon le bord du logo
bg_frame = '#f2f2f2'
bg_textbox = '#eeeeee'
bg_button = '#c0c0c0'
text_colour = '#333333'
accent_colour = '#5c6bc0'

# ------------------------
# Fenêtre principale
# ------------------------
window = Tk()
window.title('Python Database Tool')
window.configure(bg=bg_main)


# ------------------------
# Fichiers recents
# ------------------------
load_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)
load_recent_files("recent_db_files.txt", global_vars.recent_db_files)



# Logo (facultatif)
try:
    euro_logo = PhotoImage(file='European_School_logoBR.png')
except:
    euro_logo = None
    

# ------------------------
# Cadres supérieurs (logo + boutons)
# ------------------------
frame_buttons = Frame(window, bg=bg_main)
frame_buttons.grid(row=0, column=0, sticky="nsew")
frame_buttons.grid_rowconfigure(0, weight=0)
frame_buttons.grid_columnconfigure((0, 1, 2), weight=0)


frame_logo = Frame(window, bg=bg_main)
frame_logo.grid(row=0, column=1, sticky="ne")
if euro_logo:
    Label(frame_logo, image=euro_logo, bg=bg_main).grid(row=0, column=0, sticky="ne")

# Boutons du haut centrés verticalement avec espacements

# Database Menu (Open/Create + récents)
db_button = Menubutton(frame_buttons, text="Database", bg=bg_button, fg=text_colour, relief=RAISED)
db_menu = Menu(db_button, tearoff=0)

db_menu.add_command(label="Open Database...", command=lambda: choose_database(window, output_textbox, None, db_menu))
db_menu.add_command(label="Create New Database...", command=create_new_database)
db_menu.add_separator()

##for filename in global_vars.recent_db_files:
##    db_menu.add_command(
##        label=f"Recent: {filename}",
##        command=lambda f=filename: choose_database(window, output_textbox, f, db_menu)
##    )

db_button.config(menu=db_menu)
db_button.grid(row=0, column=0, padx=10, pady=10, sticky="n")


##button_tables = Button(frame_buttons, text="List Tables", width=15, bg=bg_button, fg=text_colour,
##                       command=lambda: get_tables(output_textbox))

button_quit = Button(frame_buttons, text="Quit", width=10, bg=bg_button, fg=text_colour,
                     command=window.quit)

##button_tables.grid(row=0, column=1, padx=5, pady=10, sticky="n")
button_quit.grid(row=0, column=2, padx=5, pady=10, sticky="n")


# SQL File Menu (Open/Save + récents)
sql_file_button = Menubutton(frame_buttons, text="SQL File", bg=bg_button, fg=text_colour, relief=RAISED)
sql_file_menu = Menu(sql_file_button, tearoff=0)

sql_file_menu.add_command(
    label="Open SQL...",
    command=lambda: [open_sql_code(sql_textbox), refresh_sql_file_menu(sql_file_menu, sql_textbox)]
)
##sql_file_menu.add_command(
##    label="Save SQL...",
##    command=lambda: [save_sql_code(sql_textbox), refresh_sql_file_menu(sql_file_menu, sql_textbox)]
##)

sql_file_menu.add_command(label="Save SQL...", command=lambda: save_sql_code(sql_textbox, sql_file_menu))


sql_file_menu.add_separator()

# Ajouter les fichiers récents s’ils existent
for filename in global_vars.recent_sql_files:
    sql_file_menu.add_command(
        label=f"Recent: {filename}",
        command=lambda f=filename: [open_sql_code(sql_textbox, f), refresh_sql_file_menu(sql_file_menu, sql_textbox)]
    )


    

sql_file_button.config(menu=sql_file_menu)
sql_file_button.grid(row=0, column=3, padx=5, pady=10, sticky="n")


# ------------------------
# Zone principale
# ------------------------
main_paned = PanedWindow(window, orient=VERTICAL)
main_paned.grid(row=1, column=0, columnspan=2, sticky="nsew")

horizontal_paned = PanedWindow(main_paned, orient=HORIZONTAL)
frame_query = Frame(bg=bg_frame)
frame_output = Frame(bg=bg_frame)
horizontal_paned.add(frame_query)
horizontal_paned.add(frame_output)

##frame_new_db = Frame(main_paned, bg=bg_frame)
##main_paned.add(horizontal_paned)
##main_paned.add(frame_new_db, minsize=40)

# Config stretch
main_paned.paneconfigure(horizontal_paned, stretch="always")
##main_paned.paneconfigure(frame_new_db, stretch="always")
horizontal_paned.paneconfigure(frame_query, stretch="always")
horizontal_paned.paneconfigure(frame_output, stretch="always")
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)


# ------------------------
# Frame: SQL Query
# ------------------------
Label(frame_query, text='SQL Shell :', bg=bg_frame, fg=text_colour).grid(row=0, column=0, sticky="nw")

sql_font = font.Font(family="Courier", size=global_vars.font_size_sql)

sql_textbox = Text(frame_query, width=60, height=10, background=bg_textbox, font=sql_font)
sql_textbox.grid(row=1, column=0, sticky="nsew")


refresh_sql_file_menu(sql_file_menu, sql_textbox)


button_frame = Frame(frame_query, bg=bg_frame)
button_frame.grid(row=2, column=0, sticky="nw", pady=2)

Button(button_frame, text="Run SQL", width=10, bg=bg_button, fg=text_colour,
       command=lambda: run_query(sql_textbox, output_textbox)).pack(side=LEFT)
Button(button_frame, text="List Tables", width=12, bg=bg_button, fg=text_colour,
       command=lambda: get_tables(output_textbox)).pack(side=LEFT, padx=10)

##Button(button_frame, text="Save SQL", width=10, bg=bg_button, fg=text_colour,
##       command=lambda: save_sql_code(sql_textbox)).pack(side=LEFT, padx=10)
##Button(button_frame, text="Open SQL", width=10, bg=bg_button, fg=text_colour,
##       command=lambda: open_sql_code(sql_textbox)).pack(side=LEFT, padx=5)

sql_font_size_var = StringVar()
sql_font_size_var.set(str(global_vars.font_size_sql))
sql_font_menu = OptionMenu(
    button_frame, sql_font_size_var, *[str(size) for size in range(8, 25, 2)],
    command=lambda sel: change_font_size(sel, sql_font, "sql")
)
sql_font_menu.pack(side=LEFT, padx=10)

frame_query.grid_rowconfigure(1, weight=1)
frame_query.grid_columnconfigure(0, weight=1)


# ------------------------
# Frame: Output
# ------------------------
Label(frame_output, text='Output :', bg=bg_frame, fg=text_colour).grid(row=0, column=0, sticky="nw")

output_font = font.Font(family="Courier", size=global_vars.font_size_output)

output_textbox = Text(frame_output, width=75, height=20, background=bg_textbox, font=output_font)
output_textbox.grid(row=1, column=0, sticky="nsew")
output_textbox.config(state='disabled')


refresh_db_file_menu(db_menu, output_textbox)


button_frame_out = Frame(frame_output, bg=bg_frame)
button_frame_out.grid(row=2, column=0, sticky="nw", pady=2)

Button(button_frame_out, text="Clear result box", bg=bg_button, fg=text_colour,
       command=lambda: clear_output(output_textbox)).pack(side=LEFT)

output_font_size_var = StringVar()
output_font_size_var.set(str(global_vars.font_size_output))
output_font_menu = OptionMenu(
    button_frame_out, output_font_size_var, *[str(size) for size in range(8, 25, 2)],
    command=lambda sel: change_font_size(sel, output_font, "output")
)
output_font_menu.pack(side=LEFT, padx=10)

frame_output.grid_rowconfigure(1, weight=1)
frame_output.grid_columnconfigure(0, weight=1)


def on_closing():
    save_recent_files("recent_sql_files.txt", global_vars.recent_sql_files)
    save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)


# ------------------------
# Boucle principale
# ------------------------
window.mainloop()
