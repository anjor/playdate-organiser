from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class PlaydateStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Playdate(Base):
    __tablename__ = "playdates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    date_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(PlaydateStatus), default=PlaydateStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("Child", back_populates="playdates")
    parent = relationship("User", back_populates="playdates")
    interests = relationship("Interest", back_populates="playdate", cascade="all, delete-orphan")