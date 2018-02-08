from abc import ABCMeta, abstractmethod, abstractproperty

""" Maybe use this pattern and chain of resp to send
    Data on modbus or other devices.
"""

class Light:

    def __init__(self):
        self.switch = False

    def turnOn(self):
        self.switch = True
    
    def turnOff(self):
        self.switch = False

class ICommand:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        pass

class LightCommand(ICommand):

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turnOn()

light = Light()
print(light.switch)
command = LightCommand(light)
command.execute()
print(light.switch)