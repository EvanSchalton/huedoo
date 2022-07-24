from pydantic import BaseModel


class ResourceButton(BaseModel):
    last_event: str  # TODO: Enum
