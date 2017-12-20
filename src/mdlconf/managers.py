 
from bases import BaseManager

class ModuleFactory:

	@staticmethod
	def make(prefix, modules):
		klasses = {
			"providers": [],
			"registries": [],
			"operators": [],
			"binders": []
		}
		for k,v in modules.items():
			mod = __import__(k)
			for c in v:
				m = k.split(".")
				if m[1] == "providers":
					klasses["providers"].append({"name": prefix + "-provider", "class": getattr(mod, c)})
				if m[1] == "registries":
					klasses["registries"].append({"name": prefix + "-registry", "class": getattr(mod, c)})
				if m[1] == "operators":
					klasses["operators"].append({"name": prefix + "-operator", "class": getattr(mod, c)})
				if m[1] == "binders":
					klasses["binders"].append({"name": prefix + "-binder", "class": getattr(mod, c)})
		return klasses
		
class ConfigurationManager(BaseManager):

	def __init__(self, name):
		minprefix = "conf"
		prefixs = ["Configuration"]
		super().__init__(name, prefixs, minprefix)
		
	def load(self):
		self.classes = ModuleFactory.make(self.minprefix, self.modules)
		for c in self.classes["registries"]:
			self.registries.append({"name": c["name"], "instance": c["class"](c["name"])})
		for c in self.classes["providers"]:
			p = c["class"](c["name"], self)
			self.providers.append({"name": c["name"], "instance": p})
			self.registries[0]["instance"].register(p)
		for c in self.classes["binders"]:
			self.binders.append({"name": c["name"], "instance": c["class"](c["name"], self.registries[0]["instance"])})
		self._reading_all()