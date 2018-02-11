"""Fichier d'installation de notre script salut.py."""

import os

# from distutils.core import setup
# import py2exe

from cx_Freeze import setup, Executable

SRC_DIR = "./src/"

packages = []

print(os.getcwd())

for root, dirnames, filenames in os.walk(SRC_DIR):
    for name in dirnames:
        if "mdl" in name:
            packages.append(name)

exe = Executable(
    script="./src/core.py",
    targetName="ryn-server",
)

setup(
    name = "ryn-server",
    version = "0.020818",
    author = "THIVOLLE Dorian",
    description = "Server Protoype",
    options = {"build_exe" : {"packages" : packages}},
    executables = [exe]
)

# setup(console=['src/core.py'])