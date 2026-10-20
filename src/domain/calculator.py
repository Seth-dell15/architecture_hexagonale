# src/domain/calculator.py

# Constantes métier
LOYALTY_DISCOUNT_RATE = 0.10
VAT_RATE = 0.20

def calculate_order_totals(amount_ht: float, is_loyal: bool) -> tuple[float, float, float]:
    """
    Calcule la remise, le montant après remise et le montant TTC 
    en fonction du montant HT et du statut de fidélité du client.
    
    Args:
        amount_ht (float): Le montant hors taxes de la commande.
        is_loyal (bool): Vrai si le client est fidèle, Faux sinon.
        
    Returns:
        tuple: (discount, amount_after_discount, amount_ttc)
    """
    if amount_ht < 0:
        raise ValueError("Le montant HT ne peut pas être négatif.")

    discount = amount_ht * LOYALTY_DISCOUNT_RATE if is_loyal else 0.0
    amount_after_discount = amount_ht - discount
    amount_ttc = amount_after_discount * (1 + VAT_RATE) 
    
    # Correction propre pour éviter les imprécisions de calcul flottant en Python (ex: 108.00000000000001)
    discount = round(discount, 2)
    amount_ttc = round(amount_ttc, 2)
    
    return discount, amount_after_discount, amount_ttc