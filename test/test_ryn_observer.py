#!/usr/bin/env python3

###############################################
# Observable is the Registry. The Observable
# contain one or many observer (Providers).
# This observer(s) updates when data coming
# in Binder. Binder notify Registry and 
# Registry update his Providers.
#
#        Schema
#   ------------------
#   Provider(Observer)
#       |       ^
#       v       |
#   Registry(Observable)
#       |       ^
#       v       |
#     Binder(object)
###############################################

""" Observer Learning """

# Providers.py (Observer)

import time
from abc import ABCMeta, abstractmethod

class Observer(object):
    __metaclass__ = ABCMeta
 
    @abstractmethod
    def update(self, *args, **kwargs):
        pass

class ProviderAmericanStockMarket(Observer):
    def update(self, *args, **kwargs):
        print("American stock market received: {0}\n{1}".format(args, kwargs))
 
 
class ProviderEuropeanStockMarket(Observer):
    def update(self, *args, **kwargs):
        print("European stock market received: {0}\n{1}".format(args, kwargs))

# Registry.py (Observable)

class Observable(object): # Registry
 
    def __init__(self):
        self.observers = []
 
    def register(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
 
    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
 
    def unregister_all(self):
        if self.observers:
            del self.observers[:]
 
    def update_observers(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)

# Binders

class Binder(object):

    def __init__(self, registry):
        self.registry = registry

    def recv(self, sec):
        time.sleep(sec)
        self.registry.update_observers('Market Rally', something='Hello World') # update all when data is coming

# app.py
if __name__ == "__main__":

    observable = Observable()

    american_observer = ProviderAmericanStockMarket()
    observable.register(american_observer)
    european_observer = ProviderEuropeanStockMarket()
    observable.register(european_observer)

    b = Binder(observable)
    b.recv(2)





    
