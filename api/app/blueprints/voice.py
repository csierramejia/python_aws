from flask import Blueprint, request
from api.voice_api import VoiceApi

bp = Blueprint(
    "voice", __name__, url_prefix="/registro/voice"
)


@bp.route("/send_code_register", methods=["POST"])
def send_code_register():
    return VoiceApi(request).send_code_register()







