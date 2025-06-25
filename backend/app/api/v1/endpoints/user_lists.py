from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_user_list, crud_user
from app.models.user import User
from app.models.user_list import ListType
from app.schemas import UserList, UserListCreate

router = APIRouter()


@router.get("/allowlist", response_model=List[UserList])
def read_allowlist(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return crud_user_list.get_by_user_and_type(
        db, user_id=current_user.id, list_type=ListType.ALLOWLIST
    )


@router.get("/denylist", response_model=List[UserList])
def read_denylist(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return crud_user_list.get_by_user_and_type(
        db, user_id=current_user.id, list_type=ListType.DENYLIST
    )


@router.post("/", response_model=UserList)
def add_to_list(
    *,
    db: Session = Depends(deps.get_db),
    user_list_in: UserListCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Verify target user exists
    target_user = crud_user.get(db, id=user_list_in.target_user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")
    
    # Can't add self to list
    if user_list_in.target_user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot add yourself to list")
    
    # Check if already exists
    existing = crud_user_list.get_by_user_and_target(
        db, user_id=current_user.id, target_user_id=user_list_in.target_user_id
    )
    if existing:
        # Update the list type if different
        if existing.list_type != user_list_in.list_type:
            existing.list_type = user_list_in.list_type
            db.add(existing)
            db.commit()
            db.refresh(existing)
            return existing
        else:
            raise HTTPException(status_code=400, detail="User already in list")
    
    user_list = crud_user_list.create_with_user(
        db, obj_in=user_list_in, user_id=current_user.id
    )
    return user_list


@router.delete("/{list_id}", response_model=UserList)
def remove_from_list(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    user_list = crud_user_list.get(db, id=list_id)
    if not user_list:
        raise HTTPException(status_code=404, detail="List entry not found")
    if user_list.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user_list = crud_user_list.remove(db, id=list_id)
    return user_list