from typing import Optional
from pydantic import BaseModel  # type:ignore
from .resource_mirek_schema import ResourceMirekSchema


class ResourceColorTemperature(BaseModel):
    mirek: Optional[int]
    mirek_schema: Optional[ResourceMirekSchema] = None
    mirek_valid: Optional[bool] = None

    class Config:
        use_enum_values = False
