 
from bases import BaseManager
from factories import ModuleFactory
		
class MdlBaseManager(BaseManager):

	def __init__(self, name):
		minprefix = "base"
		prefixs = ["MdlBase"]
		super().__init__(name, prefixs, minprefix)

	def __str__(self):
		""" Display Debug """
		ret = "__MDLBASEMANAGER__ = (name : {})\n".format(self.name)
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
			p = c["class"](c["name"], self)
			self.providers.append({"name": c["name"], "instance": p})
			self.registries[0]["instance"].register(p)
		for c in self.classes["binders"]:
			self.binders.append({"name": c["name"], "instance": c["class"](c["name"], self.registries[0]["instance"])})
		self._reading_all()