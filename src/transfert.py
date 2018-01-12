
import datetime
import time
from utils import list2str, JSON

class SimpleFrameTransfert:

    """ Serialize @param : frame to SimpleFrameTransfert :
        [Command] => BaseCommand (actually )
        [Callback] => Optionnal
        [Log] => class Logger (message, exception, comments) ???   
    """

    def __init__(self, command, callback=None, log=None):
        ts = time.time()
        self.command = command
        self.callback = callback
        self.timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.log = log

    def __str__(self):
        return "__SIMPLE_FRAME__ = (|command : {} | callback : {} | timestamp : {} | log : {})".format(self.command, self.callback, self.timestamp, self.log)

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

    def __init__(self, srcAddr=[], destAddr=[], command=None, payload=None, callback=None, timestamp=None, log=None):
        ts = time.time()
        self.srcAddr = srcAddr
        self.destAddr = destAddr
        self.command = command
        self.payload = payload
        self.callback = callback
        self.timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.log = log

    def __str__(self):
        return "__MODULE_FRAME__ = (|src : {} | dest : {} | command: {} | payload : {} | callback : {} | timestamp : {} | log : {}|)".format(self.srcAddr, self.destAddr, self.command, self.payload, self.callback, self.timestamp, self.log)

    def addToSrcAddr(self, _id):
        if len(self.srcAddr) != 4:
            self.srcAddr.append(_id)
    
    def addToDestAddr(self, _id):
        if len(self.destAddr) != 4:
            self.destAddr.append(_id)

    def serialize(self):
        try:
            frame = {}
            frame["srcAddr"] = list2str(self.srcAddr, ".")
            frame["destAddr"] = list2str(self.destAddr, ".")
            frame["command"] = self.command
            frame["payload"] = self.payload
            frame["callback"] = self.callback
            frame["timestamp"] = self.timestamp
            frame["log"] = self.log
            return JSON.serialize(frame)
        except Exception as e:
            print(e)

    @staticmethod
    def deserialize(f_frame):
        try:
            frame = JSON.deserialize(f_frame)
            src = frame["srcAddr"].split(".")
            dest = frame["destAddr"].split(".")
            return ModuleFrameTransfert(src, dest, frame["command"], frame["payload"], frame["callback"], frame["timestamp"], frame["log"])
        except Exception as e:
            print(e)

if __name__ == "__main__":
    from bases import BaseCommand
    mft = ModuleFrameTransfert([1,2,2,1], [1,2,2,1], BaseCommand.COMMAND_ALL, [{"data": [{"choin": "hello", "choc": "olat"}]}])
    f_mft = mft.serialize()
    print(f_mft)
    d_mft = ModuleFrameTransfert.deserialize(f_mft)
    print(d_mft)
