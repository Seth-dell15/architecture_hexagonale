# Stratégie de Test — ShopLite

Ce document définit la stratégie de test pour l'application **ShopLite**. L'objectif est d'assurer la non-régression du programme existant tout en introduisant progressivement des tests unitaires robustes grâce à l'architecture hexagonale.

---

## 1. Le Défi : Pourquoi ne pas tester le code actuel immédiatement ?

Dans son état initial, ShopLite présente un **couplage fort** : la logique métier (calculs), les entrées/sorties (`input` / `print`) et la persistance (SQLite) sont mélangées dans un flux procédural unique. 
* **Problème** : Écrire des tests unitaires sur ce code exigerait de simuler des flux clavier et d'intercepter les sorties terminal, ce qui rendrait les tests fragiles, artificiels et complexes à maintenir.
* **Solution** : Ne pas tester le code legacy directement, mais s'appuyer sur une approche par étapes, du global vers le granulaire.

---

## 2. Typologie des Tests à Mettre en Place

Pour couvrir l'ensemble du cycle de vie de l'application et sécuriser la refactorisation, nous allons combiner deux niveaux de tests :

### A. Les Tests d'Intégration / "Boîte Noire" (Filet de sécurité initial)
* **Quoi** : Des tests globaux qui exécutent le script entier (`python src/app.py`), injectent des entrées standard (ex: nom, montant, fidélité) et vérifient le résultat final (création correcte de la base `shoplite.db` et intégrité des données enregistrées).
* **Pourquoi** : Ils garantissent que le comportement fonctionnel global de l'application de départ n'est pas cassé avant d'avoir touché au code.
* **Outil** : Scripts Python automatisés utilisant le module `subprocess` ou `unittest.mock`.

### B. Les Tests Unitaires (Cœur de la stratégie)
* **Quoi** : Des tests ciblant de manière isolée et ultra-rapide chaque composant de l'architecture cible (calculateur de prix, entités, cas d'utilisation, dépôts mockés).
* **Pourquoi** : Ils s'exécutent en quelques millisecondes, ne dépendent d'aucune base de données ni d'aucun terminal, et valident mathématiquement et logiquement le domaine métier.
* **Outil** : `pytest` (standard de fait en Python).

---

## 3. Processus et Étapes de Test lors de la Refactorisation

La mise en place des tests suivra rigoureusement l'évolution de l'architecture :

### Étape 1 : Avant de modifier le code (Filet de sécurité)
1. Écrire un test d'intégration rapide simulant le scénario nominal (ex: Alice, 100 HT, fidèle -> vérification de la base SQLite).
2. S'assurer que ce test passe sur le code d'origine (ou documenter le comportement de référence).

### Étape 2 : Lors de l'extraction du Domaine (Étape 1 du refactoring)
1. Isoler les calculs (remise, TVA) dans un module pur (`calculator.py`).
2. **Action de test immédiate** : Écrire des tests unitaires stricts sur ce calculateur (`test_calculator.py`). On teste les cas limites : client fidèle, client non fidèle, montants décimaux, etc., sans aucune base de données.

### Étape 3 : Lors de l'isolation de la Persistance (Étape 3 du refactoring)
1. Mettre en place le port `OrderRepository` et l'adaptateur `SqliteOrderRepository`.
2. **Action de test** : Valider que l'adaptateur SQLite fonctionne correctement via un test d'intégration dédié à la base de données. 
3. *Alternative (Bonus)* : Implémenter un dépôt en mémoire (`InMemoryOrderRepository`) pour tester les cas d'utilisation sans jamais toucher au disque dur.

### Étape 4 : Lors de la création des Cas d'Utilisation (Étape 4 du refactoring)
1. Écrire des tests unitaires pour chaque cas d'utilisation (`CreateOrderUseCase`, `ListOrdersUseCase`, etc.) en utilisant des faux objets (Mocks ou Dépôts en mémoire) pour simuler la base de données.

---

## 4. Résumé des bénéfices de cette stratégie

* **Sécurité** : Aucun risque de régression silencieuse grâce au filet de sécurité initial.
* **Rapidité** : La majorité des tests (domaine et cas d'utilisation) tournent en mémoire et s'exécutent instantanément.
* **Maintenabilité** : Chaque brique de l'architecture hexagonale possède sa propre responsabilité de test, garantissant un code propre et pérenne pour l'ajout ultérieur des fonctionnalités CRUD.