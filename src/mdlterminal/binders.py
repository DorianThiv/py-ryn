
import sys
import socket

from bases import BaseBinder, BaseCommand
from mdlutils.network import getIpAddress
from mdlterminal.specifics.templates import *

class TerminalBinder(BaseBinder):

    """ Initialize an internal terminal to communicate with the user """
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        self.server = None
        self.socket = None
        self.host = getIpAddress()
        self.port = 1297

    def load(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.observable.parent.observable.status = True
            print("[SUCCESS - BINDER - TERMINAL] : Connection (host: {}, port: {})".format(self.host, self.port))
        except Exception as e:
            print("ErrorTerminal : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 
            self.socket.close()

    def execute(self, data):
        """ Interactiv with an Action derived class from BaseAction """
        # Change command.ALL execution to LOAD or INIT
        if data.command == BaseCommand.ALL:
            self.read()        
        if data.command == BaseCommand.LOAD:
            self.read()
        if data.command == BaseCommand.WRITE:
            self.write(data)

    def read(self):
        try:
            self.server = TerminalThreadServer(self.socket, self._get_event)
            self.server.start()
            self.server.join()
        except Exception as e:
            print("[ERROR - TERMINAL_BINDER - READ] : {}".format(e))
        
    def write(self, data):
        try:
            self.server.write(data)
        except Exception as e:
            print("[ERROR - TERMINAL_BINDER - WRITE] : {}".format(e))
    
    def _get_event(self, addr, msg):
        data = TerminalRawModel(address=addr, payload=msg, binder=self)
        self.observable.observers_update(data)    
    
