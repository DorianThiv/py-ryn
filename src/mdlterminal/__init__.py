
# -*- coding: utf-8 -*-
"""Example Python style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python core.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

""" imports """

import os
import sys
import inspect

from mdlterminal.providers import *
from mdlterminal.registries import *
from mdlterminal.binders import *

""" Modules loaded """

# package name important to found right classes
packages = ["mdlterminal.providers", "mdlterminal.registries", "mdlterminal.binders"]


def __getclasses():

    """
    Get classes function return all classes in this module.
    Args:
        * No params
    Returns:
        list: array with few classes founded in modules : [providers, registries, binders]
    """
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