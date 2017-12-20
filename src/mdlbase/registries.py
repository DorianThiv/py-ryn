
from bases import BaseRegistry

from mdlbase.operators import MdlBaseOperator

class MdlBaseRegistry(BaseRegistry):

    def __init__(self, name):
        super().__init__(name, MdlBaseOperator("base-operator"))
    
    def __str__(self):
        return "__CONFIGREGISTRY__ = (name : {})\n".format(self.name)

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
