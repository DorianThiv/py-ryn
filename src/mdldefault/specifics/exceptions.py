
import sys

class DefaultError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}".format(self.message)