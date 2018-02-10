import sys

from bases import BaseCommand, BaseOperator
from mdlutils.transfert import ModuleFrameTransfert, SimpleFrameTransfert
from mdlterminal.specifics.exceptions import TerminalCommandError
from mdlterminal.registries import TerminalRegistry
from mdlterminal.specifics.models import DataRawModel
from mdlterminal.specifics.operations import Operations

class TerminalOperator(BaseOperator):

    def __init__(self, name, provider):
        super().__init__(name, TerminalRegistry("terminal-operator"), provider)

    def encapsulate(self, data):
        frame = Operations.operate(self.module, data)
        if isinstance(frame, ModuleFrameTransfert) or isinstance(frame, SimpleFrameTransfert):
            return frame
        else:
            self.logger.log(0, "Transfert cannot be done. The frame format is : '{}'".format(type(frame)))
            raise TypeError("Transfert cannot be done. Cannot convert '{}' to 'ModuleFrameTransfert' or 'SimpleFrameTransfert'".format(type(frame)))

    def decapsulate(self, frame):
        try:
            if isinstance(frame, SimpleFrameTransfert):
                data = DataRawModel(frame.command)
            if isinstance(frame, ModuleFrameTransfert):
                data = DataRawModel(frame.payload[BaseCommand.PARSE_DIRECTION], frame.payload[BaseCommand.PARSE_ADDRESS], frame.payload[BaseCommand.PARSE_TEXT])
            return data
        except Exception as e:
            print("[ERROR - DECAPSULATE - BASE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
    
    def emit(self, data):
        try:
            for observer in self.observers:
                decaps_data = self.encapsulate(data)
                observer.update(decaps_data)
        except TerminalCommandError as e:
            data.payload = e.message
            data.binder.write(data)
        except Exception as e:
            print("[ERROR - TERMINAL - OPERATOR - UPDATE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e)) 

