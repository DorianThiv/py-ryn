
from bases import BaseRegistry, BaseCommand, BaseManager

from mdlterminal.operators import TerminalOperator
from mdlterminal.specifics.exceptions import *

class TerminalRegistry(BaseRegistry):

    def __init__(self, name, provider):
        super().__init__(name, TerminalOperator("terminal-operator"), provider)
        
    def execute(self, frame):
        for b in self.binders:
            self.binders[b].execute(self.operator.decapsulate(frame))    
    
    def observers_update(self, data):
        try:
            for observer in self.observers:
                decaps_data = self.operator.encapsulate(data)
                observer.update(decaps_data, decaps_data[BaseManager.PARSE_TEXT])
        except TerminalCommandError as e:
            """ Get the right binder to use write command and send error """
            data.payload = e.message
            data.binder.write(data)
        except Exception as e:
            print("[ERROR - UPDATE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))    