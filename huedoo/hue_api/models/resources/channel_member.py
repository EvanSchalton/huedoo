from pydantic import BaseModel
from .resource_service import ResourceService


class ChannelMember(BaseModel):
    index: int
    service: ResourceService
