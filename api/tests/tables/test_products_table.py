from mock import patch
from app.models import ProductsModel

@patch("app.models.connection.Manager.execute")
def test_get_inventory(mock_execute_query):
    ProductsModel().get_inventory()

    mock_execute_query.assert_called_with("SELECT id, name, quantity FROM products")

@patch("app.models.connection.Manager.execute")
def test_get_orders_products(mock_execute_query):
    ProductsModel().get_orders_products()

    query = "SELECT p.*, op.order_id AS order_id FROM products AS p " \
            "INNER JOIN orders_products AS op ON p.id = op.product_id"

    mock_execute_query.assert_called_once_with(query)
