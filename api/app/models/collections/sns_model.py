from models.connection import Manager


class SnsModel(Manager):
    def __init__(self):
        self.collection = "sns"

    def get_account(self, query):
        if not isinstance(query, list):
            return {}
        return self.execute(query)
