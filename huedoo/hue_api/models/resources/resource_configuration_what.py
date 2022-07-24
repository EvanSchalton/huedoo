from pydantic import BaseModel
from .resource_service import ResourceService


class ResourceConfigurationWhat(BaseModel):
    group: ResourceService
    recall: ResourceService
