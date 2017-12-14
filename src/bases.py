
from interfaces import ISATObject, ICore, ILoader, IManager, IProvider, IRegistry, IOperator, IBinder, IObserver, IObservable 

class BaseCore(ISATObject, ICore):
    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def __repr__(self):
        pass

    def __str__(self):
        return "__BASECORE__"

    def load(self):
        pass

    def start(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

class BaseLoader(ISATObject, ILoader):
    
    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def __repr__(self):
        pass

    def __str__(self):
        return "__BASELOADER__"

    def load(self):
        pass

    def reload(self):
        pass

class BaseManager(ISATObject, IManager):

    def __init__(self, ref, name):
        self.ref = ref
        self.name = name
        self.providers = {}
        self.registries = {}
        self.binders = {}

    def load(self):
        pass

    def debug(self):
        pass

class BaseProvider(ISATObject, IProvider, IObserver):

    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def load(self):
        pass

    def provide(self):
        pass

    def update(self):
        pass

class BaseRegistry(ISATObject, IRegistry, IObservable):

    def __init__(self, ref, name):
        self.ref = ref
        self.name = name
        self.observers = []

    def load(self):
        pass

    def operate(self):
        pass

    def register(self, observer):
        pass
    
    def unregister(self, observer):
        pass

    def unregister_all(self):
        pass

    def observers_update(self):
        pass

class BaseOperator(ISATObject, IOperator):
    
    def __init__(self, ref, name):
        self.ref = ref
        self.name = name

    def load(self):
        pass

    def serialize(self):
        pass

    def deserialize(self):
        pass

class BaseBinder(ISATObject, IBinder):
    
    def __init__(self, ref, name, observable):
        self.ref = ref
        self.name = name
        self.observable = observable

    def load(self):
        pass

    def read(self):
        pass

    def write(self):
        pass
