import sys
import os
import json

class ConfigurationModule:

    @staticmethod
    def getConfiguration(filename="config.json", callback=None):
        try:
            with open(os.path.dirname(__file__) + "/" + filename, 'r') as f:
                data = json.load(f)
            if callback != None:
                callback(data)
            else:
                return data
        except Exception as e:
            print("[ERROR - CONFIGURATION - MODULE] : {}".format(e))

    @staticmethod
    def getModulesNames(filename="config.json", callback=None):
        try:
            with open(os.path.dirname(__file__) + "/" + filename, 'r') as f:
                data = json.load(f)
            mdls = []
            for mdl in data["config"]["modules"]:
                mdls.append(mdl['name'])

            if callback != None:
                callback(mdls)
            else:
                return mdls
        except Exception as e:
            print("[ERROR - CONFIGURATION - MODULE] : {}".format(e))