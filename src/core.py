#!/usr/bin/env python3
# coding: utf-8

from bases import BaseCore

def main():
    """ Main method to start server """
    core = BaseCore("core")
    print("==== SAT => Initialize")
    core.start()
    print("==== SAT => Run")
    core.run()
    print("==== SAT => Stopped")
    
if __name__ == "__main__":
    main()
    