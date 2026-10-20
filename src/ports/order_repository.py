# src/ports/order_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.model import Order

class OrderRepository(ABC):
    """Port sortant définissant le contrat pour la persistance des commandes."""

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def get_all(self) -> List[Order]:
        pass

    @abstractmethod
    def update(self, order: Order) -> None:
        pass

    @abstractmethod
    def delete(self, order_id: int) -> None:
        pass