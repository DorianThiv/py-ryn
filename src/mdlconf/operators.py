
from bases import BaseOperator

class ConfigurationOperator(BaseOperator):
    
    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def load(self):
        pass

    def serialize(self):
        pass

    def deserialize(self):
        pass