
import os
import sys
import inspect

from mdlexemple.providers import *
from mdlexemple.registries import *
from mdlexemple.binders import *

package = "mdlexemple"

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