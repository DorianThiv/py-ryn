
class ComponentTypeError(Exception):
    pass
    
class AddressOutOfRangeError(Exception):
    pass
    
class DHCP:
    
    IDX_TYPE_MANAGER = 0
    IDX_TYPE_PROVIDER = 1
    IDX_TYPE_REGISTRY = 2
    IDX_TYPE_BINDER = 3

    IDX_TYPE_PRIVATE_MANAGER = 4
    IDX_TYPE_PUBLIC_MANAGER = 5
    
    NULL_ID = 0
    CORE_ID = 1
    BROADCAST_ID = 255
    
    MIN_PRIVATE_ID = 2
    MAX_PRIVATE_ID = 49
    MIN_PUBLIC_ID = 50
    MAX_PUBLIC_ID = 254
    
    def __init__(self):
        self.managers_private_ids = {}
        self.managers_public_ids = {}
        self.providers_ids = {}
        self.registries_ids = {}
        self.binders_ids = {}
    
    def discover(self, component_type, callback=None):
        if component_type == DHCP.IDX_TYPE_PUBLIC_MANAGER or component_type == DHCP.IDX_TYPE_MANAGER:
            if DHCP.MAX_PUBLIC_ID in self.managers_public_ids:
                raise AddressOutOfRangeError("No more address for public manager component")
            idx = self.__greater(self.managers_public_ids, DHCP.MIN_PUBLIC_ID) + 1
            self.managers_public_ids[idx] = component_type
            return idx
        if component_type == DHCP.IDX_TYPE_PRIVATE_MANAGER:
            if DHCP.MAX_PRIVATE_ID in self.managers_private_ids:
                raise AddressOutOfRangeError("No more address for private manager component")
            idx = self.__greater(self.managers_private_ids, DHCP.MIN_PRIVATE_ID) + 1
            self.managers_private_ids[idx] = component_type
            return idx
        elif component_type == DHCP.IDX_TYPE_PROVIDER:
            if DHCP.MAX_PUBLIC_ID in self.providers_ids:
                raise AddressOutOfRangeError("No more address for provider component")
            idx = self.__greater(self.providers_ids, DHCP.MIN_PRIVATE_ID) + 1
            self.providers_ids[idx] = component_type
            return idx
        elif component_type == DHCP.IDX_TYPE_REGISTRY:
            if DHCP.MAX_PUBLIC_ID in self.registries_ids:
                raise AddressOutOfRangeError("No more address for registery component")
            idx = self.__greater(self.registries_ids, DHCP.MIN_PRIVATE_ID) + 1
            self.registries_ids[idx] = component_type
            return idx
        elif component_type == DHCP.IDX_TYPE_BINDER:
            if DHCP.MAX_PUBLIC_ID in self.binders_ids:
                raise AddressOutOfRangeError("No more address for binder component")
            idx = self.__greater(self.binders_ids, DHCP.MIN_PRIVATE_ID) + 1
            self.binders_ids[idx] = component_type
            return idx
        else:
            raise ComponentTypeError("No component type for {}".format(component_type))
        
    def __greater(self, _dict, _min):
        if len(_dict) == 0:
            return _min - 1
        return max(_dict, key=int)
		
