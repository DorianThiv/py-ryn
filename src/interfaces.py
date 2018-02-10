
""" Find interfaces of this prototype """

from abc import ABCMeta, abstractmethod, abstractproperty

class IRYNObject:
    __metaclass__ = ABCMeta

    ref = 0 # 00000000 - FFFFFFFFF
    name = None

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def load(self):
        pass
        
    @abstractmethod
    def uninitialize(self):
        pass

class ICore:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """ Start the core """ 
        pass

    @abstractmethod
    def run(self):
        """ Run the core """ 
        pass

    @abstractmethod
    def pause(self):
        """ Pause the core """ 
        pass

    @abstractmethod
    def stop(self):
        """ Stop the core """ 
        pass

class ILoader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def reload(self):
        """ Reload Managers """ 
        pass

class IDirectory:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, manager):
        """ Add Managers """ 
        pass

    @abstractmethod
    def remove(self, mdladdr):
        """ Remove Manager """ 
        pass

    @abstractmethod
    def find(self, mdladdr):
        """ Find a manager in manager dict """ 
        pass

class IDealer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, manager):
        """ Add Manager """ 
        pass

    @abstractmethod
    def remove(self, mname):
        """ Remove Manager """ 
        pass

class IManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def command(self, command):
        pass

class IProvider:
    __metaclass__ = ABCMeta

    @abstractmethod
    def provide(self):
        pass

class IRegistry:
    __metaclass__ = ABCMeta

    @abstractmethod
    def subscribe(self, name):
        pass

    @abstractmethod
    def unsubscribe(self, name):
        pass

class IOperator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def encapsulate(self, data):
        pass

    @abstractmethod
    def decapsulate(self, frame):
        pass

class IBinder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass
    
class IObserver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self):
        pass

class IObservable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def register(self, observer):
        pass
    
    @abstractmethod
    def unregister(self, observer):
        pass

    @abstractmethod
    def unregister_all(self):
        pass

    @abstractmethod
    def emit(self):
        pass

class ICommand:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        pass

__all__ = ('IRYNObject', 'ICore', 'IManager', 'IProvider', 'IRegistry', 'IOperator', 'IObserver', 'IObservable', 'ICommand')
