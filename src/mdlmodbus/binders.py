
import sys
import socket
import mdlmodbus.exceptions

from mdlmodbus.templates import ModbusTCPFrame, ModbusRTUFrame, ModbusThreadRead, ModbusThreadWrite
from bases import BaseBinder

# Ayncronous modbus : TCP/IP (Modbus Ethernet) 
class ModbusTcpBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Modbus connection at : {} on port {} ...".format("192.168.1.17", 502))
            self.socket.connect(("192.168.1.17", 502))
            print("[SUCCES] : Modbus connection on port {}".format(502))
        except Exception as e:
            print("ErrorModbus : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 
            self.socket.close()

    def action(self):
        self.read()
        self.write()

    def read(self):
        self.thMdbR = ModbusThreadRead(self.socket, self._get_event)
        self.thMdbR.start()

    def write(self):
        data = [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0x0B, 0x07, 0x9A]
        self.thMdbW = ModbusThreadWrite(self.socket, data)
        self.thMdbW.start()

# Syncronous modbus : RS-485
class ModbusRtuBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self):
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
    