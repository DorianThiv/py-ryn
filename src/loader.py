
from factories import PackageFactory
from dealer import Dealer
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
			self.__load_once(manager)

	def reload(self, frame):
		for mdl in frame.payload["config"]["modules"]:
			self.__load_once(mdl["name"])

	def __load_once(self, manager):
		m = PackageFactory.make(manager)
		m.register(self.dealer)
		self.dealer.add(m)
		m.load()

	
