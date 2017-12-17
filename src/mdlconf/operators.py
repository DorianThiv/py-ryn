
import datetime
import time
from bases import BaseOperator
from transfert import FrameTransfert

class ConfigurationOperator(BaseOperator):
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "__CONFIGOPERATOR__ = (name : {})".format(self.name)

    def load(self):
        pass

    def encapsulate(self, data):
        ts = time.time()
        return FrameTransfert("mdlconf", "mdl???", "read", data, datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), "crc")

    def decapsulate(self, frame):
        pass