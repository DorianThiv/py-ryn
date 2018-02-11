import sys
import os

from mdlutils.exceptions import ArgumentsError, PathError
from mdlutils.config import ConfigurationModule

if len(sys.argv) != 2:
    raise ArgumentsError("expected 1 arguments")
if not os.path.isdir(sys.argv[1]):
    raise PathError("directory '{}' doesn't exist".format(sys.argv[1]))

print("[?] Are you sure to remove '{}'".format(sys.argv[1]))
rep = input("(y or n) : ")
rep = str.lower(rep)
if rep == "n" or rep == "no":
    sys.exit()
elif rep == "y" or rep == "yes":
    for root, dirs, files in os.walk(sys.argv[1], topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    for name in sys.argv[1].split('/'):
        if "mdl" in name:
            ConfigurationModule.removeModule(name)
    os.rmdir(sys.argv[1])
else:
    print("[x] Sorry i don't understand your answer.")


