
import sys
import socket
from bases import BaseBinder
from network import *
from mdlterminal.templates import TerminalThreadServer, TerminalThreadWrite

class TerminalBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        self.server = None
        self.host = getIpAdress()
        self.port = 38000

    def load(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            print("[SUCCESS - BINDER - TERMINAL] : Connection (host: {}, port: {})".format(self.host, self.port))
        except Exception as e:
            print("ErrorTerminal : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 
            self.socket.close()

    def action(self, data):
        """ Interactiv with an Action derived class from BaseAction """
        if data[1] == "all":
            self.read()
        else:
            self.write(data[1])

    def read(self):
        self.server = TerminalThreadServer(self.socket, self._get_event)
        self.server.start()
        self.server.join()
        
    def write(self, data): 
        termThW = TerminalThreadWrite(data)
        termThW.start()
        termThW.join()
    
