
from bases import BaseBinder

class ConfigurationBinder(BaseBinder):
    
    def __init__(self, ref, name, observable=None):
        super().__init__(ref, name, observable)

    def __str__(self):
        return "__CONFIGBINDER__ = (ref : {}, name : {}, observable : {})\n".format(self.ref, self.name, self.observable.name)

    def load(self, observable):
        pass

    def read(self, filename="managers.py"):
        import sys
        import os
        with open(os.path.dirname(__file__) + "/" + filename, 'r') as f:
            contents = f.read()
        self.observable.observers_update(emitter=self.name, data=contents)

    def write(self):
        pass
    
