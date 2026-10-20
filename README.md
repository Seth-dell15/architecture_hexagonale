# Projet fil rouge — Diagnostic d'architecture

## Contexte

Vous rejoignez l'équipe qui maintient **ShopLite**, une petite application en ligne de commande permettant d'enregistrer des commandes clients.

Le programme fonctionne, mais il est devenu difficile à modifier et à tester. Votre mission initiale n'est **pas** de le réécrire : vous devez comprendre son fonctionnement, repérer les problèmes d'architecture et proposer une cible plus maintenable.

---

## Prérequis

- **Python** : 3.10 ou supérieur
- **Dépendances** : Aucune dépendance externe

---

## Lancer l'application

Depuis la racine du projet :

```bash
python src/app.py
```

La base SQLite `shoplite.db` est créée automatiquement à la première exécution.

Le programme demande un nom de client, un montant hors taxes et si le client bénéficie d'une remise fidélité. Il enregistre ensuite la commande et affiche un récapitulatif.

### Exemple de scénario :
- **Client** : `Alice`
- **Montant HT** : `100`
- **Client fidèle** : `oui`

**Comportement attendu** : Nom non vide ; montant HT strictement positif ; remise fidélité de 10 % ; TVA de 20 % appliquée après remise ; commande enregistrée puis récapitulatif affiché.

---

## Travail demandé — Diagnostic initial

Sans modifier le code au premier passage :

1. Exécutez l'application et résumez le scénario métier.
2. Dessinez l'architecture actuelle et identifiez les composants réellement présents.
3. Repérez au moins **trois** responsabilités mélangées ou dépendances problématiques.
4. Identifiez une règle métier qui devrait pouvoir être testée sans base de données ni saisie clavier.
5. Proposez une architecture cible (hexagonale) comprenant : présentation, cas d'utilisation, domaine métier, ports et adaptateurs techniques.
6. Proposez un plan de refactorisation progressif qui préserve le comportement existant.

---

## Réponses et Analyses

### 1. Résumé du scénario métier
Le programme demande le nom du client, le montant hors taxes (HT) et si le client bénéficie d'une remise fidélité. 
- **Validations** : Vérifie que le nom n'est pas vide et que le montant est un nombre strictement positif.
- **Calculs** : Une remise de 10 % est appliquée si le client est fidèle (0 % sinon). La TVA de 20 % est ensuite calculée sur le montant après remise.
- **Persistance & Restitution** : La commande est enregistrée dans une base de données SQLite locale (`shoplite.db`) avec la date/heure courante, puis un récapitulatif textuel (ID, montant HT, remise, montant TTC) est affiché à l'utilisateur.

---

### 2. Architecture actuelle (Monolithique / Script procédural)
Les composants présents dans le code actuel sont mélangés dans un unique flux procédural (`main`) :
- **Interface Utilisateur (UI)** : Saisie (`input()`) et affichage (`print()`).
- **Validation** : Contrôle de surface des types et des valeurs directement dans le flux principal.
- **Logique Métier** : Calculs de la remise et de la TVA codés en dur.
- **Persistance** : Connexion SQLite, création de table et requêtes SQL écrites *inline*.

---

### 3. Trois responsabilités mélangées et dépendances problématiques
1. **Couplage fort entre UI et Logique** : Les instructions d'interaction (`input` / `print`) sont imbriquées au milieu des calculs. Il est impossible d'exécuter ce code sans un terminal interactif.
2. **Absence d'isolation de la persistance** : Les requêtes SQL (`sqlite3.connect`, `cursor.execute`) sont exécutées directement dans le parcours principal, rendant le système totalement dépendant de SQLite.
3. **Logique métier non encapsulée** : Les règles de calcul (taux de remise à 10 %, TVA à 20 %) reposent sur des variables et des formules éparpillées, sans structure de données métier dédiée (pas d'entité `Order` ou de *Value Objects*).

---

### 4. Règle métier isolable (Testable unitairement)
La règle de calcul du montant TTC après remise et TVA peut et doit être isolée. 
- **Entrées** : `amount_ht` (float), `is_loyal` (bool)
- **Sorties** : `discount` (float), `amount_ttc` (float)
Cette logique mathématique pure ne nécessite **ni base de données ni saisie clavier** et peut être testée instantanément.

---

### 5. Proposition d'Architecture Cible (Hexagonale)

Pour séparer clairement les préoccupations, voici l'arborescence cible inspirée de l'architecture hexagonale :

```text
src/
├── domain/                  # Cœur métier (Règles pures, Entités)
│   ├── model.py             # Entité Order, Value Objects
│   └── calculator.py        # Règles de calcul (Remise, TVA)
├── use_cases/               # Cas d'utilisation / Application (Ports entrants)
│   └── create_order.py      # Orchestration du scénario d'achat
├── ports/                   # Interfaces (Ports sortants pour la persistance)
│   └── order_repository.py  # Contrat abstrait pour la persistance
└── adapters/                # Adaptateurs techniques (Entrées / Sorties)
    ├── inbound/             # Adaptateurs primaires (CLI, API HTTP...)
    │   └── cli.py
    └── outbound/            # Adaptateurs secondaires (SQLite, In-Memory...)
        └── sqlite_repository.py
```

---

### 6. Plan de refactorisation progressif

* **Étape 1 — Extraire le domaine** : Isoler les calculs de prix (remise et TVA) dans un module de calcul pur testable par des tests unitaires.
* **Étape 2 — Créer une entité métier** : Modéliser une classe ou une structure `Order` pour structurer les données.
* **Étape 3 — Abstraire la persistance (Port & Adaptateur Sortant)** : Créer une interface de dépôt (`OrderRepository`) et déplacer le code SQLite dans une classe d'implémentation dédiée (`SqliteOrderRepository`).
* **Étape 4 — Isoler le cas d'utilisation** : Regrouper la logique d'orchestration dans un service applicatif (`CreateOrderUseCase`).
* **Étape 5 — Découpler l'interface utilisateur (Adaptateur Entrant)** : Faire en sorte que le script CLI se contente de capturer les entrées, d'appeler le cas d'utilisation, puis d'afficher le résultat.

---

## Questions à discuter

* **Où se trouvent les règles de calcul ?**  
  Elles sont actuellement noyées dans la fonction `main()`, au niveau des lignes gérant les calculs de discount, `amount_after_discount` et `amount_ttc`.
* **Peut-on tester la remise sans lancer l'application interactive ?**  
  Non, car la logique de remise est déclenchée séquentiellement après des `input()`. Il faut séparer la logique de calcul des I/O pour permettre des tests unitaires.
* **Que faudrait-il changer pour remplacer SQLite par une API distante ou un stockage en mémoire ?**  
  Il suffirait d'implémenter un nouveau dépôt respectant la même interface (le même *Port*) que le dépôt SQLite, sans modifier le cœur métier ni les cas d'utilisation (Principe d'Inversion des Dépendances).
* **Que faudrait-il changer pour appeler le même cas d'utilisation depuis une API HTTP ?**  
  Rien dans le cœur métier ni dans les cas d'utilisation ! Il faudrait simplement ajouter un nouvel adaptateur d'entrée (par exemple, un contrôleur FastAPI ou Flask) qui reçoit la requête HTTP et appelle le cas d'utilisation `CreateOrderUseCase`.
* **Le programme gère-t-il correctement toutes les entrées invalides ? Comment le vérifier ?**  
  Partiellement. Il intercepte les noms vides et les erreurs de conversion de nombre (`ValueError`), mais :
  - Il n'empêche pas la saisie de montants négatifs (le test `amount_ht <= 0` intervient après la conversion, ce qui est correct, mais les messages d'erreur restent basiques).
  - La gestion de la réponse *"Client fidèle ?"* est très fragile : tout ce qui n'est pas strictement égal à `"oui"` (en minuscules) est considéré comme `False`, sans avertir l'utilisateur en cas de faute de frappe (ex: taper `"o"` ou `"yes"` est considéré par défaut comme `"non"`).

---
