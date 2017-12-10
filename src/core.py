#! /usr/bin/env python3
# coding: utf-8

import os
import sys

import interfaces

from interfaces import ICore
from loader import Loader

class Core(ICore):

    def __init__(self):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        return "[SERVER]"

    def start(self):
        managers = ["mdlcmd", "mdltest"]
        self.loader = Loader(managers)
        print(self.loader)

    def pause(self):
        pass

    def stop(self):
        pass

def main():
    core = Core()
    core.start()

if __name__ == "__main__":
    main()