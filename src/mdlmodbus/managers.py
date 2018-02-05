 
from bases import BaseManager
from factories import ModuleFactory
		
class ModbusManager(BaseManager):

	def __init__(self, mod):
		super().__init__(mod)