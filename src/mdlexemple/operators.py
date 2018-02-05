
from mdlutils.interfaces import IOperator
from mdlutils.bases import BaseCommand
from mdlutils.transfert import ModuleFrameTransfert, SimpleFrameTransfert

class ExempleOperator(IOperator):
    
    def __init__(self, name):
        self.name = name

    def load(self):
        pass

    def encapsulate(self, data):
        pass

    def decapsulate(self, frame):
        if isinstance(frame, SimpleFrameTransfert):
            return frame.command
        if isinstance(frame, ModuleFrameTransfert):
            return frame.payload[BaseCommand.PARSE_TEXT]