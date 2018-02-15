

class DataRawModel:

    def __init__(self, payload=None, binder=None):
        self.payload = payload
        self.binder = binder
        
    def __str__(self):
        return "{}".format(self.payload)