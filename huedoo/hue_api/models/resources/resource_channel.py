from pydantic import BaseModel
from .location import Location
from .channel_member import ChannelMember


class ResourceChannel(BaseModel):
    channel_id: int
    position: Location
    members: list[ChannelMember]
