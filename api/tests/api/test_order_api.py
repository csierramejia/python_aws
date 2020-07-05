import json
from mock import patch
from flask import request
from app.api.orders_api import OrdersApi

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

@patch("app.models.OrdersModel.get_order", return_value=ORDERS[2])
def test_get_order(mock_get_order):
    instance = OrdersApi(request)

    order_id = 10
    response = instance.get_order(order_id)
    result = json.loads(response.data.decode('utf8'))

    mock_get_order.assert_called_once_with(order_id)
    assert result['data'] == ORDERS[2]


@patch("app.models.OrdersProductsModel.products_by_order_id", return_value=ORDER_PRODUCTS)
def test_stock_products(mock_order_products_by_id):
    instance = OrdersApi(request)

    order_id = 10
    products = list(map(filter_product, ORDER_PRODUCTS))

    response = instance.order_products_stock(order_id)
    result = json.loads(response.data.decode('utf8'))

    assert result['data'] == {
        "out_of_stock": [
            {**products[1]}, {**products[2], 'quantity': 2}
        ],
        "in_stock": [
            {**products[0]}, {**products[2], 'quantity': 1}
        ]
    }

    mock_order_products_by_id.assert_called_once_with(order_id)
