from fastapi import APIRouter, Depends, HTTPException, status, Header  # Creating endpoints and dependency helpers
from pydantic import BaseModel  # Defining request schema
from typing import Optional
from sqlalchemy.orm import Session  # Typing DB session
from jose import jwt, JWTError  # Decoding JWT tokens
from app import get_db  # Getting DB session
from app.models.chef import Chef  # Chef model
from app.models.user import User  # User model for owner checks
from config.settings import settings  # Loading JWT settings

router = APIRouter()  # Creating chef router


class ChefUpdateSchema(BaseModel):
    bio: Optional[str] = None
    cuisines: Optional[str] = None
    specialties: Optional[str] = None
    hourly_rate: Optional[float] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    years_of_experience: Optional[int] = None
    is_available: Optional[bool] = None


def get_current_user_from_token(authorization: Optional[str], db: Session):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization")
    scheme, _, token = authorization.partition(" ")  # Parsing Bearer token
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth header")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # Decoding token
        user_id = int(payload.get("sub"))
    except (JWTError, Exception):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.get("/{chef_id}")  # Returning chef profile by id
def get_chef(chef_id: int, db: Session = Depends(get_db)):
    chef = db.query(Chef).get(chef_id)
    if not chef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chef not found")
    return chef.to_dict()


@router.patch("/{chef_id}")  # Updating chef profile; only owner allowed
def update_chef(chef_id: int, payload: ChefUpdateSchema, Authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user = get_current_user_from_token(Authorization, db)  # Authenticating user
    chef = db.query(Chef).get(chef_id)
    if not chef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chef not found")
    if chef.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not owner of this profile")

    data = payload.dict(exclude_unset=True)
    if "hourly_rate" in data and (data["hourly_rate"] is None or data["hourly_rate"] < 0):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid hourly_rate")

    for key, value in data.items():
        if hasattr(chef, key):
            setattr(chef, key, value)

    db.add(chef)
    db.commit()
    db.refresh(chef)
    return chef.to_dict()
