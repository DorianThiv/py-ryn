import os
import sys
import fnmatch

from samples.exceptions import ArgumentsError, PathError
from samples.config import ConfigurationModule

if __name__ == "__main__":    

    configuration = None

    # check command
    if len(sys.argv) != 3:
        raise ArgumentsError("expected 2 arguments")
    if not os.path.isdir(sys.argv[1]):
        raise PathError("directory '{}' doesn't exist".format(sys.argv[1]))
    for name in sys.argv[1].split('/'):
        if "mdl" in name:
            configuration = ConfigurationModule.getModuleProperties(name)
    if configuration == None:
        raise PathError("path '{}' doesn't comport module".format(sys.argv[1]))    
    
    # digest names
    words = sys.argv[2].split('-')
    words = [str.lower(word) for word in words]
    low_name = "".join(words)
    upper_name = str.upper("".join(words))
    class_name = "".join([str.upper(word[0]) + word[1:len(word)] for word in words])

    # calcul paths
    files = {} # path: content
    newfiles = []
    for root, dirnames, filenames in os.walk(sys.argv[1]):
        for filename in fnmatch.filter(filenames, '*.py'):
            files[os.path.join(root, filename)] = []
    
    for path in files:
        with open(path, mode="r") as f:
            files[path] = f.readlines()
        
    for path in files:
        files[path] = [line.replace(configuration["prefix"], low_name) for line in files[path]]
        files[path] = [line.replace(configuration["class"], class_name) for line in files[path]]
        files[path] = [line.replace(configuration["upperprefix"], upper_name) for line in files[path]]

    destfiles = {}

    for path in files.keys():
        for name in path.split('/'):
            if "mdl" in name:
                destfiles[path.replace(configuration["prefix"], low_name)] = files[path] 
    
    for path in destfiles.keys():
        print("cloning : {}".format(path))

    for path in destfiles.keys():
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, mode="w+") as f:        
            for line in destfiles[path]:
                f.write(line)

    ConfigurationModule.addModule("mdl" + low_name, low_name, upper_name, class_name)
            
    
        