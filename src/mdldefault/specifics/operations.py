
import shlex

from bases import BaseDirectory, BaseCommand
from samples.transfert import ModuleFrameTransfert
from mdldefault.specifics.models import DataRawModel

class DefaultOperations:

    def __init__(self):
        pass

    def operate_up(self, module, data):
        # return ModuleFrametransfert
        pass

    def operate_down(self, frame):
        return DataRawModel(command=frame.command, payload=frame.payload)