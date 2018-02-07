
from mdlutils.bases import BaseRegistry
from mdlmodbus.operators import ModbusOperator

class ModbusRegistry(BaseRegistry):

    def __init__(self, name):
        super().__init__(name)
