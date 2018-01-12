import sys

from interfaces import IOperator
from transfert import ModuleFrameTransfert, SimpleFrameTransfert

class TerminalOperator(IOperator):
    
    def __init__(self, name):
        self.name = name

    def load(self):
        pass

    def encapsulate(self, data):
        try:
            __type = data['type']
            if __type == 0:
                f = data
            elif __type == 1:
                f = ModuleFrameTransfert("mdlterminal", "mdlexemple", "write", data["data"], None, "crc")
            elif __type == 2:
                __dest = data["dest-module"]
                f = ModuleFrameTransfert("mdlterminal", __dest, "write", data["data"], "crc")
            return f
        except Exception as e:
            print("[ERROR - ENCAPSULATE - TERMINAL] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))

    def decapsulate(self, frame):
        try:
            return (frame.command, frame.payload)
        except Exception as e:
            print("[ERROR - DECAPSULATE - TERMINAL] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
