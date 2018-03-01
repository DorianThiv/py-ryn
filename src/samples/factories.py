
import sys

from samples.exceptions import LoadModuleError

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

    PROVIDERS = "providers"
    OPERATORS = "operators"
    BINDERS = "binders"

    KCLASSES = "name"
    VCLASSES = "class"

    @staticmethod
    def make(prefix, package):
        klasses = {ModuleFactory.PROVIDERS: [], ModuleFactory.OPERATORS: [], ModuleFactory.BINDERS: []}
        mod = __import__(package)
        for clss in mod.classes:
            _cls = clss.__module__.split(".")
            if _cls[1] == ModuleFactory.PROVIDERS:
                klasses[ModuleFactory.PROVIDERS].append({ModuleFactory.KCLASSES: prefix + "-provider", ModuleFactory.VCLASSES: getattr(mod, clss.__name__)})
            if _cls[1] == ModuleFactory.OPERATORS:
                klasses[ModuleFactory.OPERATORS].append({ModuleFactory.KCLASSES: prefix + "-operator", ModuleFactory.VCLASSES: getattr(mod, clss.__name__)})
            if _cls[1] == ModuleFactory.BINDERS:
                klasses[ModuleFactory.BINDERS].append({ModuleFactory.KCLASSES: prefix + "-binder", ModuleFactory.VCLASSES: getattr(mod, clss.__name__)})
        return klasses