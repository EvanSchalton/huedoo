from pydantic import BaseModel
from .resource_service import ResourceService


class ResourceConfigurationWhere(BaseModel):
    group: ResourceService
