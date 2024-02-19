from .abstract import *
import aioeapi
from logging import Logger

from models.data.arp import ARP_Entry, ARP_Table
from models.data.facts import Device_Facts, Device_SW_Ver
from models.data.lldp import LLDP_Neighbor_Entry, LLDP_Neighbor_Table
from models.data.nd import ND_Entry, ND_Table
from models.data.security import Device_Banner

class Arista(Config_MGMT, Firmware, Hardware, L2, L3, Routing):
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

    # Convert MAC address from Cisco dot Notation to standard colon uppercase format
    def __convert_mac__(mac: str) -> str:
        dot_mac = mac.replace(".", "")
        mac     = ":".join(a + b for a, b in zip(dot_mac[::2], dot_mac[1::2]))
        mac     = mac.upper()

        return mac

    async def commit_config(self, parameters: list = []) -> bool:
        data: dict = await self.dev.cli(commands=["enable", "write memory"])
        
        if data[1]["messages"][0].lower().startswith("copy completed successfully"):
            return True
        else:
            return False
        
    async def get_arp_table(self) -> ARP_Table:
        data: dict = await self.dev.cli("show ip arp")
        
        entries: list[ARP_Entry] = []
        arps: list = data["ipV4Neighbors"]
        
        for entry in arps:
            mac = self.__convert_mac__(entry["hwAddress"])

            entries.append(ARP_Entry(address=entry["address"], age=entry["age"],
                                        interface=entry["interface"], mac=mac))

        return ARP_Table(entries=entries)

    async def get_banner(self, type) -> Device_Banner:
        if type not in ["login", "motd"]:
            return Device_Banner(type="", content="")

        data: dict = await self.dev.cli(commands=["enable", f"show banner {type}"])
        
        if type in data[1].keys():
            return Device_Banner(type=type, content=data[1][type])
        else:
            return Device_Banner(type="", content="")

    async def get_facts(self) -> Device_Facts:
        data: dict = await self.dev.cli("show version")
        
        ver_breakdown: list = data["version"].split(".")
        
        if len(ver_breakdown) == 2:
            fw: Device_SW_Ver = Device_SW_Ver(major=int(ver_breakdown[0]), minor=int(ver_breakdown[1]))
        elif len(ver_breakdown) == 3:
            fw: Device_SW_Ver = Device_SW_Ver(major=int(ver_breakdown[0]), minor=int(ver_breakdown[1]),
                                                build=ver_breakdown[3])
        elif len(ver_breakdown) == 4:
            fw: Device_SW_Ver = Device_SW_Ver(major=int(ver_breakdown[0]), minor=int(ver_breakdown[1]),
                                                build=ver_breakdown[2], special=ver_breakdown[3])
            
        cmd_style: str = "new"
        
        if fw.major == 4 and fw.minor <= 20:
            cmd_style = "old"

        virtual: bool = False
        
        if "cEOS" in data["modelName"] or "vEOS" in data["modelName"] or "CloudEOS" in data["modelName"]:
            virtual = True
            
        data2: dict = await self.dev.cli("show hostname")
        hostname = data2["hostname"]

        facts: Device_Facts = Device_Facts(cmd_style=cmd_style, hostname=hostname,
                                            hw_rev=data["hardwareRevision"],
                                            mac_addr=data["systemMacAddress"], make="Arista",
                                            model=data["modelName"], serial=data["serialNumber"],
                                            version=fw, virtual=virtual, uptime=int(data["uptime"]))
        
        return facts
    
    async def get_lldp_neighbors(self, type) -> LLDP_Neighbor_Table:
        data: dict = await self.dev.cli("show lldp neighbors")
        
        entries: list[LLDP_Neighbor_Entry] = []
        neighbors: list = data["lldpNeighbors"]
        
        for entry in neighbors:
            entries.append(LLDP_Neighbor_Entry(neighbor_device=entry["neighborDevice"],
                                                    neighbor_interface=entry["neighborPort"],
                                                    interface=entry["port"], ttl=entry["ttl"]))
            
        return LLDP_Neighbor_Table(entries=entries)
    
    async def get_nd_table(self) -> ND_Table:
        data: dict = await self.dev.cli("show ipv6 neighbors")
        
        entries: list[ND_Entry] = []
        arps: list = data["ipV6Neighbors"]
        
        for entry in arps:
            mac = self.__convert_mac__(entry["hwAddress"])

            entries.append(ND_Entry(address=entry["address"], age=entry["age"],
                                        interface=entry["interface"], mac=mac, state=entry["state"]))

        return ND_Table(entries=entries)