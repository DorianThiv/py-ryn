
import sys

class ErrorTerminal(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "ErrorTerminal : {}".format(self.message)