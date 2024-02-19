from abc import ABC, abstractmethod

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

class Config_MGMT(ABC):
    @abstractmethod
    async def commit_config(self, parameters: list = []) -> bool:
        pass

class Firmware(ABC):
    @abstractmethod
    async def get_facts(self) -> Device_Facts:
        pass

class Hardware(ABC):
    pass

class L2(ABC):
    @abstractmethod
    async def get_lldp_neighbors(self, type) -> LLDP_Neighbor_Table:
        pass

class L3(ABC):
    @abstractmethod
    async def get_arp_table(self) -> ARP_Table:
        pass
    
    @abstractmethod
    async def get_nd_table(self) -> ND_Table:
        pass

class Routing(ABC):
    pass

class Security(ABC):
    @abstractmethod
    async def get_banner(self, type) -> Device_Banner:
        pass