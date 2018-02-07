
from mdlexemple.registries import ExempleRegistry
from mdlutils.bases import BaseCommand, BaseOperator
from mdlutils.transfert import ModuleFrameTransfert, SimpleFrameTransfert

class ExempleOperator(BaseOperator):
    
    def __init__(self, name, provider):
        super().__init__(name, ExempleRegistry("exemple-registry"), provider)

    def encapsulate(self, data):
        pass

    def decapsulate(self, frame):
        if isinstance(frame, SimpleFrameTransfert):
            return frame.command
        if isinstance(frame, ModuleFrameTransfert):
            return frame.payload[BaseCommand.PARSE_TEXT]