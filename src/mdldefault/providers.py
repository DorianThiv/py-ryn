
from bases import BaseProvider

class DefaultProvider(BaseProvider):

    def __init__(self, name, observable=None):
        super().__init__(name, observable)

