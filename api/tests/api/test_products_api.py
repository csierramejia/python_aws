import json
from mock import patch
from flask import request
from app.api.products_api import ProductsApi

def get_json_content(json_path):
    with open(json_path, 'r') as json_file:
        return json.loads(json_file.read())

SOLD_PRODUCTS = get_json_content("tests/fixtures/sold_products.json")
ORDERS = get_json_content("tests/fixtures/orders.json")

def filter_sold_products(reverse=False):
    sold_filtered = sorted(SOLD_PRODUCTS, key=lambda prod: prod['quantity'], reverse=reverse)
    return sold_filtered[:3]


@patch("flask.request")
@patch("app.models.OrdersProductsModel.sold_products_by_date")
def test_sold_descending(mock_sold_products_by_date, mock_request):
    mock_request.args.return_value = {}
    mock_sold_products_by_date.return_value = filter_sold_products()

    response = ProductsApi(mock_request).sold_products()
    result = json.loads(response.data.decode('utf8'))
    assert result['data'] == [SOLD_PRODUCTS[5], SOLD_PRODUCTS[1], SOLD_PRODUCTS[2]]


@patch("flask.request")
@patch("app.models.OrdersProductsModel.sold_products_by_date")
def test_sold_ascending(mock_sold_products_by_date, mock_request):
    mock_request.args.return_value = {}
    mock_sold_products_by_date.return_value = filter_sold_products(True)

    response = ProductsApi(mock_request).sold_products()
    result = json.loads(response.data.decode('utf8'))
    assert result['data'] == [SOLD_PRODUCTS[0], SOLD_PRODUCTS[4], SOLD_PRODUCTS[7]]


@patch("flask.request")
@patch('app.models.ProductsModel.get_inventory')
@patch('app.controllers.orders_controller.OrdersController.get_orders_with_products')
def test_calc_products_to_organize(mock_get_orders_with_products, mock_get_inventory, mock_request):
    mock_request.args.return_value = {}
    mock_get_orders_with_products.return_value = ORDERS
    mock_get_inventory.return_value = [
        {"id": 1, "quantity":4},
        {"id": 10, "quantity":34},
        {"id": 8, "quantity":89}
    ]

    orders, inventory = ProductsApi(mock_request).calc_products_to_organize()
    assert inventory == {1:4, 10:34, 8:89}
    assert len(orders) == 2
    assert len(orders[0]['products']) == 3


@patch("flask.request")
@patch('app.models.ProductsModel.get_inventory')
@patch('app.models.OrdersProductsModel.sold_products_by_date')
def test_new_inventory(mock_sold_products_by_date, mock_get_inventory, mock_request):
    mock_request.args.return_value = {}
    mock_sold_products_by_date.return_value = SOLD_PRODUCTS
    mock_get_inventory.return_value = [
        {"id": 1, "quantity":4},
        {"id": 10, "quantity":34},
        {"id": 8, "quantity":89}
    ]

    response = ProductsApi(mock_request).new_inventory()
    result = json.loads(response.data.decode('utf8'))
    assert result['data'] == [
        {"quantity": 3, "id": 1},
        {"quantity": 34, "id": 10},
        {"quantity": 89, "id": 8}
    ]


@patch("flask.request", return_value = {})
@patch('app.models.ProductsModel.get_inventory', return_value = [])
@patch('app.models.OrdersProductsModel.sold_products_by_date', return_value = [])
def test_new_inventory_empty(mock_sold_products_by_date, mock_get_inventory, mock_request):
    response = ProductsApi(mock_request).new_inventory()
    result = json.loads(response.data.decode('utf8'))
    assert result['data'] == []
