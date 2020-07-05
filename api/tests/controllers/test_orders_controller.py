import json
from mock import patch
from flask import request
from app.controllers.orders_controller import OrdersController

def get_json_content(json_path):
    with open(json_path, 'r') as json_file:
        return json.loads(json_file.read())

def filter_product(product):
    return {
        'quantity': product['quantity'],
        'product_id': product['product_id'],
        'name': product['name']
    }

ORDERS = get_json_content("tests/fixtures/orders.json")
ORDER_PRODUCTS = get_json_content("tests/fixtures/order_products.json")

@patch("app.models.OrdersModel.get_all_orders", return_value = ORDERS)
@patch("app.models.OrdersProductsModel.products_by_order_id", return_value=ORDER_PRODUCTS)
def test_get_orders_with_products(mock_products_by_order_id, mock_get_all_orders):
    response = OrdersController().get_orders_with_products()
    mock_products_by_order_id.assert_called_with([1, 3, 2])

@patch("app.models.OrdersModel.get_all_orders")
def test_get_priorized_orders(mock_get_all_orders):
    mock_get_all_orders.return_value = ORDERS

    response = OrdersController().get_priorized_orders()
    assert response == [ORDERS[0], ORDERS[2], ORDERS[1]]

@patch("app.models.OrdersModel.get_all_orders")
def test_get_priorized_orders_empty(mock_get_all_orders):
    mock_get_all_orders.return_value = []

    response = OrdersController().get_priorized_orders()
    assert not response

@patch('app.controllers.orders_controller.OrdersController.get_orders_with_products')
def test_get_complete_grouped_orders(mock_get_orders_with_products):
    mock_get_orders_with_products.return_value = ORDERS
    response = OrdersController().get_complete_grouped_orders()
    assert len(response) == 2
    assert len(response[0]['products']) == 2
