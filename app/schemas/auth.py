from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    email: EmailStr  # Validates email format automatically.
    password: str = Field(min_length=6)  # Password must be at least 6 characters.
    name: str = Field(min_length=1)  # Name cannot be empty.
    role: str = Field(pattern="^(chef|client)$")  # Only "chef" or "client" allowed.


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models.
