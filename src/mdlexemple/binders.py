
import json
from bases import BaseBinder

class ExempleBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        self.load()

    def load(self):
        self.read()

    def read(self):
        import sys
        import os
        data = "Hello World"
        self.observable.observers_update(data)

    def write(self):
        pass
    
