
import re

from bases import BaseManager

from samples.factories import ModuleFactory

from mdlterminal.specifics.commands import TerminalBaseCommand

class TerminalManager(BaseManager):

	def __init__(self, mod):
		super().__init__(mod)

	def command(self, command):
		""" Use inheritance to parse command and use the specific module
		commands.py where are few commands. """
		status, response = super().command(command)
		if status is False:
			return (status, response)
		else:
			return TerminalBaseCommand.parse(response)
			
