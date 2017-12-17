 
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

	def __str__(self):
		ret = "__CONFIGMANAGER__ = (name : {})\n".format(self.name)
		i = 0
		j = 0
		k = 0
		for i in range(len(self.providers)):
			ret += "\t{}".format(self.providers[i]["instance"])
			for j in range(len(self.registries)):
				ret += "\t\t{}".format(self.registries[j]["instance"])
				for k in range(len(self.binders)):
					ret += "\t\t\t{}".format(self.binders[k]["instance"])
		return ret

	def load(self):
		self.classes = ModuleFactory.make(self.minprefix, self.modules)
		for c in self.classes["registries"]:
			self.registries.append({"name": c["name"], "instance": c["class"](c["name"])})
		for c in self.classes["providers"]:
			self.providers.append({"name": c["name"], "instance": c["class"](c["name"], self)})
		for c in self.classes["binders"]:
			self.binders.append({"name": c["name"], "instance": c["class"](c["name"], self.registries[0]["instance"])})
		self._reading_all()