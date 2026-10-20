from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Order:
    """Représente l'entité métier Order (Commande) au cœur du domaine."""
    customer_name: str
    amount_ht: float
    is_loyal: bool
    discount: float = 0.0
    amount_ttc: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    id: Optional[int] = None

    def __post_init__(self):
        """Validation basique à la création de l'entité."""
        if not self.customer_name or not self.customer_name.strip():
            raise ValueError("Le nom du client ne peut pas être vide.")
        if self.amount_ht < 0:
            raise ValueError("Le montant HT ne peut pas être négatif.")