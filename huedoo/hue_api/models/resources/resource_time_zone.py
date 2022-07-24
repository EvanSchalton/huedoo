from pydantic import BaseModel
from .time_zone import TimeZone


class ResourceTimeZone(BaseModel):
    time_zone: TimeZone
