import sys
import datetime
import time

from bases import BaseOperator
from transfert import ModuleFrameTransfert, SimpleFrameTransfert

class TerminalOperator(BaseOperator):
    
    def __init__(self, name):
        self.name = name

    def load(self):
        pass

    def encapsulate(self, data):
        ts = time.time()
        try:
            __type = data['type']
            if __type == 0:
                f = data
            elif __type == 1:
                f = ModuleFrameTransfert("mdlterminal", "mdlexemple", "write", data["data"], datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), "crc")
            elif __type == 2:
                __dest = data["dest-module"]
                f = ModuleFrameTransfert("mdlterminal", __dest, "write", data["data"], datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), "crc")
            return f
        except Exception as e:
            print("[ERROR - ENCAPSULATE - TERMINAL] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))

    def decapsulate(self, frame):
        try:
            return (frame.direction, frame.payload)
        except Exception as e:
            print("[ERROR - DECAPSULATE - TERMINAL] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
