
from bases import BaseRegistry

from mdlexemple.operators import ExempleOperator

class ExempleRegistry(BaseRegistry):

    def __init__(self, name, provider):
        super().__init__(name, ExempleOperator("exemple-operator"), provider)
