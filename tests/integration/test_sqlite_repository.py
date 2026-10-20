# tests/integration/test_sqlite_repository.py

import os
import pytest
from src.adapters.outbound.sqlite_repository import SqliteOrderRepository
from src.domain.model import Order

TEST_DB_PATH = "data/test_shoplite.db"

@pytest.fixture
def repository():
    """Fixture qui initialise un dépôt SQLite propre avec une base de test isolée."""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    repo = SqliteOrderRepository(db_path=TEST_DB_PATH)
    yield repo
    
    # Nettoyage après le test
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_save_and_get_by_id(repository):
    """Vérifie la sauvegarde d'une commande et sa récupération par ID."""
    order = Order(
        customer_name="Alice",
        amount_ht=100.0,
        is_loyal=True,
        discount=10.0,
        amount_ttc=108.0
    )
    saved_order = repository.save(order)
    
    assert saved_order.id is not None
    
    fetched = repository.get_by_id(saved_order.id)
    assert fetched is not None
    assert fetched.customer_name == "Alice"
    assert fetched.amount_ht == 100.0
    assert fetched.discount == 10.0
    assert fetched.amount_ttc == 108.0

def test_get_by_id_not_found(repository):
    """Vérifie qu'un ID inexistant retourne None."""
    fetched = repository.get_by_id(999)
    assert fetched is None

def test_get_all_orders(repository):
    """Vérifie la récupération de toutes les commandes."""
    repository.save(Order(customer_name="Alice", amount_ht=100.0, is_loyal=False, discount=0.0, amount_ttc=120.0))
    repository.save(Order(customer_name="Bob", amount_ht=200.0, is_loyal=True, discount=20.0, amount_ttc=216.0))
    
    orders = repository.get_all()
    assert len(orders) == 2
    assert orders[0].customer_name == "Alice"
    assert orders[1].customer_name == "Bob"

def test_update_order(repository):
    """Vérifie la mise à jour d'une commande en base."""
    order = repository.save(Order(
        customer_name="Alice",
        amount_ht=100.0,
        is_loyal=True,
        discount=10.0,
        amount_ttc=108.0
    ))
    
    # Modification des valeurs
    order.customer_name = "Alice Modifiée"
    order.amount_ht = 200.0
    order.discount = 20.0
    order.amount_ttc = 216.0
    
    repository.update(order)
    
    updated = repository.get_by_id(order.id)
    assert updated.customer_name == "Alice Modifiée"
    assert updated.amount_ht == 200.0
    assert updated.amount_ttc == 216.0

def test_delete_order(repository):
    """Vérifie la suppression d'une commande en base."""
    order = repository.save(Order(
        customer_name="Alice",
        amount_ht=100.0,
        is_loyal=False,
        discount=0.0,
        amount_ttc=120.0
    ))
    order_id = order.id
    
    repository.delete(order_id)
    assert repository.get_by_id(order_id) is None