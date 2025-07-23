-- Ligne A : requête de sélection simple
SELECT * FROM books;

-- Ligne B : comptage des livres
SELECT COUNT(*) FROM books;

-- Ligne C : titre des livres publiés après 2010
SELECT title FROM books WHERE year > 2010;

-- Ligne D : requête potentiellement destructrice (NE PAS EXÉCUTER en entier !)
DROP TABLE books;
