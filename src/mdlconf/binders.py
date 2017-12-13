

class ConfigurationBinder(BaseBinder):
    
    def __init__(self, ref, name):
        super().__init__(ref, name)

    def load(self):
        pass

    def read(self, path):
        import sys
        with open(path, 'r') as f:
            contents = f.read()
        print contents

    def write(self):
        pass
    