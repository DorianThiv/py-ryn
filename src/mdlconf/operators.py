
from bases import BaseOperator

class ConfigurationOperator(BaseOperator):
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "__CONFIGOPERATOR__ = (name : {})".format(self.name)

    def load(self):
        pass

    def serialize(self):
        pass

    def deserialize(self):
        pass