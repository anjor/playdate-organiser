from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.interest import Interest
from app.schemas.interest import InterestCreate


class CRUDInterest(CRUDBase[Interest, InterestCreate, InterestCreate]):
    def create_with_parent(
        self, db: Session, *, obj_in: InterestCreate, parent_id: int
    ) -> Interest:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, parent_id=parent_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_playdate_and_parent(
        self, db: Session, *, playdate_id: int, parent_id: int
    ) -> Optional[Interest]:
        return (
            db.query(Interest)
            .filter(
                Interest.playdate_id == playdate_id,
                Interest.parent_id == parent_id
            )
            .first()
        )

    def get_by_playdate(
        self, db: Session, *, playdate_id: int
    ) -> List[Interest]:
        return db.query(Interest).filter(Interest.playdate_id == playdate_id).all()

    def get_by_parent(
        self, db: Session, *, parent_id: int
    ) -> List[Interest]:
        return db.query(Interest).filter(Interest.parent_id == parent_id).all()


crud_interest = CRUDInterest(Interest)