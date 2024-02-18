from abc import ABC, abstractmethod

from models.data.facts import Device_Facts

class Firmware(ABC):
    @abstractmethod
    async def get_facts(self) -> Device_Facts:
        pass

class Hardware(ABC):
    pass

class L2(ABC):
    pass

class L3(ABC):
    pass

class Routing(ABC):
    pass