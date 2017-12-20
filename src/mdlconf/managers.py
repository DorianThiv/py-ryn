 
from bases import BaseManager

class ConfigurationManager(BaseManager):

	def __init__(self, name):
		package = "mdlconf"
		minprefix = "conf"
		super().__init__(name, package, minprefix)
