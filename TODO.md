
---


# 📋 TODO – SQL Desk

Liste des fonctionnalités prévues, bugs à corriger, et idées d’amélioration pour le projet **SQL Desk**.

---

## 🚀 Chantiers majeurs (post-migration GitHub)

- [x] Insérer une ligne vide à chaque sortie dans l'output, pas seulement dans make_pretty_table ✔️ 23/07/2025
- [x] Permettre l’exécution **de la sélection active** dans la zone SQL, si une sélection est faite ✔️ 23/07/2025
- [ ] Permettre l’exécution de suites d’instructions SQL (scripts contenant plusieurs `;`).
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
