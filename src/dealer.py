from bases import BaseDealer

class Dealer(BaseDealer):

    def __init__(self, managers={}):
        super().__init__(managers)

    def __str__(self):
        ret = "__DEALER__ : (Echangeur)\n"
        for manager in self.managers:
            ret += "= module : {}\n".format(self.managers[manager])
        return ret

    def add(self, manager):
        """ Add a module module in the managers dict """
        super().add(manager)

    def remove(self, mname):
        """ Remove a module module from the managers dict """
        pass

    def find(self):
        """ Find another module to send the received frame """
        pass

    def update(self, frame):
        """ Notification from a module """
        print("{}".format(frame))