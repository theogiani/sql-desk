# TODO – SQL Desk

Liste des fonctionnalités prévues, bugs à corriger, et idées d'amélioration pour le projet **SQL Desk**.

---

## À faire


### Points cruciaux
- [ ] Refactor – **Database menu refresh**: decouple UI from DB logic
      - Move UI wiring (lambdas) to `sql_desk.py` and keep `database_management.py` pure (no Tkinter).
      - Add a pure helper (e.g. `get_recent_db_entries()`) returning recent DB items.
      - Define static menu items once; refresh only the dynamic “Recent DBs” section.

- [ ] Permettre la création d'une base de données dans le répertoire désiré
- [ ] Affichage des FK et PK dans List Tables
- [ ] Coloration des commentaires `--` et `/* ... */`
- [ ] Ajouter un fichier d’aide SQL en anglais au format Markdown (`HELP_SQL_BASICS.md`) ainsi qu'un mode d'emploi de SQL Desk
- [ ] Export CSV ou TXT des résultats de requête
- [ ] Export facultatif des résultats et du code SQL au format `.md` (Markdown)
- [ ] Ajout d’un historique local des requêtes exécutées (ex. : CTRL Z, CTRL Y, CTRL S...)
- [ ] Préserver la position du curseur et du défilement vertical dans `sql_textbox` après `pretty_print_sql()` (actuellement, le curseur et la vue reviennent en haut du code après le formatage)
- [ ] Corriger le bouton **Quit**
- [ ] Refactor – `refresh_db_file_menu()` : déplacer ce qui concerne les fonctions lambda dans `sql_desk.py`
- [ ] Amélioration suggérée – Résumé d'exécution des requêtes SQL
- [ ] ## Documentation / Mode d’emploi

	### PRAGMA foreign_keys = ON;

	SQLite n’active pas les contraintes d’intégrité référentielle par défaut.  
	Dans SQL Desk, la commande suivante est exécutée automatiquement à chaque connexion pour s’assurer que les clés étrangères (y compris les clés composites) sont respectées :

	```sql 	PRAGMA foreign_keys = ON;
```
	Sans cette commande, il est possible d’insérer dans Booking une activité qui n’existe 
	pas dans Activity ou qui ne correspond pas au resortName indiqué. 
	Cela peut fausser les résultats de requêtes et rompre la cohérence de la base.

	Action : Mentionner clairement cette particularité dans le mode d’emploi, 
	afin que les utilisateurs comprennent pourquoi l’application active systématiquement
	cette option.


#### Organisation des fichiers

| Fichier                  | Contenu principal |
| ------------------------ | ----------------- |
| `utils.py`               | Fonctions utilitaires autonomes : sauvegarde de fichiers, formatage de tables, helpers divers |
| `database_management.py` | Fonctions de gestion des bases : ouverture, création, sélection, mise à jour de la liste des bases récentes |
| `GUI_functions.py`       | Fonctions liées à l'interface Tkinter : boutons, menus, zones de texte, rafraîchissement d’UI |
| `sql_desk.py`            | Script principal lançant l’application et initialisant l’interface |
| `global_vars.py`         | Variables globales et constantes partagées entre modules |



##  Chantiers majeurs (post-migration GitHub)



 À intégrer dès que possible pour permettre une exécution fluide de scripts SQL complets.

- [ ] Permettre la création d'une base de données dans le répertoire désiré
- [ ] Affichage des FK et PK dans List Tables
- [ ] Coloration des commentaires `--` et `/* ... */`

---

##  Idées pédagogiques

- [ ] Ajouter des exemples de bases de données (ex : `School.db`, `Library.db`, `Cinema.db`).
- [ ] Ajouter un **mode “élève”** (lecture seule, pas de suppression/ALTER).
- [ ] Ajouter un fichier d’aide SQL en anglais au format Markdown (`HELP_SQL_BASICS.md`).
- [ ] Ajouter un fichier `README_fr.md` comme mode d'mploi du logiciel

---

##  Développement futur

- [ ] Export CSV ou TXT des résultats de requête.
- [ ] Export facultatif des résultats et du code SQL au format `.md` (Markdown).
- [ ] Ajout d’un historique local des requêtes exécutées.
- [ ] Interface multilingue (anglais / français au minimum).
- [ ] Intégration future dans un environnement type Jupyter Notebook.
- [ ] Système d’extensions simples ou plugins (formatage, snippets...).

---

## En cours



---


---

## Fait (historique)


- [x] Insérer une ligne vide à chaque sortie dans l'output, pas seulement dans make_pretty_table  23/07/2025
- [x] Permettre l’exécution **de la sélection active** dans la zone SQL, si une sélection est faite  23/07/2025
- [x] Permettre l’exécution de suites d’instructions SQL (scripts contenant plusieurs `;`).

    ###  [À FAIRE] Exécution de scripts SQL multi-instructions (`;`)

**Objectif** : permettre à l’utilisateur d’exécuter un bloc SQL contenant plusieurs instructions (ex. : `DROP TABLE`, `CREATE`, `INSERT`, `SELECT`, etc.), séparées par des points-virgules, **dans une seule exécution**.

####  Problèmes à résoudre

1. **Ne pas faire un simple `split(';')`** :  
   Un point-virgule peut exister **à l’intérieur d’une chaîne de caractères** (ex. : `'Je t’aime ; tu me fuis'`).  
   Il ne faut **pas découper à cet endroit**, sinon la requête sera invalide.

2. **Détecter les `;` *hors chaînes*** :  
   Il faut parcourir le SQL caractère par caractère en gardant un état logique :
   - `in_single_quote = True/False`
   - `in_double_quote = True/False`
   - On coupe uniquement les `;` **hors guillemets**

---
--> ##Fait le 09/08/25

---

- [x] Affiner les retours à la ligne automatiques dans la mise en forme SQL :
  - Ne pas insérer de `\n` entre `LEFT`, `RIGHT`, `INNER`, etc. et `JOIN`.
  - Ajouter un retour à la ligne devant `JOIN` **seulement** s’il est utilisé seul.
  ( implémenté dans utils.py le 22/07/2025)

- [x] Vérifier le comportement et l’ergonomie des zones scrollables (résultats, éditeur SQL…)  23/07/2025  
- [x] Vérifier que le menu « Recent files » fonctionne correctement (bases et SQL)  23/07/2025  
  - Correction du bug d’actualisation immédiate du menu après ouverture ou sauvegarde de fichiers  
  - Passage du paramètre `menu` aux fonctions `open_sql_code` et `save_sql_code`  
  - Rafraîchissement du menu réalisé à l’intérieur des fonctions d’ouverture/sauvegarde  
- [ ] Vérifier la lisibilité des requêtes longues dans la zone de sortie.  
- [ ] Prévoir un message d’erreur plus explicite quand aucune base de données n’est sélectionnée.

---

#  Historique des mises à jour

- **23/07/2025**  
  - [x] Permis l’exécution de la sélection SQL dans l’éditeur  23/07/2025  
  - Modification de la fonction `run_query` pour détecter si une portion de texte est sélectionnée dans le widget SQL.  
  - Si une sélection existe, uniquement cette partie est extraite et exécutée, sinon toute la requête dans le textbox est exécutée.  
  - Gestion de la sélection conservée avant et après l’application du formatage SQL (pretty print) pour ne pas perdre le surlignage de la sélection.  
  - Correction des erreurs liées à l’exécution de multiples instructions dans `run_query`, avec l’abandon des anciennes fonctions `run_sql` et `run_sql_pretty`.  
  - Adaptation de l’interface pour que le bouton « Run SQL » déclenche cette fonction unifiée prenant en charge la sélection.
 
  - Corrigé le bug de rafraîchissement immédiat du menu « fichiers récents » (SQL et bases).  
  - Consolidé la suppression des fonctions `run_sql` et `run_sql_pretty`, tout est maintenant géré par `run_query`.  
  - Ajouté la gestion du paramètre `menu` pour rafraîchir les menus récents directement dans `open_sql_code` et `save_sql_code`.  
  - Exécution unifiée des requêtes SQL via `run_query` (qui gère maintenant aussi la sélection)  23/07/2025  
  - Abandon des fonctions `run_sql` et `run_sql_pretty` qui n’étaient plus utilisées depuis longtemps.  
  - Possibilité d’envisager un renommage futur de `run_query` en `run_sql` si besoin, notamment si la gestion des scripts multi-requêtes est ajoutée.

- **22/07/2025**  
  - Amélioration des retours à la ligne automatiques dans la mise en forme SQL (gestion des mots-clés JOIN).  
  - Vérification de l’ergonomie des zones scrollables (éditeur SQL et sortie).  


---

##  Collaborateurs bienvenus !

N’hésitez pas à proposer des idées ou des améliorations via issues ou pull requests.  
Projet conçu initialement pour un usage pédagogique (15–18 ans) dans le cadre du cours d’ICT au sein des Écoles Européennes.







---

##  [2025-07-25] Migration vers `/src/` et correction du bug de mise à jour des fichiers récents .db

- Tous les fichiers `.py` principaux ont été déplacés dans le sous-répertoire `src/` :
  - `sql_desk.py`, `GUI_functions.py`, `database_management.py`, `utils.py`, `global_vars.py`
- Le menu des bases de données récentes (db_menu) se met désormais à jour **sans redémarrage** :
  - `refresh_db_file_menu()` a été déplacée de `utils.py` à `database_management.py` pour éviter une circularité d'import.
  - Cette fonction est maintenant appelée à la fin de `choose_database()`, ce qui garantit que toute ouverture ou création de base met à jour le menu.
- Le comportement est maintenant **cohérent avec** celui du menu des fichiers SQL récents (`recent_sql_files`), qui fonctionnait déjà sans redémarrage.
- Des appels `print()` de debug sont présents un peu partout pour suivi temporaire :
  - ➤ **PRIORITÉ PROCHAINE SESSION** : Nettoyer tous les `print()` de debug et supprimer la fonction inutilisée de `sql_desk.py`.

## Affichage et ergonomie

-  Préserver la position du curseur et du défilement vertical dans `sql_textbox` après `pretty_print_sql()`  
  (actuellement, le curseur et la vue reviennent en haut du code après le formatage).
Nettoyage refresh_db_file_menu()

## Refactor – `refresh_db_file_menu()`  

### Situation actuelle  
- La fonction `refresh_db_file_menu()` est définie dans `database_management.py`.  
- Elle supprime (`db_menu.delete(0, 'end')`) puis recrée **entièrement** le menu des bases récentes, y compris les entrées **"Open Database..."** et **"Create New Database..."**.  
- Les commandes de menu (`add_command(...)`) utilisent des `lambda` qui pointent vers :  
  - des fonctions de gestion DB (`menu_open_database`, `create_new_database`, `choose_database`),  
  - **et** des éléments d’UI (`db_menu`, `output_textbox`, `window`).  

### Pourquoi ça pose problème  
- `database_management.py` devrait gérer **la logique métier** (création/choix d’une base, gestion des fichiers récents), pas l’interface graphique.  
- Le couplage fort entre UI (Tkinter `Menu`) et gestion DB rend le code moins clair, moins testable et plus difficile à maintenir.  
- Chaque appel reconstruit tout le menu, y compris les commandes statiques (“Open…”, “Create…”), ce qui est fonctionnel mais inutilement répétitif.

### Changements souhaitables  
- Déplacer toute la partie **UI** (construction du menu Tkinter) dans `sql_desk.py` ou `GUI_functions.py`.  
- Ne laisser dans `database_management.py` que :  
  - la mise à jour de `global_vars.recent_db_files`,  
  - la lecture/écriture des fichiers `.txt`.  
- Reconstruire **dynamiquement** uniquement la partie “Bases récentes” du menu.  
- Définir les commandes statiques (“Open…”, “Create…”) une seule fois au démarrage.

### Comment y parvenir  
1. Créer dans `GUI_functions.py` (ou `sql_desk.py`) une fonction `refresh_db_menu_ui(db_menu, recent_files, callbacks)` qui reconstruit l’UI du menu.  
2. Laisser `database_management.py` se contenter de mettre à jour la liste des fichiers récents, puis appeler la fonction UI pour l’affichage.  
3. Adapter `menu_open_database()` et `create_new_database()` pour qu’ils utilisent un **callback** de rafraîchissement UI au lieu de manipuler `db_menu` directement.  
4. Tester l’ouverture, la création et la sélection de DB pour vérifier que la mise à jour du menu fonctionne toujours.



### [Optionnel] Améliorer la création de nouvelles bases (`create_new_database`)

**Situation actuelle**  
- Utilisation de `simpledialog.askstring` pour demander uniquement un nom de fichier.  
- La base est créée automatiquement dans le répertoire de travail courant.  
- Pas de choix du dossier, risque de noms invalides, et possibilité d’écraser un fichier sans avertissement.

**Problème**  
- L’utilisateur ne peut pas choisir l’emplacement du fichier.  
- Le nom de fichier peut contenir des caractères problématiques (espaces, accents, etc.).  
- Aucun contrôle avant écrasement d’un fichier existant.

**Amélioration souhaitée**  
- Utiliser `filedialog.asksaveasfilename` pour permettre à l’utilisateur de choisir **à la fois** le nom et l’emplacement.  
- Ajouter `.db` par défaut via `defaultextension`.  
- Laisser Tkinter demander confirmation si le fichier existe déjà.

**Comment y parvenir**  
1. Remplacer `askstring` par `asksaveasfilename`.  
2. Vérifier si `filepath` n’est pas vide (l’utilisateur peut annuler).  
3. Créer le fichier à l’emplacement choisi.  
4. Mettre à jour `global_vars.current_database` avec le chemin complet.  
5. Ajouter ce chemin à `recent_db_files` comme dans `menu_open_database`.  

**Exemple de code**  
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

### Corriger le bouton "Quit"

**Situation actuelle**  
- Le bouton **Quit** de l’interface ne ferme pas l’application.  
- Aucune action visible lorsque l’utilisateur clique dessus.

**Problème**  
- L’utilisateur s’attend à ce que **Quit** termine l’application immédiatement.  
- Cela peut donner l’impression d’un bug ou d’une interface inachevée.

**Amélioration souhaitée**  
- Faire en sorte que **Quit** appelle `root.destroy()` (ou `window.destroy()` selon la variable utilisée pour l’instance Tk principale).  
- Optionnel : demander confirmation avant de quitter (`messagebox.askokcancel`).

**Comment y parvenir**  
1. Localiser la création du bouton Quit dans le code principal (`sql_desk_main_ui.py`).  
2. Remplacer l’action associée par une fonction fermant proprement la fenêtre principale.  
3. (Optionnel) Ajouter un message de confirmation pour éviter les fermetures accidentelles.  

**Exemple minimal**  
```python
from tkinter import messagebox

def quit_app(window):
    if messagebox.askokcancel("Quit", "Do you really want to exit?"):
        window.destroy()
```
		
## Technical priorities

- [ ] Simple Save (Ctrl+S) — GUI_functions.py
  - Add `current_sql_file` to `global_vars.py` (path of the current file).
  - Implement `save_sql_code(sql_textbox, menu, force_save_as=False)`:
    - If `current_sql_file` exists and `force_save_as` is False ⇒ overwrite that file.
    - Otherwise ⇒ open a “Save As” dialogue and update `current_sql_file`.
    - No Unicode in the code; end with `return None`.
  - “SQL File” menu:
    - Add **Save** (above **Save As**).
    - **Save** calls `save_sql_code(..., force_save_as=False)`.
    - **Save As** calls `save_sql_code(..., force_save_as=True)`.
  - Shortcuts:
    - **Ctrl+S** ⇒ Save (unless the file has not been named yet ⇒ Save As).
    - **Ctrl+Shift+S** ⇒ Save As.
  - On “Open…”:
    - In `open_sql_code(...)`, set `global_vars.current_sql_file = filepath`.
  - Acceptance criteria:
    - Ctrl+S overwrites the same file if already named; otherwise opens Save As.
    - The menu shows **Save** and **Save As** correctly.
    - After **Open…**, Ctrl+S targets the opened file.
    - Errors handled with `messagebox.showerror`.



### Gérer le retour à la ligne en tout début de texte dans `insert_linebreaks_before_keywords`
- **Situation** : si le texte commence par un mot-clé (ex. `SELECT`), la fonction ajoute un `\n` au tout début, puis `.strip()` le supprime.  
- **Problème** : ce comportement pourrait poser souci si la chaîne est réutilisée sans `.strip()`.  
- **Solution envisagée** : empêcher l’insertion du `\n` si le mot-clé est au tout début (regex avec lookbehind négatif `(?<!^)` ou test d’index).  
- **Statut** :  à faire.

### Supprimer les espaces avant les retours de ligne dans `insert_linebreaks_before_keywords`
- **Situation** : après insertion, un espace peut subsister avant `\n` (ex. `* \nFROM`).  
- **Solution** : suppression par  
```
python
  re.sub(r"[ \t]+\n", "\n", formatted)
```
  
  
##  2025-08-09 – Avancées de la session

- **utils.py**  
  - Amélioration de `insert_linebreaks_before_keywords()` pour éviter l’ajout d’un retour à la ligne initial.  
  - Tests validés pour tous les cas connus.
- **TODO.md**  
  - Mise à jour des entrées liées à la gestion du retour à la ligne.
- **.gitignore**  
  - Ajout de la règle `test*.py` pour ignorer les fichiers de test Python.
- **GUI_functions.py, database_management.py, sql_desk.py**  
  - Ajustements mineurs.
- **EcoAdv.db**  
  - Mise à jour de la base d’exemple.
- **Git**  
  - Commit et push effectués avec message clair et complet.

### Renommage de `run_query()` en `run_sql()`  
   - La nouvelle fonction `run_sql()` remplacera l’ancienne `run_sql` abandonnée.  
   - Elle gèrera à la fois l’exécution d’une requête unique (ou portion sélectionnée dans l’éditeur)  
     et l’exécution d’un script multi-instructions séparées par `;`.
	 
## 2025-08-10 
### — Ajout affichage du nombre de lignes affectées
- **Contexte :** Affichage automatique dans la console après exécution d'une requête `INSERT`, `UPDATE` ou `DELETE`, indiquant combien de lignes ont été modifiées.  
- **Objectif :** Donner un retour utilisateur immédiat sur l'impact d'une requête de modification.  
- **Fichiers concernés :**  
  - `sql_functions.py` (fonction `run_sql()` ou `run_query()`, selon implémentation actuelle)
- **Détail technique :**
  - Utilisation de `cursor.rowcount` pour récupérer le nombre de lignes affectées.
  - Message ajouté à la fin de l'exécution, juste après la confirmation de succès.
  
###  Correction bug bouton quit

- **Contexte :** Le bouton **Quit** arrêtait la boucle principale (`mainloop`) dans 
la console, mais l’interface Tkinter restait ouverte et opérationnelle, permettant 
encore d’ouvrir des bases et d’exécuter des requêtes.
- **Cause :** Le bouton appelait `window.quit` au lieu de la procédure `on_closing()` 
qui gère correctement la fermeture et la sauvegarde des fichiers récents.
- **Solution :**
  - Remplacement de `command=window.quit` par `command=lambda: on_closing(window)` 
  dans la création du bouton Quit (`sql_desk.py`).
  - Cette modification garantit que la fonction `on_closing()` est exécutée lors de 
  l’appui sur le bouton, ce qui :
    - Sauvegarde les fichiers récents (`recent_sql_files.txt` et `recent_db_files.txt`).
    - Ferme proprement la fenêtre Tkinter avec `window.destroy()`.
- **Fichiers concernés :**
  - `sql_desk.py` (modification du bouton Quit)
  - `utils.py` (fonction `on_closing()` déjà existante)
  
  ### 2025-08-10 — Refactor refresh_db_file_menu (Database menu)
- **But** : Séparer la logique UI de la logique métier pour le menu Database, tout en évitant de dupliquer les commandes statiques ("Open...", "Create...").
- **Changements** :
  1. Déplacé `refresh_db_file_menu()` de `database_management.py` vers `GUI_functions.py`.
  2. Conserver dans `sql_desk.py` la création initiale du bouton/menu Database avec les commandes statiques (`Open Database...`, `Create New Database...`) comme pour le menu SQL File.
  3. Adapté `refresh_db_file_menu()` pour ne rafraîchir que les entrées dynamiques (bases récentes), en supprimant uniquement les éléments après le séparateur (`menu.delete(3, 'end')`).
  4. Mis à jour `menu_open_database()` et `create_new_database()` pour appeler la nouvelle fonction `refresh_db_file_menu()` depuis `GUI_functions.py`.
- **Note technique** :
  - Choix de l’**option 2** pour l’import : `database_management.py` importe désormais `refresh_db_file_menu` depuis `GUI_functions.py`. Cela crée un import croisé latent mais fonctionnel, à surveiller en cas de refactorisation ultérieure.
- **Résultat** : le menu Database fonctionne comme avant, mais la partie UI est centralisée, et seules les entrées dynamiques sont reconstruites lors du refresh.

 ###2025-08-12** — **Refactor Quit & connection handling, DB creation flow** ✅  
- **Bouton Quit** : ferme désormais proprement toutes les connexions SQLite ouvertes avant de quitter l’application.  
- **`run_sql()`** : supprime la création systématique d’une nouvelle connexion, réutilise `global_vars.current_connection` pour assurer une seule connexion persistante par session.  
- **`create_new_database()`** :  
  - supprime l’appel direct à `refresh_db_file_menu()` (rafraîchissement du menu désormais géré par le GUI après création).  
  - ouvre immédiatement la nouvelle base via `choose_database()` afin d’appliquer la logique unique de connexion et d’initialisation.  
- **Compatibilité vérifiée** entre `database_management.py` et `GUI_functions.py` après refactorisation.  
- **Correction d’un bug** dans l’appel à `make_pretty_table()` (ordre des arguments `headers, rows`) qui provoquait des erreurs `object of type 'int' has no len()` sur certains `SELECT`.  
- **Nettoyage des commentaires** pour éviter tout caractère UTF-8 non ASCII.


 ###2025-08-13** Bug : Pretty Print modifie les commentaires SQL

- **Description** : La fonction `pretty_print_sql()` applique ses transformations même à l'intérieur des commentaires (`-- ...`), par exemple en mettant un retour à la ligne après un mot-clé SQL détecté dans un commentaire.
- **Impact** : Les commentaires peuvent être déformés ou fragmentés (ex. `-- Schema based\nON the exercise ...`).
- **Proposition de correction** :
  - Adapter la fonction pour ignorer toute ligne commençant par `--` (après suppression des espaces initiaux).
  - Même logique à envisager pour les commentaires multilignes `/* ... */`.
- **Priorité** : Moyenne (impact visuel uniquement, pas d’erreur SQL).
- **Statut** : À faire.

### Bug : en-têtes tronquées à la 1re lettre

- **Date** : 13/08/2025
- **Description** : Les noms de colonnes s’affichaient réduits à leur première lettre (`a, n, g, c`…), rendant les tableaux illisibles.
- **Cause** : `make_pretty_table()` utilisait `[col[0] for col in info]` même quand `info` était déjà une liste de noms de colonnes (`list[str]`), transformant chaque nom en sa première lettre.
- **Remède** : Ajout d’un test `isinstance(info[0], str)` pour détecter et traiter directement le cas `list[str]`.
- **Historique** : Comportement apparu soudainement après refactor (probablement changement dans la façon de passer `info` à la fonction).
- **Statut** : Corrigé aujourd’hui.


## Preserve caret and scroll in `pretty_print_sql` ✅

**Context.** Running `pretty_print_sql()` reformatted the SQL but annoyingly reset the caret (cursor) and viewport to the top.

**What we changed (how it works).**
- **Save state** before formatting:
  - caret index: `insert_idx = sql_textbox.index("insert")`
  - (optional) selection: try `sel.first` / `sel.last`
  - vertical scroll: `top_frac = sql_textbox.yview()[0]`
  - horizontal scroll (if enabled): `x_frac = sql_textbox.xview()[0]`
- **Format** the text as before (line breaks, blank line after `;` + optional `--` comments, keyword capitalisation).
- **Atomic undo**: call `sql_textbox.edit_separator()` just before and just after the replacement so the whole format is one undo step.
- **Replace** buffer: `delete("1.0","end")` → `insert("1.0", formatted_query)` → re-run `colorize_keywords(sql_textbox)`.
- **Restore state** after formatting:
  - caret: `mark_set("insert", insert_idx)`
  - selection (if any): clear + `tag_add("sel", sel_start, sel_end)`
  - scroll: `yview_moveto(top_frac)` then (if used) `xview_moveto(x_frac)`
  - ensure visibility: `see("insert")` and optionally `focus_set()`

**Order matters.** Restore **viewport first**, then make sure the caret is visible (`see("insert")`). This avoids unexpected recentering.

**Notes.**
- Behaviour is **idempotent**: re-running the formatter immediately should not change the buffer again.
- Minor caret shifts can occur if the transformer inserts/removes characters **before** the caret.  
  - *Optional refinement (not implemented):* a “cursor sentinel” (temporary marker string inserted at the caret, then removed post-format) pins the caret to the exact logical spot if we ever need pixel-perfect stability.

**Touched function.** `pretty_print_sql(sql_textbox)` (no signature change; no external side effects).

### ✅  **2025-08-17**  
  • Improved `get_tables()`: primary keys displayed in red, foreign keys marked with `#`.  
  • Added `tag_config` in `sql_desk.py` to handle text styles (PK red, FK hash, etc.).  
  • Updated `display_result()` in `utils.py` to accept both plain text and tagged text; 
     ensured backward compatibility with all existing calls.  
  • Preserved behaviour of appending output without clearing the previous content.  
  • Successfully tested with SkillUp database: PKs shown in red, FKs marked with `#`.  
  
## ✅ Done — 26 Aug 2025

- [x] Keyboard shortcuts in the SQL editor
  - Ctrl+Z → Undo
  - Ctrl+Y / Ctrl+Shift+Z → Redo
  - Ctrl+S → Save As (temporary)
- [x] Undo history enabled in the editor
  - `undo=True`, `maxundo=2000`, `autoseparators=True`

### How 
- Enabled Tkinter’s native undo on `ScrolledText`.
- Key bindings: `Ctrl+Z` → `<<Undo>>`, `Ctrl+Y` / `Ctrl+Shift+Z` → `<<Redo>>`, `Ctrl+S` → `save_sql_file()`.
- `save_sql_file()` opens `asksaveasfilename`, writes UTF-8, and handles errors with `messagebox`.

### Notes
- A simple **Save** (overwrite) is not implemented yet.
- For now, **Ctrl+S** always triggers Save As.



 
### Mise en forme & coloration des commentaires SQL
- **Situation** : les commentaires `-- ...` (et plus tard `/* ... */`) ne sont pas colorés et subissent le pretty print (ex. mots uppercasés).
- **Problème** : le formatter modifie le contenu des commentaires (lisibilité, sens altéré).
- **Objectifs**
  - Colorier les commentaires (ex. gris/italique) dans l’éditeur.
  - Exclure les commentaires du `highlight_keywords` et des autres transformations.
- **Approche**
  - Étape 1 : support `--` (ligne) ; Étape 2 : `/* ... */` (multi-ligne).
  - Adapter `highlight_keywords(text)` pour ignorer les segments marqués comme commentaires :
    - Parcours ligne par ligne : séparer `code_part` / `comment_part` via `--`.
    - Uppercase seulement sur `code_part`, concaténer `code_part + comment_part` inchangé.
  - (Optionnel) Ajouter un tag Tkinter `sql_comment` avec `foreground="#888"` et `slant="italic"`.
- **Statut** : à faire.

####  Amélioration suggérée – Résumé d'exécution des requêtes SQL
- **Objectif** : Afficher un court résumé après l'exécution de `run_sql()` indiquant :
  - Le nombre total d'instructions exécutées.
  - Le nombre de succès et d'erreurs.
- **Exemple** :
- **Remarque** : Le résumé serait affiché à la fin de l'output, sans interrompre les résultats intermédiaires.
- **Statut** : À implémenter après stabilisation des fonctions multi-statements et du pretty-print.




#### 01 Nov 2025 — Repository clean-up, `.gitignore` update, and database creation workflow

* **.gitignore**
  * Simplified and modernised for a cleaner repository layout.
  * Keeps all code under `/src`, documentation files (`.docx`, `.pdf`, `.md`), and teaching materials (`sample_databases/`).
  * Ignores cache files, local databases, virtual environments, and temporary folders such as `Old/` or backup directories like `src-2025-...`.

* **Database creation**
  * `create_new_database()` successfully refactored with `filedialog.asksaveasfilename` to let users pick both the directory and filename.
  * Integrated immediate database opening via `choose_database()` for smoother workflow.
  * Tested with new sample databases — fully functional.

* **Repository organisation**
  * Confirmed that `/WorkingArea` is the root of the Git repository.
  * `/src` now clearly hosts all core Python modules.
  * `sample_databases/` kept under version control (pedagogical examples).

* **Next development focus**
  * Comment colouring and protection (`--` and `/* ... */`).
  * Goal: preserve comments during Pretty Print and display them in grey italics.

### 2025-11-01 — Codebase documentation and cleanup
- Rewrote all docstrings and inline comments in Queen’s English.
- Removed obsolete commented-out code fragments and minor redundancies.
- Ensured consistent style, indentation, and tone across all core modules (`sql_desk.py`, `GUI_functions.py`, `database_management.py`, `utils.py`).
- Verified that logic and functionality remain unchanged.


#### 03 Nov 2025 - Pretty Print bug — line breaks inserted after comment markers

**Date:** 2025-11-03  
**Category:** Pretty Print / Safety

**Description:**  
The Pretty Print function introduces unwanted line breaks right after the `--` comment marker.  
As a result, commented SQL queries are split over two lines:
the `--` remains alone, while the SQL code moves to the next line and becomes executable.

**Observed behaviour:**  
```sql
-- SELECT * FROM Role;
```
is reformatted as:
```sql
--
SELECT * FROM Role;
```
Hence, on the next execution, the SQL statements run even though they were originally commented out.

**Expected behaviour:**  
- Preserve comments and their associated lines as single logical units.  
- Never insert a newline between `--` and the text following it.

**Suggested fixes:**  
1. Detect lines starting with `--` and treat them as atomic (no internal line breaks).  
2. Render them in Dark metallic Green for readability but never reflow them.  
3. Add regression tests using seed scripts (like GalaxyQuest) to ensure comment integrity.

**Priority:**  **High (execution safety)**


#### 03 Nov 2025 - Excessive blank lines in output:
The console currently inserts multiple empty lines between successive messages or result tables, making the output unnecessarily long and harder to read.
Normalise the spacing so that only one blank line is displayed between result blocks, and remove redundant leading or trailing empty lines.
The objective is to produce a compact, consistent layout that remains visually clear after multiple executions.



#### 04 Nov 2025 - 

1. Add spacing around operators in Pretty Print
Insert one idempotent space on each side of = (and possibly other operators such as <, >, <=, >=, <>, +, -, *, /).

Example:
Current: IdRole=8
Desired: IdRole = 8

⚙️ Ensure that repeated formatting does not insert additional spaces (idempotence required).

2. Display NULL explicitly

When a database field has a NULL value, display NULL instead of leaving the cell blank.
Apply to all output formats (plain text and pretty table).
Keep alignment and column widths consistent.


####  13 Dec 2025  Multi-row `INSERT` formatting (Pretty Print)

**Description**
Currently, multi-row `INSERT INTO ... VALUES (...), (...), ...;` statements remain in a single block.
The pretty printer does not detect commas separating tuples.

**Goal**
Improve readability by inserting a newline between tuples while keeping commas inside tuples untouched.

**Possible approaches**

1. **Regex approach (simple):**

   ```python
   text = re.sub(r'\)\s*,\s*\(', '),\n(', text)
   ```

   ✅ Fast and good enough for educational use.
2. **Structured parse (advanced):**
   Iterate through characters while tracking parentheses depth; insert `\n` when a comma appears **outside** any parentheses.
   ⚙️ More robust but heavier to implement.

**Status:** To do — to be tested with scripts like *EcoRide.db*.
⚠️ Ensure no newline insertion in string literals containing `),(`.

---

#### (2025-12-13) Couleur des messages dans la console (feedback utilisateur)

**Description :**  
Actuellement, tous les messages s'affichent en noir dans la zone d'output, qu'ils soient informatifs, positifs ou liés à une erreur.  
Pour améliorer la lisibilité et le retour visuel, il serait utile d'appliquer des couleurs différentes selon le type de message.

**Proposition :**
- 🔴 **Rouge foncé** pour les messages d’erreur (exceptions SQLite, syntax errors, etc.)  
- 🟢 **Vert** pour les messages de réussite (`Query executed`, `Database opened`, etc.)  
- ⚫ **Noir ou gris neutre** pour les messages d’information généraux

**Remarques techniques :**  
→ Utiliser les balises `tag_config()` de `tk.Text` (ou `ScrolledText`) pour définir les couleurs à l’initialisation.  
→ Le choix du rouge foncé (au lieu du rouge vif) garantit une bonne lisibilité sur fond clair.  
→ S'assurer que les couleurs restent compatibles avec les thèmes futurs (Dark/Light).

**Statut :** à implémenter.



#### (2025-12-13) Taille de police non appliquée aux lignes "Tables in current database"

**Description :**  
Lorsque l'on modifie la taille de la police dans la fenêtre d'output, tous les caractères s'adaptent correctement,  
sauf la ligne d'en-tête `"Tables in current database:"` et les noms de tables listés juste en dessous.

**Cause probable :**  
Ces lignes utilisent des balises (`tag_add`, `tag_config`) appliquées lors de la génération du menu des tables,  
et leur police est fixée manuellement (ex. `("Consolas", 10, "bold")`) au lieu d’hériter de la police globale.

**Objectif :**  
Faire en sorte que ces éléments utilisent la même police que le reste de la fenêtre d'output,  
et se redimensionnent lorsque la taille de police est modifiée par l'utilisateur.

**Piste technique :**
- Définir une *font variable* (`tk.font.Font`) commune à toute la zone d’output.  
- L’utiliser pour la configuration des tags `db_header` et `db_table` au lieu de fixer la taille en dur.  
- Reconfigurer dynamiquement cette police lorsqu’un changement de taille est détecté.

**Statut :** à corriger.


#### 06 Jan 2026 – P0 : Coloration des commentaires + gestion fine des lignes vides (Pretty Print)

- **Coloration des commentaires SQL (ligne et bloc)**  
  Mettre en place la coloration syntaxique des commentaires dans l’éditeur SQL :
  - Commentaires de ligne : `-- ...`
  - Commentaires de bloc : `/* ... */` (y compris multi-lignes)

  Appliquer un style dédié (actuellement vert sombre « métallique ») et garantir que la coloration des mots-clés SQL **ne s’applique jamais à l’intérieur des commentaires**.

- **Amélioration de la normalisation des retours à la ligne (Pretty Print)**  
  Corriger les règles de mise en forme afin que :
  - Les lignes vides entre commentaires successifs soient conservées.
  - En cas de plus de **3 lignes vides consécutives**, le Pretty Print conserve **au maximum 2 lignes vides**.
  - L’insertion automatique de retours à la ligne avant certains mots-clés SQL soit **idempotente** et n’introduise pas de lignes vides parasites  
    (ex. : pas de ligne vide forcée entre `INSERT INTO ...` et `VALUES` lorsque `VALUES` est déjà sur une nouvelle ligne).

  L’objectif est d’obtenir une mise en forme **stable, lisible et respectueuse de l’intention de l’utilisateur**, même après des exécutions répétées du Pretty Print.



- [ ] 2026-01-18 — Pretty Print / Coloration syntaxique : ignorer les mots-cles SQL dans les commentaires.

  **Contexte**
  - Dans le SQL shell, le pretty printer et la coloration syntaxique traitent actuellement
    les mots-cles SQL meme lorsqu ils apparaissent dans des commentaires (lignes commencant par "--").
  - Probleme observe avec le script de setup "Music Academy".

  **Symptomes**
  - Le mot-cle "CREATE" dans un commentaire declenche :
    - des retours a la ligne automatiques,
    - une coloration bleue des mots-cles,
    - et parfois une interpretation partielle par SQLite.
  - Le script SQL peut alors etre corrompu et echouer a l execution.
  - Fait interessant : les mots-cles "DROP" et "INSERT" dans les commentaires ne declenchent PAS le probleme,
    ce qui suggere que seule une sous-liste de mots-cles (probablement ceux utilises pour les retours a la ligne)
    est concernee.

  **Hypothese**
  - La logique de pretty print analyse probablement tout le texte (y compris les commentaires) et applique :
    - detection des mots-cles,
    - regles de mise en forme,
    - coloration,
    sans exclure les zones commentees.
  - "CREATE" semble appartenir a une liste speciale de mots-cles declenchant le formatage,
    contrairement a "DROP" et "INSERT".

  **Correctif attendu**
  - Avant toute application du pretty print ou de la coloration syntaxique :
    - detecter les zones de commentaire ("-- ...", et eventuellement "/* ... */"),
    - les exclure totalement de tout traitement de mots-cles et de mise en forme,
    - preserver leur contenu tel quel.
  - Alternative : masquer temporairement les commentaires pendant le formatage, puis les restaurer.

  **Impact**
  - Ce probleme n est pas seulement cosmetique : il peut modifier le SQL executable et provoquer
    des erreurs d execution, ce qui est problematique dans un contexte pedagogique.

  **Observation complementaire**
  - Apres suppression manuelle des retours a la ligne indus, les commentaires retrouvent
    une coloration verte correcte et SQLite execute normalement le script.
  - Cela confirme que le probleme est bien cause par des retours a la ligne inseres
    a l interieur des lignes commentees.


- [ ] 2026-01-18 — Pretty Print : les fonctions SQL (count, sum, avg, min, max) ne sont pas colorees.

  **Observation**
  - Les fonctions SQL comme count, sum, avg, min et max ne sont actuellement pas detectees
    ni colorees par le moteur de coloration syntaxique.
  - Seuls les mots-cles structurels (select, from, where, join, etc.) sont colores.

  **Impact**
  - Ce n est pas bloquant fonctionnellement.
  - La lisibilite reste correcte, mais une coloration des fonctions pourrait ameliorer
    la lecture et la pedagogie.

  **Piste d evolution**
  - Envisager d ajouter les fonctions SQL courantes dans une liste dediee (ex: SQL_FUNCTIONS)
    et de leur appliquer une coloration differenciee, sans impacter le pretty print existant.



## 2026-01-19 — Refactorisation Pretty Print / Sécurisation des commentaires

### ✅ Corrigé
- Implémentation de `split_sql_segments()` pour découper proprement un texte SQL en :
  - ("code", ...)
  - ("comment", ...)
  en détectant :
  - les commentaires de ligne `-- ...`
  - les commentaires de bloc `/* ... */`
  Hypothèse documentée : `/*` et `*/` n’apparaissent jamais en dehors des commentaires.

- Refactorisation de `highlight_keywords()` :
  - mise en majuscules appliquée uniquement aux segments "code",
  - préservation stricte des commentaires.
  Cela évite également toute corruption des commentaires lors des opérations Save / Save As.

- Refactorisation de `insert_linebreaks_before_keywords()` :
  - insertion de retours à la ligne uniquement dans les segments "code",
  - aucune modification à l’intérieur des commentaires.

- Correction du bug d’affichage des JOIN :
  - suppression de la coupure incorrecte :
    - `LEFT\nJOIN`, `INNER\nJOIN`, etc.
  - `JOIN` n’est mis à la ligne que lorsqu’il apparaît seul.

- Validation par une batterie complète de tests :
  - sécurité des commentaires de ligne,
  - sécurité des commentaires de bloc,
  - commentaires inline,
  - comportement du pretty print,
  - formatage des JOIN,
  - idempotence (stabilité après la deuxième exécution),
  - coloration syntaxique correcte.

###  Connu (faible priorité)
- Cosmétique : lorsqu’un commentaire de bloc n’est pas fermé (`/*` sans `*/` en fin de fichier),
  une ligne vide supplémentaire peut apparaître lors de la deuxième exécution du Pretty Print.
  Le comportement est sûr et stable ensuite.
  → Pas de correction prévue à court terme.

###  Prochaines priorités
- Implémenter un vrai comportement Save / Save As :
  - Ctrl+S : écrasement du fichier courant s’il existe,
  - Ctrl+Shift+S : Save As,
  - gestion cohérente du fichier courant (`current_sql_file`).
- Rédaction du mode d’emploi / documentation utilisateur.


- [ ] **2026-01-20 — Implémenter un vrai comportement Save / Save As pour les fichiers SQL**

  - Clarifier que l’action actuelle **"Save SQL..."** correspond en réalité à un **Save As**.
  - Mettre à jour le menu **SQL File** pour proposer :
    - **Save**
    - **Save As...**
  - Ajouter une variable globale `current_sql_file` dans `global_vars.py`.
  - Lors de l’ouverture d’un fichier SQL, mettre à jour `current_sql_file` en conséquence.
  - Implémenter une fonction unifiée `save_sql_code(...)` :
    - Si `current_sql_file` existe et que le mode n’est pas forcé → écrasement du fichier.
    - Sinon → ouverture de la boîte de dialogue **Save As** et mise à jour de `current_sql_file`.
  - Raccourcis clavier :
    - **Ctrl+S** → Save
    - **Ctrl+Shift+S** → Save As
  - Vérifier que le menu des fichiers SQL récents continue à se mettre à jour correctement.



## 2026-01-20 — Save / Save As (fichiers SQL) + menu + raccourcis

### Fait aujourd’hui (implémenté + testé)
- [x] Ajout d’un état de session pour le fichier SQL courant :
  - Ajout de `current_sql_file` dans `global_vars.py` (initialisé à `None`).
- [x] **Open SQL...** initialise correctement le fichier courant :
  - Dans `open_sql_code(...)`, affectation de `global_vars.current_sql_file = filepath` après sélection valide.
- [x] Évolution de `save_sql_code(...)` vers un vrai **Save + Save As** :
  - Signature étendue : `save_sql_code(sql_textbox, menu=None, force_save_as=False)`.
  - Comportement :
    - Si `current_sql_file` existe et que `force_save_as` est False → écrasement du fichier courant (sans dialogue).
    - Sinon → ouverture de la boîte de dialogue **Save As** et mise à jour de `current_sql_file`.
  - Après une écriture réussie, mise à jour de `global_vars.current_sql_file = filepath`.
- [x] Mise à jour du menu **SQL File** :
  - Remplacement de l’ancien **"Save SQL..."** par :
    - **Save**
    - **Save As...**
- [x] Raccourcis clavier opérationnels :
  - **Ctrl+S** → Save
  - **Ctrl+Shift+S** → Save As
  - Compatibilité Redo conservée :
    - **Ctrl+Y** et **Ctrl+Shift+Z** → Redo
- [x] Affichage des raccourcis dans le menu (accelerators) :
  - **Save** affiche `Ctrl+S`
  - **Save As...** affiche `Ctrl+Shift+S`
- [x] Correction du rafraîchissement du menu :
  - `refresh_sql_file_menu(...)` reconstruit désormais correctement :
    - Open SQL...
    - Save (Ctrl+S)
    - Save As... (Ctrl+Shift+S)
    - fichiers récents
- [x] Tests manuels validés :
  - Save As depuis un buffer vierge.
  - Save overwrite sans boîte de dialogue.
  - Save As forcé avec changement de fichier courant.
  - Redémarrage → Open SQL → Save overwrite.

---

## Pistes de développement futures (moyen / long terme)

### (Long terme) Rationalisation de la construction du menu SQL File
- [ ] **(Plus tard) Centraliser la construction du menu SQL File**
  - Situation actuelle : le menu est construit dans `sql_desk.py` **et** reconstruit dans `refresh_sql_file_menu(...)`.
  - Objectif : éviter les duplications et les incohérences (comme le retour involontaire de "Save SQL...").
  - Piste :
    - Créer l’objet `Menu` dans `sql_desk.py` (menu vide),
    - Appeler une seule fois `refresh_sql_file_menu(menu, textbox)` au démarrage,
    - Supprimer la construction initiale redondante dans `sql_desk.py`.

### (Moyen terme) Indication du fichier SQL courant (sans surcharge visuelle)
- [ ] Ajouter un indicateur léger du fichier SQL courant, sur le modèle de l’affichage du chemin de la base :
  - Options possibles :
    - Ajouter le nom du fichier dans le titre de la fenêtre :  
      `SQL Desk — <nom_fichier.sql>`
    - Ajouter une petite zone de statut près de l’éditeur (nom seul, chemin complet éventuellement en tooltip).
  - Conserver une interface sobre et lisible pour les élèves.

### (Moyen terme) Colorisation des messages d’erreur dans la zone Output
- [ ] Afficher les messages d’erreur SQL en rouge dans la zone Output.
  - La majorité des erreurs proviennent probablement des exceptions SQLite.
  - Piste technique :
    - Intercepter explicitement les exceptions (`sqlite3.Error`, etc.).
    - Centraliser l’affichage via une fonction dédiée (ex. `append_output(text, tag="error")`).
    - Configurer les tags du widget `Text` (tag `error` en rouge).
  - Harmoniser les chemins d’erreur si certains messages sont encore imprimés ou retournés sous forme brute.

### (Long terme) Sauvegarde / export de la base de données
- [ ] Ajouter **Database → Backup / Export database...**
  - Comportement attendu : copie explicite du fichier `.db` vers un emplacement choisi par l’utilisateur.
  - Bien distinguer cette action du Save/Save As des fichiers SQL (éviter toute confusion conceptuelle).
  - Raccourci clavier : optionnel / à définir (probablement non nécessaire).



