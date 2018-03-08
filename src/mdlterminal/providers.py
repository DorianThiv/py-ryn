
import sys

from bases import BaseProvider

class TerminalProvider(BaseProvider):

    def __init__(self, name, parent):
        super().__init__(name, parent)

