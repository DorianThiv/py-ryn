
import os
import sys
import inspect

from mdlmodbus.providers import *
from mdlmodbus.registries import *
from mdlmodbus.binders import *

package = "mdlmodbus"

def __getclasses():
    ret = []
    clss = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for c in clss:
        if c[1].__module__.split(".")[0] == package:
            ret.append(c[1])
    return ret

classes = __getclasses()

path = os.path.join(os.path.dirname(__file__))
sys.path.append(path)