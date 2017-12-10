# Base Manager 

from SATObjects import ISATObject
from IManager import IManager

class BaseManager(ISATObject, IManager):

    def __init__(self):
        pass

    def __str__(self):
        pass

    def debug(self):
        print(self)
