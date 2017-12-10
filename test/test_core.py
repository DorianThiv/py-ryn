#! /usr/bin/env python3
# coding: utf-8

import socket, sys, threading

class Threader(threading.Thread):
    
    def __init__(self, conn):
        threading.Thread.__init__(self)

    def run(self):
        pass

class FileManager(object):

    def __init__(self):
        self.name = "File Manager"

    def __str__(self):
        return "I'm {}".format(self.name)

class MySQLManager(object):

    def __init__(self):
        self.name = "MySQL Manager"

    def __str__(self):
        return "I'm {}".format(self.name)

class ManagerFactory(object):

    def make(name):
        if name == "file-manager":
            return FileManager()
        if name == "mysql-manager":
            return MySQLManager()

class TestLoader(object):

    def __init__(self, managers):
        self.managers = {}
        for manager in managers:
            self.managers[manager] = ManagerFactory.make(manager)
    
    def __str__(self):
        ret = ""
        for manager in self.managers:
            ret += "* {}\n".format(self.managers[manager])
        return ret

class TestCore(object):

    DEFAULT_IP = "127.0.0.1"
    DEFAULT_PORT = 38660

    def __init__(self, ip=None, port=None):
        self.loaders = {}
        self.host = ip if ip != None else TestCore.DEFAULT_IP 
        self.port = port if port != None else TestCore.DEFAULT_PORT

        self.start()

    def __repr__(self):
        pass

    def __str__(self):
        return "[SERVER] : host : {}, port : {}".format(self.host, self.port)

    def start(self):
        managers = ["file-manager", "mysql-manager"]
        self.loaders["main-loader"] = TestLoader(managers)
        print(self.loaders["main-loader"])

    def pause(self):
        pass

    def stop(self):
        pass

if __name__ == "__main__":
    core = TestCore()