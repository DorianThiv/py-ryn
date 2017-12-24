

import sys
from bases import BaseThreadRead, BaseThreadWrite

class TerminalThreadClient(BaseThreadRead):

    def __init__(self, socket, callback):
        super().__init__(socket, callback)

class TerminalThreadRead(BaseThreadRead):

    def __init__(self, socket, callback):
        super().__init__(socket, callback)
        self.socket.listen(2)

    def run(self):
        try:
            self.isRunning = True
            while self.isRunning:
                connection, addr = self.socket.accept()
                termThC = TerminalThreadClient(self.socket, self.callback)
                termThC.start()
        except Exception as e:
            print("[ERROR - SERVER] {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.socket.close()

    