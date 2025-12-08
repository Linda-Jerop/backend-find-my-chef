from pydantic import BaseModel, Field
from typing import Optional, List


class ChefCreate(BaseModel):
    bio: Optional[str] = None
    cuisines: Optional[str] = None  # Comma-separated string.
    specialties: Optional[str] = None
    hourly_rate: float = Field(ge=0)  # Must be greater than or equal to 0.
    location: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    years_of_experience: int = Field(ge=0, default=0)


class ChefUpdate(BaseModel):
    bio: Optional[str] = None
    cuisines: Optional[str] = None
    specialties: Optional[str] = None
    hourly_rate: Optional[float] = Field(ge=0, default=None)
    location: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    years_of_experience: Optional[int] = Field(ge=0, default=None)
    is_available: Optional[bool] = None


class ChefResponse(BaseModel):
    id: int
    user_id: int
    name: str
    bio: Optional[str]
    cuisines: List[str]  # Frontend expects array.
    specialties: Optional[str]
    hourly_rate: float
    location: Optional[str]
    phone: Optional[str]
    photo_url: Optional[str]
    years_of_experience: int
    rating: float
    total_bookings: int
    is_available: bool
    
    class Config:
        from_attributes = True
