from pydantic import BaseModel
from .resource_service import ResourceService


class ResourceConfigurationDepends(BaseModel):
    level: str  # TODO: Enum
    target: ResourceService
    type: str
