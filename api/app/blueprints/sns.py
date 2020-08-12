from flask import Blueprint, request
from api.sns_api import SnsApi

bp = Blueprint(
    "sns", __name__, url_prefix="/registro/sns"
)


@bp.route("/send_code_register", methods=["POST"])
def send_code_register():
    return SnsApi(request).send_code_register()


@bp.route("/valid_code/<code>", methods=["GET"])
def valid_code(code):
    return SnsApi(request).valid_code(code)



@bp.route("/", methods=["GET"])
def helloWorld():
  return "Hello, cross-origin-world cors enabled python!"




