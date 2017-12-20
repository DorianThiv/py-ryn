
from bases import BaseRegistry

from mdlconf.operators import ConfigurationOperator

class ConfigurationRegistry(BaseRegistry):

    def __init__(self, name):
        super().__init__(name, ConfigurationOperator("conf-operator"))

    def load(self, providers):
        for provider in providers:
            self.observers.append(provider)

    # def register(self, observer):
       # self.observers.append(observer)
    
    # def unregister(self, observer):
        # pass

    # def unregister_all(self):
        # pass

    # TODO: Give frame at super :)
    # def observers_update(self, emitter, receptor, action, data, timestamp, crc):
    #     frame = self.operate(emitter, receptor, action, data, timestamp, crc)
    #     super().observers_update(frame)
