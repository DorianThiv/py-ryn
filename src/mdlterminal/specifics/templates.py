

import sys
import threading

from bases import BaseDirectory
from network import getIpAddress
from mdlterminal.specifics.exceptions import TerminalWrongCommandModuleError, ErrorTerminalClientDisconnect

class TerminalClientModel:

    PACKET_SIZE = 1024

    def __init__(self, connection, ip, port):
        self.connection = connection
        self.ip = ip
        self.port = port

class TerminalThreadRead(threading.Thread):

    PACKET_SIZE = 1024

    def __init__(self, connection, callback):
        super().__init__()
        self.connection = connection
        self.callback = callback
        self.name = self.getName()
        self.isRunning = False
        self.treat = TerminalTreatResponse()

    def run(self):
        try:
            self.isRunning = True
            while self.isRunning:
                rawmsg = self.connection.recv(TerminalThreadRead.PACKET_SIZE)
                if self.__check_raw_line(rawmsg) == True:
                    msg = rawmsg.decode()
                    if msg == "":
                        raise ErrorTerminalClientDisconnect("Client Terminal was disconnected : {}".format(self.connection))
                    else:
                        data = self.treat.treat(msg)
                        if data != None:
                            self.callback(data)
        except ErrorTerminalClientDisconnect as e:
            print("{}".format(e))
        except UnicodeDecodeError as e:
            print("Ligne : {}, {}".format(sys.exc_info()[-1].tb_lineno, e))

    def __check_raw_line(self, raw):
        flg = False
        if "\r" not in raw.decode():
            flg = True
        return flg

    def stop(self):
        self.isRunning = False

class TerminalThreadServer(threading.Thread):

    CLIENTS = {}

    def __init__(self, socket, callback):
        super().__init__()
        self.socket = socket
        self.callback = callback
        self.isRunning = False
        self.socket.listen(2)

    def run(self):
        try:
            self.isRunning = True
            while self.isRunning:
                connection, addr = self.socket.accept()
                TerminalThreadServer.CLIENTS[addr[0]] = TerminalThreadRead(connection, self.callback)
                TerminalThreadServer.CLIENTS[addr[0]].start()
        except Exception as e:
            print("[ERROR - SERVER] {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.socket.close()
    
    def stop(self):
        self.isRunning = False # Vrai ou faux ??!
        self.socket.close()

class TerminalThreadWrite(threading.Thread):

    def __init__(self, connection, data):
        super().__init__()
        self.connection = connection # find in a command the connection id or default
        self.data = str(data + "\r\n")
        self.name = self.getName()
    
    def run(self):
        try: 
            self.connection.send(self.data.encode())
        except Exception as e:
            print("ErrorWrite : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 

class TerminalTreatResponse:

    SIMPLE_REQUEST = 0
    UNKNOWN_REQUEST = 1
    MODULE_REQUEST = 2

    def __init__(self):
        pass

    def treat(self, msg):
        """
            * Command : data : [n, .......]
        """
        data = {}
        splitted = msg.split(" ")
        print(splitted)
        if splitted[0] in BaseDirectory.CONNECTED_MANAGERS_BY_NAME:
            treatedCommand = BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]].command(msg)
            if treatedCommand[0] == True:
                return treatedCommand[1]
            else:
                TerminalThreadWrite(TerminalThreadServer.CLIENTS[getIpAddress()].connection, "[ERROR - COMMAND] : {}\r\nusage:\r\n\t* {}".format(treatedCommand[1], BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]].usage)).start()
        else:
            TerminalThreadWrite(TerminalThreadServer.CLIENTS[getIpAddress()].connection, "[WARNING - COMMAND] : '{}' command is not known.".format(msg)).start() # list of connected modules
            

