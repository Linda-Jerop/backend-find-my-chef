from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import Base


class Chef(Base):
    __tablename__ = "chefs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # Links to User table, one chef per user.
    
    bio = Column(Text, nullable=True)  # Chef's description and background.
    cuisines = Column(String(500), nullable=True)  # Comma-separated list like "Italian,French,Mediterranean".
    specialties = Column(Text, nullable=True)  # Special skills or signature dishes.
    hourly_rate = Column(Float, nullable=False, default=0.0)  # How much they charge per hour.
    location = Column(String(255), nullable=True)  # City or area where they operate.
    phone = Column(String(20), nullable=True)  # Contact phone number.
    photo_url = Column(String(500), nullable=True)  # URL to profile photo.
    years_of_experience = Column(Integer, default=0)  # Years cooking professionally.
    rating = Column(Float, default=0.0)  # Average rating from bookings.
    total_bookings = Column(Integer, default=0)  # Number of times booked.
    is_available = Column(Integer, default=1)  # 1 for available, 0 for unavailable.
    
    user = relationship("User", backref="chef_profile", foreign_keys=[user_id])
    bookings = relationship("Booking", back_populates="chef", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.user.name if self.user else None,
            "bio": self.bio,
            "cuisines": self.cuisines.split(",") if self.cuisines else [],
            "specialties": self.specialties,
            "hourly_rate": self.hourly_rate,
            "location": self.location,
            "phone": self.phone,
            "photo_url": self.photo_url,
            "years_of_experience": self.years_of_experience,
            "rating": self.rating,
            "total_bookings": self.total_bookings,
            "is_available": bool(self.is_available),
        }
