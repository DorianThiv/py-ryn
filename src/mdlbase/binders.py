
import json
from bases import BaseBinder

class MdlBaseBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def __str__(self):
        return "__CONFIGBINDER__ = (name : {}, observable : {})\n".format(self.name, self.observable.name)

    def load(self, observable):
        pass

    def read(self):
        import sys
        import os
        data = "Hello World"
        self.observable.observers_update(data)

    def write(self):
        pass
    
