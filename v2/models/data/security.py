from pydantic import BaseModel, Field
from typing import *

class Device_Banner(BaseModel):
    type: str
    content: str