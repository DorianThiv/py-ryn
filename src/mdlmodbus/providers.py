
from bases import BaseProvider

class ModbusProvider(BaseProvider):

    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def action(self, frame):
        binder_type, data = self.registries[0].decapsulate(frame)
        if binder_type == "tcp":
            self.binders["modbus-tcp-binder"].action(data)
        if binder_type == "rtu":
            self.binders["modbus-rtu-binder"].action(data)
        
        
