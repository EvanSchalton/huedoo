from pydantic import BaseModel  # type:ignore
from .resource_service import ResourceService


class ResourceStreamProxy(BaseModel):
    mode: str  # TODO: Enum
    node: ResourceService
