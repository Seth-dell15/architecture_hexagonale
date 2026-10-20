from src.adapters.outbound.sqlite_repository import SqliteOrderRepository
from src.use_cases.create_order import CreateOrder
from src.use_cases.get_order import GetOrder
from src.use_cases.list_orders import ListOrders
from src.use_cases.update_order import UpdateOrder
from src.use_cases.delete_order import DeleteOrder
from src.adapters.inbound.cli import ShopLiteCLI

def main():
    # 1. Instanciation de l'adaptateur de persistance (Sortant)
    repository = SqliteOrderRepository()

    # 2. Instanciation des cas d'utilisation en leur injectant le dépôt (Principe d'Inversion des Dépendances)
    create_order = CreateOrder(repository)
    get_order = GetOrder(repository)
    list_orders = ListOrders(repository)
    update_order = UpdateOrder(repository)
    delete_order = DeleteOrder(repository)

    # 3. Instanciation et lancement de l'adaptateur CLI (Entrant)
    cli = ShopLiteCLI(
        create_order=create_order,
        get_order=get_order,
        list_orders=list_orders,
        update_order=update_order,
        delete_order=delete_order
    )
    cli.run()

if __name__ == "__main__":
    main()