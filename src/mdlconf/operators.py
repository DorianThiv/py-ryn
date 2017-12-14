
from bases import BaseOperator

class ConfigurationOperator(BaseOperator):
    
    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def __str__(self):
        return "__CONFIGOPERATOR__ = (ref : {}, name : {})".format(self.ref, self.name)

    def load(self):
        pass

    def serialize(self):
        pass

    def deserialize(self):
        pass