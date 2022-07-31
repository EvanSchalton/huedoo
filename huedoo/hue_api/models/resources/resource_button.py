from pydantic import BaseModel  # type:ignore


class ResourceButton(BaseModel):
    last_event: str  # TODO: Enum

    class Config:
        use_enum_values = False
