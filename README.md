# ShopLite

Application en ligne de commande permettant d'enregistrer des commandes clients. Développé dans le cadre d'un projet fil rouge sur l'architecture logicielle et la refactorisation (passage à une architecture hexagonale).

---

## Prérequis

- **Python** : 3.10 ou supérieur
- **Dépendances** : Aucune dépendance externe (hors outils de test)

---

## Installation et environnement de développement

1. **Cloner le projet** :
   ```bash
   git clone <url-du-repo>
   cd ShopLite
   ```

2. **Créer et activer un environnement virtuel** :
   ```bash
   python -m venv venv
   # Sur macOS / Linux :
   source venv/bin/activate
   # Sur Windows (Git Bash / PowerShell) :
   # venv\Scripts\activate
   ```

3. **Installer les dépendances de test** :
   ```bash
   pip install pytest
   ```

---

## Lancer l'application

Depuis la racine du projet (avec le venv activé) :

```bash
python src/app.py
```

---

## Lancer les tests

Pour exécuter le test d'intégration (filet de sécurité avant refactorisation) :
```bash
pytest
```

---

## Documentation du projet

Pour en savoir plus sur la conception de l'application :
- [Architecture Cible et CRUD](./docs/ARCHITECTURE.md)
- [Justifications des choix architecturaux](./docs/ARCH_JUSTIFICATIONS.md)
- [Stratégie de test](./docs/TESTING_STRATEGY.md)