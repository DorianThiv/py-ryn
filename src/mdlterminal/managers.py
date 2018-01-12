 
from bases import BaseManager
from factories import ModuleFactory
		
class TerminalManager(BaseManager):

	def __init__(self, mod):
		module = mod
		minprefix = "terminal"
		name = minprefix + "-manager" 
		super().__init__(name, minprefix, module)