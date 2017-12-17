
from bases import BaseProvider

class ConfigurationProvider(BaseProvider):

    def __init__(self, name, observable=None):
        super().__init__(name, observable)
    
    def __str__(self):
        return "__CONFIGPROVIDER__ = (name : {})\n".format(self.name)

    def load(self):
        pass
        

    def provide(self):
        """  """
        pass

    def update(self, frame):
        """ Update to notify the manager with a frame instance """
        self.observable.observers_update(frame)