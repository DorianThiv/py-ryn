
import sys
from bases import BaseDealer

class ErrorTerminal(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}".format(self.message)

class ErrorTerminalClientDisconnect(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}".format(self.message)

class TerminalWrongCommandModuleError(Exception):

    """ WarningTerminalWrongRequestModule : 
        Modules commands usage :
    """

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}\n".format(self.message)
        
class TerminalCommandError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}\n".format(self.message)
    
class TerminalWriteError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "TerminalWriteError {}\n".format(self.message)
