

class DataRawModel:

    def __init__(self, command = None, address=None, payload=None, binder=None):
        self.command = command
        self.address = address
        self.payload = payload
        self.binder = binder