# SAT Object Global Object

from abc import ABCMeta, abstractmethod, abstractproperty

class ISATObject:
    __metaclass__ = ABCMeta

    @abstractproperty
    def id(self):
        pass

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def ref(self):
        pass

    @abstractmethod
    def load(self):
        pass