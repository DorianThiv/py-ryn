
import sys

from bases import BaseOperator
from mdlmodbus.registries import ModbusRegistry

class ModbusOperator(BaseOperator):
     
    def __init__(self, name, provider):
        super().__init__(name, ModbusRegistry("modbus-registry"), provider)

    def load(self):
        pass

    def execute(self, frame):
        b_type, payload = self.decapsulate(frame)
        if b_type == "tcp":
            self.binders["modbus-tcp-binder"].execute(payload)
        if b_type == "rtu": 
            self.binders["modbus-rtu-binder"].execute(payload)

    def encapsulate(self, data):
        pass

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
        
