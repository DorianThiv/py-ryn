
import re
from bases import BaseManager, BaseCommand
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
	
	def command(self, command):
		""" 
			mdlexemple -t "Hello test"
		"""
		status, response = super().command(command)
		if status is False:
			return (status, response)
		else:
			commanddict = response
			if len(commanddict) == 1:
				return (False, "no arguments detected")
			if BaseCommand.PARSE_TEXT not in commanddict:
				return (False, "no message detected : (-t \"hello world\") | (--text \"hello world\")")
		return (True, commanddict)
