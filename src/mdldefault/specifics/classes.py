import sys
import threading

from mdldefault.specifics.models import DataRawModel

class DefaultWriter:

    def __init__(self, callback):
        self.bcallback = callback

    def write(self, data):
        print(data.payload)
    
    def scallback(self, text):
        data = DataRawModel(payload=text)
        self.bcallback(data)
