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

    # 1. Calcul et arrondi immédiat de la remise
    discount = round(amount_ht * LOYALTY_DISCOUNT_RATE, 2) if is_loyal else 0.0
    
    # 2. Calcul du montant après remise (arrondi aussi pour la propreté financière)
    amount_after_discount = round(amount_ht - discount, 2)
    
    # 3. Calcul et arrondi du TTC
    amount_ttc = round(amount_after_discount * (1 + VAT_RATE), 2)
    
    return discount, amount_after_discount, amount_ttc