
from bases import BaseRegistry

from mdlconf.operators import ConfigurationOperator

class ConfigurationRegistry(BaseRegistry):

    def __init__(self, name):
        super().__init__(name, ConfigurationOperator("conf-operator"))

    def load(self, providers):
        for provider in providers:
            self.observers.append(provider)
