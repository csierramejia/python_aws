import json
from mock import patch
from app.models import ProvidersModel


@patch("app.models.connection.Manager.execute")
def test_get_providers(mock_execute_query):
    ProvidersModel().get_providers()
    mock_execute_query.assert_called_with("SELECT * FROM providers")
