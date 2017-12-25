

import sys
from bases import BaseDealer, BaseThreadClient, BaseThreadRead, BaseThreadWrite
from mdlterminal.exceptions import *

class TerminalThreadClient(BaseThreadClient):

    def __init__(self, connection, callback):
        super().__init__(connection, callback)
        self.treat = TerminalTreatResponse()

    def run(self):
        try:
            self.isRunning = True
            while self.isRunning:
                msg = self.connection.recv(BaseThreadRead.PACKET_SIZE).decode()
                if msg == "":
                    raise ErrorTerminalClientDisconnect("Client Terminal was disconnected : {}".format(self.connection))
                else:
                    self.callback(self.treat.treat(msg))
        except ErrorTerminalClientDisconnect as e:
            print("{}".format(e))

class TerminalThreadRead(BaseThreadRead):

    def __init__(self, socket, callback):
        super().__init__(socket, callback)
        self.socket.listen(2)

    def run(self):
        try:
            self.isRunning = True
            while self.isRunning:
                connection, addr = self.socket.accept()
                termThC = TerminalThreadClient(connection, self.callback)
                termThC.start()
        except Exception as e:
            print("[ERROR - SERVER] {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.socket.close()

class TerminalTreatResponse:

    UNKNOWN_REQUEST = 0
    MODULE_REQUEST = 1

    def __init__(self):
        pass

    def treat(self, msg):
        """
            * Command :
            Module : [..., ..., ..., ...]
            Provider : [tcp, rtu, ...]
            Binder : [-w | -r] (read | write)
            Data : [n, .......]
        """
        splitted = msg.split(" ")
        data = {}
        if self.__check_module_request(splitted[0]):
            data = self.__module_request(splitted)
        else:
            data = self.__unknown_request(splitted)
        return data
    
    def __check_module_request(self, module):
        flg = False
        for name in BaseDealer.CONNECTED_MANAGERS:
            if module == name:
                flg = True
        return flg

    def __module_request(self, splitted):
        data = {}
        try:
            data["type"] = TerminalTreatResponse.MODULE_REQUEST
            data["module"] = splitted[0]
            data["provider"] = splitted[1]
            data["binder"] = splitted[2]
            data["data"] = splitted[2:len(splitted)-1]
        except Exception as e:
            print("[WARNING] Ligne {} : {}".format(sys.exc_info()[-1].tb_lineno, WarningTerminalWrongRequestModule(e, splitted[0])))
        return data

    def __unknown_request(self, splitted):
        data = {}
        data["type"] = TerminalTreatResponse.UNKNOWN_REQUEST
        data["data"] = splitted[0:len(splitted)-1]
        return data