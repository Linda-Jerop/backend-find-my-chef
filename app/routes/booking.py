from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app import get_db
from app.models.booking import Booking, BookingStatus
from app.models.chef import Chef
from app.models.client import Client
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.utils.auth import get_current_user

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BookingResponse)
def create_booking(booking_data: BookingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.user_id == current_user.id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only clients can create bookings")
    
    chef = db.query(Chef).filter(Chef.id == booking_data.chef_id).first()
    if not chef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chef not found")
    
    total_price = booking_data.duration_hours * chef.hourly_rate
    
    new_booking = Booking(
        client_id=client.id,
        chef_id=booking_data.chef_id,
        booking_date=booking_data.booking_date,
        booking_time=booking_data.booking_time,
        duration_hours=booking_data.duration_hours,
        location=booking_data.location,
        hourly_rate=chef.hourly_rate,
        total_price=total_price,
        special_requests=booking_data.special_requests,
        status=BookingStatus.PENDING
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return new_booking.to_dict()


@router.get("", response_model=List[BookingResponse])
def list_bookings(
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.user_id == current_user.id).first()
    chef = db.query(Chef).filter(Chef.user_id == current_user.id).first()
    
    if client:
        query = db.query(Booking).filter(Booking.client_id == client.id)
    elif chef:
        query = db.query(Booking).filter(Booking.chef_id == chef.id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has no profile")
    
    if status_filter:
        query = query.filter(Booking.status == BookingStatus(status_filter))
    
    bookings = query.all()
    return [booking.to_dict() for booking in bookings]


@router.patch("/{booking_id}", response_model=BookingResponse)
def update_booking_status(booking_id: int, booking_update: BookingUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    
    chef = db.query(Chef).filter(Chef.user_id == current_user.id).first()
    if not chef or booking.chef_id != chef.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the chef can update booking status")
    
    booking.status = BookingStatus(booking_update.status)
    if booking_update.notes:
        booking.notes = booking_update.notes
    
    db.commit()
    db.refresh(booking)
    
    return booking.to_dict()
