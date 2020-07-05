from flask import Blueprint, request
from api.rekognition_api import RekognitionApi

bp = Blueprint(
    "rekognition", __name__, url_prefix="/rekognition"
)


@bp.route("/detect_faces", methods=["POST"])
def detect_faces():
    return RekognitionApi(request).detect_faces()


@bp.route("/detect_text", methods=["POST"])
def detect_text():
    return RekognitionApi(request).detect_text()




