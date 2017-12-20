from bases import BaseDealer

class Dealer(BaseDealer):

    def __init__(self, managers=[]):
        super().__init__(managers)

    def __str__(self):
        ret = "__DEALER__ : (Echangeur)\n"
        for manager in self.managers:
            if manager.name != "mdlloader":
                ret += "= module : {}\n".format(manager)
        return ret

    def update(self, frame):
        """ Notification from a module """
        for manager in self.managers:
            if frame.receptor == manager.name:
                manager.reload(frame.payload)