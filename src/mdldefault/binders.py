
import sys
import socket

from bases import BaseBinder
from samples.network import ipv4
from mdldefault.specifics.models import DataRawModel
from mdldefault.specifics.classes import DefaultWriter

class DefaultBinder(BaseBinder):

    """ Initialize an internal default to communicate with the user """
    
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.writer = DefaultWriter()

    def initialize(self):
        try:
            self.parent.parent.status = True
        except Exception as e:
            self.logger.log(0, "[DEFAULT - LOAD] {}".format(e)) 
            self.socket.close()

    def run(self):
        pass

    def read(self, data):
        self.parent.emit(data) 
        
    def write(self, data):
        try:
            self.writer.write(data)
        except Exception as e:
            print("[ERROR - DEFAULT_BINDER - WRITE] : {}".format(e))
            self.logger.log(1, e)
           
    
