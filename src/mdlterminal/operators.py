import sys
import shlex

from bases import BaseManager, BaseDirectory, BaseCommand
from interfaces import IOperator
from transfert import ModuleFrameTransfert, SimpleFrameTransfert
from mdlterminal.specifics.exceptions import *
from mdlterminal.specifics.templates import TerminalRawModel

class TerminalOperator(IOperator):

    def __init__(self, name, mdlname):
        self.name = name
        self.mdlname = mdlname

    def encapsulate(self, data):
        splitted = self.__split_command(data)
        if splitted != [] and splitted != None:
            if splitted[0] in BaseDirectory.CONNECTED_MANAGERS_BY_NAME:
                manager = BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]]
                status, commandline = manager.command(splitted)
                if status is True:
                    return ModuleFrameTransfert(
                        src=self.mdlname, 
                        dest=commandline[BaseManager.PARSE_MODULE],
                        payload=commandline
                    )
                else:
                    raise TerminalCommandError("[ERROR - COMMAND] : {}\r\nusage:\r\n\t* {}".format(commandline, BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]].usage))
            else:
                raise TerminalCommandError("[WARNING - COMMAND] : Module '{}' not exist.".format(data.payload))
        else:
            raise TerminalCommandError("[WARNING - COMMAND] : Incomprehensible command.")

    def decapsulate(self, frame):
        try:
            if isinstance(frame, SimpleFrameTransfert):
                data = TerminalRawModel(frame.command)
            if isinstance(frame, ModuleFrameTransfert):
                data = TerminalRawModel(frame.payload[BaseManager.PARSE_DIRECTION], frame.payload[BaseManager.PARSE_ADDRESS], frame.payload[BaseManager.PARSE_TEXT])
            return data
        except Exception as e:
            print("[ERROR - DECAPSULATE - TERMINAL] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
    
    def __split_command(self, data):
        """ Split a command line with shlex """
        try:
            return shlex.split(data.payload)
        except Exception as e:
            print("[ERROR - ENCAPSULATE - SPLITTED] : {}".format(e))

