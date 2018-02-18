
from bases import BaseRegistry
from mdlterminal.specifics.models import *
from mdlterminal.specifics.exceptions import *

class TerminalRegistry(BaseRegistry):

    def __init__(self, name):
        super().__init__(name)

           