from pydantic import BaseModel  # type:ignore


class ResourceColorGamut(BaseModel):
    x: float
    y: float

    class Config:
        use_enum_values = False
