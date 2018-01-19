
from bases import BaseRegistry

from mdlterminal.operators import TerminalOperator
from mdlterminal.specifics.exceptions import *

class TerminalRegistry(BaseRegistry):

    def __init__(self, name, provider):
        super().__init__(name, TerminalOperator("exemple-operator"), provider)
    
    def observers_update(self, data):
        try:
            for observer in self.observers:
                observer.update(self.operator.encapsulate(data))
        except TerminalCommandError as e:
            """ Get the right binder to use write command and send error """
            print(e)
            print("[ERROR - UPDATE - TERMINAL] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            data["binder"].write(data, e.message)
        except Exception as e:
            print("[ERROR - UPDATE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))    