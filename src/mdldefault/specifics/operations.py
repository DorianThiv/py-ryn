
import shlex

from bases import Directory, BaseCommand
from samples.transfert import ModuleFrameTransfert
from mdldefault.specifics.models import DataRawModel
from mdldefault.specifics.exceptions import DefaultCommandError

class DefaultOperations:

    def __init__(self):
        pass

    def operate_up(self, module, data):
        pass
    
    def operate_down(self, frame):
        return DataRawModel(command=frame.command, payload=frame.payload)
