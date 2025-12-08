"""
Chef routes
"""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement chef routes
@router.get("/")
async def get_chefs():
    """Get all chefs"""
    return {"message": "Get all chefs endpoint"}
from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import get_db
from app.models.chef import Chef
from app.models.user import User, UserRole

router = APIRouter()  # Creating a router for chef endpoints


class ChefUpdate(BaseModel):
    hourly_rate: float = None  # Defining updatable chef fields


def _get_user_from_token(db: Session, token: str):
    return db.query(User).filter(User.email == token).first()  # Looking up user by token (email)


@router.patch("/{chef_id}")
def update_chef(chef_id: int, payload: ChefUpdate, db: Session = Depends(get_db), Authorization: str | None = Header(None)):
    """Updating chef fields such as hourly_rate; using simple token auth via Authorization header."""
    token = Authorization.replace("Bearer ", "") if Authorization else ""  # Extracting token from header
    user = _get_user_from_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    chef = db.query(Chef).filter(Chef.id == chef_id).first()
    if not chef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chef not found")

    if chef.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if payload.hourly_rate is not None:
        chef.hourly_rate = payload.hourly_rate  # Updating chef hourly_rate
    db.add(chef)
    db.commit()
    db.refresh(chef)
    return chef.to_dict()
