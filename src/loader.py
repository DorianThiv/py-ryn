
class ManagerFactory:
    
    @staticmethod
    def make(name):
        if name == "mdlcmd":
            from mdlcmd.managers import CmdManager
            m = CmdManager("111-111", name)
            return m 
        if name == "mdltest":
            from mdltest.managers import TestManager
            m = TestManager("111-121", name)
            return m 

class Loader:
    def __init__(self, managers):
        self.managers = {}
        for manager in managers:
            self.managers[manager] = ManagerFactory.make(manager)
    
    def __str__(self):
        ret = ""
        for manager in self.managers:
            ret += "* {}\n".format(self.managers[manager])
        return ret