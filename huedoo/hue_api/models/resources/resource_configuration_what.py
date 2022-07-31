from pydantic import BaseModel  # type:ignore
from .resource_service import ResourceService


class ResourceConfigurationWhat(BaseModel):
    group: ResourceService
    recall: ResourceService

    class Config:
        use_enum_values = False
