from uuid import UUID
from pydantic import BaseModel  # type:ignore
from .resource_type import ResourceType


class ResourceService(BaseModel):
    rid: UUID
    rtype: ResourceType
