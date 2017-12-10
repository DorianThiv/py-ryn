
from abc import ABCMeta, abstractmethod, abstractproperty

# --- SAT Object Global Interfaces
class ISATObject:
    __metaclass__ = ABCMeta

    ref = None
    name = None

    @abstractmethod
    def load(self):
        pass

# ICore
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


# IManager
class IManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def debug(self):
        pass

#IProvider
class IProvider:
    __metaclass__ = ABCMeta

    @abstractmethod
    def provide(self):
        pass

#IRegistry
class IRegistry:
    __metaclass__ = ABCMeta

    @abstractmethod
    def operate(self):
        pass

# IOperator
class IOperator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def down_operate(self):
        pass

    @abstractmethod
    def up_operate(self):
        pass

# --- Pattern Interfaces :
# IObserver
class IObserver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self):
        pass

# IObservable
class IObservable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def register(self):
        pass
    
    @abstractmethod
    def unregister(self):
        pass

    @abstractmethod
    def unregister_all(self):
        pass

    @abstractmethod
    def observers_update(self):
        pass

__all__ = ('ISATObject', 'ICore', 'IManager', 'IProvider', 'IRegistry', 'IOperator', 'IObserver')