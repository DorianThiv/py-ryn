
from bases import BaseManager
from mdldefault.specifics.commands import DefaultBaseCommand

class DefaultManager(BaseManager):

	def __init__(self, mod):
		super().__init__(mod, DefaultBaseCommand())
			
