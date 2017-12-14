

from bases import BaseRegistry

class ConfigurationRegistry(BaseRegistry):

    def __init__(self, ref, name):
        super().__init__(ref, name)

    def __str__(self):
        return "__CONFIGREGISTRY__ = (ref : {}, name : {})\n".format(self.ref, self.name)

    def load(self):
        pass

    def operate(self):
        pass

    def register(self, observer):
        pass
    
    def unregister(self, observer):
        pass

    def unregister_all(self):
        pass

    def observers_update(self):
        pass
