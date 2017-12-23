
from util import bytes2int

INITIAL_MODBUS = 0xFFFF
INITIAL_POLY = 0xA001

class MBAPHeader:

    def __init__(self, num_trans=0x0000, proto=0x0000, lendata1=0x00, lendata2=0x00):
        self.num_trans = num_trans
        self.proto = proto
        self.lendata1 = lendata1
        self.lendata2 = lendata2

class ModbusTCPFrame:

    def __init__(self, saddress, function, data):
        self.header = MBAPHeader(lendata2=0x06)
        self.slave_address = saddress
        self.function = function
        self.payload = data

    def serialize(self):
        pass

    def deserialize(self):
        pass

class ModbusRTUFrame:

    def __init__(self):
        pass

    def __crc16(self, frame=[]):
        crc = INITIAL_MODBUS 
        poly = INITIAL_POLY
        for b in frame:
            crc ^= bytes2int(b)
            for i in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= poly
                else:
                    crc = crc >> 1 
        swap = ((crc << 8) & 0xff00) | ((crc >> 8) & 0x00ff)
        return swap
