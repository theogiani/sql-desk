# global_vars.py
# Shared state and constants for the SQL Desk GUI
# Author: Théo Giani (2025)


# Font sizes
font_size_sql = 10
font_size_output = 12


# GUI colours (harmonised with logo tones)
bg_main = '#b9b9b4'
bg_frame = '#f2f2f2'
bg_textbox = '#eeeeee'
bg_button = '#c0c0c0'
text_colour = '#333333'
accent_colour = '#5c6bc0'


# Current selected database path
current_database = ''
current_connection = None

# Current SQL file path
current_sql_file = None


# Recent database and SQL file tracking
recent_sql_files = []
recent_db_files = []

RECENT_SQL_FILE_PATH = "recent_sql_files.txt"
RECENT_DB_FILE_PATH = "recent_db_files.txt"


# Optional references (e.g. to GUI widgets)
output_textbox = None
databases = []
