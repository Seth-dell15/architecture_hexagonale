from src.domain.model import Order
from src.domain.calculator import calculate_order_totals
from src.ports.order_repository import OrderRepository

class UpdateOrder:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self, order_id: int, customer_name: str, amount_ht: float, is_loyal: bool) -> Order:
        order = self.repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Commande introuvable avec l'ID {order_id}.")

        # Recalcul des montants si modification financière
        discount, _, amount_ttc = calculate_order_totals(amount_ht, is_loyal)

        order.customer_name = customer_name
        order.amount_ht = amount_ht
        order.is_loyal = is_loyal
        order.discount = discount
        order.amount_ttc = amount_ttc

        self.repository.update(order)
        return order