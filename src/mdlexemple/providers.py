
from bases import BaseProvider

class ExempleProvider(BaseProvider):
    """
        Provider component have an observable :
        This observable is a Manager. 
        The provider can provide a specific type of data.
        For exemple : 
            * I/O Text File
            * I/O XML File 
            There are two differents treatment but it the 
            same process.
        The choise of the right provider will be transparent
        for the user. With a simple terminal command it be able
        to choise the appropriate provider.
    """

    def __init__(self, name, observable=None):
        super().__init__(name, observable)