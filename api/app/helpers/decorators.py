from flask import Response
from helpers.utils import serialize_dict_and_list


def flask_request(fun):
    def inner(*args, **kwargs):
        result = []
        status = "error"
        error_message = ""
        status_code = "500"

        try:
            status = "success"
            status_code = "200"
            result = fun(*args, **kwargs)

        except Exception as error:
            error_message = str(error)

        result = {"status": status, "data": result, "error": error_message}
        return Response(
            serialize_dict_and_list(result), status_code, mimetype="application/json"
        )

    return inner
