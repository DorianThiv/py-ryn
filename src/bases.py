
from interfaces import *

class BaseManager(ISATObject, IManager):
    
    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def load(self):
        pass

    def debug(self):
        pass