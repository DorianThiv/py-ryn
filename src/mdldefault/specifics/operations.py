
import shlex

from bases import Directory, BaseCommand
from samples.transfert import ModuleFrameTransfert
from mdldefault.specifics.models import DataRawModel
from mdldefault.specifics.exceptions import DefaultCommandError

class DefaultOperations:

    def __init__(self):
        pass

    def operate_up(self, module, data):
        splitted = self.__split_command(data.payload)
        if splitted != [] and splitted != None:
            if splitted[0] in Directory.CONNECTED_MANAGERS_BY_NAME:
                manager = Directory.CONNECTED_MANAGERS_BY_NAME[splitted[0]]
                status, commandline = manager.command(splitted)
                if status is True:
                    return ModuleFrameTransfert(src=module, dest=commandline[BaseCommand.PARSE_MODULE], command=commandline[BaseCommand.PARSE_COMMAND], payload=commandline)
                else:
                    raise DefaultCommandError("[WARNING - COMMAND] : {}\r\nusage:\r\n* {}".format(commandline, Directory.CONNECTED_MANAGERS_BY_NAME[splitted[0]].usage))
            else:
                raise DefaultCommandError("[WARNING - COMMAND] : Module '{}' not exist.".format(data.payload))
        else:
            raise DefaultCommandError("[WARNING - COMMAND] : Incomprehensible command.")
    
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