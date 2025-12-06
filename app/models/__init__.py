"""
Models package for Find My Chef

This package contains all database models:
- User: Base authentication model (email, password, role)
- Chef: Chef profile (bio, cuisines, pricing, location)
- Client: Client profile (contact info, preferences)
- Booking: Appointment/booking between client and chef

Import all models here so they can be used throughout the app.
"""
from app.models.user import User, UserRole
from app.models.chef import Chef
from app.models.client import Client
from app.models.booking import Booking, BookingStatus

# Export all models and enums
__all__ = [
    'User', 
    'UserRole',      # Enum: chef or client
    'Chef', 
    'Client', 
    'Booking',
    'BookingStatus'  # Enum: pending, accepted, declined, etc.
]
