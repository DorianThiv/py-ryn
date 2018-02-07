import sys
import threading

from bases import BaseBinder
from mdlutils.network import getIpAddress
from mdlterminal.specifics.exceptions import TerminalWrongCommandModuleError, ErrorTerminalClientDisconnect, TerminalWriteError

class TerminalRawModel:

    PACKET_SIZE = 1024

    def __init__(self, command = None, address=None, payload=None, binder=None):
        self.command = command
        self.address = address
        self.payload = payload
        if isinstance(binder, BaseBinder):
            self.binder = binder

class TerminalThreadServer(threading.Thread):

    CONNECTIONS = 3
    CLIENTS_DIRECTORY = {}

    def __init__(self, socket, callback):
        super().__init__()
        self.socket = socket
        self.bcallback = callback
        self.isRunning = False
        self.current_connections = 0
        self.directory = {}
        self.socket.listen(TerminalThreadServer.CONNECTIONS)

    def run(self):
        try:
            self.isRunning = True
            while self.isRunning:
                connection, addr = self.socket.accept()
                if self.current_connections != 3:
                    self.directory[addr[0]] = TerminalThreadRead(connection, addr, self.scallback)
                    self.directory[addr[0]].start()
                    self.current_connections += 1
                else:
                    print("[ERROR - SERVER] : No more connection is allowed.")        
        except Exception as e:
            print("[ERROR - SERVER] {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.socket.close()

    def write(self, data):
        connection = None
        if data.address in self.directory:
            connection = self.directory[data.address].connection
        else:
            raise TerminalWriteError("Not found destination address.")
        msg = str(data.payload + "\r\n")
        connection.send(msg.encode())
    
    def scallback(self, ip, msg):
        if msg == -1:
            del self.directory[ip]
        else:
            self.bcallback(ip, msg)

    def stop(self):
        self.isRunning = False # Vrai ou faux ??!
        self.socket.close()

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
            self.callback(self.ip, -1)
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
