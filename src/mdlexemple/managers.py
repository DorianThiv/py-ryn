
import re
from bases import BaseManager, BaseCommand
from mdlutils.factories import ModuleFactory
		
class ExempleManager(BaseManager):
	"""
		Manager component define his content. These provders and prefix 
		for them.
	"""
	
	def __init__(self, mod):
		super().__init__(mod)
		self.usage = "mdlexemple [(-r or --read) or (-w | --write)] [(-t or --text) \"your text\"]"
	
	def command(self, command):
		""" 
			mdlexemple -w -t "Hello test"
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
