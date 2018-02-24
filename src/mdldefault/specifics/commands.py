
""" Command Chain 

It's a command creator.

Property label make reference to BaseCommand: 
"READ", "WRITE", "SUBSCRIBE", "UNSUBSCRIBE", etc... 

"""

from bases import BaseCommand

class DefaultBaseCommand:

    def __init__(self):
        pass
    
    def parse(self, commanddict):
        commands = [
            DefaultMessageCommand(),
        ]
        if len(commanddict) == 1:
            return (False, "no arguments detected")
        if BaseCommand.PARSE_COMMAND not in commanddict:
            return (False, "no command detected : (-w)")
        else:
            for command in commands:
                if command.label == commanddict[BaseCommand.PARSE_COMMAND]:
                    return command.parse(commanddict)
                else:
                    return (False, "no command found for : {}".format(commanddict[BaseCommand.PARSE_COMMAND]))

class DefaultMessageCommand:

    def __init__(self):
        self.label = BaseCommand.WRITE
    
    def parse(self, commanddict):
        if BaseCommand.PARSE_TEXT not in commanddict:
            return (False, "no message detected : (-t \"hello world\") | (--text \"hello world\")")
        return (True, commanddict)
        