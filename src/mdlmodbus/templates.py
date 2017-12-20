
class ModbusFrame:

    def __init__(self, addr, func, start_addr, num_states, crc):
        self.addr = addr
        self.func = func
        self.start_addr = start_addr
        self.num_states = num_states
        self.crc = crc

    def __crc16(self, octets):
        crc = int("0xffff", 16)
        i, done = 0
        todo
        nb = len(octets)

        if (nb >= 0):
            while done < nb:
                todo = octets[done]
                crc ^= todo
                for i in range(8):
                    i+=1
                    if crc % 2 != 0:
                        crc = (crc >> 1) ^ 0xA001
                    else:
                        crc = crc >> 1
            done+=1
        return crc
