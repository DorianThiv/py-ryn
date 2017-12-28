
from bases import BaseProvider

class ConfigurationProvider(BaseProvider):

    def __init__(self, name, observable=None):
        super().__init__(name, observable)