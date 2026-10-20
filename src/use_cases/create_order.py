from src.domain.model import Order
from src.domain.calculator import calculate_order_totals
from src.ports.order_repository import OrderRepository

class CreateOrder:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self, customer_name: str, amount_ht: float, is_loyal: bool) -> Order:
        # 1. Calculs métier purs
        discount, _, amount_ttc = calculate_order_totals(amount_ht, is_loyal)

        # 2. Création de l'entité (valide les règles de base)
        order = Order(
            customer_name=customer_name,
            amount_ht=amount_ht,
            is_loyal=is_loyal,
            discount=discount,
            amount_ttc=amount_ttc
        )

        # 3. Persistance via le port
        return self.repository.save(order)