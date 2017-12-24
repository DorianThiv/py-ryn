""" 
    MODBUS protocol
    
    Modbus RTU (Remote Terminal Unit)
    Only one master.
    [START|B0|B1|B2|B3|B4|B5|B6|B7|STOP|STOP]
    [START|B0|B1|B2|B3|B4|B5|B6|B7|PARITE|STOP]
    PARITE : Pair (even) or Impair (odd)

    Modbus TCP allow the multi-masters

    CRC (Cyclical Redundancy Check) - test de refondance cyclique
    The crc is on 16 bits / 0x0000

    Proctocol PHY modbus:
        * RS-232
        * RS-485
        * RS-422
        * TCP/IP (Modbus Ethernet)

    MODBUS FRAME RTU :
        * Start : silence
        * Slave adress : 0x00
        * Code function : 0x00
        * Data : 0xn...
        * CRC : 0x0000
        * End : silence
"""
import sys
import socket
import mdlmodbus.exceptions

from mdlmodbus.templates import ModbusTCPFrame, ModbusRTUFrame, ModbusThreadRead, ModbusThreadWrite
from bases import BaseBinder

# Ayncronous modbus : TCP/IP (Modbus Ethernet)
class ModbusTcpBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        print("__init__")
        self.load()

    def load(self):
        print("load")
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(("192.168.1.16", 502))
            print("Connection on {}".format(502))
            self.write()
            self.read()
        except Exception as e:
            print("ErrorModbus : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 
            self.socket.close()

    # 01 2C 00 00 00 06 01 06 00 06 00 2B
    def read(self):
        self.thMdbR = ModbusThreadRead(self.socket, self._get_event)
        self.thMdbR.start()

    def write(self):
        data = "88 01 93 00 00 00 06 01 06 00 0A 01 64"
        self.thMdbW = ModbusThreadWrite(self.socket, data)
        self.thMdbW.start()

# Syncronous modbus : RS-485
class ModbusRtuBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self, observable):
        pass

    def read(self):
        data = "Modbus RTU Binder"
        # crc = ModbusTcpBinder.crc16(frame)
        # print(crc)
        # frame.append(str(ModbusTcpBinder.high_byte(crc)))
        # frame.append(str(ModbusTcpBinder.low_byte(crc)))
        self.observable.observers_update(data)

    def write(self):
        pass
    