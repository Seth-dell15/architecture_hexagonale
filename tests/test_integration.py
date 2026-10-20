import subprocess
import sqlite3
import os
import pytest

DB_PATH = "shoplite.db"

@pytest.fixture(autouse=True)
def clean_database():
    """Nettoie la base de données avant et après le test."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_app_nominal_scenario():
    """
    Test d'intégration "boîte noire" de l'application ShopLite.
    Simule une saisie utilisateur complète et vérifie l'effet de bord (base de données).
    """
    # Données simulées envoyées au terminal : 
    # 1. Nom : Alice
    # 2. Montant HT : 100
    # 3. Client fidèle : oui
    user_inputs = "Alice\n100\noui\n"

    # Exécution du script app.py en tant que processus externe
    result = subprocess.run(
        ["python", "src/app.py"],
        input=user_inputs,
        text=True,
        capture_output=True,
        check=True
    )

    # 1. Vérifier que la sortie console contient les éléments clés du récapitulatif
    assert "Commande enregistrée !" in result.stdout
    assert "Client : Alice" in result.stdout
    assert "Montant HT : 100.00 €" in result.stdout
    assert "Remise : 10.00 €" in result.stdout
    assert "Montant TTC : 108.00 €" in result.stdout

    # 2. Vérifier que la base de données SQLite a bien été créée et contient l'enregistrement
    assert os.path.exists(DB_PATH), "Le fichier shoplite.db aurait dû être créé."

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT customer_name, amount_ht, discount, amount_ttc FROM orders")
    row = cursor.fetchone()
    connection.close()

    assert row is not None, "La table orders ne devrait pas être vide."
    customer_name, amount_ht, discount, amount_ttc = row

    # 3. Validation de l'intégrité métier en base
    assert customer_name == "Alice"
    assert amount_ht == 100.0
    assert discount == 10.0
    assert amount_ttc == 108.0