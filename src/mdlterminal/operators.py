import sys
import shlex

from mdlutils.bases import BaseManager, BaseDirectory, BaseCommand, BaseOperator
from mdlutils.interfaces import IOperator
from mdlutils.transfert import ModuleFrameTransfert, SimpleFrameTransfert
from mdlterminal.specifics.exceptions import *
from mdlterminal.registries import TerminalRegistry
from mdlterminal.specifics.templates import TerminalRawModel

class TerminalOperator(BaseOperator):

    def __init__(self, name, provider):
        super().__init__(name, TerminalRegistry("terminal-operator"), provider)

    def execute(self, frame):
        for b in self.childs:
            self.childs[b].execute(self.decapsulate(frame))    

    def encapsulate(self, data):
        splitted = self.__split_command(data)
        if splitted != [] and splitted != None:
            if splitted[0] in BaseDirectory.CONNECTED_MANAGERS_BY_NAME:
                manager = BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]]
                status, commandline = manager.command(splitted)
                if status is True:
                    return ModuleFrameTransfert(
                        src=self.module, 
                        dest=commandline[BaseCommand.PARSE_MODULE],
                        payload=commandline
                    )
                else:
                    raise TerminalCommandError("[WARNING - COMMAND] : {}\r\nusage:\r\n* {}".format(commandline, BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]].usage))
            else:
                raise TerminalCommandError("[WARNING - COMMAND] : Module '{}' not exist.".format(data.payload))
        else:
            raise TerminalCommandError("[WARNING - COMMAND] : Incomprehensible command.")

    def decapsulate(self, frame):
        try:
            if isinstance(frame, SimpleFrameTransfert):
                data = TerminalRawModel(frame.command)
            if isinstance(frame, ModuleFrameTransfert):
                data = TerminalRawModel(frame.payload[BaseCommand.PARSE_DIRECTION], frame.payload[BaseCommand.PARSE_ADDRESS], frame.payload[BaseCommand.PARSE_TEXT])
            return data
        except Exception as e:
            print("[ERROR - DECAPSULATE - TERMINAL] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
    
    def __split_command(self, data):
        """ Split a command line with shlex """
        try:
            return shlex.split(data.payload)
        except Exception as e:
            print("[ERROR - ENCAPSULATE - SPLITTED] : {}".format(e))
    
    def observers_update(self, data):
        try:
            for observer in self.observers:
                decaps_data = self.encapsulate(data)
                observer.update(decaps_data)
        except TerminalCommandError as e:
            """ Get the right binder to use write command and send error """
            data.payload = e.message
            data.binder.write(data)
        except Exception as e:
            print("[ERROR - UPDATE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e)) 

