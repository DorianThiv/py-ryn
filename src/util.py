

def bytes2int(bts):
    result = 0
    for b in bts:
        result = result * 256 + int(b)
    return result

def low_byte(u):
    return (u & 0x00FF)

def high_byte(u):
    return (u >> 8)

def list2str(l):
    ret = ""
    for o in l:
        ret += o
    return ret