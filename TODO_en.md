# SQL Desk — TODO (EN)

*List of planned features, bug fixes, and improvement ideas for **SQL Desk**.*

> This file is a structured, English re‑organisation of the original French TODO. Nothing has been removed unless it was strictly redundant. Historical notes are preserved in Part II.

---

## PART I — BACKLOG (TO‑DO)

### A. Critical items

* [ ] **Refactor – Database menu refresh:** decouple UI from DB logic

  * Move UI wiring (lambdas) to `sql_desk.py` and keep `database_management.py` pure (no Tkinter).
  * Add a pure helper (e.g. `get_recent_db_entries()`) returning recent DB items.
  * Define static menu items once; refresh only the dynamic “Recent DBs” section.
* [ ] **Create a database in a user‑chosen directory** (also listed under Major tracks — kept intentionally; see Part I‑B).
* [ ] **Show PK and FK in “List Tables”.**
* [ ] **Comment colouring for** `--` **and** `/* ... */`.
* [ ] **Add a SQL help file in English** (`HELP_SQL_BASICS.md`) plus a short user guide for SQL Desk.
* [ ] **Export query results to CSV or TXT.**
* [ ] **Optional export of results and SQL code to Markdown (`.md`).**
* [ ] **Local history of executed queries** (e.g., for quick recall; note: *keyboard shortcuts Ctrl+Z / Ctrl+Y / Ctrl+S are already handled in the editor*).
* [ ] **Preserve caret position and vertical scroll** in `sql_textbox` after `pretty_print_sql()` (**currently jumps to the top**).
* [ ] **Fix the “Quit” button.**
* [ ] **Refactor – `refresh_db_file_menu()`**: move lambda/UI concerns into `sql_desk.py`.
* [ ] **Suggested enhancement – Execution summary:** brief recap after running SQL (counts of statements, successes, errors).

#### Documentation / User Guide – Foreign keys

**PRAGMA foreign\_keys = ON;**
SQLite does not enforce referential integrity by default. In SQL Desk, the following command is executed automatically on every connection to ensure foreign keys (including composite keys) are enforced:

```sql
PRAGMA foreign_keys = ON;
```

Without this, one could insert in `Booking` an activity that does not exist in `Activity`, or one that mismatches the `resortName`, breaking query correctness and database consistency.
**Action:** document this behaviour clearly so users understand why the app always enables this option.

---

### B. Major tracks (post‑GitHub migration)

> To be integrated as soon as possible to support smooth execution of complete SQL scripts.

* [ ] Create a database in the desired directory (**duplicate of A; intentionally retained**).
* [ ] Display PK/FK in List Tables (**duplicate of A; intentionally retained**).
* [ ] Comment colouring for `--` and `/* ... */` (**duplicate of A; intentionally retained**).

---

### C. Pedagogical ideas

* [ ] Add example databases (e.g., `School.db`, `Library.db`, `Cinema.db`).
* [ ] Add a **student mode** (read‑only; no DROP/ALTER).
* [ ] Add a SQL help file in English (`HELP_SQL_BASICS.md`).
* [ ] Add a `README_fr.md` as a French user guide.

---

### D. Future development

* [ ] Export query results to CSV or TXT.
* [ ] Optional export of results and SQL code to Markdown (`.md`).
* [ ] Local history of executed queries.
* [ ] Multi‑language UI (English / French at minimum).
* [ ] Possible integration in a Jupyter‑like environment.
* [ ] Simple extension / plugin system (formatting helpers, snippets, etc.).

---

### E. Technical priorities

* [ ] **Simple Save (Ctrl+S) —** `GUI_functions.py`

  * Add `current_sql_file` to `global_vars.py` (path of the current file).
  * Implement `save_sql_code(sql_textbox, menu, force_save_as=False)`:

    * If `current_sql_file` exists and `force_save_as` is `False` ⇒ overwrite that file.
    * Otherwise ⇒ open a “Save As” dialog and update `current_sql_file`.
    * No Unicode in the code; end with `return None`.
  * **“SQL File” menu:**

    * Add **Save** (above **Save As**).
    * **Save** calls `save_sql_code(..., force_save_as=False)`.
    * **Save As** calls `save_sql_code(..., force_save_as=True)`.
  * **Shortcuts:**

    * **Ctrl+S** ⇒ Save (unless the file has not yet been named ⇒ Save As).
    * **Ctrl+Shift+S** ⇒ Save As.
  * **On “Open…”:** in `open_sql_code(...)`, set `global_vars.current_sql_file = filepath`.
  * **Acceptance criteria:**

    * Ctrl+S overwrites the same file if already named; otherwise opens Save As.
    * Menu shows **Save** and **Save As** correctly.
    * After **Open…**, Ctrl+S targets the opened file.
    * Errors handled with `messagebox.showerror`.

---

### F. Known issues & formatting notes

* **Line‑break at start** in `insert_linebreaks_before_keywords`:

  * **Situation:** if the text starts with a keyword (e.g., `SELECT`), the function inserts a `\n` at the very beginning, then `.strip()` removes it.
  * **Potential issue:** may cause problems if code is reused without `.strip()`.
  * **Planned fix:** avoid inserting `\n` when the keyword is at position 0 (negative look‑behind `(?<!^)` or index test).
  * **Status:** To do.

* **Remove spaces before line breaks** in `insert_linebreaks_before_keywords`:

  * After insertion, a space may remain before `\n` (e.g., `* \nFROM`).
  * **Solution:**

    ```python
    re.sub(r"[ \t]+\n", "\n", formatted)
    ```

* **SQL comment formatting & colouring**

  * **Situation:** `-- ...` (and later `/* ... */`) are not coloured and are affected by pretty print (e.g., keywords upper‑cased inside comments).
  * **Problem:** formatter modifies comment content (legibility, meaning).
  * **Objectives:**

    * Colour comments in the editor (e.g., grey/italic).
    * Exclude comments from `highlight_keywords` and other transforms.
  * **Approach:**

    * Step 1: line comments `--`; Step 2: block comments `/* ... */`.
    * Adapt `highlight_keywords(text)` to ignore segments marked as comments:

      * Line‑by‑line parse: split `code_part` / `comment_part` using `--`.
      * Uppercase only `code_part`, then concat `code_part + comment_part` unchanged.
    * (Optional) Add Tk tag `sql_comment` with `foreground="#888"` and `slant="italic"`.
  * **Status:** To do.

---

### G. File layout

| File                     | Main contents                                                        |
| ------------------------ | -------------------------------------------------------------------- |
| `utils.py`               | Stand‑alone utilities: file saves, table formatting, generic helpers |
| `database_management.py` | Database management: open/create/select DBs, update recent DB list   |
| `GUI_functions.py`       | Tkinter UI helpers: buttons, menus, text areas, UI refresh           |
| `sql_desk.py`            | Main script launching the app and initialising the UI                |
| `global_vars.py`         | Global variables and constants shared across modules                 |

---

## PART II — HISTORY & IN‑DEPTH NOTES

> This section preserves the chronological record and design notes from the original file.

### A. “Done” (historical checklist)

* [x] Insert a blank line after every output in the console, not just in `make_pretty_table` — **23 Jul 2025**

* [x] Allow execution of the **selected range** in the SQL editor, if any — **23 Jul 2025**

* [x] Allow execution of SQL scripts containing multiple `;`.

  #### \[Originally To‑Do] Multi‑statement script execution (`;`)

  **Goal:** execute a block with multiple statements (`DROP TABLE`, `CREATE`, `INSERT`, `SELECT`, etc.) separated by semicolons **in a single run**.

  **Pitfalls:**

  1. **Do not just `split(';')`:** a semicolon may appear **inside a string** (e.g., `'I like ; separators'`) and must not split.
  2. **Detect semicolons outside strings:** traverse SQL char‑by‑char while tracking state:

     * `in_single_quote = True/False`
     * `in_double_quote = True/False`
     * Only split on `;` **outside quotes**

  —> **Marked as done on 09 Aug 2025**

* [x] Refine automatic line breaks in SQL formatting:

  * Do **not** insert `\n` between `LEFT`, `RIGHT`, `INNER`, etc. and `JOIN`.
  * Add a line break before `JOIN` **only** when `JOIN` appears by itself.
    *(Implemented in `utils.py` on 22 Jul 2025.)*

* [x] Check scrollable areas (results, SQL editor, …) — **23 Jul 2025**

* [x] Ensure the "Recent files" menus (DB and SQL) update immediately — **23 Jul 2025**

  * Fixed immediate refresh of the menu after opening or saving files.
  * Passed `menu` parameter to `open_sql_code` and `save_sql_code`.
  * Menu refresh handled inside open/save functions.

* [ ] Check readability of long queries in the output area.

* [ ] Provide a clearer error when **no database** is selected.

---

### B. Changelog (by date)

#### 23 Jul 2025

* [x] Execute the **selected** SQL in the editor (when present).
  Updated `run_query` to detect a selection in the SQL widget. If there is a selection, only that part is executed; otherwise the whole editor content is executed.
  Preserved selection before/after pretty print to keep highlighting.
  Fixed issues executing multiple statements by consolidating older `run_sql` and `run_sql_pretty` into `run_query`.
  Updated UI so the **Run SQL** button triggers the unified function.

* Fixed immediate refresh of the "Recent files" menus (SQL and DB).
  Removed obsolete functions `run_sql` and `run_sql_pretty` (not used for a long time).
  Consider renaming `run_query` to `run_sql` later, especially if multi‑statement execution is expanded.

#### 22 Jul 2025

* Improved automatic line breaks re: `JOIN` handling.
* Reviewed scroll ergonomics (editor and output).

#### 25 Jul 2025 — Migration to `/src/` and recent DB menu refresh bugfix

* Moved main `.py` files to `src/`: `sql_desk.py`, `GUI_functions.py`, `database_management.py`, `utils.py`, `global_vars.py`.
* Recent DB menu now updates **without restart**: moved `refresh_db_file_menu()` from `utils.py` to `database_management.py` to avoid import cycles. It is now called at the end of `choose_database()` so open/create always refreshes the menu.
* Behaviour aligns with recent SQL files menu (which already refreshed immediately).
* Temporary debug `print()` calls left in place; **NEXT SESSION PRIORITY:** remove debug prints and the unused function in `sql_desk.py`.

#### Preserve caret and scroll in `pretty_print_sql` — ✅

**Context.** Reformatting would reset caret and viewport to top.

**Changes.**

* Save state before formatting:

  * caret: `insert_idx = sql_textbox.index("insert")`
  * selection: attempt `sel.first` / `sel.last`
  * vertical scroll: `top_frac = sql_textbox.yview()[0]`
  * horizontal scroll (if enabled): `x_frac = sql_textbox.xview()[0]`
* Make the format pass (line breaks, blank line after `;`, optional `--` comments, upper‑case keywords), wrapped as **one undo step** via `edit_separator()`.
* Replace buffer, recolour, and **restore** caret/selection/scroll. Ensure visibility with `see("insert")` and `focus_set()`.

**Notes.** Idempotent behaviour expected; tiny caret drifts may occur if text is inserted/removed before caret. Optional “cursor sentinel” can pin the logical position if ever required.

#### 09 Aug 2025 — Session progress

* **utils.py** – Improved `insert_linebreaks_before_keywords()` to avoid inserting an initial line break; tests validated.
* **TODO.md** – Updated entries for line‑break handling.
* **.gitignore** – Added `test*.py`.
* **GUI\_functions.py, database\_management.py, sql\_desk.py** – Minor adjustments.
* **EcoAdv.db** – Updated example DB.
* **Git** – Commit and push with a clear message.

**Planned rename of `run_query()` to `run_sql()`**
The new `run_sql()` would handle both a single query (or selected range) **and** a multi‑statement script separated by `;`.

#### 10 Aug 2025 — Show number of affected rows

* **Context:** display a message after `INSERT`/`UPDATE`/`DELETE` indicating how many rows were modified.
* **Target:** immediate feedback on the impact of write queries.
* **Files:** `sql_functions.py` (`run_sql()` or `run_query()` as currently implemented).
* **Detail:** use `cursor.rowcount` and append the info at the end of execution.

#### 10 Aug 2025 — Fix **Quit** button

* **Issue:** the **Quit** button was stopping the mainloop in the console, but the Tk window stayed open and usable.
* **Cause:** button used `window.quit` instead of `on_closing()` which saves recent files then closes properly.
* **Fix:** replace `command=window.quit` with `command=lambda: on_closing(window)` in `sql_desk.py`.
* **Result:** ensures recent file lists are saved and the window closes cleanly.
* **Files:** `sql_desk.py`, `utils.py` (`on_closing()` already present).

#### 10 Aug 2025 — Refactor database menu refresh

* **Goal:** separate UI from business logic and avoid rebuilding static items on every refresh.
* **Changes:**

  1. Moved `refresh_db_file_menu()` from `database_management.py` to `GUI_functions.py`.
  2. Keep initial creation of Database menu/button in `sql_desk.py` (static items `Open Database…`, `Create New Database…`).
  3. Update `refresh_db_file_menu()` to refresh **only** dynamic entries (recent DBs), e.g., `menu.delete(3, 'end')` after a separator.
  4. Updated `menu_open_database()` and `create_new_database()` to call the new UI‑level `refresh_db_file_menu()`.
* **Note:** chose import option 2 (let `database_management.py` import the UI refresher). This creates a mild cross‑import but is acceptable; monitor in later refactors.
* **Result:** same behaviour, with centralised UI and dynamic refresh only.

#### 12 Aug 2025 — Refactor Quit & connection handling; DB creation flow — ✅

* **Quit button:** now properly closes any open SQLite connections before exiting.
* **`run_sql()`:** stop creating a new connection every time; reuse `global_vars.current_connection` so there is a single persistent connection per session.
* **`create_new_database()`:**

  * Remove direct call to `refresh_db_file_menu()` (menu now refreshed by the GUI after creation).
  * Immediately open the new DB via `choose_database()` to apply unified connection and initialisation logic.
* **Compatibility** verified between `database_management.py` and `GUI_functions.py` post‑refactor.
* **Bug fix** in `make_pretty_table()` (argument order `headers, rows`) eliminating `object of type 'int' has no len()` errors on some `SELECT`s.
* **Comment clean‑up:** avoid any UTF‑8 non‑ASCII characters in code comments.

#### 13 Aug 2025 — Pretty Print affects SQL comments

* **Description:** `pretty_print_sql()` also transforms inside comments (e.g., adding a line break after a keyword found in a comment).
* **Impact:** comments can be distorted (e.g., `-- Schema based\nON the exercise ...`).
* **Proposed fix:** ignore any line starting with `--` (after trimming leading spaces). Consider `/* ... */` as well.
* **Priority:** Medium (visual impact; no SQL error).
* **Status:** To do.

#### 13 Aug 2025 — Truncated headers (first letter only)

* **Issue:** column names were reduced to their first letter (`a, n, g, c`…), making tables unreadable.
* **Cause:** `make_pretty_table()` used `[col[0] for col in info]` even when `info` was already `list[str]`, thus truncating each name to one character.
* **Fix:** add `isinstance(info[0], str)` guard and handle that case directly.
* **Status:** Fixed.

#### 17 Aug 2025 — PK/FK styling in table list — ✅

* Improved `get_tables()`: primary keys in red, foreign keys marked with `#`.
* Added `tag_config` in `sql_desk.py` to style text (PK red, FK hash, etc.).
* Updated `display_result()` in `utils.py` to accept both plain and tagged text; kept backward compatibility.
* Preserved append‑only behaviour for console output.
* Tested successfully with **SkillUp** DB: PKs shown in red, FKs marked with `#`.

#### 26 Aug 2025 — Editor shortcuts and undo — ✅

* **Keyboard shortcuts in the SQL editor**

  * Ctrl+Z → Undo
  * Ctrl+Y / Ctrl+Shift+Z → Redo
  * Ctrl+S → Save As (temporary)
* **Undo history enabled**

  * `undo=True`, `maxundo=2000`, `autoseparators=True`

**How it was done (brief):**
Enabled Tkinter’s native undo on `ScrolledText`; bound `Ctrl+Z` → `<<Undo>>`, `Ctrl+Y` / `Ctrl+Shift+Z` → `<<Redo>>`, `Ctrl+S` → `save_sql_file()`; `save_sql_file()` opens `asksaveasfilename`, writes UTF‑8, and handles errors with `messagebox`.

**Notes:**
Simple **Save** (overwrite) is not implemented yet; for now, **Ctrl+S** always triggers Save As.

---

## PART III — OPTIONAL APPENDICES

### A. Creation of new databases — UI improvement (kept from the original text)

**Current situation**

* Uses `simpledialog.askstring` to request only a filename.
* DB is created in the working directory.
* No folder choice; risk of invalid names; potential overwrite without warning.

**Problem**

* User cannot choose the file location.
* Filenames may contain problematic characters (spaces, accents, etc.).
* No check before overwriting existing files.

**Desired improvement**

* Use `filedialog.asksaveasfilename` to let the user choose **both** name and location.
* Add `.db` by default via `defaultextension`.
* Let Tkinter prompt before overwriting.

**How to proceed**

1. Replace `askstring` with `asksaveasfilename`.
2. Check for a non‑empty `filepath` (user may cancel).
3. Create the file at the chosen location.
4. Update `global_vars.current_database` with the full path.
5. Add this path to `recent_db_files` like in `menu_open_database`.

**Minimal example**

```python
def create_new_database(output_textbox, window=None, db_menu=None):
    filepath = filedialog.asksaveasfilename(
        title="Create New Database",
        defaultextension=".db",
        filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
    )
    if filepath:
        with open(filepath, "w"):
            pass
        global_vars.current_database = filepath
        display_result(output_textbox, f"Created new database: {os.path.basename(filepath)}")
        global_vars.recent_db_files.insert(0, filepath)
        global_vars.recent_db_files = list(dict.fromkeys(global_vars.recent_db_files))[:10]
        save_recent_files("recent_db_files.txt", global_vars.recent_db_files)
        if db_menu is not None:
            refresh_db_file_menu(db_menu, output_textbox, window)
```

### B. Quit button — clean exit (kept from the original text)

**Goal:** make **Quit** call `window.destroy()` (or `root.destroy()`), optionally with a confirmation dialog.
**Minimal example**

```python
from tkinter import messagebox

def quit_app(window):
    if messagebox.askokcancel("Quit", "Do you really want to exit?"):
        window.destroy()
```
