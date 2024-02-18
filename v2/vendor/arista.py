from .abstract import *
import aioeapi
from logging import Logger

from models.data.facts import Device_Facts, Device_SW_Ver

class Arista(Firmware, Hardware, L2, L3, Routing):
    '''
    This is a vendor class. It will contain the necessary code to required
    to interact with a device. All functions outside magic functions
    (__init__ really), should come from the abstract classes set above.
    
    It is mandatory that functions return a Pydantic model defined in the
    models/data folder, to maintain a known data structure for the output
    models to parse very easily.
    '''

    cfg: dict           = {}
    dev: aioeapi.Device = None
    log: Logger         = None
    
    def __init__(self, hostname: str, credentials: tuple, cfg: dict, log: Logger):
        username, password = credentials
        
        self.cfg = cfg
        self.dev = aioeapi.Device(hostname, username, password, timeout=180)
        self.log = log

    async def get_facts(self) -> Device_Facts:
        data: dict = await self.dev.cli("show version")
        
        ver_breakdown: list = data["version"].split(".")
        
        if len(ver_breakdown) == 2:
            fw: Device_SW_Ver = Device_SW_Ver(major=int(ver_breakdown[0]), minor=int(ver_breakdown[1]))
        elif len(ver_breakdown) == 3:
            fw: Device_SW_Ver = Device_SW_Ver(major=int(ver_breakdown[0]), minor=int(ver_breakdown[1]), build=ver_breakdown[3])
        elif len(ver_breakdown) == 4:
            fw: Device_SW_Ver = Device_SW_Ver(major=int(ver_breakdown[0]), minor=int(ver_breakdown[1]), build=ver_breakdown[2], special=ver_breakdown[3])
            
        cmd_style: str = "new"
        
        if fw.major == 4 and fw.minor <= 20:
            cmd_style = "old"

        virtual: bool = False
        
        if "cEOS" in data["modelName"] or "vEOS" in data["modelName"] or "CloudEOS" in data["modelName"]:
            virtual = True

        facts: Device_Facts = Device_Facts(cmd_style=cmd_style, hw_rev=data["hardwareRevision"], mac_addr=data["systemMacAddress"], make="Arista",
                            model=data["modelName"], serial=data["serialNumber"], version=fw, virtual=virtual, uptime=int(data["uptime"]))
        
        return facts