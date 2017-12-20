
import os
import sys
import inspect

from mdlconf.providers import *
from mdlconf.registries import *
from mdlconf.binders import *

packages = ["mdlconf.providers", "mdlconf.registries", "mdlconf.binders"]

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