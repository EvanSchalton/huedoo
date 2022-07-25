from typing import Optional
from pydantic import BaseModel  # type:ignore


class ResourceDimming(BaseModel):
    brightness: float
    min_dim_level: Optional[float] = None
