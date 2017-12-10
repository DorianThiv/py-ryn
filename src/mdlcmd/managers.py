 
from bases import BaseManager

class CmdManager(BaseManager):
    
    def __init__(self, ref, name):
        super().__init__(ref, name)

    def __str__(self):
        return "CmdManager(ref : {}, name : {})".format(self.ref, self.name)