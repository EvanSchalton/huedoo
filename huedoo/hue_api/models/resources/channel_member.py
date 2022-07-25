from pydantic import BaseModel  # type:ignore
from .resource_service import ResourceService


class ChannelMember(BaseModel):
    index: int
    service: ResourceService
