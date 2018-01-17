
import sys
import socket
from bases import BaseBinder
from network import getIpAddress
from mdlterminal.specifics.templates import TerminalThreadServer, TerminalThreadWrite

class TerminalBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        self.server = None
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
        if data.command == "all":
            self.read()
        else:
            #self.write(data[1])
            pass

    def read(self):
        self.server = TerminalThreadServer(self.socket, self._get_event)
        self.server.start()
        self.server.join()
        
    def write(self, data): 
        termThW = TerminalThreadWrite(data)
        termThW.start()
        termThW.join()
    
