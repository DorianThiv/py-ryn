
from factories import PackageFactory
from dealer import Dealer
from error import ErrorLoadModule
from bases import BaseLoader 

class Loader(BaseLoader):
	
	def __init__(self, name):
		super().__init__(name, Dealer())

	def load(self, managers):
		""" 
			Load all managers in a list. 
			Create managers with the ManagerFactory and give them 
			at the dealer to share data. 
		"""
		self.dealer.add(self)
		for manager in managers:
			self.__reload_once(manager)

	def reload(self, payload):
		for mdl in payload["config"]["modules"]:
			self.__reload_once(mdl["name"])

	def __reload_once(self, manager):
		m = PackageFactory.make(manager)
		m.register(self.dealer)
		self.dealer.add(m)
		m.load()

	
