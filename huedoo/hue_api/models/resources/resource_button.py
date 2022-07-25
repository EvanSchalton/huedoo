from pydantic import BaseModel  # type:ignore


class ResourceButton(BaseModel):
    last_event: str  # TODO: Enum
