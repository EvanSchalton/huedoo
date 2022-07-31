from typing import Optional
from pydantic import BaseModel, Field


class SchemaRef(BaseModel):
    ref: Optional[str] = Field(alias="$ref", default=None)

    class Config:
        use_enum_values = False
