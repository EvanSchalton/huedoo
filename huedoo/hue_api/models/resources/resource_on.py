from pydantic import BaseModel  # type:ignore


class ResourceOn(BaseModel):
    on: bool
