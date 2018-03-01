
""" Command Chain 

It's a command creator.

Property label make reference to BaseCommand: 
"READ", "WRITE", "SUBSCRIBE", "UNSUBSCRIBE", etc... 

"""

from bases import BaseCommand

class TerminalBaseCommand:

    def __init__(self):
        pass
    
    def parse(self, commanddict):
        commands = [
            TerminalMessageCommand(),
            TerminalSubscribeCommand(),
            TerminalUnsubscribeCommand()
        ]
        if len(commanddict) == 1:
            return (False, "no arguments detected")
        if BaseCommand.PARSE_COMMAND not in commanddict:
            return (False, "no command detected : (-r | -w | -s | -u)")
        else:
            for command in commands:
                if command.label == commanddict[BaseCommand.PARSE_COMMAND]:
                    return command.parse(commanddict)

class TerminalMessageCommand:

    def __init__(self):
        self.label = BaseCommand.WRITE
    
    def parse(self, commanddict):
        if BaseCommand.PARSE_ADDRESS not in commanddict:
            return (False, "no destination address detected : (-a | --address x.x.x.x)")
        if BaseCommand.PARSE_TEXT not in commanddict:
            return (False, "no message detected : (-t \"hello world\") | (--text \"hello world\")")
        return (True, commanddict)
        
class TerminalSubscribeCommand:

    def __init__(self):
        self.label = BaseCommand.SUBSCRIBE
    
    def parse(self, commanddict):
        if BaseCommand.PARSE_ADDRESS not in commanddict:
            return (False, "no destination address detected : (-a | --address x.x.x.x)")
        return (True, commanddict)

class TerminalUnsubscribeCommand:

    def __init__(self):
        self.label = BaseCommand.UNSUBSCRIBE
    
    def parse(self, commanddict):
        if BaseCommand.PARSE_ADDRESS not in commanddict:
            return (False, "no destination address detected : (-a | --address x.x.x.x)")
        return (True, commanddict)