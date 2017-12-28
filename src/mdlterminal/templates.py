

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
                rawmsg = self.connection.recv(BaseThreadRead.PACKET_SIZE)
                if self.__check_raw_line(rawmsg) == True:
                    msg = rawmsg.decode()
                    if msg == "":
                        raise ErrorTerminalClientDisconnect("Client Terminal was disconnected : {}".format(self.connection))
                    else:
                        self.callback(self.treat.treat(msg))
        except ErrorTerminalClientDisconnect as e:
            print("{}".format(e))
        except UnicodeDecodeError as e:
            print("Ligne : {}, {}".format(sys.exc_info()[-1].tb_lineno, e))

    def __check_raw_line(self, raw):
        flg = False
        if "\r" not in raw.decode():
            flg = True
        return flg

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
            type : 0 | 1 | ...
            src : ["binder", "registry", "operator", "provider", "module"]
            dest-module : [..., ..., ..., ...]
            dest-provider | binder : [tcp, rtu, ...]
            dest-binder : [-w | -r] (read | write)
            data : [n, .......]
        """
        data = {}
        if self.__check_module_request(msg):
            print("module request")
            splitted = msg.split(" ")
            data = self.__module_request(splitted)
        else:
            data = self.__unknown_request(msg)
        return data
    
    def __check_module_request(self, msg):
        flg = False
        splitted = msg.split(" ")
        for name in BaseDealer.CONNECTED_MANAGERS:
            if splitted[0] == name:
                flg = True
        return flg

    def __check_integtity_cmd(self, splitted):
        if splitted[1] == "-r" or splitted[1] == "-w":
            return True
        elif splitted[1] == "--read" or splitted[1] == "--write":
            return True
        else:
            return False

    def __module_request(self, splitted):
        data = {}
        try:
            self.__check_integtity_cmd(splitted)
            data["type"] = TerminalTreatResponse.MODULE_REQUEST
            data["dest-module"] = splitted[0]
            data["dest-action"] = splitted[1]
            data["data"] = splitted[2:len(splitted)-1]
        except Exception as e:
            print("[WARNING] Ligne {} : {}".format(sys.exc_info()[-1].tb_lineno, WarningTerminalWrongRequestModule(e, splitted[0])))
        return data

    def __unknown_request(self, msg):
        data = {}
        data["type"] = TerminalTreatResponse.UNKNOWN_REQUEST
        data["data"] = msg
        return data