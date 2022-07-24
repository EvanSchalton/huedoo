from typing import Optional
from pydantic import BaseModel


class ResourceDimming(BaseModel):
    brightness: float
    min_dim_level: Optional[float] = None
