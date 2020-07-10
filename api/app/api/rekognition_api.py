from controllers.rekognition_controller import RekognitionController
from helpers.decorators import flask_request


class RekognitionApi(object):
    def __init__(self, request):
        self.request = request

    @flask_request
    def detect_faces(self):
        return RekognitionController().detect_faces(self.request.json)
    

    @flask_request
    def detect_text(self):
        return RekognitionController().detect_text(self.request.json)


    
