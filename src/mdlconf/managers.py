 
from bases import BaseManager
from mdlconf.providers import ConfigurationProvider

class ConfigurationManager(BaseManager):

	def __init__(self, ref, name):
		super().__init__(ref, name)
		self.providers = {}
		p = ConfigurationProvider("000-498", "confprov")
		self.providers[p.name] = p

	def __str__(self):
		ret = "__CONFIGMANAGER__ = (ref : {}, name : {})".format(self.ref, self.name)
		for provider in self.providers:
			ret += "\n\t{}\n".format(self.providers[provider])
		return ret

	def load(self):
		pass
