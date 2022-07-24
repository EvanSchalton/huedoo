from pydantic import BaseModel


class ResourceSegmentItem(BaseModel):
    length: int
    start: int
