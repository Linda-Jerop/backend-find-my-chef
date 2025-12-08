"""
Booking routes
"""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement booking routes
@router.get("/")
async def get_bookings():
    """Get all bookings"""
    return {"message": "Get all bookings endpoint"}
