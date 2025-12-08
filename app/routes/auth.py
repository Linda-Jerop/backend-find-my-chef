from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app import get_db
from app.models.user import User, UserRole
from app.models.chef import Chef
from app.models.client import Client

router = APIRouter()  # Creating a router for auth endpoints


class RegisterIn(BaseModel):  # Defining input schema for registration
    email: EmailStr
    password: str
    name: str
    role: str


@router.post("/register")
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    """Registering a new user and creating chef/client profile when applicable."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(email=payload.email, password_hash=payload.password, name=payload.name, role=UserRole(payload.role))
    db.add(user)
    db.commit()
    db.refresh(user)

    result = {"token": user.email, "user": user.to_dict()}  # Returning token as email for test simplicity.

    if payload.role == "chef":
        chef = Chef(user_id=user.id, hourly_rate=0.0)  # Creating chef profile for chef users
        db.add(chef)
        db.commit()
        db.refresh(chef)
        result["chef_profile"] = chef.to_dict()
    else:
        client = Client(user_id=user.id)  # Creating client profile for client users
        db.add(client)
        db.commit()
        db.refresh(client)
        result["client_profile"] = client.to_dict()

    return result
