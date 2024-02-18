import aiosnmp
from .config import Config
from .log import Log
from vendor import *

class UnknownDeviceTypeException(Exception):
    pass

class Device:
    @staticmethod
    async def get(hostname: str, credentials: tuple):
        cfg: dict             = Config.get()
        entPhysicalDescr: str = ""
        sysDescr: str         = ""
        
        # Begin SNMP autodetection, to know what vendor class we need to return

        async with aiosnmp.Snmp(host=hostname, port=161, community=cfg["snmp"]["ro"], retries=2, timeout=1) as snmp:
            try:
                for res in await snmp.get(".1.3.6.1.2.1.1.1.0"):
                    sysDescr: str = res.value.decode("utf-8")
            except aiosnmp.exceptions.SnmpTimeoutError:
                pass

            try:
                for res in await snmp.get(".1.3.6.1.2.1.47.1.1.1.1.2.1"):
                    entPhysicalDescr: str = res.value.decode("utf-8")
            except aiosnmp.exceptions.SnmpTimeoutError:
                pass

        sysDescr: str          = sysDescr.lower()
        entPhysicalDescr: str  = entPhysicalDescr.lower()
        
        if ("arista" in sysDescr) or ("arista" in entPhysicalDescr or "ceoslab" in entPhysicalDescr):
            return Arista(hostname, credentials, cfg, Log.get())
        
        # We failed to get the vendor for this device, raise an alarm before problems arise
        raise UnknownDeviceTypeException(f"ERROR: Unable to identify vendor for {hostname}")
