# SQL Desk

**SQL Desk** is an educational tool designed to help students practise writing SQL queries in a safe, user-friendly environment. It was developed by Théo Giani as part of a pedagogical initiative at the European School of Varese.

---

## 🎯 Purpose

This program allows students to:
- Select a sample SQLite database
- Write and run SQL queries interactively
- View formatted results and tables
- Understand basic database concepts

It is designed for use in ICT and Computer Science courses (e.g. IGCSE, European Schools syllabus).

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.10+
- No external libraries required (only `tkinter` and `sqlite3`, both included in standard Python)

### 📁 Required Files

To run **SQL Desk** locally, ensure that the following Python files are present in the same folder:

- `sql_desk.py`               ← main program
- `GUI_functions.py`
- `sql_functions.py`
- `database_management.py`
- `utils.py`
- `global_vars.py`

Recommended but optional:
- A folder `sample_databases/` containing test databases like `Library.db`

---

## ▶️ How to Run

From a terminal or your Python IDE, run:

```bash
python sql_desk.py
