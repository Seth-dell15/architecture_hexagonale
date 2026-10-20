# src/adapters/outbound/sqlite_repository.py

import sqlite3
import os
from typing import List, Optional
from src.domain.model import Order
from src.ports.order_repository import OrderRepository

class SqliteOrderRepository(OrderRepository):
    """Adaptateur secondaire gérant la persistance dans une base SQLite."""

    def __init__(self, db_path: str = "data/shoplite.db"):
        self.db_path = db_path
        self._ensure_data_dir()
        self._create_database()

    def _ensure_data_dir(self):
        dir_name = os.path.dirname(self.db_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

    def _create_database(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                amount_ht REAL NOT NULL,
                discount REAL NOT NULL,
                amount_ttc REAL NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()
        connection.close()

    def save(self, order: Order) -> Order:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO orders
            (customer_name, amount_ht, discount, amount_ttc, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                order.customer_name,
                order.amount_ht,
                order.discount,
                order.amount_ttc,
                order.created_at,
            ),
        )
        order.id = cursor.lastrowid
        connection.commit()
        connection.close()
        return order

    def get_by_id(self, order_id: int) -> Optional[Order]:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, customer_name, amount_ht, discount, amount_ttc, created_at FROM orders WHERE id = ?",
            (order_id,)
        )
        row = cursor.fetchone()
        connection.close()

        if not row:
            return None

        return Order(
            id=row[0],
            customer_name=row[1],
            amount_ht=row[2],
            discount=row[3],
            amount_ttc=row[4],
            created_at=row[5],
            is_loyal=(row[3] > 0)  # Déduit de la présence d'une remise
        )

    def get_all(self) -> List[Order]:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, customer_name, amount_ht, discount, amount_ttc, created_at FROM orders")
        rows = cursor.fetchall()
        connection.close()

        orders = []
        for row in rows:
            orders.append(
                Order(
                    id=row[0],
                    customer_name=row[1],
                    amount_ht=row[2],
                    discount=row[3],
                    amount_ttc=row[4],
                    created_at=row[5],
                    is_loyal=(row[3] > 0)
                )
            )
        return orders

    def update(self, order: Order) -> None:
        if order.id is None:
            raise ValueError("Impossible de mettre à jour une commande sans ID.")
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE orders 
            SET customer_name = ?, amount_ht = ?, discount = ?, amount_ttc = ?
            WHERE id = ?
            """,
            (order.customer_name, order.amount_ht, order.discount, order.amount_ttc, order.id)
        )
        connection.commit()
        connection.close()

    def delete(self, order_id: int) -> None:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        connection.commit()
        connection.close()