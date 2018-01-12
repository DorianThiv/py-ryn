 
from bases import BaseManager
from factories import ModuleFactory
		
class ExempleManager(BaseManager):
	"""
		Manager component define his content. These provders and prefix 
		for them.
	"""
	
	def __init__(self, mod):
		module = mod
		minprefix = "exemple"
		name = minprefix + "-manager"
		super().__init__(name, minprefix, module)