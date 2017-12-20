
from dealer import Dealer

from error import ErrorLoadModule

from bases import BaseLoader 

class ManagerFactory:
	
	@staticmethod
	def make(name):
		# if name == "mdlcmd":
		# 	try:
		# 		from mdlcmd.managers import CmdManager
		# 		m = CmdManager(name)
		# 		return m
		# 	except Exception as e:
		# 		raise ErrorLoadModule(e)
		if name == "mdlconf":
			try:
				from mdlconf.managers import ConfigurationManager
				m = ConfigurationManager(name)
				return m
			except Exception as e:
				raise ErrorLoadModule(e)
		# if name == "mdlbase":
		# 	try:
		# 		from mdlbase.managers import MdlBaseManager
		# 		m = MdlBaseManager(name)
		# 		return m
		# 	except Exception as e:
		# 		raise ErrorLoadModule(e)


class Loader(BaseLoader):
	
	def __init__(self, name, dealer=None):
		super().__init__(name, dealer)

	def __str__(self):
		return "{}".format(self.dealer)

	def load(self, managers):
		""" 
			Load all managers in a list. 
			Create managers with the ManagerFactory and give them 
			at the dealer to share data. 
		"""
		self.dealer = Dealer()
		self.dealer.add(self)
		for manager in managers:
			self.__reload_once(manager)

	def reload(self, payload):
		for mdl in payload["config"]["modules"]:
			self.__reload_once(mdl["name"])

	def __reload_once(self, manager):
		m = ManagerFactory.make(manager)
		m.register(self.dealer)
		self.dealer.add(m)
		m.load()

	
