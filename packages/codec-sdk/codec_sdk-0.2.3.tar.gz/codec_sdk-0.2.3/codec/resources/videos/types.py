from typing import Union, Optional, Any
from pydantic import BaseModel


class VideoObject(BaseModel):
    uid: str
    collection: Optional[Union[str, Any]] = None
    created_at: str
    video_url: Optional[str] = None
    duration: int
    dimensions: list[int]
    aspect_ratio: str
    codec: str


class VideoStatusObject(BaseModel):
    status: str
    video: str


class PreUploadedVideoObject(BaseModel):
    video: str
    signed_upload_url: str
    token: str
    path: str

