
import os
import sys
import inspect

from mdlmodbus.providers import *
from mdlmodbus.registries import *
from mdlmodbus.binders import *

packages = ["mdlmodbus.providers", "mdlmodbus.registries", "mdlmodbus.binders"]

def __getclasses():
    ret = []
    clss = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for c in clss:
        for package in packages:
            if c[1].__module__ == package:
                ret.append(c[1])
    return ret

classes = __getclasses()

path = os.path.join(os.path.dirname(__file__))
sys.path.append(path)