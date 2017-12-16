 
from bases import BaseManager

from mdlconf.registries import ConfigurationRegistry
from mdlconf.providers import ConfigurationProvider
from mdlconf.binders import ConfigurationBinder

class ConfigurationManager(BaseManager):

	def __init__(self, ref, name):
		super().__init__(ref, name)

	def __str__(self):
		ret = "__CONFIGMANAGER__ = (ref : {}, name : {})\n".format(self.ref, self.name)
		for provider in self.providers:
			ret += "\t{}".format(self.providers[provider])
			for register in self.registries:
				ret += "\t\t{}".format(self.registries[register])
				for binder in self.binders:
					ret += "\t\t\t{}".format(self.binders[binder])
		return ret

	def load(self):
		self.registries["conf-registry"] = ConfigurationRegistry("152-125", "conf-registry")
		p = ConfigurationProvider("000-498", "conf-provider1", self)
		self.providers[p.name] = p
		self.registries["conf-registry"].register(p)
		self.binders["conf-binder"] = ConfigurationBinder("123-154", "conf-binder", self.registries["conf-registry"])
		self.binders["conf-binder"].read()

	# def register(self, loader):
		# self.observers.append(loader)
    
	# def unregister(self, observer):
		# pass

	# def unregister_all(self):
		# pass

	# def observers_update(self, frame):
		# for observer in self.observers:
			# observer.update(frame) 
		
