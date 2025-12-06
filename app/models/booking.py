from sqlalchemy import Column, Integer, String, Float, Date, Time, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app import Base
import enum


class BookingStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)  # Which client made the booking.
    chef_id = Column(Integer, ForeignKey("chefs.id"), nullable=False)  # Which chef is being booked.
    
    booking_date = Column(Date, nullable=False)  # The day of the booking.
    booking_time = Column(Time, nullable=False)  # The time of the booking.
    duration_hours = Column(Float, nullable=False)  # How many hours the booking lasts.
    location = Column(String(500), nullable=False)  # Where the chef should come.
    
    hourly_rate = Column(Float, nullable=False)  # Chef's rate locked at booking time.
    total_price = Column(Float, nullable=False)  # Calculated as duration_hours * hourly_rate.
    
    status = Column(SQLEnum(BookingStatus), nullable=False, default=BookingStatus.PENDING)  # Current booking status.
    
    special_requests = Column(Text, nullable=True)  # Client can add notes about the booking.
    notes = Column(Text, nullable=True)  # Chef can add their own notes.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    client = relationship("Client", back_populates="bookings")
    chef = relationship("Chef", back_populates="bookings")
    
    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "client_name": self.client.user.name if self.client and self.client.user else None,
            "chef_id": self.chef_id,
            "chef_name": self.chef.user.name if self.chef and self.chef.user else None,
            "booking_date": self.booking_date.isoformat() if self.booking_date else None,
            "booking_time": self.booking_time.isoformat() if self.booking_time else None,
            "duration_hours": self.duration_hours,
            "location": self.location,
            "hourly_rate": self.hourly_rate,
            "total_price": self.total_price,
            "status": self.status.value,
            "special_requests": self.special_requests,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
