
from interfaces import ISATObject, ICore, ILoader, IDealer, IManager, IProvider, IRegistry, IOperator, IBinder, IObserver, IObservable 

class BaseObservable(IObservable):
    
    def __init__(self):
        self.observers = []
    
    def register(self, observer):
        self.observers.append(observer)
    
    def unregister(self, observer):
        pass

    def unregister_all(self):
        pass

    def observers_update(self, emitter=None, receptor=None, action=None, data=None, timestamp=None, crc=None):
        for observer in self.observers:
            observer.update(data)

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
    
    def __init__(self, ref, name, dealer):
        self.ref = ref
        self.name = name
        self.managers = {}

    def __repr__(self):
        pass

    def __str__(self):
        return "__BASELOADER__"

    def load(self):
        pass

    def reload(self):
        pass

    def update(self):
        pass

class BaseDealer(IDealer, IObserver):

    def __init__(self, managers={}):
        self.managers = managers

    def __repr__(self):
        pass

    def __str__(self):
        return "__BASEDEALER__"

    def add(self, manager):
        self.managers[manager.name] = manager

    def remove(self, mname):
        pass

    def find(self, mname):
        pass

    def update(self, frame):
        pass

class BaseManager(ISATObject, IManager, BaseObservable):

    def __init__(self, ref, name):
        self.ref = ref
        self.name = name
        self.providers = {}
        self.registries = {}
        self.binders = {}
        super().__init__()

    def load(self):
        pass

    def debug(self):
        pass

    def register(self, observer):
        super().register(observer)
    
    def unregister(self, observer):
        pass

    def unregister_all(self):
        pass

    def observers_update(self, emitter=None, receptor=None, action=None, data=None, timestamp=None, crc=None):
        super().observers_update(emitter, receptor, action, data, timestamp, crc)

class BaseProvider(ISATObject, IProvider, IObserver):

    def __init__(self, ref, name, observable):
        self.ref = ref
        self.name = name
        self.observable = observable

    def load(self):
        pass

    def provide(self):
        pass

    def update(self):
        pass

class BaseRegistry(ISATObject, IRegistry, BaseObservable):

    def __init__(self, ref, name):
        self.ref = ref
        self.name = name
        super().__init__()

    def load(self):
        pass

    def operate(self):
        pass

    def register(self, observer):
        super().register(observer)
    
    def unregister(self, observer):
        pass

    def unregister_all(self):
        pass

    def observers_update(self, emitter=None, receptor=None, action=None, data=None, timestamp=None, crc=None):
        super().observers_update(emitter, receptor, action, data, timestamp, crc)

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
