
from bases import BaseProvider

class ModbusProvider(BaseProvider):

    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def load(self):
        pass
        

    def provide(self):
        """  """
        pass

    def update(self, frame):
        """ Update to notify the manager with a frame instance 
            The provider will apply a new operation and provide 
            functionality at the frame level. 
        """
        self.observable.observers_update(frame)