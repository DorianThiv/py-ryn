
import json
from bases import BaseBinder

class ExempleBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self):
        self.observable.parent.observable.status = True
        pass

    def execute(self, frame):
        print("[MDLEXEMPLE] : {}".format(frame))

    def read(self):
        data = "Hello World"
        self.observable.observers_update(data)

    def write(self):
        pass
    
