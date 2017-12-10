# IManager

from abc import ABCMeta, abstractmethod

class IOperator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def down_operate(self):
        pass

    @abstractmethod
    def up_operate(self):
        pass