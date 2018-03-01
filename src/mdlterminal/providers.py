
import sys

from bases import BaseProvider
from mdlterminal.operators import TerminalOperator
from mdlterminal.registries import TerminalRegistry
from mdlterminal.specifics.exceptions import TerminalCommandError

class TerminalProvider(BaseProvider):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.operator = TerminalOperator(self)
        self.registry = TerminalRegistry()
        
    def emit(self, data):
        try:
            super().emit(data)
        except TerminalCommandError as e:
            data.payload = e.message
            data.binder.write(data)
        except Exception as e:
            print("[ERROR - TERMINAL - OPERATOR - UPDATE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e)) 
            self.logger.log(0, "Terminal operator: (error: {}, data: {})".format(e, data))    

