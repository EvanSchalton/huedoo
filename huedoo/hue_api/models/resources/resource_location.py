from pydantic import BaseModel  # type:ignore
from .service_location import ServiceLocation


class ResourceLocation(BaseModel):
    service_locations: list[ServiceLocation]

    class Config:
        use_enum_values = False
