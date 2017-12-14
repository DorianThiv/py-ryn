
from bases import BaseBinder

class ConfigurationBinder(BaseBinder):
    
    def __init__(self, ref, name, observable):
        super().__init__(ref, name, observable)

    def __str__(self):
        return "__CONFIGBINDER__ = (ref : {}, name : {})\n".format(self.ref, self.name)

    def load(self, observable):
        pass

    def read(self, path):
        import sys
        with open(path, 'r') as f:
            contents = f.read()
        print(contents)

    def write(self):
        pass
    
