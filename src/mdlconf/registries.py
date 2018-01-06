
from bases import BaseRegistry

from mdlconf.operators import ConfigurationOperator

class ConfigurationRegistry(BaseRegistry):

    def __init__(self, name, provider):
        super().__init__(name, ConfigurationOperator("conf-operator"), provider)

