import pytest
from mock import patch
from app.app import create_app

@pytest.fixture
def client():
    api = create_app()
    return api.test_client(use_cookies=False)


def decode_api_response(res):
    return res.data.decode('utf8')


def test_sold_not_allowed(client):
    url = '/products/sold'
    response = client.post(url)
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.put(url)
    assert response.status == '405 METHOD NOT ALLOWED'


@patch("app.api.products_api.ProductsApi.sold_products")
def test_sold(mock_sold, client):
    client.get('/products/sold')
    mock_sold.assert_called()


def test_inventory_not_allowed(client):
    url = '/products/inventory'
    response = client.post(url)
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.put(url)
    assert response.status == '405 METHOD NOT ALLOWED'


@patch("app.api.products_api.ProductsApi.new_inventory")
def test_new_inventory(mock_new_inventory, client):
    client.get('/products/inventory')
    mock_new_inventory.assert_called()


def test_organize_inventory_not_allowed(client):
    url = '/products/organize/inventory'
    response = client.post(url)
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.put(url)
    assert response.status == '405 METHOD NOT ALLOWED'


@patch("app.api.products_api.ProductsApi.organize_from_inventory")
def test_organize_inventory(mock_organize_inventory, client):
    client.get('/products/organize/inventory')
    mock_organize_inventory.assert_called()


def test_organize_providers_not_allowed(client):
    url = '/products/organize/providers'
    response = client.post(url)
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.put(url)
    assert response.status == '405 METHOD NOT ALLOWED'


@patch("app.api.products_api.ProductsApi.organize_from_providers")
def test_organize_providers(mock_organize_providers, client):
    client.get('/products/organize/providers')
    mock_organize_providers.assert_called()
