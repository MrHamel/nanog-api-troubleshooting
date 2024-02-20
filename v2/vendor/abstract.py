from abc import ABCMeta, abstractmethod

from models.data.arp import ARP_Table
from models.data.facts import Device_Facts
from models.data.lldp import LLDP_Neighbor_Table
from models.data.nd import ND_Table
from models.data.security import Device_Banner

'''
This file will contain the necessary abstractions for working with various
vendors. Not all vendors will need all classes. This will also help in
various scripts when it needs to know if its capable of X feature set by
way of 'if isinstance(variable, L3)' branching.
'''

class Config_MGMT(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'commit_config') and 
                callable(subclass.commit_config) or 
                NotImplemented)

    @abstractmethod
    async def commit_config(self, parameters: list = []) -> bool:
        """Commit configuration changes to the device"""
        raise NotImplementedError

class Firmware(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_facts') and 
                callable(subclass.get_facts) or 
                NotImplemented)

    @abstractmethod
    async def get_facts(self) -> Device_Facts:
        """Get very basic information about a device"""
        raise NotImplementedError

class Hardware(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (NotImplemented)

class L2(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_lldp_neighbors') and 
                callable(subclass.get_lldp_neighbors) or 
                NotImplemented)

    @abstractmethod
    async def get_lldp_neighbors(self, type) -> LLDP_Neighbor_Table:
        """Return a list of LLDP neighbors"""
        raise NotImplementedError

class L3(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_arp_table') and 
                callable(subclass.get_arp_table) and
                hasattr(subclass, 'get_nd_table') and 
                callable(subclass.get_nd_table) or 
                NotImplemented)

    @abstractmethod
    async def get_arp_table(self) -> ARP_Table:
        """Get the devices IPv4 ARP table"""
        raise NotImplementedError

    @abstractmethod
    async def get_nd_table(self) -> ND_Table:
        """Get the IPv6 neighbors table"""
        raise NotImplementedError

class Routing(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (NotImplemented)

class Security(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_banner') and 
                callable(subclass.get_banner) or 
                NotImplemented)

    @abstractmethod
    async def get_banner(self, type) -> Device_Banner:
        """Retrieve the devices login or motd banner"""
        raise NotImplementedError