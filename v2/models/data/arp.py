from pydantic import BaseModel, Field
from typing import *

class ARP_Entry(BaseModel):
    address: str
    age: int
    interface: str
    mac: str

class ARP_Table(BaseModel):
    entries: List[ARP_Entry]