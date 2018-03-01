#!/usr/bin/env python3
# coding: utf-8

""" RYN SOFTWARE """

import sys

from bases import BaseCore

def main():
    """ Main """
    try:
        core = BaseCore("core")
        print("==== RYN => Initialize")
        core.start()
        print("==== RYN => Run")
        core.run()
        print("==== RYN => Stopped")
    except KeyboardInterrupt:
        print("[CORE] : KeyboardInterrupt")
        sys.exit()

if __name__ == "__main__":
    main()
