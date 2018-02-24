import sys

from bases import BaseOperator
from mdlterminal.specifics.exceptions import TerminalCommandError
from mdlterminal.registries import TerminalRegistry
from mdlterminal.specifics.operations import TerminalOperations

class TerminalOperator(BaseOperator):

    def __init__(self, name, provider):
        super().__init__(name, TerminalRegistry("terminal-operator"), TerminalOperations(), provider)

    def emit(self, data):
        try:
            super().emit(data)
            for observer in self.observers:
                decaps_data = self.encapsulate(data)
                observer.update(decaps_data)
        except TerminalCommandError as e:
            data.payload = e.message
            data.binder.write(data)
        except Exception as e:
            print("[ERROR - TERMINAL - OPERATOR - UPDATE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e)) 
            self.logger.log(0, "Terminal operator: (error: {}, data: {})".format(e, data))

