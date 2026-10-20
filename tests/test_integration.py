import subprocess
import sqlite3
import os
import pytest

DB_PATH = "data/shoplite.db"

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
    Simule une saisie utilisateur complète via le menu CLI et vérifie l'effet de bord en base.
    """
    user_inputs = "1\nAlice\n100\noui\n6\n"

    result = subprocess.run(
        ["python", "-m", "src.app"],
        input=user_inputs,
        text=True,
        capture_output=True,
        check=True
    )

    # 1. Vérifier que la sortie console contient les éléments clés du récapitulatif
    assert "Commande créée avec succès !" in result.stdout
    assert "Client : Alice" in result.stdout
    assert "Montant HT : 100.00 €" in result.stdout
    assert "Remise : 10.00 €" in result.stdout
    assert "Montant TTC : 108.00 €" in result.stdout

    # 2. Vérifier que la base de données SQLite a bien été créée dans data/ et contient l'enregistrement
    assert os.path.exists(DB_PATH), "Le fichier data/shoplite.db aurait dû être créé."

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

def test_app_invalid_amount_error_scenario():
    """
    Test E2E simulant une erreur de saisie (montant HT invalide avec des lettres) dans la CLI.
    Vérifie que l'application gère l'erreur proprement sans crasher et n'enregistre rien en base.
    """
    # Séquence de touches envoyées au terminal :
    # 1. "1" -> Choisir "Créer une commande"
    # 2. "Bob" -> Nom du client
    # 3. "abc" -> Montant HT invalide (provoque une ValueError dans la CLI)
    # 4. "6" -> Quitter l'application
    user_inputs = "1\nBob\nabc\n6\n"

    result = subprocess.run(
        ["python", "-m", "src.app"],
        input=user_inputs,
        text=True,
        capture_output=True,
        check=True
    )

    # 1. Vérifier que l'application a intercepté l'erreur et l'a affichée
    assert "Erreur :" in result.stdout

    # 2. Vérifier qu'aucune commande n'a été enregistrée en base de données
    if os.path.exists(DB_PATH):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders")
        count = cursor.fetchone()[0]
        connection.close()
        assert count == 0, "Aucune commande ne devrait être enregistrée en cas d'erreur de saisie."