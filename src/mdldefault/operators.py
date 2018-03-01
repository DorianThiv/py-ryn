import sys

from bases import BaseOperator
from mdldefault.specifics.exceptions import DefaultError
from mdldefault.registries import DefaultRegistry
from mdldefault.specifics.operations import DefaultOperations

class DefaultOperator(BaseOperator):

    def __init__(self, name, provider):
        super().__init__(name, DefaultRegistry("default-operator"), DefaultOperations(), provider)

