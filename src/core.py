#!/usr/bin/env python3
# coding: utf-8

import os
import sys

from bases import BaseCore

from loader import Loader

class Core(BaseCore):

    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        pass

    def __str__(self):
        return "__CORE__ = (name : {}".format(self.name)

    def load(self):
        pass

    def start(self):
        managers = ["mdlconf"]
        self.loader = Loader("loader")
        self.loader.load(managers)
        print(self)
        print(self.loader)

    def pause(self):
        pass

    def stop(self):
        pass

def main():
    core = Core("core")
    core.start()

if __name__ == "__main__":
    main()