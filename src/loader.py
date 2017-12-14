
from bases import BaseLoader 

class ManagerFactory:
    
    @staticmethod
    def make(name):
        if name == "mdlcmd":
            try:
                from mdlcmd.managers import CmdManager
                m = CmdManager("111-111", name)
                return m                
            except:
                print("Except : ErrorLoadModule : {}".format(name)) 
        if name == "mdlconf":
            try:
                from mdlconf.managers import ConfigurationManager
                m = ConfigurationManager("111-001", name)
                return m                
            except:
                print("Except : ErrorLoadModule : {}".format(name)) 

class Loader(BaseLoader):
    def __init__(self, ref, name):
        super().__init__(ref, name)
    
    def __str__(self):
        ret = ""
        for manager in self.managers:
            ret += "{}\n".format(self.managers[manager])
        return ret

    def load(self, managers):
        self.managers = {}
        for manager in managers:
            self.managers[manager] = ManagerFactory.make(manager)

    def reload(self):
        pass