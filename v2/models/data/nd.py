from pydantic import BaseModel, Field
from typing import *

class ND_Entry(BaseModel):
    address: str
    age: int
    interface: str
    mac: str
    state: str

class ND_Table(BaseModel):
    entries: List[ND_Entry]