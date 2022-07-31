from typing import Optional
from pydantic import BaseModel  # type:ignore
from .product_name import ProductName


class ResourceProductData(BaseModel):
    certified: bool
    hardware_platform_type: Optional[str] = None
    manufacturer_name: str
    model_id: str
    product_archetype: str
    product_name: ProductName
    software_version: str

    class Config:
        use_enum_values = False
