
import re

from bases import BaseManager
from factories import ModuleFactory
		
class TerminalManager(BaseManager):

	def __init__(self, mod):
		module = mod
		minprefix = "terminal"
		name = minprefix + "-manager" 
		super().__init__(name, minprefix, module)
	
	def command(self, command):
		""" Terminal Module command :
			* mdlterminal [(-r or --read) or (-w | --write)] [(-a or --address) 0.0.0.0)] [(-t or --text) 'your text']
		"""
		splitted = command.split(" ")
		for i in range(splitted):
			if re.match(r"mdl([a-z])+", splitted[i]) == None and splitted[i] == self.module:
				error = "module name doesn't match"
				return (False, error)
			if re.match(r"(-|-{2})+", splitted[i]) == None:
				error = "no arguments in this command"
				return (False, error)
			
		return (True, None)