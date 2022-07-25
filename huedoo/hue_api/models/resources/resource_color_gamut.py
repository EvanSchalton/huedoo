from pydantic import BaseModel  # type:ignore


class ResourceColorGamut(BaseModel):
    x: float
    y: float
