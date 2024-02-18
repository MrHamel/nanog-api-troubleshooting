from pydantic import BaseModel, Field
from typing import *

class Device_SW_Ver(BaseModel):
    major: int = Field(gt=0)
    minor: int = Field(gt=0)
    build: Optional[int] = Field(gt=0)
    special: Optional[str]

class Device_Facts(BaseModel):
    cmd_style: Optional[str]
    hw_rev: str
    mac_addr: str
    make: str
    model: str
    serial: str
    version: Device_SW_Ver
    uptime: int = Field(gt=0)