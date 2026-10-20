import pytest
from src.domain.calculator import calculate_order_totals
from src.domain.model import Order

def test_calculator_zero_amount():
    """Vérifie le calcul avec un montant HT de 0."""
    discount, after_discount, ttc = calculate_order_totals(0.0, is_loyal=True)
    assert discount == 0.0
    assert after_discount == 0.0
    assert ttc == 0.0

def test_calculator_decimal_amounts():
    """Vérifie la précision des arrondis avec des montants décimaux."""
    # 99.99 HT, client fidèle -> 10% de remise = 10.00 (arrondi) ou 9.999 ? 
    # Notre calculateur fait amount_ht * 0.10 -> 9.999 arrondi à 10.00
    discount, after_discount, ttc = calculate_order_totals(99.99, is_loyal=True)
    assert discount == 10.00
    assert after_discount == 89.99
    assert ttc == round(89.99 * 1.20, 2)

def test_order_whitespace_name_raises_error():
    """Vérifie qu'un nom composé uniquement d'espaces lève une erreur."""
    with pytest.raises(ValueError):
        Order(customer_name="   ", amount_ht=100.0, is_loyal=False)