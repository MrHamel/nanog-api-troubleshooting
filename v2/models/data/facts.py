from pydantic import BaseModel, Field
from typing import *

class Device_SW_Ver(BaseModel):
    '''
    A store for device software version.
    '''
    major: int = Field(gt=0)
    minor: int = Field(gt=0)
    build: Optional[str]
    special: Optional[str]

class Device_Facts(BaseModel):
    '''
    A store for basic information about a device.
    '''
    cmd_style: Optional[str]
    hw_rev: str
    mac_addr: str
    make: str
    model: str
    serial: str
    version: Device_SW_Ver
    virtual: bool
    uptime: int = Field(gt=0)