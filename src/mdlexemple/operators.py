
from interfaces import IOperator
from transfert import ModuleFrameTransfert

class ExempleOperator(IOperator):
    
    def __init__(self, name):
        self.name = name

    def load(self):
        pass

    def encapsulate(self, data):
        # return ModuleFrameTransfert()
        pass

    def decapsulate(self, frame):
        return frame