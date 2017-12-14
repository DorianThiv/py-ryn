#! /usr/bin/env python3
# coding: utf-8

import os
import sys

from bases import BaseCore
from loader import Loader

class Core(BaseCore):

    def __init__(self, ref, name):
        super().__init__(ref, name)

    def __repr__(self):
        pass

    def __str__(self):
        return "__CORE__ = (ref : {}, name : {})".format(self.ref, self.name)

    def load(self):
        pass

    def start(self):
        managers = ["mdlcmd", "mdlconf"]
        self.loader = Loader("000-412", "loader")
        self.loader.load(managers)
        print(self)
        print(self.loader)

    def pause(self):
        pass

    def stop(self):
        pass

def main():
    core = Core("000-012", "core")
    core.start()

if __name__ == "__main__":
    main()