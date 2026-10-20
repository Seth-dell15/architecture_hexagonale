# Justifications des Choix Architecturaux — ShopLite

Ce document formalise les motivations et les bénéfices attendus des choix de conception retenus pour faire évoluer l'application **ShopLite** vers une architecture hexagonale et un CRUD complet.

---

## 1. Pourquoi l'Architecture Hexagonale (Ports & Adaptateurs) ?

### Problème initial
Le code d'origine présentait un couplage fort : la logique de calcul, les interactions utilisateur (CLI) et la persistance (SQLite) étaient entremêlées dans un unique script procédural. Il était impossible de tester un calcul sans ouvrir un terminal, ni changer de base de données sans réécrire le code principal.

### Justification du choix
L'architecture hexagonale permet de **mettre le métier au centre** et de rejeter les technologies (base de données, frameworks, interfaces) à la périphérie (les "adaptateurs").
* **Bénéfice** : Le cœur de l'application ignore tout de SQLite, de la ligne de commande ou d'une éventuelle future API Web. Les dépendances vont de l'extérieur vers l'intérieur (principe d'inversion des dépendances).

---

## 2. Isolation du Cœur Métier (`domain/`)

### Justification du choix
Les règles de calcul (remise de 10 % pour les fidèles, application de la TVA à 20 %) et la modélisation des données (`Order`) ne doivent subir aucune interférence externe.
* **Bénéfice** : En isolant ces règles dans des modules purs (sans `input()`, sans `print()`, sans `sqlite3`), nous permettons des **tests unitaires instantanés** et ultra-rapides. On peut vérifier la conformité financière du logiciel en quelques millisecondes, sans base de données.

---

## 3. Utilisation de Ports et de Dépôts Abstraits (`ports/` & `adapters/outbound/`)

### Justification du choix
Plutôt que d'appeler directement `sqlite3` dans le code métier, nous introduisons une interface (un Port, ex: `OrderRepository`) que l'adaptateur SQLite vient implémenter.
* **Bénéfice majeur** : 
  1. **Testabilité** : Pour les tests, on peut facilement créer un "Mock Repository" ou un stockage en mémoire (`InMemoryOrderRepository`) sans toucher à la base de données réelle.
  2. **Évolutivité** : Si demain l'équipe décide de remplacer SQLite par PostgreSQL ou par une API REST externe, **le code du domaine et des cas d'utilisation ne changera pas d'une seule ligne**. Seul un nouvel adaptateur sortant sera créé.

---

## 4. Introduction de Cas d'Utilisation Dédiés (`use_cases/`) pour le CRUD

### Justification du choix
Pour étendre l'application à un CRUD complet (Create, Read, Update, Delete), l'approche naïve consisterait à ajouter du code dans le script principal. Cela aggraverait la complexité. 
* **Bénéfice** : Chaque action métier (créer, lister, modifier, supprimer) devient un objet ou une fonction d'orchestration distinct(e) (`CreateOrderUseCase`, `ListOrdersUseCase`, etc.). Cela garantit une **responsabilité unique (principe S de SOLID)** : chaque cas d'utilisation ne fait qu'une seule chose et la fait bien, facilitant grandement la maintenance et l'ajout de nouvelles fonctionnalités métiers par la suite.