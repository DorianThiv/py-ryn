
from bases import BaseProvider

class TerminalProvider(BaseProvider):

    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self):
        pass
        

    def provide(self):
        """  """
        pass

    def update(self, frame):
        """ Update to notify the manager with a frame instance """
        self.observable.observers_update(frame)