from pydantic import BaseModel  # type:ignore
from .resource_service import ResourceService


class ResourceConfigurationDepends(BaseModel):
    level: str  # TODO: Enum
    target: ResourceService
    type: str

    class Config:
        use_enum_values = False
