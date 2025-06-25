from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    school_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    children = relationship("Child", back_populates="parent", cascade="all, delete-orphan")
    playdates = relationship("Playdate", back_populates="parent", cascade="all, delete-orphan")
    interests = relationship("Interest", back_populates="parent", cascade="all, delete-orphan")
    user_lists = relationship("UserList", foreign_keys="UserList.user_id", back_populates="user", cascade="all, delete-orphan")
    targeted_lists = relationship("UserList", foreign_keys="UserList.target_user_id", back_populates="target_user")