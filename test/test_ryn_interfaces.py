#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod

class Imanager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def loadProviders(self):
        pass
    
    @abstractmethod
    def loadRegistry(self):
        pass

class FileManager(Imanager):

    def __init__(self):
        pass

    def loadProviders(self):
        print("Load Providers")

    def loadRegistry(self):
        print("Load Registry")

if __name__ == "__main__":
    fm = FileManager()
    fm.loadProviders()
    fm.loadRegistry()
