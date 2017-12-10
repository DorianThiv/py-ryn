
from interfaces import *

class BaseCore(ISATObject, ICore):
    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def __repr__(self):
        pass

    def __str__(self):
        return "__BASECORE__"

    def load(self):
        pass

    def start(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

class BaseManager(ISATObject, IManager):
    
    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def load(self):
        pass

    def debug(self):
        pass

class BaseProvider(ISATObject, IProvider, IObserver):
    
    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def load(self):
        pass

    def provide(self):
        pass

    def update(self):
        pass