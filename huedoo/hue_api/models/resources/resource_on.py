from pydantic import BaseModel  # type:ignore


class ResourceOn(BaseModel):
    on: bool

    class Config:
        use_enum_values = False
