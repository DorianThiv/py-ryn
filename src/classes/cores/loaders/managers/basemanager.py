# Base Manager 

import interfaces
from interfaces.imanager import IManager
from interfaces.isatobject import ISATObject

class BaseManager(ISATObject, IManager):

    def __init__(self):
        pass

    def __str__(self):
        pass

    def debug(self):
        print(self)
