
import sys
import datetime
import time

from interfaces import IOperator
from transfert import ModuleFrameTransfert
from mdlmodbus.templates import ModbusTreatRequest, ModbusTCPFrame, ModbusRTUFrame

class ModbusOperator(IOperator):
    
    def __init__(self, name):
        self.name = name

    def load(self):
        pass

    def encapsulate(self, data):
        ts = time.time()
        return ModuleFrameTransfert("mdlmodbus", "mdlexemple", "read", data, datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), "crc")

    def decapsulate(self, frame):
        try:
            print(type(frame))
            # if isinstance(frame, ModuleFrameTransfert):
            #     __action = frame.payload[0]
            #     __proto = frame.payload[1].replace("-", "")
            #     if __proto == "tcp":
            #         modbus = ModbusTCPFrame(frame.payload[2:len(frame.payload)])
            #         modbus.serialize()
            #         return modbus

            # __type = frame["type"]
            # if __type == 0:
            #     return frame["action"]

        except Exception as e:
            print("[ERROR - DECAPSULATE - MODBUS] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
        
