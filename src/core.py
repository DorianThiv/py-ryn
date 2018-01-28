#!/usr/bin/env python3
# coding: utf-8

""" RYN SOFTWARE """

import os
from bases import BaseCore

def main():
    core = BaseCore("core")
    print("==== RYN => Initialize")
    core.start()
    print("==== RYN => Run")
    core.run()
    print("==== RYN => Stopped")
    
if __name__ == "__main__":
    main()

    