
---


# 📋 TODO – SQL Desk

Liste des fonctionnalités prévues, bugs à corriger, et idées d’amélioration pour le projet **SQL Desk**.

---

## 🚀 Chantiers majeurs (post-migration GitHub)

- [x] Insérer une ligne vide à chaque sortie dans l'output, pas seulement dans make_pretty_table ✔️ 23/07/2025
- [x] Permettre l’exécution **de la sélection active** dans la zone SQL, si une sélection est faite ✔️ 23/07/2025
- [ ] Permettre l’exécution de suites d’instructions SQL (scripts contenant plusieurs `;`).

    ### 🟨 [À FAIRE] Exécution de scripts SQL multi-instructions (`;`)

**Objectif** : permettre à l’utilisateur d’exécuter un bloc SQL contenant plusieurs instructions (ex. : `DROP TABLE`, `CREATE`, `INSERT`, `SELECT`, etc.), séparées par des points-virgules, **dans une seule exécution**.

#### ✅ Problèmes à résoudre

1. **Ne pas faire un simple `split(';')`** :  
   Un point-virgule peut exister **à l’intérieur d’une chaîne de caractères** (ex. : `'Je t’aime ; tu me fuis'`).  
   Il ne faut **pas découper à cet endroit**, sinon la requête sera invalide.

2. **Détecter les `;` *hors chaînes*** :  
   Il faut parcourir le SQL caractère par caractère en gardant un état logique :
   - `in_single_quote = True/False`
   - `in_double_quote = True/False`
   - On coupe uniquement les `;` **hors guillemets**

---

#### ✨ Fonction proposée (à intégrer plus tard)

```python
def split_sql_statements(sql_code: str):
    statements = []
    current_stmt = ''
    in_single_quote = False
    in_double_quote = False

    for char in sql_code:
        current_stmt += char

        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif char == ';' and not in_single_quote and not in_double_quote:
            statements.append(current_stmt.strip())
            current_stmt = ''

    if current_stmt.strip():
        statements.append(current_stmt.strip())

    return statements
```

---

#### 🔧 À faire dans `run_sql()` (anciennement `run_query()`)

- Remplacer l’appel direct `cursor.execute(sql_code)` par une boucle :

```python
statements = split_sql_statements(sql_code)

for stmt in statements:
    try:
        cursor.execute(stmt)
        if stmt.lower().startswith("select"):
            rows = cursor.fetchall()
            info = cursor.description
            result = make_pretty_table(info, rows)
        else:
            result = f"> OK: {cursor.rowcount} row(s) affected."
        output_textbox.insert(END, result + "\n\n")
    except Exception as e:
        output_textbox.insert(END, f"> Error: {e}\n\n")
```

---

💡 À intégrer dès que possible pour permettre une exécution fluide de scripts SQL complets.

- [ ] Permettre la création d'une base de données dans le répertoire désiré
- [ ] Affichage des FK et PK dans List Tables
- [ ] Coloration des commentaires `--` et `/* ... */`

---

## 🔧 Priorités techniques

- [x] Affiner les retours à la ligne automatiques dans la mise en forme SQL :
  - Ne pas insérer de `\n` entre `LEFT`, `RIGHT`, `INNER`, etc. et `JOIN`.
  - Ajouter un retour à la ligne devant `JOIN` **seulement** s’il est utilisé seul.
  (✔️ implémenté dans utils.py le 22/07/2025)

- [x] Vérifier le comportement et l’ergonomie des zones scrollables (résultats, éditeur SQL…) ✔️ 23/07/2025  
- [x] Vérifier que le menu « Recent files » fonctionne correctement (bases et SQL) ✔️ 23/07/2025  
  - Correction du bug d’actualisation immédiate du menu après ouverture ou sauvegarde de fichiers  
  - Passage du paramètre `menu` aux fonctions `open_sql_code` et `save_sql_code`  
  - Rafraîchissement du menu réalisé à l’intérieur des fonctions d’ouverture/sauvegarde  
- [ ] Vérifier la lisibilité des requêtes longues dans la zone de sortie.  
- [ ] Prévoir un message d’erreur plus explicite quand aucune base de données n’est sélectionnée.

---

## 🧠 Idées pédagogiques

- [ ] Ajouter des exemples de bases de données (ex : `School.db`, `Library.db`, `Cinema.db`).
- [ ] Ajouter un **mode “élève”** (lecture seule, pas de suppression/ALTER).
- [ ] Ajouter un fichier d’aide SQL en anglais au format Markdown (`HELP_SQL_BASICS.md`).
- [ ] Ajouter un fichier `README_fr.md` pour usage dans un contexte francophone.

---

## 🛠️ Développement futur

- [ ] Export CSV ou TXT des résultats de requête.
- [ ] Export facultatif des résultats et du code SQL au format `.md` (Markdown).
- [ ] Ajout d’un historique local des requêtes exécutées.
- [ ] Interface multilingue (anglais / français au minimum).
- [ ] Intégration future dans un environnement type Jupyter Notebook.
- [ ] Système d’extensions simples ou plugins (formatage, snippets...).

---

## 💭 À discuter / idées en attente

- [ ] Deux idées supplémentaires à retrouver et ajouter ici.

---

# 🗓️ Historique des mises à jour

- **23/07/2025**  
  - [x] Permis l’exécution de la sélection SQL dans l’éditeur ✔️ 23/07/2025  
  - Modification de la fonction `run_query` pour détecter si une portion de texte est sélectionnée dans le widget SQL.  
  - Si une sélection existe, uniquement cette partie est extraite et exécutée, sinon toute la requête dans le textbox est exécutée.  
  - Gestion de la sélection conservée avant et après l’application du formatage SQL (pretty print) pour ne pas perdre le surlignage de la sélection.  
  - Correction des erreurs liées à l’exécution de multiples instructions dans `run_query`, avec l’abandon des anciennes fonctions `run_sql` et `run_sql_pretty`.  
  - Adaptation de l’interface pour que le bouton « Run SQL » déclenche cette fonction unifiée prenant en charge la sélection.
 
  - Corrigé le bug de rafraîchissement immédiat du menu « fichiers récents » (SQL et bases).  
  - Consolidé la suppression des fonctions `run_sql` et `run_sql_pretty`, tout est maintenant géré par `run_query`.  
  - Ajouté la gestion du paramètre `menu` pour rafraîchir les menus récents directement dans `open_sql_code` et `save_sql_code`.  
  - Exécution unifiée des requêtes SQL via `run_query` (qui gère maintenant aussi la sélection) ✔️ 23/07/2025  
  - Abandon des fonctions `run_sql` et `run_sql_pretty` qui n’étaient plus utilisées depuis longtemps.  
  - Possibilité d’envisager un renommage futur de `run_query` en `run_sql` si besoin, notamment si la gestion des scripts multi-requêtes est ajoutée.

- **22/07/2025**  
  - Amélioration des retours à la ligne automatiques dans la mise en forme SQL (gestion des mots-clés JOIN).  
  - Vérification de l’ergonomie des zones scrollables (éditeur SQL et sortie).  


---

## 🙌 Collaborateurs bienvenus !

N’hésitez pas à proposer des idées ou des améliorations via issues ou pull requests.  
Projet conçu initialement pour un usage pédagogique (15–18 ans) dans le cadre du cours d’ICT au sein des Écoles Européennes.
24/07/25 TOUT merde :

Tu as raison d’être furieux : entre circularité, imports impossibles et fonctions déplacées dans tous les sens, ton projet est devenu un champ de mines. Voici un **récap clair et une marche à suivre** pour reprendre la main dès que tu reviens :

---

### 🧠 **Ce qui t’a mis dans la panade**

1. **Circularité** :

   * `utils.py` importe `database_management.py`
   * `database_management.py` importe `utils.py`
   * Résultat : 💥 `ImportError` au démarrage

2. **Fonction `refresh_db_file_menu` mal placée** :

   * Elle dépend à la fois du menu (`tk.Menu`) et des fonctions de gestion de BDD.
   * Placée dans `utils.py`, ça rendait les dépendances inextricables.

---

### ✅ **Solution fonctionnelle à appliquer au calme**

1. **Déplace `refresh_db_file_menu()` dans `GUI_functions.py`**

   * C’est une fonction **d’interface graphique**, pas de gestion pure.
   * Elle manipule le **menu tkinter**, donc elle a sa place dans `GUI_functions`.

2. **Dans `database_management.py`** :

   * Tu peux **l’appeler via un `from GUI_functions import refresh_db_file_menu`** sans circularité.

3. **Dans `utils.py`** :

   * Tu **ne dois pas importer** `database_management`. Laisse `utils.py` neutre (helpers seulement).

4. **Organisation des fichiers** :

   | Fichier                  | Contenu principal                                                |
   | ------------------------ | ---------------------------------------------------------------- |
   | `utils.py`               | Fonctions autonomes : sauvegarde fichiers, tables jolies…        |
   | `database_management.py` | Fonctions logiques : ouvrir/créer/choisir une BDD                |
   | `GUI_functions.py`       | Fonctions Tkinter : boutons, menus, affichage, rafraîchissements |
   | `sql_desk_main_ui.py`    | Interface principale (ancien `sql_desk.py`)                      |

---


---

## ✅ [2025-07-25] Migration vers `/src/` et correction du bug de mise à jour des fichiers récents .db

- Tous les fichiers `.py` principaux ont été déplacés dans le sous-répertoire `src/` :
  - `sql_desk.py`, `GUI_functions.py`, `database_management.py`, `utils.py`, `global_vars.py`
- Le menu des bases de données récentes (db_menu) se met désormais à jour **sans redémarrage** :
  - `refresh_db_file_menu()` a été déplacée de `utils.py` à `database_management.py` pour éviter une circularité d'import.
  - Cette fonction est maintenant appelée à la fin de `choose_database()`, ce qui garantit que toute ouverture ou création de base met à jour le menu.
- Le comportement est maintenant **cohérent avec** celui du menu des fichiers SQL récents (`recent_sql_files`), qui fonctionnait déjà sans redémarrage.
- Des appels `print()` de debug sont présents un peu partout pour suivi temporaire :
  - ➤ **PRIORITÉ PROCHAINE SESSION** : Nettoyer tous les `print()` de debug et supprimer la fonction inutilisée de `sql_desk.py`.

