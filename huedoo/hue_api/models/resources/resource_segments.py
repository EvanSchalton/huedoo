from pydantic import BaseModel  # type:ignore
from .resource_segment_item import ResourceSegmentItem


class ResourceSegments(BaseModel):
    configurable: bool
    max_segments: int
    segments: list[ResourceSegmentItem]
