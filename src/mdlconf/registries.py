
from transfert import FrameTransfert
from bases import BaseRegistry

class ConfigurationRegistry(BaseRegistry):

    def __init__(self, ref, name):
        super().__init__(ref, name)
        
    
    def __str__(self):
        return "__CONFIGREGISTRY__ = (ref : {}, name : {})\n".format(self.ref, self.name)

    def load(self, providers):
        for provider in providers:
            self.observers.append(provider)
    
    def operate(self, emitter, data):
    	pass

    # def register(self, observer):
       # self.observers.append(observer)
    
    # def unregister(self, observer):
        # pass

    # def unregister_all(self):
        # pass

    # def observers_update(self, emitter, receptor, action, data, timestamp, crc):
        # super().observers_update(emitter, receptor, action, data, timestamp, crc)
