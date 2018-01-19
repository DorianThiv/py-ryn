

import sys
import threading

from network import getIpAddress
from mdlterminal.specifics.exceptions import TerminalWrongCommandModuleError, ErrorTerminalClientDisconnect, TerminalWriteError

class TerminalClientModel:

    PACKET_SIZE = 1024

    def __init__(self, connection, ip, port):
        self.connection = connection
        self.ip = ip
        self.port = port

class TerminalThreadRead(threading.Thread):

    PACKET_SIZE = 1024

    def __init__(self, connection, addr, callback):
        super().__init__()
        self.connection = connection
        self.ip = addr[0]
        self.port = addr[1]
        self.callback = callback
        self.name = self.getName()
        self.isRunning = False

    def run(self):
        try:
            self.isRunning = True
            while self.isRunning:
                rawmsg = self.connection.recv(TerminalThreadRead.PACKET_SIZE)
                if self.__check_raw_line(rawmsg) == True:
                    msg = rawmsg.decode("latin1").encode("utf-8").decode()
                    if msg == "":
                        raise ErrorTerminalClientDisconnect("Client Terminal was disconnected : {}".format(self.connection))
                    else:
                        self.callback(self.ip, msg)
        except ErrorTerminalClientDisconnect as e:
            print("{}".format(e))
        except UnicodeDecodeError as e:
            print("UnicodeDecodeError ligne : {}, {}".format(sys.exc_info()[-1].tb_lineno, e))
        except Exception as e:
            print("Exception ligne : {}, {}".format(sys.exc_info()[-1].tb_lineno, e))

    def __check_raw_line(self, raw):
        flg = False
        if "\r" not in raw.decode("latin1").encode("utf-8").decode():
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
                TerminalThreadServer.CLIENTS[addr[0]] = TerminalThreadRead(connection, addr, self.callback)
                TerminalThreadServer.CLIENTS[addr[0]].start()
        except Exception as e:
            print("[ERROR - SERVER] {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.socket.close()
    
    def stop(self):
        self.isRunning = False # Vrai ou faux ??!
        self.socket.close()

class TerminalThreadWrite(threading.Thread):

    def __init__(self, data, msg):
        super().__init__()
        self.name = self.getName()
        self.msg = str(msg + "\r\n")
        if data["address"] in TerminalThreadServer.CLIENTS:
            self.connection = TerminalThreadServer.CLIENTS[data["address"]].connection
        else:
            raise TerminalWriteError("Not found destination address.")
    
    def run(self):
        try:
            self.connection.send(self.msg.encode())
        except Exception as e:
            print("ErrorWrite : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 

