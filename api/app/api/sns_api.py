from controllers.sns_controller import SnsController
from helpers.decorators import flask_request


class SnsApi(object):
    def __init__(self, request):
        self.request = request

    @flask_request
    def send_code_register(self):
        return SnsController().send_code_register(self.request.json)
    

    @flask_request
    def valid_code(self, code):
        return SnsController().valid_code(code)


    
