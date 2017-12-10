
from abc import ABCMeta, abstractmethod, abstractproperty
# SAT Object Global Object
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
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def stop(self):
        pass


# IManager
class IManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def debug(self):
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

__all__ = ('ISATObject', 'ICore', 'IManager', 'IOperator')