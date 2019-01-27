
import sys

class ErrorDefault(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}".format(self.message)

class DefaultClientDisconnectError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}".format(self.message)

class DefaultWrongCommandModuleError(Exception):

    """ WarningDefaultWrongRequestModule : 
        Modules commands usage :
    """

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}\n".format(self.message)
        
class DefaultCommandError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}\n".format(self.message)
    
class DefaultWriteError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "DefaultWriteError {}\n".format(self.message)
