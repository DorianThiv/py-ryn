
import sys
import threading

from transfert import ModuleFrameTransfert, SimpleFrameTransfert
from factories import PackageFactory
from util import *
from interfaces import ISATObject, ICore, ILoader, IDealer, IManager, IProvider, IRegistry, IOperator, IBinder, IObserver, IObservable, IAction

class BaseSATObject(ISATObject): 

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        pass

    def __str__(self):
        return "__BASESATOBJECT__"

    def load(self):
        pass

    def action(self, frame=None):
        """ 
            TODO: Call LoaderTreatAction class. it will
            contains all treatment actions.
            Will reaload module name by name.
            To reload the loader give ["config"]["module"]
        """
        # print("Component : {}, Action :{}".format(self, frame))
        action = BaseAction(self, frame)
        action.treat()


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

    def start(self, loader):
        self.state = BaseCore.STATE_START
        self.loader = loader

    def run(self):
        self.state = BaseCore.STATE_RUN
        self.loader.action(SimpleFrameTransfert(0, 1, "all"))

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
    def __init__(self, name, core, pmanagers):
        super().__init__(name)
        self.core = core
        self.dealer = BaseDealer()
        self.pmanagers = []
        self.pmanagers.append(self.name)
        for m in pmanagers:
            self.pmanagers.append(m)
        self.managers = {}
        self.dealer.add_principal(self)
        self.load(pmanagers)

    def load(self, managers):
        """ 
            Load all managers in a list. 
            Create managers with the ManagerFactory and give them 
            at the dealer to share data. 
        """
        for manager in managers:
            """ Load differents component in function of core state """
            self.__load_once(manager)

    def __load_once(self, manager):
        m = PackageFactory.make(manager)
        m.register(self.dealer)
        if manager not in list(self.pmanagers):
            self.dealer.add(m)
        else:
            self.dealer.add_principal(m)
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
        """ Remove a module from the managers dict """
        BaseDealer.CONNECTED_MANAGERS.remove(mname)
        del self.managers[mname]

    def find(self, mname):
        """ Find another module to send the received frame """
        return self.managers[mname]

    def update(self, frame):
        """ Notification from a module 
            Keyword list() force to make a copy of 
            dictionnary keys. 
        """
        try:
            if frame.receiver not in list(self.managers):
                self.principals_managers[frame.receiver].action(frame)
            else:
                self.managers[frame.receiver].action(frame)
        except Exception as e:
            print("[ERROR - NOT FOUND MODULE - /!\ MAKE EXCEPTION /!\] Ligne {}, msg: {}".format(sys.exc_info()[-1].tb_lineno, e))
            print("[ERROR - NOT FOUND METHOD - IN MODULE ... /!\ MAKE EXCEPTION /!\] Ligne {}, msg: {}".format(sys.exc_info()[-1].tb_lineno, e))

class BaseManager(BaseSATObject, IManager, IObservable):
    """ Manager load all components in this his module """
    def __init__(self, name, package, minprefix=""):
        super().__init__(name)
        self.minprefix = minprefix
        self.package = package
        self.classes = {}
        self.providers = {}
        self.observers = []
    
    def __str__(self):
        """ Display Debug """
        ret = "__BASEMANAGER__ = (name : {})\n".format(self.name)
        return ret

    def load(self):
        from factories import ModuleFactory
        self.classes = ModuleFactory.make(self.minprefix, self.package)
        for c in self.classes["providers"]:
            name = class_name_gen(self.minprefix, c["class"])
            instance = c["class"](class_name_gen(self.minprefix, c["class"]), self)
            self.providers[name] = instance
            self.providers[name].load(self.minprefix, self.classes)
    
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
        self.registries = {}

    def __str__(self):
        return "__BASEPROVIDER__ = (name : {})\n".format(self.name)

    def load(self, minprefix, classes):
        for c in classes["registries"]:
            name = class_name_gen(minprefix, c["class"])
            instance = c["class"](class_name_gen(minprefix, c["class"]), self)
            self.registries[name] = instance
            self.registries[name].load(minprefix, classes)

    def update(self, frame):
        """ Update to notify the manager with a frame instance """
        self.observable.observers_update(frame)

class BaseRegistry(BaseSATObject, IRegistry, IObservable):

    def __init__(self, name, operator, provider):
        super().__init__(name)
        self.operator = operator
        self.observers = []
        self.binders = {}
        self.observers.append(provider)

    def __str__(self):
        return "__BASEREGISTRY__ = (name : {})\n".format(self.name)

    def load(self, minprefix, classes):
        for c in classes["binders"]:
            name = class_name_gen(minprefix, c["class"])
            instance = c["class"](class_name_gen(minprefix, c["class"]), self)
            self.binders[name] = instance
            self.binders[name].load()

    def action(self, frame):
        for b in self.binders:
            self.binders[b].action(self.operator.decapsulate(frame))

    def register(self, observer):
        self.observers.append(observer)
    
    def unregister(self, observer):
        pass

    def unregister_all(self):
        pass

    def observers_update(self, data):
        for observer in self.observers:
            observer.update(self.operator.encapsulate(data))

class BaseOperator(BaseSATObject, IOperator):
    
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return "__BASEOPERATOR__ = (name : {})".format(self.name)

    def load(self):
        pass

    def encapsulate(self, data):
        return data

    def decapsulate(self, frame):
        return (frame.direction, frame.payload)

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

    def action(self, direction, data):
        print(direction, data)

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
        self.isRunning = False

    def run(self):
        self.isRunning = True
        while self.isRunning:
            try:
                msg = self.socket.recv(BaseThreadRead.PACKET_SIZE)
                print(msg) # Là j'écrit juste le message :)
            except Exception as e:
                print("ErrorRead : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 
    
    def stop(self):
        self.isRunning = False # Vrai ou faux tu crois quoi ??!
        self.socket.close()

class BaseThreadWrite(threading.Thread):

    def __init__(self, socket, data):
        super().__init__()
        self.socket = socket
        self.data = str(data)
        self.name = self.getName()

    def run(self):
        try: 
            self.socket.send(self.data.encode())
        except Exception as e:
            print("ErrorWrite : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 

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

class BaseAction(IAction):
    
    """ Internal Actions on differents componenents """

    """ Direction Commands """

    DIRECTION_UP = 0
    DIRECTION_DOWN = 1
    
    """ Simple Commands """

    CONF_MODULE = "mdlconf"

    LOADER = 0
    MANAGER = 1
    PROVIDER = 2
    REGISTRY = 3
    BINDER = 4

    def __init__(self, component, command):
        self.component = component
        self.cpttype = self.__define_component_type()
        self.command = command
        self.cmdtype = self.__define_command_type()

    def treat(self):
        """ Enter point of actions """
        self.__send_request()

    def __define_component_type(self):
        if isinstance(self.component, BaseLoader):
            return BaseAction.LOADER
        elif isinstance(self.component, BaseManager):
            return BaseAction.MANAGER
        elif isinstance(self.component, BaseProvider):
            return BaseAction.PROVIDER
        elif isinstance(self.component, BaseRegistry):
            return BaseAction.REGISTRY
        elif isinstance(self.component, BaseBinder):
            return BaseAction.BINDER
        else:
            return None

    def __define_command_type(self):
        if isinstance(self.command, ModuleFrameTransfert):
            return 1
        elif isinstance(self.command, SimpleFrameTransfert):
            return 0

    def __send_request(self):
        """ Check for a command line which specify a module """
        if self.cpttype == BaseAction.LOADER:
            if self.cmdtype == 1 and self.command.emitter == BaseAction.CONF_MODULE:
                mdls = []
                for mdl in self.command.payload["config"]["modules"]:
                    mdls.append(mdl['name'])
                self.component.load(mdls)
            elif self.cmdtype == 0:
                for m in list(self.component.dealer.managers):
                    self.component.dealer.managers[m].action(self.command)
        if self.cpttype == BaseAction.MANAGER:
            for p in self.component.providers:
                self.component.providers[p].action(self.command)
        if self.cpttype == BaseAction.PROVIDER:
            for r in self.component.registries:
                self.component.registries[r].action(self.command)

