
class CoreAlreadyExistError(Exception):
    pass

class LoaderAlreadyExistError(Exception):
    pass

class ComponentTypeError(Exception):
    pass
    
class AddressOutOfRangeError(Exception):
    pass
    
class DHCP:

    IDX_TYPE_CORE = -2
    IDX_TYPE_LOADER = -1
    IDX_TYPE_MANAGER = 0
    IDX_TYPE_PROVIDER = 1
    IDX_TYPE_OPERATOR = 2
    IDX_TYPE_BINDER = 3
    
    NULL_ID = 0
    CORE_ID = 1
    LOADER_ID = 2
    BROADCAST_ID = 255
    
    MIN_PUBLIC_ID = 1
    MAX_PUBLIC_ID = 254
    
    DHCP_MANAGER_INSTANCES = {}

    def __init__(self):
        self.core = None
        self.loader = None
        self.managers_ids = {}
        self.providers_ids = {}
        self.registries_ids = {}
        self.binders_ids = {}
    
    @staticmethod
    def getInstance(mdlid):
        if mdlid in DHCP.DHCP_MANAGER_INSTANCES:
            return DHCP.DHCP_MANAGER_INSTANCES[mdlid]
        elif mdlid == None:
            return DHCP()
        
    def discover(self, component, callback=None):
        if component.type == DHCP.IDX_TYPE_CORE:
            if self.core != None:
                raise CoreAlreadyExistError("No more address for public manager component")
            self.core = component
            return DHCP.CORE_ID
        elif component.type == DHCP.IDX_TYPE_LOADER:
            if self.loader != None:
                raise LoaderAlreadyExistError("No more address for public manager component")
            self.loader = component
            return DHCP.LOADER_ID
        elif component.type == DHCP.IDX_TYPE_MANAGER:
            if DHCP.MAX_PUBLIC_ID in DHCP.DHCP_MANAGER_INSTANCES:
                raise AddressOutOfRangeError("No more address for public manager component")
            idx = self.__greater(DHCP.DHCP_MANAGER_INSTANCES, DHCP.MIN_PUBLIC_ID)
            DHCP.DHCP_MANAGER_INSTANCES[idx] = self
            return idx
        elif component.type == DHCP.IDX_TYPE_PROVIDER:
            if DHCP.MAX_PUBLIC_ID in self.providers_ids:
                raise AddressOutOfRangeError("No more address for provider component")
            idx = self.__greater(self.providers_ids, DHCP.MIN_PUBLIC_ID)
            self.providers_ids[idx] = component
            return idx
        elif component.type == DHCP.IDX_TYPE_OPERATOR:
            if DHCP.MAX_PUBLIC_ID in self.registries_ids:
                raise AddressOutOfRangeError("No more address for registery component")
            idx = self.__greater(self.registries_ids, DHCP.MIN_PUBLIC_ID)
            self.registries_ids[idx] = component
            return idx
        elif component.type == DHCP.IDX_TYPE_BINDER:
            if DHCP.MAX_PUBLIC_ID in self.binders_ids:
                raise AddressOutOfRangeError("No more address for binder component")
            idx = self.__greater(self.binders_ids, DHCP.MIN_PUBLIC_ID)
            self.binders_ids[idx] = component
            return idx
        else:
            raise ComponentTypeError("No component type for {}".format(component.type))
        
    def __greater(self, _dict, _min):
        if len(_dict) == 0:
            return _min
        return max(_dict.keys(), key=int) + 1

