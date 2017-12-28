
import threading
from factories import PackageFactory
from util import *
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

    def action(self, frame):
        print(frame)


class BaseCore(BaseSATObject, ICore):
    
    STATE_SHUTDOWN = 0
    STATE_LOAD = 1
    STATE_START = 2
    STATE_RUN = 3
    STATE_RESUME = 4
    STATE_PAUSE = 5
    STATE_STOP = 6

    def __init__(self, name):
        super().__init__(name)
        self.state = BaseCore.STATE_SHUTDOWN

    def __repr__(self):
        pass

    def __str__(self):
        return "__CORE__ = (name : {}".format(self.name)

    def load(self):
        self.state = BaseCore.STATE_LOAD

    def start(self, loader, managers):
        self.state = BaseCore.STATE_START
        self.loader = loader
        self.loader.load(managers)

    def run(self):
        self.state = BaseCore.STATE_RUN


    def resume(self):
        self.state = BaseCore.STATE_RUN

    def pause(self):
        self.state = BaseCore.STATE_PAUSE

    def stop(self):
        self.state = BaseCore.STATE_STOP

class BaseLoader(BaseSATObject, ILoader):
    """
		The loader enable to load all modules and 
		give them instances to the "Dealer"
	"""
    def __init__(self, name, core):
        super().__init__(name)
        self.core = core
        self.dealer = BaseDealer()
        self.managers = {}
        self.dealer.add(self)

    def load(self, managers):
        """ 
            Load all managers in a list. 
            Create managers with the ManagerFactory and give them 
            at the dealer to share data. 
        """
        for manager in list(managers):
            """ Load differents component in function of core state """
            self.__load_once(manager)

    def action(self, frame):
        """ 
            TODO: Call LoaderTreatAction class. it will
            contains all treatment actions.
            Will reaload module name by name.
            To reload the loader give ["config"]["module"]
        """
        if frame.emitter == "mdlconf":
            mdls = []
            for mdl in frame.payload["config"]["modules"]:
                mdls.append(mdl['name'])
            self.load(mdls)

    def __load_once(self, manager):
        m = PackageFactory.make(manager)
        m.register(self.dealer)
        self.dealer.add(m)
        m.load()

class BaseDealer(IDealer, IObserver):

    PRINCIPALS_MANAGERS = []
    CONNECTED_MANAGERS = []

    def __init__(self):
        self.principals_managers = {}
        self.managers = {}
        for m in self.managers:
            BaseDealer.CONNECTED_MANAGERS.append(m)

    def __repr__(self):
        pass

    def __str__(self):
        ret = "__DEALER__ : (Echangeur)\n"
        for manager in self.managers:
            if manager != "mdlloader":
                ret += "= module : {}\n".format(self.managers[manager])
        return ret

    def add(self, manager):
        """ Add a module module in the managers dict """
        BaseDealer.CONNECTED_MANAGERS.append(manager.name)
        self.managers[manager.name] = manager

    def add_principal(self, manager):
        """ Add a module module in the managers dict """
        BaseDealer.PRINCIPALS_MANAGERS.append(manager.name)
        self.principals_managers[manager.name] = manager

    def remove(self, mname):
        """ Remove a module module from the managers dict """
        pass

    def find(self, mname):
        """ Find another module to send the received frame """
        pass

    def update(self, frame):
        """ Notification from a module 
            Keyword list() force to make a copy of 
            dictionnary keys. 
        """
        self.managers[frame.receiver].action(frame)

class BaseManager(BaseSATObject, IManager, IObservable):
    """ Manager load all components in this his module """
    def __init__(self, name, package, minprefix=""):
        super().__init__(name)
        self.minprefix = minprefix
        self.package = package
        self.classes = {}
        self.providers = []
        self.registries = []
        self.binders = []
        self.observers = []
    
    def __str__(self):
        """ Display Debug """
        ret = "__BASEMANAGER__ = (name : {})\n".format(self.name)
        i = 0
        j = 0
        k = 0
        for i in range(len(self.providers)):
            ret += "\t{}".format(self.providers[i]["instance"])
            for j in range(len(self.registries)):
                ret += "\t\t{}".format(self.registries[j]["instance"])
                for k in range(len(self.binders)):
                    ret += "\t\t\t{}".format(self.binders[k]["instance"])
        return ret

    def load(self):
        from factories import ModuleFactory
        self.classes = ModuleFactory.make(self.minprefix, self.package)
        for c in self.classes["providers"]:
            p = c["class"](class_name_gen(self.minprefix, c["class"]), self)
            p.load(self.minprefix, self.classes)
            self.providers.append({"name": class_name_gen(self.minprefix, c["class"]), "instance": p})
    
    def action(self, frame):
        print(frame)
        for p in self.providers:
            print(p)
    
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
        self.registries = []
        self.binders = {}

    def __str__(self):
        return "__BASEPROVIDER__ = (name : {})\n".format(self.name)

    def load(self, minprefix, classes):
        for c in classes["registries"]:
            name = class_name_gen(minprefix, c["class"])
            instance = c["class"](class_name_gen(minprefix, c["class"]))
            instance.register(self)
            self.registries.append({"name": name, "instance": instance})
        for c in classes["binders"]:
            name = class_name_gen(minprefix, c["class"])
            instance = c["class"](class_name_gen(minprefix, c["class"]), self.registries[0]["instance"])
            self.binders[name] = instance
            self.binders[name].load()

    def action(self, frame):
        pass

    def update(self, frame):
        """ Update to notify the manager with a frame instance """
        self.observable.observers_update(frame)

class BaseRegistry(BaseSATObject, IRegistry, IObservable):

    def __init__(self, name, operator):
        super().__init__(name)
        self.operator = operator
        self.observers = []

    def __str__(self):
        return "__BASEREGISTRY__ = (name : {})\n".format(self.name)

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

    def __str__(self):
        return "__BASEOPERATOR__ = (name : {})".format(self.name)

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

    def __repr__(self):
        return "__BASEGBINDER__ = (name : {}, observable : {})\n".format(self.name, self.observable.name)

    def __str__(self):
        return "__BASEGBINDER__ = (name : {}, observable : {})\n".format(self.name, self.observable.name)

    def load(self):
        pass

    def read(self):
        pass

    def write(self):
        pass

    def _get_event(self, data):
        self.observable.observers_update(data)

class BaseThreadRead(threading.Thread):

    PACKET_SIZE = 1024

    def __init__(self, socket, callback):
        super().__init__()
        self.socket = socket
        self.callback = callback
        self.name = self.getName()
        self.isRunning = False

    def run(self):
        self.isRunning = True
        while self.isRunning:
            msg = self.socket.recv(BaseThreadRead.PACKET_SIZE)
            print(msg)
    
    def stop(self):
        self.isRunning = False
        self.socket.close()

class BaseThreadWrite(threading.Thread):

    def __init__(self, socket, data):
        super().__init__()
        self.socket = socket
        self.data = list2str([chr(d) for d in self.data])
        self.name = self.getName()

    def run(self):
        self.socket.send(self.data.encode())

class BaseThreadClient(threading.Thread):

    PACKET_SIZE = 1024

    def __init__(self, connection, callback):
        super().__init__()
        self.connection = connection
        self.callback = callback
        self.name = self.getName()
        self.isRunning = False

    def run(self):
        self.isRunning = True
        while self.isRunning:
            msg = self.connection.recv(BaseThreadRead.PACKET_SIZE)
            print(msg)
            self.callback(msg)
    
    def stop(self):
        self.isRunning = False