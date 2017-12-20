 
from bases import BaseManager
from factories import ModuleFactory
		
class ModbusManager(BaseManager):

	def __init__(self, name):
		minprefix = "modbus"
		prefixs = ["Modbus"]
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