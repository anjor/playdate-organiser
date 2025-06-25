from pydantic import BaseModel

from app.models.user_list import ListType


class UserListBase(BaseModel):
    target_user_id: int
    list_type: ListType


class UserListCreate(UserListBase):
    pass


class UserListInDBBase(UserListBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserList(UserListInDBBase):
    pass