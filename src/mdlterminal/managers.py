
from bases import BaseManager
from mdlterminal.specifics.commands import TerminalBaseCommand

class TerminalManager(BaseManager):

	def __init__(self, mod):
		super().__init__(mod, TerminalBaseCommand())
			
