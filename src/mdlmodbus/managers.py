 
from bases import BaseManager
from factories import ModuleFactory
		
class ModbusManager(BaseManager):

	def __init__(self, mod):
		module = mod
		minprefix = "modbus"
		name = minprefix + "-manager"
		super().__init__(name, minprefix, module) 