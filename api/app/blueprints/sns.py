from flask import Blueprint, request
from api.sns_api import SnsApi
from flask_cors import CORS, cross_origin

bp = Blueprint(
    "sns", __name__, url_prefix="/registro/sns"
)


@bp.route("/send_code_register", methods=["POST"])
@cross_origin()
def send_code_register():
    return SnsApi(request).send_code_register()


@bp.route("/valid_code/<code>", methods=["GET"])
@cross_origin()
def valid_code(code):
    return SnsApi(request).valid_code(code)




