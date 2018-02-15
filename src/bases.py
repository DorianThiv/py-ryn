
import re
import sys

from interfaces import (IBinder, ICommand, ICore, IDealer, IDirectory, ILoader,
                        IManager, IObservable, IObserver, IOperator, IProvider,
                        IRegistry, IRYNObject)
from mdlutils.config import *
from mdlutils.dhcp import *
from mdlutils.factories import ModuleFactory, PackageFactory
from mdlutils.logger import Logger
from mdlutils.network import *
from mdlutils.transfert import ModuleFrameTransfert, SimpleFrameTransfert
from mdlutils.utils import *


class BaseRYNObject(IRYNObject, ICommand): 

    def __init__(self, name, component_type, mdladdr=None):
        self.name = name
        self.type = component_type
        self.addr = DHCP.getInstance(mdladdr).discover(self)
        self.logger = Logger.getInstance()
        self.usage = "" 

    def __repr__(self):
        pass

    def __str__(self):
        return "__RYN_OBJECT__ = (name : {}, addr: {})".format(self.name, self.addr)

    def __del__(self):
        pass

    def load(self):
        """Load Method: Load a his component """
        pass

    def execute(self, frame=None):
        BaseCommand(self, frame).treat()

class BaseCore(BaseRYNObject, ICore):

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
        self.logger.log(2, "Loading ...")
        self.state = BaseCore.STATE_LOAD

    def start(self):
        self.logger.clear()
        self.logger.log(2, "Starting ...")
        self.state = BaseCore.STATE_START
        self.loader = BaseLoader("loader", self)

    def run(self):
        self.logger.log(2, "Running ...")
        self.state = BaseCore.STATE_RUN
        self.loader.execute(SimpleFrameTransfert(BaseCommand.LOAD))

    def resume(self):
        self.state = BaseCore.STATE_RUN

    def pause(self):
        self.state = BaseCore.STATE_PAUSE

    def stop(self):
        self.logger.log(2, "Stopping ...")
        self.state = BaseCore.STATE_STOP

class BaseLoader(BaseRYNObject, ILoader):
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
        self.logger.log(2, self.dealer)

    def load(self, managers):
        """ Load all managers in a list. 
            Create managers with the ManagerFactory and give them 
            at the dealer to share data. 
        """
        for manager in managers:
            m = PackageFactory.make(manager)
            m.register(self.dealer)
            m.load()
            self.dealer.add(m)

    def execute(self, frame):
        if frame.command == BaseCommand.LOAD:
            BaseCommand(self, frame).treat()
        elif frame.command == BaseCommand.SHUTDOWN:
            print("Shutdown")

    

class BaseDirectory(IDirectory):

    CONNECTED_MANAGERS_BY_ADDR = {}
    CONNECTED_MANAGERS_BY_NAME = {}

    def __init__(self):
        self.managers = {}

    def __repr__(self):
        pass

    def __iter__(self):
        pass

    def __str__(self):
        ret = "__DIRECTORY__ : \n"
        for mdladdr in self.managers:
            if self.managers[mdladdr].status == True:
                ret += "\t* module (connected) : {}\n".format(self.managers[mdladdr])
            else:
                ret += "\t* module (disconnected) : {}".format(self.managers[mdladdr])
        return ret

    def add(self, manager):
        """ Add a module module in the managers dict """
        self.managers[manager.addr] = manager
        if manager.status == True:
            BaseDirectory.CONNECTED_MANAGERS_BY_NAME[manager.module] = manager
            BaseDirectory.CONNECTED_MANAGERS_BY_ADDR[manager.addr] = manager

    def remove(self, addr):
        """ Remove a module from the managers dict """
        del self.managers[addr]

    @staticmethod
    def find(idx):
        """ Find another module to send the received frame """
        if isinstance(idx, str):
            return BaseDirectory.CONNECTED_MANAGERS_BY_NAME[idx]
        elif isinstance(idx, int):
            return BaseDirectory.CONNECTED_MANAGERS_BY_ADDR[idx]
        else:
            raise Exception() # make a specific exeption

class BaseDealer(IDealer, IObserver):

    def __init__(self):
        self.directory = BaseDirectory()

    def __str__(self):
        return str(self.directory)

    def add(self, manager):
        """ Add a module module in the managers dict """
        self.directory.add(manager)

    def remove(self, manager):
        """ Add a module module in the managers dict """
        self.directory.add(manager)

    def update(self, frame):
        """ Notification from a module

            Transfert a frame from another module.
            Frame description in transfert.py script 

            A frame must be created by the software it's for that I must 
            develop a frame integrity module. It will verify the a sum in the
            frame content.
        """
        try:
            self.directory.find(frame.dest).execute(frame)
        except Exception as e:
            print("[ERROR - NOT FOUND MODULE - /!\ MAKE EXCEPTION /!\] Ligne {}, msg: {}".format(sys.exc_info()[-1].tb_lineno, e))
            print("[ERROR - NOT FOUND METHOD - IN MODULE ... /!\ MAKE EXCEPTION /!\] Ligne {}, msg: {}".format(sys.exc_info()[-1].tb_lineno, e))

class BaseManager(BaseRYNObject, IManager, IObservable):
    """ Manager load all components in this his module """
    
    def __init__(self, module):
        mod_conf = ConfigurationModule.getModuleProperties(module)
        self.minprefix = mod_conf["prefix"]
        self.sufix = "manager"
        self.module = module        
        super().__init__(self.minprefix + "-" + self.sufix, DHCP.IDX_TYPE_MANAGER)
        self.status = False
        self.classes = {}
        self.childs = {}
        self.observers = []

    def load(self):
        self.classes = ModuleFactory.make(self.minprefix, self.module)
        for c in self.classes[ModuleFactory.PROVIDERS]:
            name = class_name_gen(self.minprefix, c[ModuleFactory.VCLASSES])
            instance = c[ModuleFactory.VCLASSES](class_name_gen(self.minprefix, c[ModuleFactory.VCLASSES]), self)
            self.childs[name] = instance
            self.childs[name].load(self.minprefix, self.classes)

    def command(self, command):
        return BaseCommand.parse(command)

    def register(self, observer):
        self.observers.append(observer)

    def emit(self, frame):
        for observer in self.observers:
            observer.update(frame)

class BaseProvider(BaseRYNObject, IProvider, IObserver):

    def __init__(self, name, parent):
        super().__init__(name, DHCP.IDX_TYPE_PROVIDER, parent.addr)
        self.observable = parent
        self.childs = {}

    def load(self, minprefix, classes):
        for c in classes[ModuleFactory.OPERATORS]:
            name = class_name_gen(minprefix, c[ModuleFactory.VCLASSES])
            instance = c[ModuleFactory.VCLASSES](class_name_gen(minprefix, c[ModuleFactory.VCLASSES]), self)
            self.childs[name] = instance
            self.childs[name].load(minprefix, classes)

    def update(self, frame):
        """ Update to notify the manager with a frame instance """
        self.observable.emit(frame)

class BaseOperator(BaseRYNObject, IOperator, IObservable):

    def __init__(self, name, registry, parent):
        super().__init__(name, DHCP.IDX_TYPE_OPERATOR, parent.observable.addr)
        self.registry = registry
        self.observers = []
        self.parent = parent
        self.module = parent.observable.module
        self.childs = {}
        self.observers.append(parent)

    def load(self, minprefix, classes):
        for c in classes[ModuleFactory.BINDERS]:
            name = class_name_gen(minprefix, c[ModuleFactory.VCLASSES])
            instance = c[ModuleFactory.VCLASSES](class_name_gen(minprefix, c[ModuleFactory.VCLASSES]), self)
            self.childs[name] = instance
            self.childs[name].load()

    def execute(self, frame):
        for b in self.childs:
            self.childs[b].execute(self.decapsulate(frame))

    def register(self, observer):
        self.observers.append(observer)

    def emit(self, data):
        try:
            for observer in self.observers:
                observer.update(self.encapsulate(data))
        except Exception as e:
            print("[ERROR - UPDATE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))

class BaseRegistry(IRegistry):
    """ Registry can know other modules and  """
    def __init__(self, name):
        self.name = name
        self.directory = {}

    def subscribe(self, name, command):
        """ subscribe a module with the subscribe command """
        if name in list(self.directory.keys()):
            self.directory[name].put(command)
        else:
            self.directory[name] = queue.Queue()
            self.directory[name].put(command)

    def unsubscribe(self, name):
        """ Unsubscribe a module """
        if name in self.directory:
            del self.directory[name]
    
    def request(self, data):
        """ Check for all data type which module was subscribe """
        pass

class BaseBinder(BaseRYNObject, IBinder):

    def __init__(self, name, parent):
        self.observable = parent
        super().__init__(name, DHCP.IDX_TYPE_BINDER, self.observable.parent.observable.addr)

    def load(self):
        pass

    def execute(self, direction, data):
        pass

    def read(self):
        pass

    def write(self):
        pass

    def _get_event(self, data):
        self.observable.emit(data)

class BaseCommand(ICommand):

    """ Component's types """
    CORE = DHCP.IDX_TYPE_CORE
    LOADER = DHCP.IDX_TYPE_LOADER
    MANAGER = DHCP.IDX_TYPE_MANAGER
    PROVIDER = DHCP.IDX_TYPE_PROVIDER
    OPERATOR = DHCP.IDX_TYPE_OPERATOR
    BINDER = DHCP.IDX_TYPE_BINDER    

    """ Internal Actions on differents componenents """
    START = "start"
    RESTART = "restart"
    SHUTDOWN = "shutdown"
    LOAD = "load"
    RELOAD = "reload"
    READ = "read"
    WRITE = "write"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"

    """ Internal Parsed items """
    PARSE_MODULE = "module"
    PARSE_COMMAND = "command"
    PARSE_TEXT = "text"
    PARSE_ADDRESS = "address"

    def __init__(self, component, command):
        self.component = component
        self.cpttype = self.component.type
        self.command = command

    def treat(self):
        """ Check for a command line which specify a module """
        if self.cpttype == BaseCommand.CORE:
            self.component.execute(self.command)
        if self.cpttype == BaseCommand.LOADER:
            for m in list(BaseDirectory.CONNECTED_MANAGERS_BY_NAME):
                BaseDirectory.CONNECTED_MANAGERS_BY_NAME[m].execute(self.command)
        if self.cpttype in [BaseCommand.MANAGER, BaseCommand.PROVIDER]:
            for p in self.component.childs:
                self.component.childs[p].execute(self.command)

    @staticmethod
    def parse(command):
        """ command parser function has a public exposition 
            to have a command line parser generally for manager.

            Get a module command line parser for the specific module.
            Args:
                * command: string
            Returns:
                * tuple(False, error: string)
                * tuple(True, None)
        """
        commanddict = {}
        for elem in command:
            if re.match(r"mdl([a-z])+", elem) != None:
                commanddict[BaseCommand.PARSE_MODULE] = elem
            if re.match(r"(-|-{2})+(r|read)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.READ
            if re.match(r"(-|-{2})+(w|write)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.WRITE
            if re.match(r"(-|-{2})+(s|subscribe)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.SUBSCRIBE
            if re.match(r"(-|-{2})+(u|unsubscribe)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.UNSUBSCRIBE
            if re.match(r"(-|-{2})+(a|address|addr)", elem) != None:
                if command.index(elem)+1 < len(command):
                    try:
                        checkIp(command[command.index(elem)+1])
                        commanddict[BaseCommand.PARSE_ADDRESS] = command[command.index(elem)+1]
                    except Exception as e:
                        return (False, "excepted IP address : (-a x.x.x.x | --address x.x.x.x) : {}".format(e))
                else:
                    return (False, "excepted IP address : (-a x.x.x.x | --address x.x.x.x)")
            if re.match(r"(-|-{2})+(t|text)", elem) != None:
                if command.index(elem)+1 < len(command):
                    commanddict[BaseCommand.PARSE_TEXT] = command[command.index(elem)+1]
                else:
                    return (False, "excepted text : (-t \"hello world\") | (--text \"hello world\")")
        return (True, commanddict)
