# IManager

from abc import ABCMeta, abstractmethod

class IManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def debug(self):
        pass