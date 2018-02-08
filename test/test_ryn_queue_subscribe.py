#!/usr/bin/env python 3

import queue

class Registry:

    def __init__(self):
        self.directory = {}
    
    def subscribe(self, name, command):
        if name in list(self.directory.keys()):
            self.directory[name].put(command)
        else:
            self.directory[name] = queue.Queue()
            self.directory[name].put(command)

    def unsubscribe(self):
        pass

    def __str__(self):
        ret = ""
        for c in self.directory:
            ret += c + "\n"
        return ret
    
if __name__ == "__main__":
    
    reg = Registry()
    reg.subscribe("mdldb", "write")
    reg.subscribe("mdldb", "read")
    reg.subscribe("mdlmodbus", "read")
    print(reg)