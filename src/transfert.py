
from util import list2str

class SimpleFrameTransfert:

    """ Serialize @param : frame to SimpleFrameTransfert :
        [Command] => BaseCommand (actually )
        [Callback] => Optionnal
        [Log] => class Logger (message, exception, comments) ???   
    """

    def __init__(self, command=None, payload=None, callback=None, log=None):
        self.command = command
        self.payload = payload
        self.callback = callback
        self.log = log

    def __str__(self):
        return "__SIMPLE_FRAME__ = (|command : {} | payload: {} | callback : {} | log : {})".format(self.command, self.payload, self.callback, self.log)

    @staticmethod
    def serialize(frame):
        pass

    @staticmethod
    def deserialize(frame):
        pass

class ModuleFrameTransfert:

    """ Serialize @param : frame to SimpleFrameTransfert :
        [src-addr] => (M = 0x00, P = 0x00, R = 0x00, B = 0x00)
        [dest-addr] => (M = 0x00, P = 0x00, R = 0x00, B = 0x00)
        [command] => BaseCommand (actually)
        [payload] => Content known buy dest module
        [callback] => Optionnal
        [log] => class Logger (message, exception, timestamp)   
    """

    def __init__(self, srcAddr=[], destAddr=[], command=None, payload=None, callback=None, log=None):
        self.srcAddr = srcAddr
        self.destAddr = destAddr
        self.command = command
        self.payload = payload
        self.callback = callback
        self.log = log

    def __str__(self):
        return "__MODULE_FRAME__ = (|src : {} | dest : {} | command: {} | payload : {} | callback : {} | log : {}|)".format(self.srcAddr, self.destAddr, self.command, self.payload, self.callback, self.log)

    def addToSrcAddr(self, _id):
        pass
    
    def addToDestAddr(self, _id):
        pass

    def serializeSrcAddr(self):
        """ In util.py implement JSON class to serialize and deserialize in json """
        pass

    def serializePayload(self, payload):
        """ In util.py implement JSON class to serialize and deserialize in json """
        pass

    @staticmethod
    def deserializePayload(payload):
        """ In util.py implement JSON class to serialize and deserialize in json """
        pass

    def createLog(self, log):
        pass

    def serialize(self):
        src = list2str(self.srcAddr)
        dest = list2str(self.destAddr)
        

    @staticmethod
    def deserialize(frame):
        pass

if __name__ == "__main__":
    import json
    from bases import BaseCommand
    from modules.dhcp import DHCP
    
    mft = ModuleFrameTransfert([1,2,2,1], [1,2,2,1], BaseCommand.COMMAND_ALL, ["data"])
    mft.serialize()
    j = json.dumps(mft.__dict__)
    # null in json = None in python
    print(json.loads(j)["srcAddr"])
