
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
		commanddict = {}
		for elem in command:
			if re.match(r"mdl([a-z])+", elem) != None:
				commanddict[BaseCommand.PARSE_MODULE] = elem
			if re.match(r"(-|-{2})+(t|text)", elem) != None:
				if command.index(elem)+1 < len(command):
					commanddict[BaseCommand.PARSE_TEXT] = command[command.index(elem)+1]
				else:
					return (False, "excepted text : (-t \"hello world\") | (--text \"hello world\")")
		if len(commanddict) == 1:
			return (False, "no arguments detected")
		if BaseCommand.PARSE_TEXT not in commanddict:
			return (False, "no message detected : (-t \"hello world\") | (--text \"hello world\")")
		return (True, commanddict)
