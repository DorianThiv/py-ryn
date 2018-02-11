import os
import sys
import fnmatch

class ArgumentsError(Exception):
    pass

class PathError(Exception):
    pass

class NameError(Exception):
    pass

if __name__ == "__main__":    
    print(sys.argv)
    if len(sys.argv) != 3:
        raise ArgumentsError()
    if not os.path.isdir(sys.argv[1]):
        print(os.path, sys.argv[1])
        raise PathError()
    words = sys.argv[2].split('-')
    words = [str.lower(word) for word in words]
    low_name = "".join(words)
    upper_name = "".join([str.upper(word[0]) + word[1:len(word)] for word in words])
    print(low_name)
    print(upper_name)

# files = []
# for root, dirnames, filenames in os.walk('test/mdlterminal/'):
#     for filename in fnmatch.filter(filenames, '*.py'):
#         files.append(os.path.join(root, filename))

# for path in files:
#     strings = []
#     with open(path, mode="r") as f:
#         strings = f.readlines()
#     with open(path, mode="w") as f:
#         for string in strings:
#             string = string.replace("terminal", "mymodule")
#             string = string.replace("Terminal", "MyModule")
#             f.write(string)
        
    
        