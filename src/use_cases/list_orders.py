from typing import List
from src.domain.model import Order
from src.ports.order_repository import OrderRepository

class ListOrders:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self) -> List[Order]:
        return self.repository.get_all()