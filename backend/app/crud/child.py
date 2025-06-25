from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.child import Child
from app.schemas.child import ChildCreate, ChildUpdate


class CRUDChild(CRUDBase[Child, ChildCreate, ChildUpdate]):
    def get_by_parent(self, db: Session, *, parent_id: int) -> List[Child]:
        return db.query(Child).filter(Child.parent_id == parent_id).all()

    def create_with_parent(
        self, db: Session, *, obj_in: ChildCreate, parent_id: int
    ) -> Child:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, parent_id=parent_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_child = CRUDChild(Child)