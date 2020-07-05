import json
from mock import patch
from flask import request
from app.controllers.providers_controller import ProvidersController

def get_json_content(json_path):
    with open(json_path, 'r') as json_file:
        return json.loads(json_file.read())

ORDERS = get_json_content("tests/fixtures/orders.json")

@patch('app.models.ProvidersModel.get_providers')
def test_set_product_providers(mock_get_providers):
    mock_get_providers.return_value = [
        {
            "id": "1",
            "name": "Esteban"
        },
        {
            "id": "2",
            "name": "Carlos"
        }
    ]

    response = ProvidersController().set_product_providers(ORDERS)
    assert 'provider' in response[0]['products'][0]
