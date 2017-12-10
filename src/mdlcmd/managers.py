 
from bases import BaseManager

class CmdManager(BaseManager):
    
    def __init__(self, ref, name):
        super().__init__(ref, name)

    def __str__(self):
        return "__CMDMANAGER__ = (ref : {}, name : {})".format(self.ref, self.name)

    def load(self):
        pass