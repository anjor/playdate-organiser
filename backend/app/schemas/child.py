from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ChildBase(BaseModel):
    name: str
    year_group: str
    age: int


class ChildCreate(ChildBase):
    pass


class ChildUpdate(BaseModel):
    name: Optional[str] = None
    year_group: Optional[str] = None
    age: Optional[int] = None


class ChildInDBBase(ChildBase):
    id: int
    parent_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Child(ChildInDBBase):
    pass