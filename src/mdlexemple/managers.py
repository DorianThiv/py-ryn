 
from bases import BaseManager
from factories import ModuleFactory
		
class ExempleManager(BaseManager):

	def __init__(self, name):
		package = "mdlexemple"
		minprefix = "exemple"
		super().__init__(name, package, minprefix)