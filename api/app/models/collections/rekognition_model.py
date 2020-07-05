from models.connection import Manager


class RekognitionModel(Manager):
    def __init__(self):
        self.collection = "rekognition"

    def get_account(self, query):
        if not isinstance(query, list):
            return {}
        return self.execute(query)
