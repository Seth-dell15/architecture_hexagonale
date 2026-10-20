from typing import Optional
from src.domain.model import Order
from src.ports.order_repository import OrderRepository

class GetOrder:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self, order_id: int) -> Optional[Order]:
        return self.repository.get_by_id(order_id)