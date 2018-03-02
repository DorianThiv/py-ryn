import sys

from bases import BaseOperator
from mdldefault.specifics.operations import DefaultOperations

class DefaultOperator(BaseOperator):

    def __init__(self, parent):
        super().__init__(DefaultOperations(), parent)

