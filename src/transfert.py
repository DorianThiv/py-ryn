

class FrameEncoder:
    pass

class FrameDecoder:
    pass

class FrameTransfert:

    """ 
        This frame define the internal tranfert protocole
        
        Data Types : 
        * Emitter : (id) ""
        * Receptor : (id) ""
        * Action : (read | write) ""
        * Payload : (json) ""
        * Timestamp : (tmestamp) ""
        * Crc : (string) "" 
    """

    def __init__(self, emitter=None, receiver=None, action=None, payload=None, timestamp=None, crc=None):
        self.emitter = emitter
        self.receiver = receiver
        self.action = action
        self.payload = payload
        self.timestamp = timestamp
        self.crc = crc

    def __str__(self):
        return "__FRAME__ = (|em : {} | re : {} | act: {} | payload : {} | timestamp : {} | crc : {}|)".format(self.emitter, self.receiver, self.action, self.payload, self.timestamp, self.crc)
