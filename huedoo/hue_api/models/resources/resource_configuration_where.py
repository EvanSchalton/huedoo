from pydantic import BaseModel  # type:ignore
from .resource_service import ResourceService


class ResourceConfigurationWhere(BaseModel):
    group: ResourceService

    class Config:
        use_enum_values = False
