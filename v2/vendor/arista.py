from .abstract import *
import aioeapi
from logging import Logger

class Arista(Firmware, Hardware, L2, L3, Routing):
    cfg: dict           = {}
    dev: aioeapi.Device = None
    log: Logger         = None
    
    def __init__(self, hostname: str, credentials: tuple, cfg: dict, log: Logger):
        username, password = credentials
        
        self.cfg = cfg
        self.dev = aioeapi.Device(hostname, username, password, timeout=180)
        self.log = log
