#!/usr/bin/env python3

import os
import sys
import time
import datetime

class Logger:

    PATH = os.path.dirname(sys.modules['__main__'].__file__) + "/mdlutils/"
    DIRECTORY = "files/"
    NAME = "ryn"
    EXT = ".log"

    FULL_PATH = PATH + DIRECTORY + NAME + EXT

    INSTANCE = None

    SUCCESS = 3
    INFO = 2
    WARNING = 1
    ERROR = 0
    CRITICAL = -1

    SUCCESS_MSG = "[SUCCESS - LOGGER]: "
    INFO_MSG = "[INFO - LOGGER]: "
    WARNING_MSG = "[WARNING - LOGGER]: "
    ERROR_MSG = "[ERROR - LOGGER]: "
    CRITICAL_MSG = "[CRITICAL - LOGGER]: "

    def __init__(self):
        if not os.path.exists(Logger.PATH + Logger.DIRECTORY):
            os.makedirs(Logger.PATH + Logger.DIRECTORY)
        if not os.path.exists(Logger.PATH + Logger.DIRECTORY + Logger.NAME + Logger.EXT):
            os.mknod(Logger.PATH + Logger.DIRECTORY + Logger.NAME + Logger.EXT)

    @staticmethod
    def getInstance():
        if Logger.INSTANCE == None:
            return Logger()
        else:
            return Logger.INSTANCE
    
    def log(self, level, msg):
        _log = None
        _file = open(Logger.FULL_PATH, "a")
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        if level == Logger.SUCCESS:
            _log = "{} [{}] : {}\n".format(Logger.SUCCESS_MSG, timestamp, msg)
        elif level == Logger.INFO:
            _log = "{} [{}] : {}\n".format(Logger.INFO_MSG, timestamp, msg)
        elif level == Logger.ERROR:
            _log = "{} [{}] : {}\n".format(Logger.ERROR_MSG, timestamp, msg)
        elif level == Logger.WARNING:
            _log = "{} [{}] : {}\n".format(Logger.WARNING_MSG, timestamp, msg)
        elif level == Logger.CRITICAL:
            _log = "{} [{}] : {}\n".format(Logger.CRITICAL_MSG, timestamp, msg)
        else:
            pass
        if _log != None:
            _file.write(_log)
            _file.close()
    
    def clear(self):
        open(Logger.FULL_PATH, "w").close()
