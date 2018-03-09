
""" Command Chain 

It's a command creator.

Property label make reference to BaseCommand: 
"READ", "WRITE", "SUBSCRIBE", "UNSUBSCRIBE", etc... 

"""

from bases import BaseCommand

class TerminalBaseCommand(BaseCommand):

    def __init__(self):
        super().__init__()
    
    def check(self, commanddict):
        commands = [
            TerminalMessageCommand(),
            TerminalSubscribeCommand(),
            TerminalUnsubscribeCommand(),
            TerminalAddCommand()
        ]
        if len(commanddict) == 1:
            return (False, BaseCommand.PARSE_ARGUMENTS_ERROR)
        if BaseCommand.PARSE_COMMAND not in commanddict:
            return (False, BaseCommand.PARSE_COMMAND_ERROR)
        else:
            for command in commands:
                if command.label == commanddict[BaseCommand.PARSE_COMMAND]:
                    return command.check(commanddict)

class TerminalMessageCommand:

    def __init__(self):
        self.label = BaseCommand.WRITE
    
    def check(self, commanddict):
        if BaseCommand.PARSE_ADDRESS not in commanddict:
            return (False, BaseCommand.PARSE_ADDRESS_ERROR)
        if BaseCommand.PARSE_TEXT not in commanddict:
            return (False, BaseCommand.PARSE_TEXT_ERROR)
        return (True, commanddict)
        
class TerminalSubscribeCommand:

    def __init__(self):
        self.label = BaseCommand.SUBSCRIBE
    
    def check(self, commanddict):
        if BaseCommand.PARSE_ADDRESS not in commanddict:
            return (False, BaseCommand.PARSE_ADDRESS_ERROR)
        return (True, commanddict)

class TerminalUnsubscribeCommand:

    def __init__(self):
        self.label = BaseCommand.UNSUBSCRIBE
    
    def check(self, commanddict):
        if BaseCommand.PARSE_ADDRESS not in commanddict:
            return (False, BaseCommand.PARSE_ADDRESS_ERROR)
        return (True, commanddict)
    
class TerminalAddCommand:

    def __init__(self):
        self.label = BaseCommand.ADD
    
    def check(self, commanddict):
        return (True, commanddict)