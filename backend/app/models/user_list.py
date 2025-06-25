from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class ListType(str, enum.Enum):
    ALLOWLIST = "allowlist"
    DENYLIST = "denylist"


class UserList(Base):
    __tablename__ = "user_lists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    list_type = Column(Enum(ListType), nullable=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="user_lists")
    target_user = relationship("User", foreign_keys=[target_user_id], back_populates="targeted_lists")