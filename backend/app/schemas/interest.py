from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class InterestBase(BaseModel):
    playdate_id: int
    message: Optional[str] = None


class InterestCreate(InterestBase):
    pass


class InterestInDBBase(InterestBase):
    id: int
    parent_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Interest(InterestInDBBase):
    pass