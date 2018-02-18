
from bases import BaseCommand

class DataRawModel:

    COMMAND = "command"
    ADDRESS = "address"
    PAYLOAD = "payload"
    BINDER = "binder"

    def __init__(self, command=None, address=None, payload=None, binder=None):
        self.command = command
        self.address = address
        self.payload = payload
        self.binder = binder

    def serialize(self):
        _dict = {}
        _dict[DataRawModel.BINDER] = self.binder
        _dict[BaseCommand.PARSE_COMMAND] = self.command
        _dict[BaseCommand.PARSE_TEXT] = self.payload
        _dict[BaseCommand.PARSE_ADDRESS] = self.address[BaseCommand.PARSE_ADDRESS]

    @staticmethod
    def deserialize(model):
        if not isinstance(model, dict):
            raise TypeError("cannot convert '{}' in 'dict' type".format(type(model)))
        return DataRawModel(model[DataRawModel.COMMAND], model[DataRawModel.PAYLOAD], model[DataRawModel.BINDER])

    def __str__(self):
        return "Address: {}, Payload: {}".format(self.address, self.payload)


