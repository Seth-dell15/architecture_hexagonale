from src.ports.order_repository import OrderRepository

class DeleteOrder:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self, order_id: int) -> None:
        order = self.repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Commande introuvable avec l'ID {order_id}.")
        self.repository.delete(order_id)