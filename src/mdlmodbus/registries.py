
from bases import BaseRegistry

from mdlmodbus.operators import ModbusOperator

class ModbusRegistry(BaseRegistry):

    def __init__(self, name):
        super().__init__(name, ModbusOperator("modbus-operator"))

    def load(self, providers):
        for provider in providers:
            self.observers.append(provider)