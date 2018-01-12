
import sys
import threading

from transfert import ModuleFrameTransfert, SimpleFrameTransfert
from factories import PackageFactory
from mdlutils.dhcp import *
from mdlutils.util import *
from mdlutils.config import *
from interfaces import ISATObject, ICore, ILoader, IDealer, IManager, IProvider, IRegistry, IOperator, IBinder, IObserver, IObservable, ICommand

class BaseSATObject(ISATObject): 

    def __init__(self, name, component_type, mdladdr=None):
        self.name = name
        self.type = component_type
        self.addr = DHCP.getInstance(mdladdr).discover(self)
        print(self)

    def __repr__(self):
        pass

    def __str__(self):
        return "__SAT_OBJECT__ = (name : {}, addr: {})".format(self.name, self.addr)

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
        action = BaseCommand(self, frame)
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
        super().__init__(name, DHCP.IDX_TYPE_CORE)
        self.state = BaseCore.STATE_SHUTDOWN

    def __repr__(self):
        pass

    def load(self):
        self.state = BaseCore.STATE_LOAD

    def start(self):
        self.state = BaseCore.STATE_START
        self.loader = BaseLoader("loader", self)

    def run(self):
        self.state = BaseCore.STATE_RUN
        self.loader.action(SimpleFrameTransfert(BaseCommand.COMMAND_ALL))

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
        super().__init__(name, DHCP.IDX_TYPE_LOADER)
        self.core = core
        self.dealer = BaseDealer()
        self.managers = {}
        self.load(ConfigurationModule.getModulesNames())

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
        self.dealer.add(m)
        m.load()

class BaseDealer(IDealer, IObserver):

    CONNECTED_MANAGERS = []

    def __init__(self):
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

    def remove(self, mname):
        """ Remove a module from the managers dict """
        BaseDealer.CONNECTED_MANAGERS.remove(mname)
        del self.managers[mname]

    def find(self, mod):
        """ Find another module to send the received frame """
        if isinstance(mod, int):
            # find by id
            pass
        if isinstance(mod, str):
            # find by name
            pass
        return self.managers[mod]

    def update(self, frame):
        """ Notification from a module 
            Keyword list() force to make a copy of 
            dictionnary keys. 
        """
        try:
            self.managers[frame.destAddr].action(frame)
        except Exception as e:
            print("[ERROR - NOT FOUND MODULE - /!\ MAKE EXCEPTION /!\] Ligne {}, msg: {}".format(sys.exc_info()[-1].tb_lineno, e))
            print("[ERROR - NOT FOUND METHOD - IN MODULE ... /!\ MAKE EXCEPTION /!\] Ligne {}, msg: {}".format(sys.exc_info()[-1].tb_lineno, e))

class BaseManager(BaseSATObject, IManager, IObservable):
    """ Manager load all components in this his module """
    def __init__(self, name, minprefix, module):
        super().__init__(name, DHCP.IDX_TYPE_MANAGER)
        self.minprefix = minprefix
        self.module = module
        self.classes = {}
        self.providers = {}
        self.observers = []

    def load(self):
        from factories import ModuleFactory
        self.classes = ModuleFactory.make(self.minprefix, self.module)
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

    def __init__(self, name, parent):
        super().__init__(name, DHCP.IDX_TYPE_PROVIDER, parent.addr)
        self.observable = parent
        self.registries = {}

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

    def __init__(self, name, operator, parent):
        super().__init__(name, DHCP.IDX_TYPE_REGISTRY, parent.observable.addr)
        self.operator = operator
        self.observers = []
        self.parent = parent
        self.binders = {}
        self.observers.append(parent)

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

class BaseBinder(BaseSATObject, IBinder):
    
    def __init__(self, name, parent):
        self.observable = parent
        super().__init__(name, DHCP.IDX_TYPE_BINDER, self.observable.parent.observable.addr)

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

class BaseCommand(ICommand):
    
    """ Internal Actions on differents componenents """

    COMMAND_ALL = "all"

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
            return BaseCommand.LOADER
        elif isinstance(self.component, BaseManager):
            return BaseCommand.MANAGER
        elif isinstance(self.component, BaseProvider):
            return BaseCommand.PROVIDER
        elif isinstance(self.component, BaseRegistry):
            return BaseCommand.REGISTRY
        elif isinstance(self.component, BaseBinder):
            return BaseCommand.BINDER
        else:
            return None

    def __define_command_type(self):
        if isinstance(self.command, ModuleFrameTransfert):
            return 1
        elif isinstance(self.command, SimpleFrameTransfert):
            return 0

    def __send_request(self):
        """ Check for a command line which specify a module """
        if self.cpttype == BaseCommand.LOADER:
            for m in list(self.component.dealer.managers):
                self.component.dealer.managers[m].action(self.command)
        if self.cpttype == BaseCommand.MANAGER:
            for p in self.component.providers:
                self.component.providers[p].action(self.command)
        # if self.cpttype == BaseCommand.PROVIDER:
        #     for r in self.component.registries:
        #         self.component.registries[r].action(self.command)

