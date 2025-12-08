from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import get_db
from app.models.user import User, UserRole
from app.models.chef import Chef
from app.models.client import Client
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.utils.auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        name=user_data.name,
        role=UserRole.CHEF if user_data.role == "chef" else UserRole.CLIENT
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    if user_data.role == "chef":
        chef_profile = Chef(user_id=new_user.id)
        db.add(chef_profile)
    else:
        client_profile = Client(user_id=new_user.id)
        db.add(client_profile)
    
    db.commit()
    
    token = create_access_token(data={"sub": str(new_user.id)})
    
    return {
        "token": token,
        "user": new_user.to_dict()
    }


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "token": token,
        "user": user.to_dict()
    }


@router.post("/google")
def google_login(db: Session = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Google authentication not yet implemented")  # TODO: Implement Firebase integration
