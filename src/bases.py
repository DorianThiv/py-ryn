
import sys
import threading

from utils import *
from transfert import ModuleFrameTransfert, SimpleFrameTransfert
from factories import PackageFactory
from mdlz.dhcp import *
from mdlz.config import *
from interfaces import ISATObject, ICore, ILoader, IDirectory, IDealer, IManager, IProvider, IRegistry, IOperator, IBinder, IObserver, IObservable, ICommand

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
        print(self.dealer)

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
        m.load()
        self.dealer.add(m)

class BaseDirectory(IDirectory):

    """ TODO : Make directory facilitator """

    CONNECTED_MANAGERS = {}

    def __init__(self):
        self.managers = {}

    def __repr__(self):
        pass

    def __str__(self):
        ret = "__DIRECTORY__ : \n"
        for mdladdr in self.managers:
            if self.managers[mdladdr].status == True:
                ret += "= module (connected) : {}\n".format(self.managers[mdladdr])
            else:
                ret += "= module (disconnected) : {}\n".format(self.managers[mdladdr])
        return ret

    def add(self, manager):
        """ Add a module module in the managers dict """
        self.managers[manager.addr] = manager
        if manager.status == True:
            BaseDirectory.CONNECTED_MANAGERS[(manager.name, manager.addr)] = manager

    def remove(self, addr):
        """ Remove a module from the managers dict """
        del self.managers[addr]

    @staticmethod
    def findAddr(idx):
        """ Find another module to send the received frame """
        if isinstance(idx, str):
            return BaseDirectory.CONNECTED_MANAGERS[[0]]
        if isinstance(idx, int):
            return BaseDirectory.CONNECTED_MANAGERS[[1]]
    
    @staticmethod
    def findName(idx):
        """ Find another module to send the received frame """
        if isinstance(idx, str):
            return BaseDirectory.CONNECTED_MANAGERS[[0]]
        if isinstance(idx, int):
            return BaseDirectory.CONNECTED_MANAGERS[[1]]

    @staticmethod
    def findBinderFromManager(mdlidx, binderidx):
        """ Find another module to send the received frame """
        if isinstance(mdlidx, str):
            return BaseDirectory.CONNECTED_MANAGERS[[0]]
        if isinstance(mdlidx, int):
            return BaseDirectory.CONNECTED_MANAGERS[[1]]

class BaseDealer(IDealer, IObserver):

    """ TODO : Make directory facilitator """

    def __init__(self):
        self.directory = BaseDirectory()

    def __repr__(self):
        pass

    def __str__(self):
        print(self.directory)

    def add(self, manager):
        """ Add a module module in the managers dict """
        self.directory.add(manager)

    def remove(self, mname):
        """ Remove a module from the managers dict """
        pass

    def find(self, idx):
        """ Find another module to send the received frame """
        return BaseDirectory.find(idx)

    def update(self, frame):
        """ Notification from a module 
            Keyword list() force to make a copy of 
            dictionnary keys. 
        """
        try:
            self.directory.managers[frame.destAddr].action(frame)
        except Exception as e:
            print("[ERROR - NOT FOUND MODULE - /!\ MAKE EXCEPTION /!\] Ligne {}, msg: {}".format(sys.exc_info()[-1].tb_lineno, e))
            print("[ERROR - NOT FOUND METHOD - IN MODULE ... /!\ MAKE EXCEPTION /!\] Ligne {}, msg: {}".format(sys.exc_info()[-1].tb_lineno, e))

class BaseManager(BaseSATObject, IManager, IObservable):
    """ Manager load all components in this his module """
    def __init__(self, name, minprefix, module):
        super().__init__(name, DHCP.IDX_TYPE_MANAGER)
        self.status = False
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

class BaseCommand(ICommand):
    
    """ Internal Actions on differents componenents """

    COMMAND_ALL = "all"
    
    """ Simple Commands """

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
        if self.cpttype == BaseCommand.PROVIDER:
            for r in self.component.registries:
                self.component.registries[r].action(self.command)

