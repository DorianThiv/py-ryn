
import sys
import socket
from bases import BaseBinder
from network import *
from mdlterminal.templates import TerminalThreadRead

class TerminalBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        self.host = getIpAdress()
        self.port = 38000

    def load(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            print("Connection at : {} on port {}".format(self.host, self.port))
        except Exception as e:
            print("ErrorTerminal : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 
            self.socket.close()

    def read(self):
        termThR = TerminalThreadRead(self.socket, self._get_event)
        termThR.start()
        
    def write(self):
        pass
    
