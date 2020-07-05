from mock import patch
from app.models import OrdersProductsModel

@patch("app.models.connection.Manager.execute")
def test_products_by_order_id_empty_id(mock_execute_query):
    instance = OrdersProductsModel()
    response = instance.products_by_order_id()

    assert response == []
    mock_execute_query.assert_not_called()


@patch("app.models.connection.Manager.execute")
def test_products_by_order_id(mock_execute_query):
    instance = OrdersProductsModel()

    order_id = 1
    response = instance.products_by_order_id(order_id)

    called_query = "SELECT op.*, p.quantity AS inventory, p.name AS name, p.provider_id AS provider_id " \
            "FROM orders_products as op INNER JOIN products as p ON p.id = op.product_id " \
            "WHERE order_id = '{}'".format(order_id)

    mock_execute_query.assert_called_once_with(called_query)


@patch("app.models.connection.Manager.execute")
def test_products_by_order_id_list_of_id(mock_execute_query):
    instance = OrdersProductsModel()

    order_ids = [1,2,3]
    response = instance.products_by_order_id(order_ids)

    called_query = "SELECT op.*, p.quantity AS inventory, p.name AS name, p.provider_id AS provider_id " \
            "FROM orders_products as op INNER JOIN products as p ON p.id = op.product_id " \
            "WHERE order_id IN (1, 2, 3)"

    mock_execute_query.assert_called_once_with(called_query)


@patch("app.models.connection.Manager.execute")
def test_sold_products_by_date(mock_execute_query):
    limit = 6
    search_date = "2019-03-01"

    instance = OrdersProductsModel()
    response = instance.sold_products_by_date(search_date=search_date, limit=limit)

    called_query = \
        "SELECT op.product_id AS product_id, p.name AS name, SUM(op.quantity) AS quantity " \
        "FROM orders AS o RIGHT JOIN orders_products AS op ON o.id = op.order_id " \
        "INNER JOIN products AS p ON p.id = op.product_id " \
        "WHERE deliveryDate = '{}' GROUP BY product_id ORDER BY quantity asc LIMIT {}".format(
            search_date,
            limit
        )

    mock_execute_query.assert_called_once_with(called_query)


@patch("app.models.connection.Manager.execute")
def test_sold_products_by_date_passing_order_by(mock_execute_query):
    limit = 6
    search_date = '2019-03-01'

    instance = OrdersProductsModel()
    response = instance.sold_products_by_date(limit=limit, order_by="DESC")

    called_query = \
        "SELECT op.product_id AS product_id, p.name AS name, SUM(op.quantity) AS quantity " \
        "FROM orders AS o RIGHT JOIN orders_products AS op ON o.id = op.order_id " \
        "INNER JOIN products AS p ON p.id = op.product_id " \
        "WHERE deliveryDate = '{}' GROUP BY product_id ORDER BY quantity DESC LIMIT {}".format(
            search_date,
            limit
        )

    mock_execute_query.assert_called_once_with(called_query)
