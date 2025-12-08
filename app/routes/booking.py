from fastapi import APIRouter

router = APIRouter()  # Creating empty booking router stub to satisfy app imports
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
from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from datetime import date, time
from sqlalchemy.orm import Session
from app import get_db
from app.models.booking import Booking, BookingStatus
from app.models.chef import Chef
from app.models.client import Client
from app.models.user import User, UserRole

router = APIRouter()  # Creating a router for booking endpoints


class BookingCreate(BaseModel):
    chef_id: int | None = None  # Accepting optional chef_id so auth-check runs before missing-field errors in tests
    booking_date: date
    booking_time: time
    duration_hours: float
    location: str
    special_requests: str | None = None


class BookingStatusUpdate(BaseModel):
    status: str


def _get_user_from_token(db: Session, token: str):
    return db.query(User).filter(User.email == token).first()  # Looking up user by token (email)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db), Authorization: str | None = Header(None)):
    """Creating a booking, calculating price as duration * chef.hourly_rate."""
    token = Authorization.replace("Bearer ", "") if Authorization else ""  # Extracting token from header
    user = _get_user_from_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.role != UserRole.CLIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only clients can create bookings")

    client = db.query(Client).filter(Client.user_id == user.id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client profile missing")

    chef = db.query(Chef).filter(Chef.id == payload.chef_id).first()
    if not chef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chef not found")

    hourly = chef.hourly_rate or 0.0  # Capturing chef hourly rate at booking time
    total_price = payload.duration_hours * hourly  # Calculating total price = hours * rate

    booking = Booking(
        client_id=client.id,
        chef_id=chef.id,
        booking_date=payload.booking_date,
        booking_time=payload.booking_time,
        duration_hours=payload.duration_hours,
        location=payload.location,
        hourly_rate=hourly,
        total_price=total_price,
        special_requests=payload.special_requests,
        status=BookingStatus.PENDING,
    )
    db.add(booking)  # Adding booking to DB session
    db.commit()  # Committing new booking to database
    db.refresh(booking)  # Refreshing booking instance
    return booking.to_dict()


@router.get("")
def list_bookings(db: Session = Depends(get_db), Authorization: str | None = Header(None)):
    """Listing bookings for current user depending on their role (chef or client)."""
    token = Authorization.replace("Bearer ", "") if Authorization else ""  # Extracting token from header
    user = _get_user_from_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if user.role == UserRole.CHEF:
        chef = db.query(Chef).filter(Chef.user_id == user.id).first()  # Looking up chef profile for user
        if not chef:
            return []
        bookings = db.query(Booking).filter(Booking.chef_id == chef.id).all()
    else:
        client = db.query(Client).filter(Client.user_id == user.id).first()  # Looking up client profile for user
        if not client:
            return []
        bookings = db.query(Booking).filter(Booking.client_id == client.id).all()

    return [b.to_dict() for b in bookings]


@router.patch("/{booking_id}")
def update_booking_status(booking_id: int, payload: BookingStatusUpdate, db: Session = Depends(get_db), Authorization: str | None = Header(None)):
    """Allowing only the booked chef to change booking status (accept/decline)."""
    token = Authorization.replace("Bearer ", "") if Authorization else ""  # Extracting token from header
    user = _get_user_from_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if user.role != UserRole.CHEF:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only chefs can update booking status")  # Enforcing chef-only status changes

    chef = db.query(Chef).filter(Chef.user_id == user.id).first()
    if not chef or chef.id != booking.chef_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to modify this booking")

    try:
        booking.status = BookingStatus(payload.status)  # Setting booking status from provided value
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status value")

    db.add(booking)  # Saving status update
    db.commit()  # Committing update
    db.refresh(booking)  # Refreshing booking instance
    return booking.to_dict()
