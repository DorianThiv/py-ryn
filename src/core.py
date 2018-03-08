#!/usr/bin/env python3
# coding: utf-8

""" RYN SERVER """

__author__ = "THIVOLLE Dorian"
__copyright__ = "Copyright 2017, RYN Server"
__credits__ = ["THIVOLLE Dorian"]
__license__ = ""
__version__ = "0.01"
__maintainer__ = "THIVOLLE Dorian"
__email__ = "dorian_thivolle@orange.fr"
__status__ = "Production"

import sys

from bases import Core

def main():
    """ Main """
    try:
        core = Core("core")
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
