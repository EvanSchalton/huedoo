from pydantic import BaseModel
from .service_location import ServiceLocation


class ResourceLocation(BaseModel):
    service_locations: list[ServiceLocation]
