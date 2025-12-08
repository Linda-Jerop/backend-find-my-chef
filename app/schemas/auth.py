"""
Pydantic schemas for authentication endpoints
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class UserRoleEnum(str, Enum):
    """User role enumeration"""
    CHEF = "chef"
    CLIENT = "client"


class UserRegister(BaseModel):
    """Schema for user registration"""
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    role: UserRoleEnum = Field(..., description="User role: 'chef' or 'client'")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "securePassword123",
                "role": "chef"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "securePassword123"
            }
        }


class GoogleLoginRequest(BaseModel):
    """Schema for Google OAuth login"""
    firebase_id_token: str = Field(..., description="Firebase ID token from Google OAuth")
    
    class Config:
        json_schema_extra = {
            "example": {
                "firebase_id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjEyMyJ9..."
            }
        }


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 86400
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (public data only)"""
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    name: str = Field(..., description="User's name")
    role: str = Field(..., description="User's role (chef or client)")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "john@example.com",
                "name": "John Doe",
                "role": "chef"
            }
        }


class AuthResponse(BaseModel):
    """Schema for authentication response with user data"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserResponse = Field(..., description="User information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "email": "john@example.com",
                    "name": "John Doe",
                    "role": "chef"
                }
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (public data only)"""
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    name: str = Field(..., description="User's name")
    role: str = Field(..., description="User's role (chef or client)")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "john@example.com",
                "name": "John Doe",
                "role": "chef"
            }
        }


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid credentials",
                "status_code": 401
            }
        }
