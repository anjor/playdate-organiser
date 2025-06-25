from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_interest, crud_playdate
from app.models.user import User
from app.schemas import Interest, InterestCreate

router = APIRouter()


@router.post("/", response_model=Interest)
def express_interest(
    *,
    db: Session = Depends(deps.get_db),
    interest_in: InterestCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Verify playdate exists
    playdate = crud_playdate.get(db, id=interest_in.playdate_id)
    if not playdate:
        raise HTTPException(status_code=404, detail="Playdate not found")
    
    # Check if user already expressed interest
    existing = crud_interest.get_by_playdate_and_parent(
        db, playdate_id=interest_in.playdate_id, parent_id=current_user.id
    )
    if existing:
        raise HTTPException(status_code=400, detail="Interest already expressed")
    
    # Can't express interest in own playdate
    if playdate.parent_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot express interest in own playdate")
    
    interest = crud_interest.create_with_parent(
        db, obj_in=interest_in, parent_id=current_user.id
    )
    return interest


@router.get("/my", response_model=List[Interest])
def read_my_interests(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    interests = crud_interest.get_by_parent(db, parent_id=current_user.id)
    return interests


@router.get("/playdate/{playdate_id}", response_model=List[Interest])
def read_playdate_interests(
    *,
    db: Session = Depends(deps.get_db),
    playdate_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Verify the playdate belongs to the current user
    playdate = crud_playdate.get(db, id=playdate_id)
    if not playdate:
        raise HTTPException(status_code=404, detail="Playdate not found")
    if playdate.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    interests = crud_interest.get_by_playdate(db, playdate_id=playdate_id)
    return interests


@router.delete("/{interest_id}", response_model=Interest)
def withdraw_interest(
    *,
    db: Session = Depends(deps.get_db),
    interest_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    interest = crud_interest.get(db, id=interest_id)
    if not interest:
        raise HTTPException(status_code=404, detail="Interest not found")
    if interest.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    interest = crud_interest.remove(db, id=interest_id)
    return interest