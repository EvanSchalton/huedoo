from pydantic import BaseModel
from .resource_service import ResourceService


class ResourceStreamProxy(BaseModel):
    mode: str  # TODO: Enum
    node: ResourceService
