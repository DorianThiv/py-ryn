
from bases import BaseCommand

class TerminalSimpleCommand:

    @staticmethod
    def parse(commanddict):
        if len(commanddict) == 1:
            return (False, "no arguments detected")
        if BaseCommand.PARSE_COMMAND not in commanddict:
            return (False, "no command detected : (-r | -w) | (--read | --write)")
        if BaseCommand.PARSE_ADDRESS not in commanddict:
            return (False, "no destination address detected : (-a | --address x.x.x.x)")
        if BaseCommand.PARSE_TEXT not in commanddict:
            return (False, "no message detected : (-t \"hello world\") | (--text \"hello world\")")
        return (True, commanddict)
        