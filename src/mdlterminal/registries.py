
from bases import BaseRegistry

from mdlterminal.operators import TerminalOperator

class TerminalRegistry(BaseRegistry):

    def __init__(self, name, provider):
        super().__init__(name, TerminalOperator("exemple-operator"), provider)
