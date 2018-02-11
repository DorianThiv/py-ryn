import os
import sys
import fnmatch

print(sys.argv[0])
print(sys.argv[1])
print(sys.argv[2])

files = []
for root, dirnames, filenames in os.walk('test/mdlterminal/'):
    for filename in fnmatch.filter(filenames, '*.py'):
        files.append(os.path.join(root, filename))

for path in files:
    strings = []
    with open(path, mode="r") as f:
        strings = f.readlines()
    with open(path, mode="w") as f:
        for string in strings:
            string = string.replace("terminal", "mymodule")
            string = string.replace("Terminal", "MyModule")
            f.write(string)
        
    
        