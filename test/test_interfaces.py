#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod

class Imanager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def loadProviders(self):
        print("Load Providers")
    
    @abstractmethod
    def loadRegistry(self):
        print("Load Registry")

class FileManager(Imanager):

    def __init__(self):
        pass

if __name__ == "__main__":
    fm = FileManager()
    fm.loadProviders()
    fm.loadRegistry()
