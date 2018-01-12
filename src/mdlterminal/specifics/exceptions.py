
import sys
from bases import BaseDealer

class ErrorTerminal(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}".format(self.message)

class ErrorTerminalClientDisconnect(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "{}".format(self.message)

class WarningTerminalWrongRequestModule(Exception):

    """
        WarningTerminalWrongRequestModule : 
        Modules commands usage :
    """

    def __init__(self, msg, module):
        self.module = module
        self.message = msg

    def __mdlexemple(self):
        """
        Exemple Command:
            * [mdlexemple] -[(r|w)] {-t blah blah}
                - r | w : read | write
                - t : text
        """

    def __mdlconf(self):
        """
        Configuration Command:
            * [mdlconf] -[(r|w)] {-t blah blah}
                - r | w : read | write
                - t : text
        """

    def __mdlmodbus(self):
        """
        Modbus Command:
            * [mdlmodbus] -[(r|w)] -[(tcp|rtu)] {[-d 0 -r 0 -v 0]}
                - tcp : TCP connection on modbus
                - rtu : RTU connection on modbus
                - r | w : read | write
                - d : device address
                - r : register address 
                - v : value of register
        """

    def __mdlunknown(self):
        """
        Unknown module :
        Available modules : 
        """

    def __str__(self):
        if self.module == "mdlexemple":
            return "{}\n{}{}".format(self.message, self.__doc__, self.__mdlexemple.__doc__)
        elif self.module == "mdlconf":
            return "{}\n{}{}".format(self.message, self.__doc__, self.__mdlconf.__doc__)
        elif self.module == "mdlmodbus":
            return "{}\n{}{}".format(self.message, self.__doc__, self.__mdlmodbus.__doc__)
        else:
            mods = "\t"
            for name in BaseDealer.CONNECTED_MANAGERS:
                mods += "* " + name + "\n\t"
            return "{}\n{}{}".format(self.message, self.__doc__, mods)