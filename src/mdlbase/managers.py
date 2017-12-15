 
from bases import BaseManager

from mdlbase.registries import MdlBaseRegistry
from mdlbase.providers import MdlBaseProvider
from mdlbase.binders import MdlBaseBinder

class MdlBaseManager(BaseManager):

	def __init__(self, ref, name):
		super().__init__(ref, name)

	def __str__(self):
		ret = "__MDLBASEMANAGER__ = (ref : {}, name : {})\n".format(self.ref, self.name)
		for provider in self.providers:
			ret += "\t{}".format(self.providers[provider])
			for register in self.registries:
				ret += "\t\t{}".format(self.registries[register])
				for binder in self.binders:
					ret += "\t\t\t{}".format(self.binders[binder])
		return ret

	def load(self):
		self.registries["base-registry"] = MdlBaseRegistry("152-125", "base-registry")
		p = MdlBaseProvider("000-498", "base-provider", self)
		self.providers[p.name] = p
		self.registries["base-registry"].register(p)
		self.binders["base-binder"] = MdlBaseBinder("123-154", "base-binder", self.registries["base-registry"])
		self.binders["base-binder"].read()

	def register(self, loader):
		self.observers.append(loader)
    
	def unregister(self, observer):
		pass

	def unregister_all(self):
		pass

	def observers_update(self, frame):
		for observer in self.observers:
			observer.update(frame) 
		
