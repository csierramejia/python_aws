import pytest
from mock import patch
from app.app import create_app

@pytest.fixture
def client():
    api = create_app()
    return api.test_client(use_cookies=False)

def decode_api_response(res):
    return res.data.decode('utf8')


def test_get_order_bad_methods(client):
    url = '/orders/{}'.format(5)
    response = client.post(url)
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.put(url)
    assert response.status == '405 METHOD NOT ALLOWED'


@patch("app.api.orders_api.OrdersApi.get_order")
def test_get_order_by_id(mock_get_order_api, client):
    order_id = 5
    url = '/orders/{}'.format(order_id)
    response = client.get(url)
    mock_get_order_api.assert_called_with(str(order_id))


def test_order_stock_bad_method(client):
    url = '/orders/{}/stock'.format(5)
    response = client.post(url)
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.put(url)
    assert response.status == '405 METHOD NOT ALLOWED'

@patch("app.api.orders_api.OrdersApi.order_products_stock")
def test_order_stock(mock_order_products_stock, client):
    order_id = 4
    url = '/orders/{}/stock'.format(order_id)
    response = client.get(url)
    mock_order_products_stock.assert_called_with(str(order_id))
