
class ErrorLoadModule(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "ErrorLoadModule : {}".format(self.message)