
from bases import BaseProvider

class ConfigurationProvider(BaseProvider):

    def __init__(self, ref, name):
        super().__init__(ref, name)
    
    def __str__(self):
        return "__CONFIGPROVIDER__ = (ref : {}, name : {})".format(self.ref, self.name)

    def load(self):
        pass

    def provide(self):
        pass

    def update(self):
        pass