from pydantic import BaseModel, Field
from typing import *

class LLDP_Neighbor_Entry(BaseModel):
    neighbor_device: str
    neighbor_interface: str
    interface: str
    ttl: Optional[int]
    
class LLDP_Neighbor_Table(BaseModel):
    entries: List[LLDP_Neighbor_Entry]