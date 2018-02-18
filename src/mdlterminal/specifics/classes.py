import sys
import threading
import shlex

from bases import BaseBinder, BaseDirectory, BaseCommand
from mdlterminal.specifics.exceptions import *
from mdlterminal.specifics.models import DataRawModel

class TerminalThreadServer(threading.Thread):

    CONNECTIONS = 3

    def __init__(self, socket, callback):
        super().__init__()
        self.socket = socket
        self.directory = {}
        self.bcallback = callback
        self.current_connections = 0
        self.socket.listen(TerminalThreadServer.CONNECTIONS)
        self._stop_event = threading.Event()

    def run(self):
        try:
            while not self._stop_event.is_set():
                connection, addr = self.socket.accept() # blocking in thread. Test stop with an event
                self.directory[addr[0]] = TerminalThreadRead(connection, addr, self.scallback)
                self.directory[addr[0]].start()
                self.current_connections += 1
        except Exception as e:
            print("[ERROR - SERVER] {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.socket.close()       

    def write(self, data):
        connection = None
        if data.address != None:
            if data.address in self.directory:
                connection = self.directory[data.address].connection
                if isinstance(data.payload, str):
                    msg = data.payload
                if isinstance(data.payload, dict):
                    msg = str(data.payload[BaseCommand.PARSE_TEXT] + "\r\n")
                connection.send(msg.encode("iso-8859-1"))
            else:
                raise TerminalWriteError("Not found destination address.")
        else:
            raise TerminalWriteError("Not found destination address.")
    
    def scallback(self, ip, msg):
        if msg == -1:
            del self.directory[ip]
            self.current_connections -= 1
        else:
            data = DataRawModel(address=ip, payload=msg)
            self.bcallback(data)

    def stop(self):
        self._stop_event.is_set() # event stop
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
                        raise TerminalClientDisconnectError("A Terminal was disconnected : {}".format(self.connection))
                    else:
                        self.callback(self.ip, msg)
        except TerminalClientDisconnectError as e:
            print("{}".format(e))
            self.connection.close()  
        except UnicodeDecodeError as e:
            print("UnicodeDecodeError ligne : {}, {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.connection.close()
        except Exception as e:
            print("[ERROR - TERMINAL - CLIENT - READ] : {}".format(e))
            self.connection.close()

    def __check_raw_line(self, raw):
        flg = False
        if "\r" not in raw.decode("latin1").encode("utf-8").decode():
            flg = True
        return flg

    def stop(self):
        self.isRunning = False
        self.connection.close()
