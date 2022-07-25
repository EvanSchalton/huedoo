from pydantic import BaseModel  # type:ignore


class ResourceSegmentItem(BaseModel):
    length: int
    start: int
