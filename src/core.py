#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import threading

from bases import BaseCore, BaseLoader

def main():
    """ Main method to start server """
    managers = ["mdlconf"]
    core = BaseCore("core")
    core.start(BaseLoader("mdlloader", core, managers))
    core.run()
    print("[PROCESS - TERMINATED] : Core stopped.")

if __name__ == "__main__":
    main()

    