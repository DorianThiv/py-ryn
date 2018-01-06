

import sys

from network import *
from bases import BaseDealer, BaseThreadClient, BaseThreadRead, BaseThreadWrite
from mdlterminal.exceptions import *

class TerminalThreadRead(BaseThreadClient):

    def __init__(self, connection, callback):
        super().__init__(connection, callback)
        self.treat = TerminalTreatResponse()

    def run(self):
        try:
            self.isRunning = True
            while self.isRunning:
                rawmsg = self.connection.recv(BaseThreadRead.PACKET_SIZE)
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

class TerminalThreadServer(BaseThreadRead):

    CLIENTS = {}

    def __init__(self, socket, callback):
        super().__init__(socket, callback)
        self.socket.listen(2)

    def run(self):
        try:
            self.isRunning = True
            while self.isRunning:
                connection, addr = self.socket.accept()
                TerminalThreadServer.CLIENTS[addr[0]] = connection
                termThC = TerminalThreadRead(connection, self.callback)
                termThC.start()
        except Exception as e:
            print("[ERROR - SERVER] {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.socket.close()
        

class TerminalThreadWrite(BaseThreadWrite):

    def __init__(self, data):
        super().__init__(TerminalThreadServer.CLIENTS[getIpAdress()], data)

class TerminalTreatResponse:

    SIMPLE_REQUEST = 0
    UNKNOWN_REQUEST = 1
    MODULE_REQUEST = 2

    def __init__(self):
        pass

    def treat(self, msg):
        """
            * Command :
            type : 0 | 1 | ...
            src : ["binder", "registry", "operator", "provider", "module"]
            dest-module : [..., ..., ..., ...]
            dest-provider | binder : [tcp, rtu, ...]
            dest-binder : [-w | -r] (read | write)
            data : [n, .......]
        """
        data = {}
        splitted = msg.split(" ")
        if self.__check_module_request(splitted):
            print("module request")
            data = self.__module_request(splitted)
        else:
            data = self.__unknown_request(msg)
        return data
    
    def __check_module_request(self, splitted):
        return True if splitted[0] in BaseDealer.CONNECTED_MANAGERS else False

    def __module_request(self, splitted):
        data = {}
        data["type"] = TerminalTreatResponse.MODULE_REQUEST
        data["dest-module"] = splitted[0]
        data["data"] = splitted[1:len(splitted)]
        return data
        # Call in a writer callback
        # print("[WARNING] Ligne {} : {}".format(sys.exc_info()[-1].tb_lineno, WarningTerminalWrongRequestModule(e, splitted[0])))

    def __unknown_request(self, msg):
        data = {}
        data["type"] = TerminalTreatResponse.UNKNOWN_REQUEST
        data["data"] = msg
        return data
