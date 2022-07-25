from pydantic import BaseModel  # type:ignore


class Location(BaseModel):
    x: float
    y: float
    z: float
