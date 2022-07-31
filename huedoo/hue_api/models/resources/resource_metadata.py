from typing import Optional
from pydantic import BaseModel  # type:ignore


class ResourceMetadata(BaseModel):
    archetype: Optional[str] = None
    name: Optional[str] = None
    control_id: Optional[int] = None
    category: Optional[str] = None  # TODO: Enum

    class Config:
        use_enum_values = False
