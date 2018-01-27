#!/usr/bin/env python3
# coding: utf-8

import os
import sys

from bases import BaseCore, BaseLoader

def main():
    """ Main method to start server """
    core = BaseCore("core")
    print("==== SAT => Initialize")
    core.start()
    print("==== SAT => Run")
    core.run()
    print("==== SAT => Stop")
    
if __name__ == "__main__":
    main()

    