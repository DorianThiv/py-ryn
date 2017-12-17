
from interfaces import ISATObject, ICore, ILoader, IDealer, IManager, IProvider, IRegistry, IOperator, IBinder, IObserver, IObservable 

class BaseSATObject(ISATObject): 

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        pass

    def __str__(self):
        return "__BASECORE__"

    def load(self):
        pass


class BaseCore(BaseSATObject, ICore):
    
    def __init__(self, name):
        super().__init__(name)

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

class BaseLoader(BaseSATObject, ILoader):
    
    def __init__(self, name, dealer):
        super().__init__(name)
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

class BaseManager(BaseSATObject, IManager, IObservable):

    def __init__(self, name, prefixs="", minprefix=""):
        super().__init__(name)
        self.minprefix = minprefix
        self.modules = {
			"{}.providers".format(name): ["{}Provider".format(pr) for pr in prefixs],
			"{}.registries".format(name): ["{}Registry".format(pr) for pr in prefixs],
			"{}.operators".format(name): ["{}Operator".format(pr) for pr in prefixs],
			"{}.binders".format(name): ["{}Binder".format(pr) for pr in prefixs]
		}
        self.classes = {}
        self.providers = []
        self.registries = []
        self.binders = []
        self.observers = []

    def load(self):
        pass

    def _reading_all(self):
        i=0
        for i in range(len(self.binders)):
            self.binders[i]["instance"].read()

    def register(self, observer):
        self.observers.append(observer)
    
    def unregister(self, observer):
        pass

    def unregister_all(self):
        pass

    def observers_update(self, frame):
        for observer in self.observers:
            observer.update(frame)

class BaseProvider(BaseSATObject, IProvider, IObserver):

    def __init__(self, name, observable=None):
        super().__init__(name)
        self.observable = observable

    def load(self):
        pass

    def provide(self):
        pass

    def update(self, frame):
        pass

class BaseRegistry(BaseSATObject, IRegistry, IObservable):

    def __init__(self, name, operator):
        super().__init__(name)
        self.operator = operator
        self.observers = []

    def load(self):
        pass

    def operate(self, data):
        return self.operator.encapsulate(data)

    def register(self, observer):
        self.observers.append(observer)
    
    def unregister(self, observer):
        pass

    def unregister_all(self):
        pass

    def observers_update(self, data):
        frame = self.operate(data=data)
        for observer in self.observers:
            observer.update(frame)

class BaseOperator(BaseSATObject, IOperator):
    
    def __init__(self, name):
        super().__init__(name)

    def load(self):
        pass

    def encapsulate(self, data):
        pass

    def decapsulate(self):
        pass

class BaseBinder(BaseSATObject, IBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name)
        self.observable = observable

    def load(self):
        pass

    def read(self):
        pass

    def write(self):
        pass
