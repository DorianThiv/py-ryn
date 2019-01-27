
from bases import BaseCommand

class DataRawModel:

    COMMAND = "command"
    ADDRESS = "address"
    PAYLOAD = "payload"
    PROVIDER = "provider"
    BINDER = "binder"

    def __init__(self, command=None, address=None, payload=None, binder=None, provider= None):
        self.command = command
        self.address = address
        self.payload = payload
        self.provider = provider
        self.binder = binder

    def serialize(self):
        pass

    @staticmethod
    def deserialize(model):
        pass

    def __str__(self):
        return "Address: {}, Payload: {}".format(self.address, self.payload)


