#! /usr/bin/env python3

""" JSON Serialize an Deserialize """
import json

class JSONSerializeFormatError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "JSONSerializeFormatError : {}".format(self.message)

class JSON:

    @staticmethod
    def serialize(data):
        """ Take params list to transform in type string """
        if not isinstance(data, list) and not isinstance(data, dict):
            raise JSONSerializeFormatError("Type is not list")
        return json.dumps(data)

    @staticmethod
    def deserialize(data):
        """ Take params string to transform in type list """
        if not isinstance(data, str):
            raise JSONSerializeFormatError("Type is not string")
        return json.loads(data)

""" Utils functions for byte calculation """

def bytes2int(bts):
    result = 0
    for b in bts:
        result = result * 256 + int(b)
    return result

def lobyte(u):
    return (u & 0x00FF)

def hibyte(u):
    return (u >> 8)

""" Utils functions for basic formats """

def list2str(l, sep=""):
    ret = ""
    for o in l:
        ret += str(o) + sep
    if sep != "":
        return ret[0:len(ret)-1]
    else:
        return ret

""" Utils function to automatise module loading """

def class_name_gen(minprefix, classname):
        import re
        ret = minprefix + "-"
        fracts = (lambda ns: re.findall("[A-Z][^A-Z]*", ns))(classname.__name__)
        for w in fracts[1:len(fracts)]: ret += w.lower() + "-"
        return ret[0:len(ret)-1]
