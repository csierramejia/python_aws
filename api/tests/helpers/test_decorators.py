import json
from datetime import datetime
from app.helpers import decorators

REQUEST_RESPONSE_DECO = "Hello World"
REQUEST_EXCEPTION_DECO = "Exception Testing"

@decorators.flask_request
def flask_request_decorated_function(raise_exception=False):
    if raise_exception:
        raise Exception(REQUEST_EXCEPTION_DECO)

    return REQUEST_RESPONSE_DECO

def test_flask_request_exception():
    response = flask_request_decorated_function(True)
    result = json.loads(response.data.decode('utf8'))
    assert "error" in result and result['error'] == REQUEST_EXCEPTION_DECO

def test_flask_request():
    response = flask_request_decorated_function()
    result = json.loads(response.data.decode('utf8'))
    assert result['data'] == REQUEST_RESPONSE_DECO
