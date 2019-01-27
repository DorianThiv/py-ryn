import sys

from bases import BaseCommand
from mdldefault.specifics.exceptions import *
from mdldefault.specifics.models import DataRawModel

class DefaultWriter:

    def __init__(self):
        pass

    def read(self):
        pass

    def write(self, data):
        print(data)
    
    def stop(self):
        pass
