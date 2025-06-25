from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    playdate_id = Column(Integer, ForeignKey("playdates.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    playdate = relationship("Playdate", back_populates="interests")
    parent = relationship("User", back_populates="interests")