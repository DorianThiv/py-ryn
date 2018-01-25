import sys
import shlex

from bases import BaseDirectory
from interfaces import IOperator
from transfert import ModuleFrameTransfert, SimpleFrameTransfert
from mdlterminal.specifics.exceptions import *

class TerminalOperator(IOperator):

    def __init__(self, name):
        self.name = name

    def load(self):
        pass

    def encapsulate(self, data):    
        splitted = shlex.split(data["payload"])
        if splitted[0] in BaseDirectory.CONNECTED_MANAGERS_BY_NAME:
            treatedCommand = BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]].command(splitted)
            if treatedCommand[0] == True:
                print(treatedCommand[1])
            else:
                raise TerminalCommandError("[ERROR - COMMAND] : {}\r\nusage:\r\n\t* {}".format(treatedCommand[1], BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]].usage))
        else:
            raise TerminalCommandError("[WARNING - COMMAND] : Module '{}' not exist.".format(data["payload"])) 

    def decapsulate(self, frame):
        try:
            return frame
        except Exception as e:
            print("[ERROR - DECAPSULATE - TERMINAL] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
