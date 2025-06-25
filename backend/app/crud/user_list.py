from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_list import UserList, ListType
from app.schemas.user_list import UserListCreate


class CRUDUserList(CRUDBase[UserList, UserListCreate, UserListCreate]):
    def create_with_user(
        self, db: Session, *, obj_in: UserListCreate, user_id: int
    ) -> UserList:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user_and_target(
        self, db: Session, *, user_id: int, target_user_id: int
    ) -> Optional[UserList]:
        return (
            db.query(UserList)
            .filter(
                UserList.user_id == user_id,
                UserList.target_user_id == target_user_id
            )
            .first()
        )

    def get_by_user_and_type(
        self, db: Session, *, user_id: int, list_type: ListType
    ) -> List[UserList]:
        return (
            db.query(UserList)
            .filter(
                UserList.user_id == user_id,
                UserList.list_type == list_type
            )
            .all()
        )


crud_user_list = CRUDUserList(UserList)