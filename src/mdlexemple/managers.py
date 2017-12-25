 
from bases import BaseManager
from factories import ModuleFactory
		
class ExempleManager(BaseManager):
	"""
		Manager component define his content. These provders and prefix 
		for them.
	"""
	
	def __init__(self, name):
		package = "mdlexemple"
		minprefix = "exemple"
		super().__init__(name, package, minprefix)