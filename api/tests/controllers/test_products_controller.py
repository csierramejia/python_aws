import json
from mock import patch
from flask import request
from app.controllers.products_controller import ProductsController

def get_json_content(json_path):
    with open(json_path, 'r') as json_file:
        return json.loads(json_file.read())

SOLD_PRODUCTS = get_json_content("tests/fixtures/sold_products.json")
ORDER_PRODUCTS = get_json_content("tests/fixtures/order_products.json")

def filter_sold_products(reverse=False):
    sold_filtered = sorted(SOLD_PRODUCTS, key=lambda prod: prod['quantity'], reverse=reverse)
    return sold_filtered[:3]


def test_get_stock_information_missing_data():
    response = ProductsController.get_stock_info()
    assert response == {"product_id": 0, "name": "", "quantity": 0}


def test_get_stock_information():
    quantity = 5
    product_info = ORDER_PRODUCTS[1]

    response = ProductsController.get_stock_info(product_info, quantity)
    assert response == {
        "product_id": product_info['product_id'],
        "name": product_info['name'],
        "quantity": quantity
    }

def test_get_inventory_list():
    inventory = [{"id": 1, "quantity":4},{"id": 10, "quantity":34},{"id": 8, "quantity":89}]
    response = ProductsController.get_inventory_list(inventory)

    assert response == {1:4, 10:34, 8:89}


def test_calculate_inventory():
    products_list = {10: 8, 9: 3, 8: 1}
    response = ProductsController.calculate_inventory(ORDER_PRODUCTS, products_list)
    assert response == [
        {**ORDER_PRODUCTS[0], "quantity": 22},
        {**ORDER_PRODUCTS[1], "quantity": 0},
        {**ORDER_PRODUCTS[2], "quantity": 2}
    ]

def test_get_products_list():
    response = ProductsController.get_products_list(ORDER_PRODUCTS)
    assert response == {
        ORDER_PRODUCTS[0]['product_id']: ORDER_PRODUCTS[0]["quantity"],
        ORDER_PRODUCTS[1]['product_id']: ORDER_PRODUCTS[1]["quantity"],
        ORDER_PRODUCTS[2]['product_id']: ORDER_PRODUCTS[2]["quantity"]
    }


def test_clean_product_info():
    response = ProductsController.clean_product_info(ORDER_PRODUCTS[2])
    assert response == {
        "id": ORDER_PRODUCTS[2]['product_id'],
        "name": ORDER_PRODUCTS[2]['name'],
        "provider_id": None,
        "quantity": ORDER_PRODUCTS[2]['quantity']
    }
