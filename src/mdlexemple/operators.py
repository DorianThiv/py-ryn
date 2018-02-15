
import sys

from bases import BaseCommand, BaseOperator
from mdlexemple.specifics.operations import Operations
from mdlexemple.specifics.models import DataRawModel
from mdlexemple.registries import ExempleRegistry
from mdlutils.transfert import ModuleFrameTransfert, SimpleFrameTransfert

class ExempleOperator(BaseOperator):
    
    def __init__(self, name, provider):
        super().__init__(name, ExempleRegistry("exemple-registry"), provider)

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
                data = DataRawModel(payload=frame.command)
            if isinstance(frame, ModuleFrameTransfert):
                data = DataRawModel(payload=frame.payload[BaseCommand.PARSE_TEXT])
            return data
        except Exception as e:
            print("[ERROR - DECAPSULATE - BASE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))