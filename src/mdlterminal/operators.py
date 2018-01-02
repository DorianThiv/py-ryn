
import datetime
import time
from bases import BaseOperator
from transfert import FrameTransfert

class TerminalOperator(BaseOperator):
    
    def __init__(self, name):
        self.name = name

    def load(self):
        pass

    def encapsulate(self, data):
        ts = time.time()
        if data['type'] == 0:
            f = FrameTransfert("mdlterminal", "mdlexemple", "write", data, datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), "crc")
        else:
            f = FrameTransfert("mdlterminal", data["dest-module"], "write", data, datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), "crc")
        return f

    def decapsulate(self, frame):
        pass