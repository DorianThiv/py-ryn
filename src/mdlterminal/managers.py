
import re

from network import *
from bases import BaseManager, BaseCommand
from factories import ModuleFactory
		
class TerminalManager(BaseManager):

	def __init__(self, mod):
		module = mod
		minprefix = "terminal"
		name = minprefix + "-manager" 
		super().__init__(name, minprefix, module)
		self.usage = "mdlterminal [(-r or --read) or (-w | --write)] [(-a or --address) 0.0.0.0)] [(-t or --text) \"your text\"]"

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
				commanddict[BaseCommand.PARSE_MODULE] = elem
			if re.match(r"(-|-{2})+(r|read)", elem) != None:
				commanddict[BaseCommand.PARSE_DIRECTION] = BaseCommand.READ
			if re.match(r"(-|-{2})+(w|write)", elem) != None:
				commanddict[BaseCommand.PARSE_DIRECTION] = BaseCommand.WRITE
			if re.match(r"(-|-{2})+(a|address|addr)", elem) != None:
				if command.index(elem)+1 < len(command):
					try:
						checkIp(command[command.index(elem)+1])
						commanddict[BaseCommand.PARSE_ADDRESS] = command[command.index(elem)+1]
					except Exception as e:
						return (False, "excepted IP address : (-a x.x.x.x | --address x.x.x.x) : {}".format(e))
				else:
					return (False, "excepted IP address : (-a x.x.x.x | --address x.x.x.x)")
			if re.match(r"(-|-{2})+(t|text)", elem) != None:
				if command.index(elem)+1 < len(command):
					commanddict[BaseCommand.PARSE_TEXT] = command[command.index(elem)+1]
				else:
					return (False, "excepted text : (-t \"hello world\") | (--text \"hello world\")")
		if len(commanddict) == 1:
			return (False, "no arguments detected")
		if BaseCommand.PARSE_DIRECTION not in commanddict:
			return (False, "no command detected : (-r | -w) | (--read | --write)")
		if BaseCommand.PARSE_ADDRESS not in commanddict:
			return (False, "no destination address detected : (-a | --address x.x.x.x)")
		if BaseCommand.PARSE_TEXT not in commanddict:
			return (False, "no message detected : (-t \"hello world\") | (--text \"hello world\")")
		return (True, commanddict)
