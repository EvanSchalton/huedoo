from typing import Optional
from pydantic import BaseModel  # type:ignore
from .gamut_color import GamutColor
from .resource_color_gamut import ResourceColorGamut
from .gamut_type import GamutType


class ResourceColor(BaseModel):
    gamut: Optional[dict[GamutColor, ResourceColorGamut]] = None
    gamut_type: Optional[GamutType] = None
    xy: Optional[ResourceColorGamut] = None

    class Config:
        use_enum_values = False
