#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import threading

from bases import BaseCore
from loader import Loader

class Core(BaseCore):

    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        pass

    def load(self):
        pass

    def start(self):
        managers = ["mdlconf"]
        self.loader = Loader("mdlloader")
        self.loader.load(managers)

    def pause(self):
        pass

    def stop(self):
        pass

def main():
    """ Main method to start server """
    core = Core("core")
    th = threading.Thread(target=core.start())
    th.start()
    th.join()
    print("Stop")

if __name__ == "__main__":
    main()
    print("Stop")
    