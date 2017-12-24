

import sys
from bases import BaseThreadClient, BaseThreadRead, BaseThreadWrite
from mdlterminal.exceptions import ErrorTerminalClientDisconnect

class TerminalThreadClient(BaseThreadClient):

    def __init__(self, connection, callback):
        super().__init__(connection, callback)

    def run(self):
        self.isRunning = True
        while self.isRunning:
            msg = self.connection.recv(BaseThreadRead.PACKET_SIZE).decode()
            if msg == "":
                raise ErrorTerminalClientDisconnect("Client Terminal was disconnected")
            self.callback(msg)

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

    