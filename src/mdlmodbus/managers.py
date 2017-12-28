 
from bases import BaseManager
from factories import ModuleFactory
		
class ModbusManager(BaseManager):

	def __init__(self, name):
		minprefix = "modbus"
		package = "mdlmodbus"
		super().__init__(name, package, minprefix) 