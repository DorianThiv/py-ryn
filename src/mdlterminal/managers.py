
import re

from bases import BaseManager, BaseCommand
from mdlutils.factories import ModuleFactory

class TerminalManager(BaseManager):

	def __init__(self, mod):
		super().__init__(mod)
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
		status, response = super().command(command)
		if status is False:
			return (status, response)
		else:
			commanddict = response
			if len(commanddict) == 1:
				return (False, "no arguments detected")
			if BaseCommand.PARSE_COMMAND not in commanddict:
				return (False, "no command detected : (-r | -w) | (--read | --write)")
			if BaseCommand.PARSE_ADDRESS not in commanddict:
				return (False, "no destination address detected : (-a | --address x.x.x.x)")
			if BaseCommand.PARSE_TEXT not in commanddict:
				return (False, "no message detected : (-t \"hello world\") | (--text \"hello world\")")
		return (True, commanddict)
