
import os
import sys
import inspect

from mdlconf.managers import *
from mdlconf.providers import *
from mdlconf.registries import *
from mdlconf.binders import *

path = os.path.join(os.path.dirname(__file__))
sys.path.append(path)

mdlmanager = "mdlconf.managers"

packages = ["mdlconf.providers", "mdlconf.registries", "mdlconf.binders"]

def __getmanager():
    """
    Get Manager classes in this module.
    Args:
        * No params
    Returns:
        list: array with few classes founded in modules : [managers]
    """
    clss = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for c in clss:
        if c[1].__module__ == mdlmanager:
                ret = c[1]
    return ret

def __getclasses():
    ret = []
    clss = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for c in clss:
        for package in packages:
            if c[1].__module__ == package:
                ret.append(c[1])
    return ret

classes = __getclasses()
manager = __getmanager()