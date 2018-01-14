
import sys

from exceptions import LoadModuleError

class PackageFactory:

    MODULES_DIRECTORY = "modules."

    @staticmethod
    def make(name):
        try:
            mod = __import__(name)
            c = mod.manager
            m = c(name)
            return m 
        except Exception as e:
            raise LoadModuleError("Ligne : {}, {} : {}".format(sys.exc_info()[-1].tb_lineno, name, e))

class ModuleFactory:
    """ Module Factory : can load module dynamically
        with a prifix loader.
    """
    @staticmethod
    def make(prefix, package):
        klasses = {"providers": [], "registries": [], "binders": []}
        mod = __import__(package)
        for clss in mod.classes:
            _cls = clss.__module__.split(".")
            if _cls[1] == "providers":
                klasses["providers"].append({"name": prefix + "-provider", "class": getattr(mod, clss.__name__)})
            if _cls[1] == "registries":
                klasses["registries"].append({"name": prefix + "-registry", "class": getattr(mod, clss.__name__)})
            if _cls[1] == "binders":
                klasses["binders"].append({"name": prefix + "-binder", "class": getattr(mod, clss.__name__)})
        return klasses