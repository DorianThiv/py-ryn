from bases import BaseDealer

class Dealer(BaseDealer):

    def __init__(self, managers={}):
        super().__init__(managers)

    def update(self, frame):
        """ Notification from a module """
        self.managers[frame.receptor].reload(frame)