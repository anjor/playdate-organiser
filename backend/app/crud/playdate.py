from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_

from app.crud.base import CRUDBase
from app.models.playdate import Playdate, PlaydateStatus
from app.models.user_list import UserList, ListType
from app.schemas.playdate import PlaydateCreate, PlaydateUpdate


class CRUDPlaydate(CRUDBase[Playdate, PlaydateCreate, PlaydateUpdate]):
    def create_with_parent(
        self, db: Session, *, obj_in: PlaydateCreate, parent_id: int
    ) -> Playdate:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, parent_id=parent_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_filtered_for_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Playdate]:
        # Get user's denylisted users
        denylisted_users = db.query(UserList.target_user_id).filter(
            and_(
                UserList.user_id == user_id,
                UserList.list_type == ListType.DENYLIST
            )
        ).subquery()

        # Get users who have the current user on their allowlist
        users_with_allowlist = db.query(UserList.user_id).filter(
            UserList.list_type == ListType.ALLOWLIST
        ).distinct().subquery()

        users_who_allow_current = db.query(UserList.user_id).filter(
            and_(
                UserList.target_user_id == user_id,
                UserList.list_type == ListType.ALLOWLIST
            )
        ).subquery()

        # Build the query
        query = db.query(Playdate).filter(
            and_(
                Playdate.status == PlaydateStatus.ACTIVE,
                # Exclude playdates from denylisted users
                not_(Playdate.parent_id.in_(denylisted_users)),
                # Include playdates where:
                or_(
                    # The parent doesn't have an allowlist
                    not_(Playdate.parent_id.in_(users_with_allowlist)),
                    # Or the current user is on their allowlist
                    Playdate.parent_id.in_(users_who_allow_current),
                    # Or it's the user's own playdate
                    Playdate.parent_id == user_id
                )
            )
        )

        return query.offset(skip).limit(limit).all()

    def get_by_parent(
        self, db: Session, *, parent_id: int, skip: int = 0, limit: int = 100
    ) -> List[Playdate]:
        return (
            db.query(Playdate)
            .filter(Playdate.parent_id == parent_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_playdate = CRUDPlaydate(Playdate)