from pydantic import BaseModel  # type:ignore
from .time_zone import TimeZone


class ResourceTimeZone(BaseModel):
    time_zone: TimeZone

    class Config:
        use_enum_values = False
