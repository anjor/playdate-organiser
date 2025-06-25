from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.models.playdate import PlaydateStatus


class PlaydateBase(BaseModel):
    title: str
    description: Optional[str] = None
    date_time: datetime
    location: str
    child_id: int


class PlaydateCreate(PlaydateBase):
    pass


class PlaydateUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date_time: Optional[datetime] = None
    location: Optional[str] = None
    status: Optional[PlaydateStatus] = None


class PlaydateInDBBase(PlaydateBase):
    id: int
    parent_id: int
    status: PlaydateStatus
    created_at: datetime

    class Config:
        from_attributes = True


class Playdate(PlaydateInDBBase):
    pass