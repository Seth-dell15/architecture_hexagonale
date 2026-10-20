# Documentation d'Architecture — ShopLite

Ce document décrit l'architecture cible (hexagonale) de l'application **ShopLite** ainsi que l'extension du domaine pour prendre en charge un CRUD complet.

---

## 1. Principes de l'Architecture Hexagonale

L'objectif est d'isoler le cœur métier (le domaine et la logique applicative) des détails techniques (base de données, interfaces utilisateurs, frameworks). Les dépendances vont toujours de l'extérieur vers l'intérieur.

Arborescence cible du projet :
```text
src/
├── domain/                  # Cœur métier (Règles pures, Entités, Value Objects)
│   ├── model.py             # Entité Order et structures de données
│   └── calculator.py        # Règles de calcul pures (Remise, TVA)
├── use_cases/               # Cas d'utilisation / Application (Ports entrants)
│   ├── create_order.py      # Créer une commande
│   ├── get_order.py         # Consulter une commande par son ID
│   ├── list_orders.py       # Lister toutes les commandes
│   ├── update_order.py      # Mettre à jour une commande
│   └── delete_order.py      # Supprimer une commande
├── ports/                   # Interfaces (Contrats pour la persistance)
│   └── order_repository.py  # Interface abstraite du dépôt de commandes
└── adapters/                # Adaptateurs techniques (Entrées / Sorties)
    ├── inbound/             # Adaptateurs primaires (CLI, API HTTP...)
    │   └── cli.py
    └── outbound/            # Adaptateurs secondaires (SQLite, In-Memory...)
        └── sqlite_repository.py
```
---

## 2. Déclinaison du CRUD en Cas d'Utilisation (Use Cases)

Pour compléter le cycle de vie des commandes (CRUD), chaque opération majeure est pilotée par un cas d'utilisation dédié :

### A. Create (Créer) — CreateOrder
* **Rôle** : Enregistrer une nouvelle commande.
* **Entrées** : Nom du client, montant HT, statut de fidélité.
* **Traitements** : 
  1. Valide les données métiers.
  2. Calcule la remise (10% si fidèle) et la TVA (20% sur le montant remisé).
  3. Instancie l'entité `Order`.
  4. Sauvegarde la commande via le port `OrderRepository`.
* **Sortie** : L'objet `Order` créé (avec son ID généré et les montants calculés).

### B. Read (Lire / Consulter) — GetOrder & ListOrders
* **Rôle 1 (GetOrder)** : Récupérer le détail d'une commande spécifique par son identifiant unique.
* **Rôle 2 (ListOrders)** : Obtenir la liste exhaustive de toutes les commandes enregistrées.
* **Entrées** : ID de commande (pour la consultation unitaire).
* **Traitements** : Interroge le dépôt via le port pour récupérer les données persistées.
* **Sortie** : Une entité `Order` ou une collection d'entités `Order`.

### C. Update (Mettre à jour) — UpdateOrder
* **Rôle** : Modifier une commande existante (par exemple, corriger un montant ou changer le statut de fidélité).
* **Entrées** : ID de la commande à modifier, nouveaux paramètres (nom, montant HT, fidélité).
* **Traitements** :
  1. Récupère la commande existante (et lève une erreur si elle n'existe pas).
  2. Met à jour les champs modifiés et recalcule automatiquement les montants (remise/TVA) si les données financières ont changé.
  3. Enregistre les modifications via le dépôt.
* **Sortie** : La commande mise à jour.

### D. Delete (Supprimer) — DeleteOrder
* **Rôle** : Supprimer ou archiver une commande erronée du système.
* **Entrées** : ID de la commande à supprimer.
* **Traitements** : Demande au dépôt de retirer l'enregistrement correspondant.
* **Sortie** : Confirmation de suppression.

---

## 3. Flux d'exécution type (Exemple : CLI vers Domaine)

1. **Adaptateur Inbound (cli.py)** : Affiche un menu interactif, capture les choix de l'utilisateur (ex: option "Lister les commandes") et récupère les données textuelles.
2. **Cas d'Utilisation (ListOrdersUseCase)** : Reçoit la demande, orchestre l'action et appelle l'interface du port.
3. **Port (OrderRepository)** : Définit la méthode abstraite `get_all()`.
4. **Adaptateur Outbound (sqlite_repository.py)** : Exécute la requête SQL `SELECT * FROM orders` sur la base SQLite `shoplite.db`.
5. **Retour** : Les données remontent la chaîne pour être formatées et affichées proprement par l'adaptateur CLI.