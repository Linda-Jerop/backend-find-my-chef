"""
Authentication routes for login, registration, and Google OAuth
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional
from app import get_db
from app.models.user import User, UserRole
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    GoogleLoginRequest,
    AuthResponse,
    TokenResponse,
    UserResponse,
)
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
)
from config.settings import settings

# Import Firebase Admin SDK (optional - will be set up later if credentials provided)
try:
    import firebase_admin
    from firebase_admin import credentials, auth as firebase_auth
    FIREBASE_ENABLED = False  # Will be True once credentials are set up
except ImportError:
    FIREBASE_ENABLED = False


router = APIRouter()


def get_token_from_header(authorization: Optional[str] = Header(None)) -> str:
    """Extract JWT token from Authorization header"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return parts[1]


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - **name**: User's full name
    - **email**: User's email address (must be unique)
    - **password**: Password (minimum 8 characters)
    - **role**: Either "chef" or "client"
    
    Returns user data with JWT token for immediate login.
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name,
        role=UserRole[user_data.role.upper()]
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate access token
    access_token = create_access_token(
        data={"sub": str(new_user.id), "email": new_user.email}
    )
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns JWT token and user data on successful login.
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate access token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/google", response_model=AuthResponse)
async def google_login(
    request: GoogleLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login or register with Google OAuth.
    
    - **firebase_id_token**: Firebase ID token from Google OAuth
    
    Creates user account if it doesn't exist, otherwise logs in existing user.
    """
    if not FIREBASE_ENABLED or not settings.FIREBASE_CREDENTIALS_PATH:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google login is not configured. Please set up Firebase credentials."
        )
    
    try:
        # Verify Firebase token
        decoded_token = firebase_auth.verify_id_token(request.firebase_id_token)
        firebase_uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name", "Google User")
        
        if not firebase_uid or not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Firebase token"
            )
        
        # Check if user exists by firebase_uid
        user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
        
        if user:
            # User exists, log them in
            access_token = create_access_token(
                data={"sub": str(user.id), "email": user.email}
            )
            return AuthResponse(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse.model_validate(user)
            )
        
        # Check if email exists (user registered with email/password before)
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            # Link Firebase UID to existing account
            existing_email.firebase_uid = firebase_uid
            db.commit()
            db.refresh(existing_email)
            
            access_token = create_access_token(
                data={"sub": str(existing_email.id), "email": existing_email.email}
            )
            return AuthResponse(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse.model_validate(existing_email)
            )
        
        # Create new user from Google OAuth
        # Default to CLIENT role, can be changed later
        new_user = User(
            email=email,
            name=name,
            firebase_uid=firebase_uid,
            password_hash=hash_password(""),  # OAuth users don't have passwords
            role=UserRole.CLIENT  # Default role
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        access_token = create_access_token(
            data={"sub": str(new_user.id), "email": new_user.email}
        )
        
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(new_user)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Firebase authentication failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user information.
    
    Requires valid JWT token in Authorization header: `Authorization: Bearer <token>`
    """
    # Verify token
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)
