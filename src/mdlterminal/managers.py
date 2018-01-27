
import re

from bases import BaseManager, BaseCommand
from factories import ModuleFactory
		
class TerminalManager(BaseManager):

	def __init__(self, mod):
		module = mod
		minprefix = "terminal"
		name = minprefix + "-manager" 
		super().__init__(name, minprefix, module)
		self.usage = "mdlterminal [(-r or --read) or (-w | --write)] [(-a or --address) 0.0.0.0)] [(-t or --text) 'your text']"

	def command(self, command):
		""" 
			mdlterminal -w -a 192.168.1.1 -t "Hello test"
			Args:
				* command: string
			Returns:
				* tuple(True, dict)
				* tuple(False, error: string)
		"""
		commanddict = {}
		for elem in command:
			if re.match(r"mdl([a-z])+", elem) != None:
				commanddict[BaseManager.PARSE_MODULE] = elem
			if re.match(r"(-|-{2})+(r|read)", elem) != None:
				commanddict[BaseManager.PARSE_DIRECTION] = BaseCommand.READ
			if re.match(r"(-|-{2})+(w|write)", elem) != None:
				commanddict[BaseManager.PARSE_DIRECTION] = BaseCommand.WRITE
			if re.match(r"(-|-{2})+(a|address|addr)", elem) != None:
				commanddict[BaseManager.PARSE_ADDRESS] = command[command.index(elem)+1]
			if re.match(r"(-|-{2})+(t|text)", elem) != None:
				commanddict[BaseManager.PARSE_TEXT] = command[command.index(elem)+1]
		if len(commanddict) == 1:
			return (False, "no arguments detected")
		return (True, commanddict)
