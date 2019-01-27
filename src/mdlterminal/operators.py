import sys

from bases import BaseOperator
from mdlterminal.specifics.operations import TerminalOperations

class TerminalOperator(BaseOperator):

    def __init__(self, parent):
        super().__init__(TerminalOperations(), parent)

