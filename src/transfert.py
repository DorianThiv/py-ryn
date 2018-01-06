

class FrameEncoder:
    pass

class FrameDecoder:
    pass

class SimpleFrameTransfert:

    """ This frame define the internal tranfert protocole
        
        Data Types : 
        * Emitter : (id) ""
        * Receptor : (id) ""
        * Direction : (read | write) ""
        * Payload : (json) ""
        * Timestamp : (tmestamp) ""
        * Crc : (string) "" 
    """

    def __init__(self, sort=0, direction=None, payload=None):
        self.sort = sort
        self.direction = direction
        self.payload = payload

    def __str__(self):
        return "__FRAME__ = (|em : {} | dir: {} | payload : {})".format(self.sort, self.direction, self.payload)

class ModuleFrameTransfert:

    """ This frame define the internal tranfert protocole
        
        Data Types : 
        * Emitter : (id) ""
        * Receptor : (id) ""
        * Direction : (read | write) ""
        * Payload : (json) ""
        * Timestamp : (tmestamp) ""
        * Crc : (string) "" 
    """

    def __init__(self, emitter=None, receiver=None, direction=None, payload=None, timestamp=None, crc=None):
        self.emitter = emitter
        self.receiver = receiver
        self.direction = direction
        self.payload = payload
        self.timestamp = timestamp
        self.crc = crc

    def __str__(self):
        return "__FRAME__ = (|em : {} | re : {} | dir: {} | payload : {} | timestamp : {} | crc : {}|)".format(self.emitter, self.receiver, self.direction, self.payload, self.timestamp, self.crc)

