from controllers.rekognition_controller import RekognitionController
from helpers.decorators import flask_request


class RekognitionApi(object):
    def __init__(self, request):
        self.request = request

    @flask_request
    def detect_faces(self):
        file = self.request.files["file"]
        return RekognitionController().detect_faces(file)
    

    @flask_request
    def detect_text(self):
        file = self.request.files["file"]
        return RekognitionController().detect_text(file)


    
