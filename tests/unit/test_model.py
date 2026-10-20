import pytest
from src.domain.model import Order

def test_create_valid_order():
    """Vérifie la création d'une entité Order valide."""
    order = Order(
        customer_name="Alice",
        amount_ht=100.0,
        is_loyal=True,
        discount=10.0,
        amount_ttc=108.0
    )
    assert order.customer_name == "Alice"
    assert order.amount_ht == 100.0
    assert order.is_loyal is True
    assert order.discount == 10.0
    assert order.amount_ttc == 108.0
    assert order.id is None

def test_order_empty_name_raises_error():
    """Vérifie qu'un nom vide lève une exception ValueError."""
    with pytest.raises(ValueError):
        Order(customer_name="", amount_ht=100.0, is_loyal=False)

def test_order_negative_amount_raises_error():
    """Vérifie qu'un montant négatif lève une exception ValueError."""
    with pytest.raises(ValueError):
        Order(customer_name="Bob", amount_ht=-10.0, is_loyal=False)