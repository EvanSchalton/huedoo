from pydantic import BaseModel  # type:ignore
from .location import Location
from .channel_member import ChannelMember


class ResourceChannel(BaseModel):
    channel_id: int
    position: Location
    members: list[ChannelMember]
