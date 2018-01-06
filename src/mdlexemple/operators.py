
import datetime
import time
from bases import BaseOperator
from transfert import ModuleFrameTransfert

class ExempleOperator(BaseOperator):
    
    def __init__(self, name):
        self.name = name

    def load(self):
        pass

    def encapsulate(self, data):
        ts = time.time()
        return ModuleFrameTransfert("mdlexemple", "mdlexemple", "read", data, datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), "crc")

    def decapsulate(self, frame):
        return frame