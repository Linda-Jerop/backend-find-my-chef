from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app import Base


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # Links to User table, one client per user.
    
    phone = Column(String(20), nullable=True)  # Client's phone number.
    address = Column(String(500), nullable=True)  # Where they want chef services.
    preferred_cuisines = Column(String(500), nullable=True)  # Comma-separated list of favorites.
    total_bookings = Column(Integer, default=0)  # Tracks how many times they've booked.
    
    user = relationship("User", backref="client_profile", foreign_keys=[user_id])
    bookings = relationship("Booking", back_populates="client", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.user.name if self.user else None,
            "email": self.user.email if self.user else None,
            "phone": self.phone,
            "address": self.address,
            "preferred_cuisines": self.preferred_cuisines.split(",") if self.preferred_cuisines else [],
            "total_bookings": self.total_bookings,
        }
