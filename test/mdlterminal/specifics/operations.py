
import shlex

from bases import BaseDirectory, BaseCommand
from mdlutils.transfert import ModuleFrameTransfert
from mdlterminal.specifics.exceptions import TerminalCommandError

class Operations:

    @staticmethod
    def operate(module, data):
        splitted = Operations.__split_command(data)
        if splitted != [] and splitted != None:
            if splitted[0] in BaseDirectory.CONNECTED_MANAGERS_BY_NAME:
                manager = BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]]
                status, commandline = manager.command(splitted)
                if status is True:
                    return ModuleFrameTransfert(src=module, dest=commandline[BaseCommand.PARSE_MODULE], payload=commandline)
                else:
                    raise TerminalCommandError("[WARNING - COMMAND] : {}\r\nusage:\r\n* {}".format(commandline, BaseDirectory.CONNECTED_MANAGERS_BY_NAME[splitted[0]].usage))
            else:
                raise TerminalCommandError("[WARNING - COMMAND] : Module '{}' not exist.".format(data.payload))
        else:
            raise TerminalCommandError("[WARNING - COMMAND] : Incomprehensible command.")
    
    @staticmethod
    def __split_command(data):
        """ Split a command line with shlex """
        try:
            return shlex.split(data.payload)
        except Exception as e:
            print("[ERROR - ENCAPSULATE - SPLITTED] : {}".format(e))