"""Fichier d'installation de notre script salut.py."""

from cx_Freeze import setup, Executable

setup(
    name = "RYN-SRV",
    version = "0.1",
    description = "Server Protoype",
    executables = [Executable("core.py")],
)