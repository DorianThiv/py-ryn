
import json
from bases import BaseBinder

class ModbusTcpBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self, observable):
        pass

    def read(self):
        data = "Modbus TCP Binder"
        self.observable.observers_update(data)

    def write(self):
        pass

class ModbusRtuBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self, observable):
        pass

    def read(self):
        data = "Modbus RTU Binder"
        self.observable.observers_update(data)

    def write(self):
        pass
    
