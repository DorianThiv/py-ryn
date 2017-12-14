
from bases import BaseProvider

class ConfigurationProvider(BaseProvider):

    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def load(self):
        pass

    def provide(self):
        pass

    def update(self):
        pass