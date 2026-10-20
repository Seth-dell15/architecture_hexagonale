import pytest
from tests.unit.fake_repository import FakeOrderRepository
from src.use_cases.create_order import CreateOrder
from src.use_cases.get_order import GetOrder
from src.use_cases.list_orders import ListOrders
from src.use_cases.update_order import UpdateOrder
from src.use_cases.delete_order import DeleteOrder

@pytest.fixture
def repository():
    return FakeOrderRepository()

def test_create_order_use_case(repository):
    use_case = CreateOrder(repository)
    order = use_case.execute("Alice", 100.0, True)

    assert order.id == 1
    assert order.customer_name == "Alice"
    assert order.discount == 10.0
    assert order.amount_ttc == 108.0
    assert len(repository.get_all()) == 1

def test_get_order_use_case(repository):
    create_uc = CreateOrder(repository)
    get_uc = GetOrder(repository)
    
    created = create_uc.execute("Bob", 200.0, False)
    fetched = get_uc.execute(created.id)

    assert fetched is not None
    assert fetched.customer_name == "Bob"
    assert fetched.amount_ttc == 240.0 # 200 + 20% TVA

def test_get_non_existent_order_returns_none(repository):
    get_uc = GetOrder(repository)
    assert get_uc.execute(999) is None

def test_list_orders_use_case(repository):
    create_uc = CreateOrder(repository)
    create_uc.execute("Alice", 100.0, True)
    create_uc.execute("Charlie", 50.0, False)

    list_uc = ListOrders(repository)
    orders = list_uc.execute()

    assert len(orders) == 2
    assert orders[0].customer_name == "Alice"
    assert orders[1].customer_name == "Charlie"

def test_update_order_use_case(repository):
    create_uc = CreateOrder(repository)
    update_uc = UpdateOrder(repository)
    
    created = create_uc.execute("Alice", 100.0, True)
    
    # Mise à jour : passage à 200 HT et perte de la fidélité
    updated = update_uc.execute(created.id, "Alice Modifiée", 200.0, False)

    assert updated.customer_name == "Alice Modifiée"
    assert updated.amount_ht == 200.0
    assert updated.discount == 0.0
    assert updated.amount_ttc == 240.0

def test_update_non_existent_order_raises_error(repository):
    update_uc = UpdateOrder(repository)
    with pytest.raises(ValueError):
        update_uc.execute(999, "Inconnu", 100.0, True)

def test_delete_order_use_case(repository):
    create_uc = CreateOrder(repository)
    delete_uc = DeleteOrder(repository)
    list_uc = ListOrders(repository)

    created = create_uc.execute("Alice", 100.0, True)
    assert len(list_uc.execute()) == 1

    delete_uc.execute(created.id)
    assert len(list_uc.execute()) == 0

def test_delete_non_existent_order_raises_error(repository):
    delete_uc = DeleteOrder(repository)
    with pytest.raises(ValueError):
        delete_uc.execute(999)