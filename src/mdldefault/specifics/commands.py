
""" Command Chain 

It's a command creator.

Property label make reference to BaseCommand: 
"READ", "WRITE", "SUBSCRIBE", "UNSUBSCRIBE", etc... 

"""

from bases import BaseCommand

class DefaultBaseCommand(BaseCommand):

    def __init__(self):
        super().__init__()
    
    def check(self, commanddict):
        commands = [
            DefaultMessageCommand()
        ]
        if len(commanddict) == 1:
            return (False, BaseCommand.PARSE_ARGUMENTS_ERROR)
        if BaseCommand.PARSE_COMMAND not in commanddict:
            return (False, BaseCommand.PARSE_COMMAND_ERROR)
        else:
            for command in commands:
                if command.label == commanddict[BaseCommand.PARSE_COMMAND]:
                    return command.check(commanddict)

class DefaultMessageCommand:

    def __init__(self):
        self.label = BaseCommand.WRITE
    
    def check(self, commanddict):
        if BaseCommand.PARSE_TEXT not in commanddict:
            return (False, BaseCommand.PARSE_TEXT_ERROR)
        return (True, commanddict)

