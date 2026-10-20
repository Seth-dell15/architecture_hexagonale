from typing import List, Optional
from src.domain.model import Order
from src.ports.order_repository import OrderRepository

class FakeOrderRepository(OrderRepository):
    """Implémentation en mémoire du port OrderRepository pour les tests unitaires."""

    def __init__(self):
        self.orders: List[Order] = []
        self._next_id = 1

    def save(self, order: Order) -> Order:
        order.id = self._next_id
        self._next_id += 1
        self.orders.append(order)
        return order

    def get_by_id(self, order_id: int) -> Optional[Order]:
        for order in self.orders:
            if order.id == order_id:
                return order
        return None

    def get_all(self) -> List[Order]:
        return list(self.orders)

    def update(self, order: Order) -> None:
        for i, existing in enumerate(self.orders):
            if existing.id == order.id:
                self.orders[i] = order
                return
        raise ValueError(f"Commande introuvable avec l'ID {order.id}")

    def delete(self, order_id: int) -> None:
        order = self.get_by_id(order_id)
        if order:
            self.orders.remove(order)