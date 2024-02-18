'''
This file will contain all the names of vendors another file will load in
when they specify the "*" on import. To do this, the class must be
imported here, and the class name in string must be appended to __all__.
'''

from .arista import Arista

__all__ = ["Arista"]