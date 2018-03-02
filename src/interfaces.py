
""" Find interfaces of this prototype """

from abc import ABCMeta, abstractmethod, abstractproperty

class IObservable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def emit(self):
        pass

class ISaveable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self):
        pass
    
    @abstractmethod
    def edit(self):
        pass
    
    @abstractmethod
    def remove(self):
        pass   

class IManageable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self):
        pass
    
    @abstractmethod
    def edit(self):
        pass
    
    @abstractmethod
    def remove(self):
        pass    

class IExecutable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        pass

__all__ = ('IRYNObject', 'ICore', 'IManager', 'IProvider', 'IRegistry', 'IOperator', 'IObserver', 'IObservable', 'ICommand')
