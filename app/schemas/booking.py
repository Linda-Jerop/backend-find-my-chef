from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime


class BookingCreate(BaseModel):
    chef_id: int
    booking_date: date  # Format: "2025-12-15"
    booking_time: time  # Format: "18:00"
    duration_hours: float = Field(gt=0)  # Must be greater than 0.
    location: str = Field(min_length=1)  # Cannot be empty.
    special_requests: Optional[str] = None


class BookingUpdate(BaseModel):
    status: str = Field(pattern="^(pending|accepted|confirmed|declined|completed|cancelled)$")
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    client_id: int
    client_name: Optional[str]
    chef_id: int
    chef_name: Optional[str]
    booking_date: date
    booking_time: time
    duration_hours: float
    location: str
    hourly_rate: float
    total_price: float
    status: str
    special_requests: Optional[str]
    notes: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
