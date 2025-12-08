from pydantic import BaseModel
from typing import Optional, List


class ClientUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    preferred_cuisines: Optional[str] = None  # Comma-separated string.


class ClientResponse(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    preferred_cuisines: List[str]  # Frontend expects array.
    total_bookings: int
    
    class Config:
        from_attributes = True
