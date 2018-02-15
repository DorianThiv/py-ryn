
import sys
import socket

from bases import BaseBinder, BaseCommand
from mdlutils.network import ipv4
from mdlterminal.specifics.models import DataRawModel
from mdlterminal.specifics.classes import TerminalThreadServer

class TerminalBinder(BaseBinder):

    """ Initialize an internal terminal to communicate with the user """
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        self.server = None
        self.socket = None
        self.host = ipv4()
        self.port = 1297

    def load(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.observable.parent.observable.status = True
            print("[SUCCESS - BINDER - TERMINAL] : Connection (host: {}, port: {})".format(self.host, self.port))
        except Exception as e:
            self.logger.log(0, "[TERMINAL - LOAD] {}".format(e)) 
            self.socket.close()

    def execute(self, data):
        """ Interactiv with an Action derived class from BaseAction """   
        if data.command == BaseCommand.LOAD:
            self.read()
        if data.command == BaseCommand.WRITE:
            self.write(data)

    def read(self):
        try:
            self.server = TerminalThreadServer(self.socket, self._get_event)
            self.server.start()
            self.server.join()
        except KeyboardInterrupt:
            print("[WARNING - TERMINAL BINDER - READ]: KeyboardInterrupt")
            self.logger.log(1, "[WARNING - TERMINAL BINDER - READ]: KeyboardInterrupt")
            self.server.stop()
        except Exception as e:
            print("[WARNING - TERMINAL BINDER - READ]: {}".format(e))
            self.logger.log(1, "[WARNING - TERMINAL BINDER - READ]: {}".format(e))
            self.server.stop()
        
    def write(self, data):
        try:
            self.server.write(data)
        except Exception as e:
            print("[ERROR - TERMINAL_BINDER - WRITE] : {}".format(e))
            self.server.stop()
    
    def _get_event(self, addr, msg):
        data = DataRawModel(address=addr, payload=msg, binder=self)
        self.observable.emit(data)    
    
