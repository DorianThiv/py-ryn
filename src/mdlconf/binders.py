
import json
from bases import BaseBinder

class ConfigurationBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        self.load()

    def load(self):
        self.read()

    def read(self, filename="config.json"):
        import sys
        import os
        with open(os.path.dirname(__file__) + "/" + filename, 'r') as f:
            data = json.load(f)
        self.observable.observers_update(data)

    def write(self):
        pass
    
