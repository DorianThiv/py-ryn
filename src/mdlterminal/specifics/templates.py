import sys
import threading

from bases import BaseBinder
from network import getIpAddress
from mdlterminal.specifics.exceptions import TerminalWrongCommandModuleError, ErrorTerminalClientDisconnect, TerminalWriteError

class TerminalThreadServer(threading.Thread):

    CLIENTS_DIRECTORY = {}

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
                TerminalThreadServer.CLIENTS_DIRECTORY[addr[0]] = TerminalThreadRead(connection, addr, self.callback)
                TerminalThreadServer.CLIENTS_DIRECTORY[addr[0]].start()
        except Exception as e:
            print("[ERROR - SERVER] {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.socket.close()
    
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

class TerminalThreadWrite(threading.Thread):

    def __init__(self, data):
        super().__init__()
        self.__finished = threading.Event()
        self.name = self.getName()
        self.newline = "\r\n"
        self.data = data
        self.msg = str(data.payload + self.newline)
        if data.address in TerminalThreadServer.CLIENTS_DIRECTORY:
            self.connection = TerminalThreadServer.CLIENTS_DIRECTORY[data.address].connection
        else:
            raise TerminalWriteError("Not found destination address.")
    
    def run(self):
        self.connection.send(self.msg.encode())

class TerminalRawModel:

    PACKET_SIZE = 1024

    def __init__(self, command = None, address=None, payload=None, binder=None):
        self.command = command
        self.address = address
        self.payload = payload
        if isinstance(binder, BaseBinder):
            self.binder = binder