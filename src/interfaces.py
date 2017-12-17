
from abc import ABCMeta, abstractmethod, abstractproperty

# --- SAT Object Global Interfaces
class ISATObject:
    __metaclass__ = ABCMeta

    name = None

    @abstractmethod
    def load(self):
        pass

class ICore:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """ Start the core """ 
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

    @abstractmethod
    def find(self, mname):
        """ Find a manager in manager dict """ 
        pass

class IManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def _reading_all(self):
        pass

class IProvider:
    __metaclass__ = ABCMeta

    @abstractmethod
    def provide(self):
        pass

class IRegistry:
    __metaclass__ = ABCMeta

    @abstractmethod
    def operate(self, data):
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
    def observers_update(self):
        pass

__all__ = ('ISATObject', 'ICore', 'IManager', 'IProvider', 'IRegistry', 'IOperator', 'IObserver')
