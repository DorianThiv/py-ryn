
from dealer import Dealer

from error import ErrorLoadModule

from bases import BaseLoader 

class ManagerFactory:
	
	@staticmethod
	def make(name):
		if name == "mdlcmd":
			try:
				from mdlcmd.managers import CmdManager
				m = CmdManager("111-111", name)
				return m
			except Exception as e:
				raise ErrorLoadModule(e)
		if name == "mdlconf":
			try:
				from mdlconf.managers import ConfigurationManager
				m = ConfigurationManager("111-001", name)
				return m
			except Exception as e:
				raise ErrorLoadModule(e)
		if name == "mdlbase":
			try:
				from mdlbase.managers import MdlBaseManager
				m = MdlBaseManager("111-001", name)
				return m
			except Exception as e:
				raise ErrorLoadModule(e)


class Loader(BaseLoader):
	
	def __init__(self, ref, name, dealer=None):
		super().__init__(ref, name, dealer)

	def __str__(self):
		return "{}".format(self.dealer)

	def load(self, managers):
		""" 
			Load all managers in a list. 
			Create managers with the ManagerFactory and give them 
			at the dealer to share data. 
		"""
		self.dealer = Dealer()
		self.managers = {}
		for manager in managers:
			m = ManagerFactory.make(manager)
			m.register(self.dealer)
			self.dealer.add(m)
			m.load()

	def reload(self):
		pass
