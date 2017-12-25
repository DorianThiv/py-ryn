
from bases import BaseRegistry

from mdlexemple.operators import ExempleOperator

class ExempleRegistry(BaseRegistry):

    def __init__(self, name):
        super().__init__(name, ExempleOperator("exemple-operator"))

    def load(self, providers):
        for provider in providers:
            self.observers.append(provider)
