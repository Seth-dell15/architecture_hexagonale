import pytest
from src.domain.calculator import calculate_order_totals

def test_calculator_with_loyalty():
    """Vérifie le calcul avec une remise fidélité (10%) et TVA (20%)."""
    # 100 HT, client fidèle -> 10 de remise, 90 HT remisé, 108 TTC
    discount, after_discount, ttc = calculate_order_totals(100.0, is_loyal=True)
    
    assert discount == 10.0
    assert after_discount == 90.0
    assert ttc == 108.0

def test_calculator_without_loyalty():
    """Vérifie le calcul sans remise fidélité (0%) et avec TVA (20%)."""
    # 100 HT, client non fidèle -> 0 de remise, 100 HT remisé, 120 TTC
    discount, after_discount, ttc = calculate_order_totals(100.0, is_loyal=False)
    
    assert discount == 0.0
    assert after_discount == 100.0
    assert ttc == 120.0

def test_calculator_negative_amount_raises_error():
    """Vérifie qu'un montant négatif lève bien une exception ValueError."""
    with pytest.raises(ValueError):
        calculate_order_totals(-50.0, is_loyal=True)