from enum import Enum
from typing import Optional
from pydantic import BaseModel


class DroppedItemType(str, Enum):
    file = "file"
    directory = "directory"
    url = "url"
    web_image = "web-image"
    unknown = "unknown"


class DroppedItem(BaseModel):
    type: DroppedItemType
    name: str
    mime_type: Optional[str] = None
    size: Optional[int] = None
    url: Optional[str] = None
    children: Optional[list[str]] = None


class DropPayload(BaseModel):
    items: list[DroppedItem]
