from controllers.voice_controller import VoiceController
from helpers.decorators import flask_request


class VoiceApi(object):
    def __init__(self, request):
        self.request = request

    @flask_request
    def send_code_register(self):
        return VoiceController().send_code_register(self.request.json)


    
