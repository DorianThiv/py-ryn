
import json
from mdlutils.bases import BaseBinder

class ExempleBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self):
        self.observable.parent.observable.status = True

    def execute(self, data):
        print("[MDLEXEMPLE] : {}".format(data))

    def read(self):
        pass

    def write(self):
        pass
    
