
from bases import BaseBinder

class ConfigurationBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def __str__(self):
        return "__CONFIGBINDER__ = (name : {}, observable : {})\n".format(self.name, self.observable.name)

    def load(self, observable):
        pass

    def read(self, filename="config.json"):
        import sys
        import os
        with open(os.path.dirname(__file__) + "/" + filename, 'r') as f:
            contents = f.read()
        self.observable.observers_update(data=contents)

    def write(self):
        pass
    
