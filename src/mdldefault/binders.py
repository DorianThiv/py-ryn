
import sys
import socket

from bases import BaseBinder
from samples.network import ipv4
from mdldefault.specifics.models import DataRawModel
from mdldefault.specifics.classes import DefaultWriter

class DefaultBinder(BaseBinder):

    """ Initialize an internal default to communicate with the user """
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        self.writer = DefaultWriter(self.read)

    def initialize(self):
        self.observable.parent.observable.status = True

    def run(self):
        pass

    def read(self, data):
        self.logger.log(2, "Read from mdldefault: {}".format(data))
        data.binder = self
        self.observable.emit(data) 
        
    def write(self, data):
        self.writer.write(data)
           
    
