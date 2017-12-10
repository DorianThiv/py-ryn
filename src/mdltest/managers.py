 
from bases import BaseManager

class TestManager(BaseManager):
    
    def __init__(self, ref, name):
        super().__init__(ref, name)

    def __str__(self):
        return "TestManager(ref : {}, name : {})".format(self.ref, self.name)