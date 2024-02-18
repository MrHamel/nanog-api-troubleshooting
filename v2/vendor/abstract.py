from abc import ABC, abstractmethod

from models.data.facts import Device_Facts

'''
This file will contain the necessary abstractions for working with various
vendors. Not all vendors will need all classes. This will also help in
various scripts when it needs to know if its capable of X feature set by
way of 'if isinstance(variable, L3)' branching.
'''

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