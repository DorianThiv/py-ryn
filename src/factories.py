
from error import ErrorLoadModule

class PackageFactory:
	
	@staticmethod
	def make(name):
		if name == "mdlconf":
			try:
				from mdlconf.managers import ConfigurationManager
				m = ConfigurationManager(name)
				return m
			except Exception as e:
				raise ErrorLoadModule(e)
		if name == "mdlbase":
			try:
				from mdlbase.managers import MdlBaseManager
				m = MdlBaseManager(name)
				return m
			except Exception as e:
				raise ErrorLoadModule(e)

class ModuleFactory:

    """ 
        Module Factory : can load module dynamically
        with a prifix loader.
    """
    @staticmethod
    def make(prefix, modules):
        klasses = {"providers": [], "registries": [], "operators": [], "binders": []}
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