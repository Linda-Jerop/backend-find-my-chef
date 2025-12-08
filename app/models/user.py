from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from app import Base


class UserRole(enum.Enum):
    CHEF = "chef"
    CLIENT = "client"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # We hash passwords with bcrypt before storing.
    name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)  # Either "chef" or "client".
    firebase_uid = Column(String(255), unique=True, nullable=True)  # For Google/Facebook login.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
