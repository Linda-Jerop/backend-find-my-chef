from fastapi import APIRouter, Depends, HTTPException, status  # Creating router and HTTP helpers
from pydantic import BaseModel, constr  # Defining request/response schemas with simple email validation
from sqlalchemy.orm import Session  # Typing DB session
from passlib.context import CryptContext  # Hashing passwords
from jose import jwt  # Generating JWT tokens
from datetime import datetime, timedelta  # Managing token expiry
from app import get_db  # Getting DB session
from app.models.user import User, UserRole  # Importing user model
from app.models.chef import Chef  # Creating chef profile when registering a chef
from config.settings import settings  # Loading app settings

router = APIRouter()  # Creating router
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Creating password hasher


class RegisterSchema(BaseModel):
    email: constr(min_length=3, max_length=255, pattern=r"^[^@]+@[^@]+\.[^@]+$")  # Validating basic email shape
    password: str
    name: str
    role: str


class LoginSchema(BaseModel):
    email: constr(min_length=3, max_length=255, pattern=r"^[^@]+@[^@]+\.[^@]+$")  # Validating basic email shape
    password: str


def create_access_token(data: dict, expires_minutes: int = None):
    expire = datetime.utcnow() + timedelta(minutes=(expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES))  # Generating expiry
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # Returning signed token


@router.post("/register", status_code=status.HTTP_201_CREATED)  # Creating user and optional chef profile
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()  # Checking duplicate email
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed = pwd_context.hash(payload.password)  # Hashing password
    role = UserRole.CHEF if payload.role.lower() == "chef" else UserRole.CLIENT  # Normalizing role
    user = User(email=payload.email, password_hash=hashed, name=payload.name, role=role)  # Creating user record
    db.add(user)
    db.commit()
    db.refresh(user)

    result = user.to_dict()  # Preparing response user object
    token = create_access_token({"sub": str(user.id), "role": user.role.value})  # Creating JWT token

    chef_profile = None
    if user.role == UserRole.CHEF:
        chef = Chef(user_id=user.id)  # Creating empty chef profile for new chef user
        db.add(chef)
        db.commit()
        db.refresh(chef)
        chef_profile = chef.to_dict()

    return {"token": token, **result, "chef_profile": chef_profile}  # Returning token and user info


@router.post("/login")  # Logging in and returning token + user
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()  # Finding user by email
    if not user or not pwd_context.verify(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "role": user.role.value})  # Creating access token
    return {"token": token, "user": user.to_dict()}  # Returning token and user object
