
from bases import BaseRegistry

from mdlmodbus.operators import ModbusOperator

class ModbusRegistry(BaseRegistry):

    def __init__(self, name, provider):
        super().__init__(name, ModbusOperator("modbus-operator"), provider)

    def action(self, frame):
        b_type, payload = self.operator.decapsulate(frame)
        if b_type == "tcp":
            self.binders["modbus-tcp-binder"].action(payload)
        if b_type == "rtu": 
            self.binders["modbus-rtu-binder"].action(payload)
