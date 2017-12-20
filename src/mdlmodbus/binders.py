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

    MODBUS FRAME :
        * Start : silence
        * Slave adress : 0x00
        * Code function : 0x00
        * Data : 0xn...
        * CRC : 0x0000
        * End : silence
"""

import socket
from mdlmodbus.templates import ModbusFrame
from bases import BaseBinder

# Ayncronous modbus : TCP/IP (Modbus Ethernet)
class ModbusTcpBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self, observable):
        pass

    def read(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("192.168.1.34", 502))
            print("Connection on {}".format(502))
            s.send("010302".encode())
        except Exception as e:
            print("ErrorModbus : {}".format(e)) 
        data = "Modbus TCP Binder"
        self.observable.observers_update(data)

    def write(self):
        pass

# Syncronous modbus : RS-485
class ModbusRtuBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self, observable):
        pass

    def read(self):
        data = "Modbus RTU Binder"
        self.observable.observers_update(data)

    def write(self):
        pass
    