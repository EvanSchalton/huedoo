from typing import Optional
from pydantic import BaseModel  # type:ignore


class ResourceDynamics(BaseModel):
    speed: Optional[float] = None
    speed_valid: Optional[bool] = None
    status: Optional[str] = None
    status_values: Optional[list[str]] = None

    class Config:
        use_enum_values = False
