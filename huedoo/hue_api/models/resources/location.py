from pydantic import BaseModel


class Location(BaseModel):
    x: float
    y: float
    z: float
