
class LoadModuleError(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "LoadModuleError : {}".format(self.message)

class NotFoundModuleError(Exception):

    def __init__(self, msg):
        self.message = msg
 
    def __str__(self):
        return "NotFoundModuleError : {}".format(self.message)

class ArgumentsError(Exception):
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class PathError(Exception):
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class NameError(Exception):
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message