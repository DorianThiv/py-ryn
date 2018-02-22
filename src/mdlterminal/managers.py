
import re

from bases import BaseManager

from mdlutils.factories import ModuleFactory

from mdlterminal.specifics.commands import TerminalSimpleCommand

class TerminalManager(BaseManager):

	def __init__(self, mod):
		super().__init__(mod)
		self.usage = "mdlterminal [(-r or --read) or (-w | --write)] [(-a or --address) 0.0.0.0)] [(-t or --text) \"your text\"]"

	def command(self, command):
		status, response = super().command(command)
		if status is False:
			return (status, response)
		else:
			return TerminalSimpleCommand.parse(response)
			
