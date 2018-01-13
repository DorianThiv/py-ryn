from abc import ABCMeta, abstractmethod, abstractproperty

class ICommand:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        pass

# Create more commands :)