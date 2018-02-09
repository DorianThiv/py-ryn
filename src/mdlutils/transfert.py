
from mdlutils.utils import JSON

class ModuleFrameTransfert:

    """ ModuleFrameTransfert
    
    Transfert format frame to ask a module with differents params.
    
    Serialize @param : frame to SimpleFrameTransfert :
    [src] => (int | str)
    [dest] => (int | str) 
    [command] => BaseCommand (actually)
    [payload] => Content known buy dest module
    [callback] => Optionnal
    [log] => class Logger (message, exception, timestamp)   
    
    """
    
    """ Define names for serialize and deserialize """

    SRC = "source"
    DEST = "destination"
    COMMAND = "command"
    PAYLOAD = "payload"
    CALLBACK = "callback"
    LOG = "log"

    def __init__(self, src, dest, command=None, payload=None, callback=None, log=None):
        self.src = src
        self.dest = dest
        self.command = command
        self.payload = payload
        self.callback = callback
        self.log = log

    def __str__(self):
        return "__MODULE_FRAME__ = (src : {}, dest : {}, command: {}, payload : {}, callback : {}, log : {})".format(self.src, self.dest, self.command, self.payload, self.callback, self.log)

    def serialize(self):
        try:
            frame = {}
            frame[ModuleFrameTransfert.SRC] = self.src
            frame[ModuleFrameTransfert.DEST] = self.dest
            frame[ModuleFrameTransfert.COMMAND] = self.command
            frame[ModuleFrameTransfert.PAYLOAD] = self.payload
            frame[ModuleFrameTransfert.CALLBACK] = self.callback
            frame[ModuleFrameTransfert.LOG] = self.log
            return JSON.serialize(frame)
        except Exception as e:
            print(e)

    @staticmethod
    def deserialize(f_frame):
        try:
            frame = JSON.deserialize(f_frame)
            return ModuleFrameTransfert(frame[ModuleFrameTransfert.SRC], frame[ModuleFrameTransfert.DEST], frame[ModuleFrameTransfert.COMMAND], frame[ModuleFrameTransfert.PAYLOAD], frame[ModuleFrameTransfert.CALLBACK], frame[ModuleFrameTransfert.LOG])
        except Exception as e:
            print(e)
    
class SimpleFrameTransfert:

    """ Serialize @param : frame to SimpleFrameTransfert :
        [Command] => BaseCommand (actually )
        [Callback] => Optionnal
        [Log] => class Logger (message, exception, comments) ???   
    """

    def __init__(self, command, callback=None, log=None):
        self.command = command
        self.callback = callback
        self.log = log

    def __str__(self):
        return "__SIMPLE_FRAME__ = (|command : {} | callback : {} | log : {})".format(self.command, self.callback, self.log)

    @staticmethod
    def serialize(frame):
        pass

    @staticmethod
    def deserialize(frame):
        pass
