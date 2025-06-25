from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    year_group = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    parent = relationship("User", back_populates="children")
    playdates = relationship("Playdate", back_populates="child", cascade="all, delete-orphan")