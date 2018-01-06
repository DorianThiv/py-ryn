
import sys
import datetime
import time
from bases import BaseOperator
from transfert import ModuleFrameTransfert

class ModbusOperator(BaseOperator):
    
    def __init__(self, name):
        self.name = name

    def load(self):
        pass

    def encapsulate(self, data):
        ts = time.time()
        return ModuleFrameTransfert("mdlmodbus", "mdlexemple", "read", data, datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), "crc")

    def decapsulate(self, frame):
        try:
            __type = frame["type"]
            if __type == 0:
                return frame["action"]
            else:
                __action = frame.payload[0]
                __proto = frame.payload[1]
                __dev, __dev_value = (frame.payload[2], frame.payload[3])
                __reg, __reg_value = (frame.payload[4], frame.payload[5])
                __val, __val_value = (frame.payload[6], frame.payload[7])
                return (None, None)
        except Exception as e:
            print("[ERROR - DECAPSULATE - MODBUS] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
        
