import json
from decimal import *
from datetime import datetime
from app.helpers import utils

def test_serialize_dict_and_list():
    number_value = 12345
    string_value = "returned string"

    response = utils.serialize_dict_and_list(string_value)
    assert response == string_value and isinstance(response, str), "return passed string"

    response = utils.serialize_dict_and_list(number_value)
    assert response == number_value and isinstance(response, int), "return passed number"

def test_serialize_dict_and_list_string_list_convertion():
    date = datetime.now()
    value = {"name": "tester", "date": date}

    response = utils.serialize_dict_and_list(value)

    value['date'] = str(value['date'])
    assert response == json.dumps(value) and isinstance(response, str)


def test_serialize_dict_and_list_string_decimal_convertion():
    decimal_value = Decimal(23)
    value = {"name": "tester", "quantity": decimal_value}

    response = utils.serialize_dict_and_list(value)

    value['quantity'] = int(value['quantity'])
    assert response == json.dumps(value) and isinstance(response, str)
