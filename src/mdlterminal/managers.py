 
from bases import BaseManager
from factories import ModuleFactory
		
class TerminalManager(BaseManager):

	def __init__(self, name):
		package = "mdlterminal"
		minprefix = "terminal"
		super().__init__(name, package, minprefix)