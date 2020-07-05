import json
from mock import patch
from app.models import OrdersModel

def get_orders():
    with open('tests/fixtures/orders.json', 'r') as json_file:
        return json.loads(json_file.read())

ORDERS = get_orders()


@patch("app.models.connection.Manager.execute")
def test_get_all_orders(mock_execute_query):
    OrdersModel().get_all_orders()
    mock_execute_query.assert_called_with("SELECT * FROM orders")


@patch("app.models.connection.Manager.execute")
def test_get_order_with_no_id(mock_execute_query):
    instance = OrdersModel()
    response = instance.get_order()

    assert response == {}
    mock_execute_query.assert_not_called()

@patch("app.models.connection.Manager.execute", return_value=[ORDERS[1]])
def test_get_order(mock_execute_query):
    instance = OrdersModel()

    order_id = 1
    response = instance.get_order(order_id)

    called_query = "SELECT * FROM orders WHERE `id` = '{}'".format(order_id)
    mock_execute_query.assert_called_once_with(called_query)
    assert response == ORDERS[1]
