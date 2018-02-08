"""Fichier d'installation de notre script salut.py."""

from cx_Freeze import setup, Executable

SRC_DIR = "./src/"

exe = Executable(
    script="./src/core.py",
    targetName="ryn-server"
)

setup(
    name = "ryn-server",
    version = "0.020818",
    author = "THIVOLLE Dorian",
    description = "Server Protoype",
    executables = [exe]
)
