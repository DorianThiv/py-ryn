
from exceptions import ErrorLoadModule

class PackageFactory:

    @staticmethod
    def make(name):
        if name == "mdlconf":
            try:
                from mdlconf.managers import ConfigurationManager
                m = ConfigurationManager(name)
                return m
            except Exception as e:
                raise ErrorLoadModule("{} : {}".format(name, e))
        if name == "mdlexemple":
            try:
                from mdlexemple.managers import ExempleManager
                m = ExempleManager(name)
                return m
            except Exception as e:
                raise ErrorLoadModule("{} : {}".format(name, e))
        if name == "mdlmodbus":
            try:
                from mdlmodbus.managers import ModbusManager
                m = ModbusManager(name)
                return m
            except Exception as e:
                raise ErrorLoadModule("{} : {}".format(name, e))

class ModuleFactory:

    """ 
        Module Factory : can load module dynamically
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