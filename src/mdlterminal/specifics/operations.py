
import shlex

from bases import BaseDirectory, BaseCommand
from samples.transfert import ModuleFrameTransfert
from mdlterminal.specifics.models import DataRawModel
from mdlterminal.specifics.exceptions import TerminalCommandError

class TerminalOperations:

    def __init__(self):
        pass

    def operate_up(self, module, data):
        splitted = self.__split_command(data.payload)
        if splitted != [] and splitted != None:
            if splitted[0] in BaseDirectory.CONNECTED_MANAGERS_BY_NAME:
                manager = BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]]
                status, commandline = manager.command(splitted)
                if status is True:
                    return ModuleFrameTransfert(src=module, dest=commandline[BaseCommand.PARSE_MODULE], command=commandline[BaseCommand.PARSE_COMMAND], payload=commandline)
                else:
                    raise TerminalCommandError("[WARNING - COMMAND] : {}\r\nusage:\r\n* {}".format(commandline, BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]].usage))
            else:
                raise TerminalCommandError("[WARNING - COMMAND] : Module '{}' not exist.".format(data.payload))
        else:
            raise TerminalCommandError("[WARNING - COMMAND] : Incomprehensible command.")
    
    def operate_down(self, frame):
        if BaseCommand.PARSE_ADDRESS in frame.payload:
            addr = frame.payload[BaseCommand.PARSE_ADDRESS]
            return DataRawModel(command=frame.command, address=addr, payload=frame.payload)
        else:
            return DataRawModel(command=frame.command, payload=frame.payload)

    def __split_command(self, command):
        """ Split a command line with shlex """
        try:
            return shlex.split(command)
        except Exception as e:
            print("[ERROR - ENCAPSULATE - SPLITTED] : {}".format(e))