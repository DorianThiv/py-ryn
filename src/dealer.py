from bases import BaseDealer

class Dealer(BaseDealer):

    def __init__(self, managers={}):
        super().__init__(managers)

    def __str__(self):
        ret = "__DEALER__ : (Echangeur)\n"
        for manager in self.managers:
            if manager != "mdlloader":
                ret += "= module : {}\n".format(self.managers[manager])
        return ret

    def update(self, frame):
        """ Notification from a module """
        self.managers[frame.receptor].reload(frame.payload)