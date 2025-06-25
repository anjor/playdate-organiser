from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_child
from app.models.user import User
from app.schemas import Child, ChildCreate, ChildUpdate

router = APIRouter()


@router.get("/", response_model=List[Child])
def read_children(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    children = crud_child.get_by_parent(db, parent_id=current_user.id)
    return children


@router.post("/", response_model=Child)
def create_child(
    *,
    db: Session = Depends(deps.get_db),
    child_in: ChildCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    child = crud_child.create_with_parent(db, obj_in=child_in, parent_id=current_user.id)
    return child


@router.put("/{child_id}", response_model=Child)
def update_child(
    *,
    db: Session = Depends(deps.get_db),
    child_id: int,
    child_in: ChildUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    child = crud_child.get(db, id=child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    if child.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    child = crud_child.update(db, db_obj=child, obj_in=child_in)
    return child


@router.delete("/{child_id}", response_model=Child)
def delete_child(
    *,
    db: Session = Depends(deps.get_db),
    child_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    child = crud_child.get(db, id=child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    if child.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    child = crud_child.remove(db, id=child_id)
    return child