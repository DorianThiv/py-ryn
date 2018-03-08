
""" Bases

    bases.py module 
      ~
    c[_] --> coffee mmmh

    Get base classes to provide a centralized source code.

    * RYNObject: Base object for module's components
    * Core: Kernel of the server (simple lifecycle)
    * Loader: Module loader find all modules implemented on the server
    * Dealer: Allow the communication beetween modules
    * Directory: Provide a module directory find a module by 'name' or 'address'
    * BaseManager: First component of a module
    * BaseProvider: Second componenent of a module
    * BaseBinder: Third component of a module
    * BaseOperator: Provide operations and encaps or decaps as a ModuleFrameTransfert
    * BaseRegistry: Allow a module to have subscribers and remember them
    * BaseCommand: Generic command parser for terminal commands

"""

import re
import sys

from interfaces import (ISaveable, IManageable, IExecutable, IObservable)
from samples.config import *
from samples.dhcp import *
from samples.factories import ModuleFactory, PackageFactory
from samples.logger import Logger
from samples.network import *
from samples.transfert import ModuleFrameTransfert, SimpleFrameTransfert
from samples.utils import *

class RYNObject(IExecutable, IObservable): 

    def __init__(self, name, component_type, mdladdr=None, parent=None):
        self.name = name
        self.type = component_type
        self.addr = DHCP.getInstance(mdladdr).discover(self)
        self.id = DHCP.getInstance(mdladdr).build_addr(component_type, self.addr, parent)
        self.logger = Logger.getInstance()

    def __str__(self):
        return "__RYN_OBJECT__ = (id: {}, name: {}, addr: {})".format(self.id, self.name, self.addr)

    def initialize(self):
        """ Initializing Load Method: Load a his component """
        pass
    
    def uninitialize(self):
        """ Initializing Load Method: Load a his component """
        pass    

    def execute(self, frame=None):
        BaseCommand(self, frame).treat()
        
    def emit(self, frame):
        pass

class Core:

    STATE_SHUTDOWN = 0
    STATE_LOAD = 1
    STATE_START = 2
    STATE_RUN = 3
    STATE_RESUME = 4
    STATE_PAUSE = 5
    STATE_STOP = 6

    def __init__(self, name):
        self.name = name
        self.state = Core.STATE_SHUTDOWN

    def start(self):
        self.state = Core.STATE_START
        self.loader = Loader(self)

    def run(self):
        self.state = Core.STATE_RUN
        self.loader.execute(SimpleFrameTransfert(BaseCommand.RUN))

    def resume(self):
        self.state = Core.STATE_RUN

    def pause(self):
        self.state = Core.STATE_PAUSE

    def stop(self):
        self.state = Core.STATE_STOP

class Loader(RYNObject):
    """ The loader enable to initialize all modules and give them instances to the "Dealer"
    """
    def __init__(self, core):
        super().__init__("loader", DHCP.IDX_TYPE_LOADER, mdladdr=None)
        self.core = core
        self.dealer = Dealer()
        self.managers = {}
        self.initialize(ConfigurationModule.getModulesNames())

    def initialize(self, managers):
        """ Load all managers in a list. 
            Create managers with the ManagerFactory and give them 
            at the dealer to share data. 
        """
        for manager in managers:
            m = PackageFactory.make(manager)
            m.dealer = self.dealer
            m.initialize()
            self.dealer.add(m)

    def execute(self, frame):
        if frame.command == BaseCommand.RUN:
            BaseCommand(self, frame).treat()
        elif frame.command == BaseCommand.SHUTDOWN:
            print("Shutdown")  

class Directory:

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
            if self.managers[mdladdr].status is True:
                ret += "\t* module (connected) : {}\n".format(self.managers[mdladdr])
            else:
                ret += "\t* module (disconnected) : {}".format(self.managers[mdladdr])
        return ret

    def add(self, manager):
        """ Add a module module in the managers dict """
        self.managers[manager.addr] = manager
        if manager.status == True:
            Directory.CONNECTED_MANAGERS_BY_NAME[manager.module] = manager
            Directory.CONNECTED_MANAGERS_BY_ADDR[manager.addr] = manager

    def remove(self, addr):
        """ Remove a module from the managers dict """
        del self.managers[addr]

    @staticmethod
    def find(idx):
        """ Find another module to send the received frame """
        if isinstance(idx, str):
            return Directory.CONNECTED_MANAGERS_BY_NAME[idx]
        elif isinstance(idx, int):
            return Directory.CONNECTED_MANAGERS_BY_ADDR[idx]
        else:
            raise Exception() # make a specific exeption

class Dealer(IObservable):

    def __init__(self):
        self.directory = Directory()

    def __str__(self):
        return str(self.directory)

    def add(self, manager):
        """ Add a module module in the managers dict """
        self.directory.add(manager)

    def remove(self, manager):
        """ Add a module module in the managers dict """
        self.directory.add(manager)

    def emit(self, frame):
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

class BaseManager(RYNObject, IManageable, ISaveable):
    """ Manager initialize all components in this his module """
    
    def __init__(self, module, parser):
        mod_conf = ConfigurationModule.getModuleProperties(module)
        self.minprefix = mod_conf["prefix"]
        self.sufix = "manager"
        self.module = module     
        self.usage = mod_conf["usage"]
        self.parser = parser
        super().__init__(self.minprefix + "-" + self.sufix, DHCP.IDX_TYPE_MANAGER)
        self.classes = {}
        self.childs = {}        
        self.dealer = None
        self.operator = None
        self.registry = None        
        self.status = False

    def initialize(self):
        """ Can be initialize for the first time like current code or 
            without any child ?? I don't know...
            But It must can be initilized with a save.
            The "save" can be an image of the module.
        """
        self.classes = ModuleFactory.make(self.minprefix, self.module)
        for c in self.classes[ModuleFactory.PROVIDERS]:
            name = class_name_gen(self.minprefix, c[ModuleFactory.VCLASSES])
            instance = c[ModuleFactory.VCLASSES](class_name_gen(self.minprefix, c[ModuleFactory.VCLASSES]), self)
            self.childs[name] = instance
            self.childs[name].initialize(self.minprefix, self.classes)
        ConfigurationModule.saveStructureModule(self)

    def command(self, command):
        status, response = BaseCommand.parse(command)
        if status is False:
            return (status, response)
        else:
            return self.parser.parse(response)
    
    def execute(self, frame):
        data = self.operator.decapsulate(frame)
        if data.command == BaseCommand.ADD:
            self.add(frame)        
        elif data.command == BaseCommand.EDIT:
            self.edit(frame)
        elif data.command == BaseCommand.REMOVE:
            self.remove(frame)        
        elif data.command == BaseCommand.SUBSCRIBE:
            self.registry.subscribe(frame)
        elif data.command == BaseCommand.UNSUBSCRIBE:
            self.registry.unsubscribe(frame)
        else:
            for child in self.childs:
                self.childs[child].execute(data)
                
    def add(self, frame):
        print("Add provider: {}".format(frame))
    
    def edit(self, frame):
        print("Edit provider: {}".format(frame))
        
    def remove(self, frame):
        print("Remove provider: {}".format(frame))    

    def emit(self, data):
        if self.dealer is not None:
            decaps_data = self.operator.encapsulate(data)
            self.dealer.emit(decaps_data)
            for module in list(self.registry.get()):
                self.dealer.emit(self.operator.encapsulate(data=data, name=module))                
        else:
            self.logger(0, "No dealer founded in {}".format(self.name))

class BaseProvider(RYNObject, IManageable):

    def __init__(self, name, parent):
        super().__init__(name, DHCP.IDX_TYPE_PROVIDER, parent.addr, parent)
        self.parent = parent
        self.childs = {}

    def initialize(self, minprefix, classes):
        for c in classes[ModuleFactory.BINDERS]:
            name = class_name_gen(minprefix, c[ModuleFactory.VCLASSES])
            instance = c[ModuleFactory.VCLASSES](class_name_gen(minprefix, c[ModuleFactory.VCLASSES]), self)
            self.childs[name] = instance
            self.childs[name].initialize()
            
    def execute(self, data):
        for b in self.childs:
            if data.command == BaseCommand.RUN:
                self.childs[b].run()
            if data.command == BaseCommand.READ:
                self.childs[b].read()
            if data.command == BaseCommand.WRITE:
                self.childs[b].write(data)    
        
    def emit(self, data):
        """ Update to notify the manager with a frame instance """
        self.parent.emit(data)

class BaseBinder(RYNObject):

    def __init__(self, name, parent):
        super().__init__(name, DHCP.IDX_TYPE_BINDER, parent.parent.addr, parent)
        self.parent = parent

    def initialize(self):
        pass

    def run(self):
        """ Run Method: Run component """
        pass

    def read(self, data):
        self.parent.emit(data)

    def write(self, data):
        pass
    
class BaseOperator:

    def __init__(self, operations, parent):
        self.module = parent.module
        self.parent = parent
        self.operations = operations

    def encapsulate(self, data, name=None):
        if name is None:
            frame = self.operations.operate_up(self.module, data)
        else:
            frame = self.operations.operate_up(name, data)
        if isinstance(frame, ModuleFrameTransfert) or isinstance(frame, SimpleFrameTransfert):
            return frame
        else:
            self.logger.log(0, "Transfert cannot be done. The frame format is : '{}'".format(type(frame)))
            raise TypeError("Transfert cannot be done. Cannot convert '{}' to 'ModuleFrameTransfert' or 'SimpleFrameTransfert'".format(type(frame)))

    def decapsulate(self, frame):
        try:
            data = self.operations.operate_down(frame)
            return data
        except Exception as e:
            print("[ERROR - TERMINAL - DECAPSULATE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e))
            self.logger.log(0, "Terminal operator: Transfert cannot be done. The frame format is : '{}'".format(type(frame)))    

class BaseRegistry:
    """ Registry can know other modules and  """
    
    def __init__(self):
        self.directory = {}

    def subscribe(self, frame):
        """ Subscriber :
        Args:
            name: string (module name)
            command: read write save etc...
        subscribe a module with the subscribe command 
        """
        if not frame.src in self.directory:
            self.directory[frame.src] = [frame]
        else:
            self.directory[frame.src].append(frame)

    def unsubscribe(self, frame):
        """ Unsubscribe a module """
        if frame.src in self.directory:
            del self.directory[frame.src]
    
    def get(self):
        """ Check for all data type which module was subscribe """
        return self.directory
        
class BaseCommand:
    """ Generic parse command """

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
    INITIALIZE = "initialize"
    RUN = "run"
    RELOAD = "reload"
    READ = "read"
    WRITE = "write"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    ADD = "add"
    EDIT = "edit"
    REMOVE = "remove"

    """ Internal Parsed items """
    PARSE_MODULE = "module"
    PARSE_COMMAND = "command"
    PARSE_TEXT = "text"
    PARSE_ADDRESS = "address"
    PARSE_CONNECTION = "connection"
    PARSE_DEVICE = "device"
    
    PARSE_ARGUMENTS_ERROR = "no arguments detected"
    PARSE_MODULE_ERROR = "error module"
    PARSE_COMMAND_ERROR = "no command detected : (-r | -w | -s | -u | --add | --edit | --remove)"
    PARSE_COMMAND_FOUND_ERROR = "no command found for : "
    PARSE_TEXT_ERROR = "excepted text : (-t \"hello world\") | (--text \"hello world\")"
    PARSE_ADDRESS_ERROR = "excepted IP address : (-a x.x.x.x | --address x.x.x.x)"
    PARSE_CONNECTION_ERROR = "error connection"
    PARSE_DEVICE_ERROR = "error device"    

    def __init__(self, component, command):
        self.component = component
        self.cpttype = self.component.type
        self.command = command

    def treat(self):
        """ Check for a command line which specify a module """
        if self.cpttype == BaseCommand.CORE:
            self.component.execute(self.command)
        if self.cpttype == BaseCommand.LOADER:
            for m in list(Directory.CONNECTED_MANAGERS_BY_NAME):
                Directory.CONNECTED_MANAGERS_BY_NAME[m].execute(self.command)
        if self.cpttype in [BaseCommand.MANAGER, BaseCommand.PROVIDER]:
            for p in self.component.childs:
                self.component.childs[p].execute(self.command)

    @staticmethod
    def parse(command):
        """ Command parser function has a public exposition 
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
            if re.match(r"(-|-{2})+(read)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.READ
            if re.match(r"(-|-{2})+(write)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.WRITE
            if re.match(r"(-|-{2})+(add)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.ADD
            if re.match(r"(-|-{2})+(edit)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.EDIT
            if re.match(r"(-|-{2})+(rm|remove)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.REMOVE            
            if re.match(r"(-|-{2})+(sub|subscribe)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.SUBSCRIBE
            if re.match(r"(-|-{2})+(unsub|unsubscribe)", elem) != None:
                commanddict[BaseCommand.PARSE_COMMAND] = BaseCommand.UNSUBSCRIBE
            if re.match(r"(-|-{2})+(addr|address)", elem) != None:
                if command.index(elem)+1 < len(command):
                    try:
                        checkIp(command[command.index(elem)+1])
                        commanddict[BaseCommand.PARSE_ADDRESS] = command[command.index(elem)+1]
                    except Exception as e:
                        return (False, "{} : {}".format(BaseCommand.PARSE_ADDRESS_ERROR, e))
                else:
                    return (False, BaseCommand.PARSE_ADDRESS_ERROR)
            if re.match(r"(-|-{2})+(t|text)", elem) != None:
                if command.index(elem)+1 < len(command):
                    commanddict[BaseCommand.PARSE_TEXT] = command[command.index(elem)+1]
                else:
                    return (False, BaseCommand.PARSE_TEXT_ERROR)
        return (True, commanddict)
