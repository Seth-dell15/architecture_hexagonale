# Rapport et Évolution de la Stratégie de Test — ShopLite

Ce document retrace la mise en place de la suite de tests de l'application **ShopLite**, détaille les choix de conception, liste les tests ajoutés suite à l'implémentation du CRUD, et documente les difficultés rencontrées ainsi que leurs résolutions.

---

## 1. Justification des Choix de Tests

La suite de tests repose sur une **pyramide de tests** rigoureuse, adaptée à l'architecture hexagonale :

* **Tests Unitaires (Domaine & Cas d'Utilisation)** : 
  * *Pourquoi* : Isoler complètement la logique métier (calculs de prix) et l'orchestration (CRUD) des détails techniques. Grâce à un faux dépôt en mémoire (`FakeOrderRepository`), ces tests s'exécutent en quelques millisecondes et ne nécessitent aucune base de données.
* **Tests d'Intégration (Adaptateur de Persistance SQLite)** : 
  * *Pourquoi* : Valider que les requêtes SQL brutes (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) de l'adaptateur `SqliteOrderRepository` interagissent correctement avec le système de fichiers et la base de données réelle (via une base de test isolée).
* **Tests de Bout en Bout / E2E (Adaptateur CLI)** : 
  * *Pourquoi* : Simuler de vrais parcours utilisateurs via le terminal (`subprocess`) pour garantir que l'ensemble de la chaîne (CLI ➔ Cas d'Utilisation ➔ Domaine ➔ SQLite) fonctionne de concert et que l'application résiste aux erreurs de saisie.

---

## 2. Nouveaux Tests Ajoutés (Couverture du CRUD)

Au total, la suite comporte **24 tests validés au vert** :
1. **Tests du Calculateur (`test_calculator.py`)** : Validation des taux de remise (10 %) et de TVA (20 %) avec et sans fidélité.
2. **Tests du Modèle (`test_model.py`)** : Vérification des règles d'intégrité de l'entité `Order` (nom non vide, montant positif).
3. **Tests des Cas d'Utilisation (`test_use_cases.py`)** : Couverture unitaire de chaque action du CRUD (`CreateOrder`, `GetOrder`, `ListOrders`, `UpdateOrder`, `DeleteOrder`).
4. **Tests de l'Adaptateur SQLite (`test_sqlite_repository.py`)** : Validation de la persistance des données.
5. **Tests des Cas Limites (`test_edge_cases.py`)** : Gestion des montants nuls, des décimaux et des espaces superflus.
6. **Tests E2E / CLI (`test_integration.py`)** : Simulation du scénario nominal (création + listing) et d'un scénario d'erreur de saisie (montant invalide avec des lettres).

---

## 3. Erreurs de Parcours et Résolutions Techniques

Durant la mise en place et l'écriture des tests, plusieurs obstacles ont été rencontrés et résolus :

### A. Problème d'importation avec Pytest (`ModuleNotFoundError`)
* **Le problème** : L'exécution simple de la commande `pytest` levait une erreur `ModuleNotFoundError: No module named 'src'` car le dossier `src/` n'était pas automatiquement inclus dans le chemin d'importation.
* **La solution** : Utiliser systématiquement l'exécution sous forme de module : `python -m pytest`, ce qui permet d'ajouter dynamiquement la racine du projet au `sys.path`.

### B. Blocage du test d'intégration E2E avec la boucle CLI (`while True`)
* **Le problème** : Le test d'intégration initial s'attendait à ce que le script s'arrête de lui-même après une action, mais la nouvelle architecture CLI intègre une boucle interactive (`while True`). Le test plantait par manque d'entrées (`EOFError`).
* **La solution** : Mettre à jour la séquence de touches simulées (`user_inputs`) pour inclure explicitement l'action de quitter le menu (ex: `6\n`).

### C. Imprécision des nombres flottants et ordre des arrondis
* **Le problème** : Un test sur des montants décimaux (ex: `99.99 HT`) a échoué en raison de l'ordre des calculs, laissant un résidu de virgule flottante inattendu (`89.991` au lieu de `89.99`).
* **La solution** : Appliquer un arrondi strict (`round(..., 2)`) à chaque étape intermédiaire des calculs financiers dans `calculator.py`.

### D. Désynchronisation des saisies CLI dans le scénario d'erreur
* **Le problème** : Lors du test d'erreur de saisie d'un montant invalide, l'ordre de la saisie dans la CLI demandait la fidélité *avant* de valider le format numérique du montant, ce qui faussait le scénario de test.
* **La solution** : Réordonner la méthode `_handle_create` dans l'adaptateur CLI pour valider et convertir le montant HT immédiatement après sa saisie, interceptant ainsi l'erreur au plus tôt.