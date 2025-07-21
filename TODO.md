# 📋 TODO – SQL Desk

Liste des fonctionnalités prévues, bugs à corriger, et idées d’amélioration pour le projet **SQL Desk**.

---

## 🚀 Chantiers majeurs (post-migration GitHub)

- [ ] Permettre l’exécution de suites d’instructions SQL (scripts contenant plusieurs `;`).
- [ ] Permettre l’exécution **de la sélection active** dans la zone SQL, si une sélection est faite.

---

## 🔧 Priorités techniques

- [ ] Affiner les retours à la ligne automatiques dans la mise en forme SQL :
  - Ne pas insérer de `\n` entre `LEFT`, `RIGHT`, `INNER`, etc. et `JOIN`.
  - Ajouter un retour à la ligne devant `JOIN` **seulement** s’il est utilisé seul.
- [ ] Vérifier la lisibilité des requêtes longues dans la zone de sortie.
- [ ] Prévoir un message d’erreur plus explicite quand aucune base de données n’est sélectionnée.
- [ ] Vérifier le comportement et l’ergonomie des zones scrollables (résultats, éditeur SQL…).

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

## 🙌 Collaborateurs bienvenus !

N’hésitez pas à proposer des idées ou des améliorations via issues ou pull requests.  
Projet conçu initialement pour un usage pédagogique (15–18 ans) dans le cadre du cours d’ICT au sein des Écoles Européennes.
