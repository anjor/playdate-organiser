from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_playdate, crud_child
from app.models.user import User
from app.schemas import Playdate, PlaydateCreate, PlaydateUpdate

router = APIRouter()


@router.get("/", response_model=List[Playdate])
def read_playdates(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    playdates = crud_playdate.get_filtered_for_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return playdates


@router.get("/my", response_model=List[Playdate])
def read_my_playdates(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    playdates = crud_playdate.get_by_parent(
        db, parent_id=current_user.id, skip=skip, limit=limit
    )
    return playdates


@router.post("/", response_model=Playdate)
def create_playdate(
    *,
    db: Session = Depends(deps.get_db),
    playdate_in: PlaydateCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Verify the child belongs to the current user
    child = crud_child.get(db, id=playdate_in.child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    if child.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    playdate = crud_playdate.create_with_parent(
        db, obj_in=playdate_in, parent_id=current_user.id
    )
    return playdate


@router.get("/{playdate_id}", response_model=Playdate)
def read_playdate(
    *,
    db: Session = Depends(deps.get_db),
    playdate_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    playdate = crud_playdate.get(db, id=playdate_id)
    if not playdate:
        raise HTTPException(status_code=404, detail="Playdate not found")
    # TODO: Add filtering logic here too
    return playdate


@router.put("/{playdate_id}", response_model=Playdate)
def update_playdate(
    *,
    db: Session = Depends(deps.get_db),
    playdate_id: int,
    playdate_in: PlaydateUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    playdate = crud_playdate.get(db, id=playdate_id)
    if not playdate:
        raise HTTPException(status_code=404, detail="Playdate not found")
    if playdate.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    playdate = crud_playdate.update(db, db_obj=playdate, obj_in=playdate_in)
    return playdate


@router.delete("/{playdate_id}", response_model=Playdate)
def delete_playdate(
    *,
    db: Session = Depends(deps.get_db),
    playdate_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    playdate = crud_playdate.get(db, id=playdate_id)
    if not playdate:
        raise HTTPException(status_code=404, detail="Playdate not found")
    if playdate.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    playdate = crud_playdate.remove(db, id=playdate_id)
    return playdate