import sys
import os
import json

class ConfigurationModule:

    CONFIG_FILE = "files/config.json"

    @staticmethod
    def addModule(mdlname, lower_name, upper_name, class_name, callback=None):
        try:
            with open(os.path.dirname(__file__) + "/" + ConfigurationModule.CONFIG_FILE, 'r') as f:
                data = json.load(f)
            name = str.lower(mdlname.replace("mdl", ""))
            data["config"]["modules"].append({
                "name": mdlname,
                "prefix": lower_name,
                "upperprefix": upper_name,
                "class": class_name,
                "usage": "no usage"
            })
            with open(os.path.dirname(__file__) + "/" + ConfigurationModule.CONFIG_FILE, 'w') as f:
                json.dump(data, f, sort_keys=True, indent=4)
        except Exception as e:
            print("[ERROR - CONFIGURATION - MODULE] : {}".format(e))

    @staticmethod
    def saveStructureModule(module, callback=None):
        """ Save a structure of a module and reload it at the begining """
        try:
            print(module.__dict__)
            with open(os.path.dirname(__file__) + "/" + ConfigurationModule.CONFIG_FILE, 'r') as f:
                data = json.load(f)
            data["structure"]["modules"].append({ module.__dict__ })
            # with open(os.path.dirname(__file__) + "/" + ConfigurationModule.CONFIG_FILE, 'w') as f:
                # json.dump(data, f, sort_keys=True, indent=4)
        except Exception as e:
            print("[ERROR - CONFIGURATION - MODULE] : {}".format(e))

    @staticmethod
    def removeModule(mdlname, callback=None):
        try:
            with open(os.path.dirname(__file__) + "/" + ConfigurationModule.CONFIG_FILE, 'r') as f:
                data = json.load(f)
            for mdl in data["config"]["modules"]:
                if mdlname == mdl["name"]:
                    data["config"]["modules"].remove(mdl)
            with open(os.path.dirname(__file__) + "/" + ConfigurationModule.CONFIG_FILE, 'w') as f:
                json.dump(data, f, sort_keys=True, indent=4)
        except Exception as e:
            print("[ERROR - CONFIGURATION - MODULE] : {}".format(e))

    @staticmethod
    def getConfiguration(callback=None):
        try:
            with open(os.path.dirname(__file__) + "/" + ConfigurationModule.CONFIG_FILE, 'r') as f:
                data = json.load(f)
            if callback != None:
                callback(data)
            else:
                return data
        except Exception as e:
            print("[ERROR - CONFIGURATION - MODULE] : {}".format(e))

    @staticmethod
    def getModulesNames(callback=None):
        try:
            with open(os.path.dirname(__file__) + "/" + ConfigurationModule.CONFIG_FILE, 'r') as f:
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
            
    @staticmethod
    def getModuleProperties(mdlname, callback=None):
        try:
            with open(os.path.dirname(__file__) + "/" + ConfigurationModule.CONFIG_FILE, 'r') as f:
                data = json.load(f)
            props = None
            for mdl in data["config"]["modules"]:
                if mdl["name"] == mdlname:
                    props = mdl
            if callback != None:
                callback(props)
            else:
                return props
        except Exception as e:
            print("[ERROR - CONFIGURATION - MODULE] : {}".format(e))
    
if __name__ == "__main__":
    pass
