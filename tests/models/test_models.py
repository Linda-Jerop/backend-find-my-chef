"""
Tests for Database Models

Tests the SQLAlchemy models directly (not through API endpoints)
Ensures database relationships and constraints work correctly
"""
import pytest
from app.models import User, Chef, Client, Booking, UserRole, BookingStatus
from datetime import date, time


class TestUserModel:
    """Tests for User model"""
    
    def test_create_user(self, db_session):
        """Test creating a basic user"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User",
            role=UserRole.CLIENT
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.role == UserRole.CLIENT
    
    def test_user_email_unique_constraint(self, db_session):
        """Test that duplicate emails are not allowed"""
        user1 = User(
            email="duplicate@example.com",
            password_hash="hash1",
            name="User 1",
            role=UserRole.CLIENT
        )
        db_session.add(user1)
        db_session.commit()
        
        # Try to create user with same email
        user2 = User(
            email="duplicate@example.com",
            password_hash="hash2",
            name="User 2",
            role=UserRole.CLIENT
        )
        db_session.add(user2)
        
        with pytest.raises(Exception):  # SQLAlchemy integrity error
            db_session.commit()


class TestChefModel:
    """Tests for Chef model and User-Chef relationship"""
    
    def test_create_chef_profile(self, db_session):
        """Test creating chef with linked user"""
        user = User(
            email="chef@example.com",
            password_hash="hash",
            name="Chef Mario",
            role=UserRole.CHEF
        )
        db_session.add(user)
        db_session.commit()
        
        chef = Chef(
            user_id=user.id,
            bio="Italian cuisine expert",
            hourly_rate=50.0,
            location="Nairobi"
        )
        db_session.add(chef)
        db_session.commit()
        
        assert chef.id is not None
        assert chef.user_id == user.id
        assert chef.user.name == "Chef Mario"  # Test relationship
    
    def test_chef_user_relationship(self, db_session):
        """Test that chef can access user data through relationship"""
        user = User(
            email="chef@example.com",
            password_hash="hash",
            name="Chef Mario",
            role=UserRole.CHEF
        )
        chef = Chef(user_id=None, hourly_rate=50.0)
        chef.user = user  # Set relationship
        
        db_session.add(chef)
        db_session.commit()
        
        # Access user through chef
        assert chef.user.email == "chef@example.com"
        # Access chef through user
        assert user.chef_profile.hourly_rate == 50.0


class TestClientModel:
    """Tests for Client model"""
    
    def test_create_client_profile(self, db_session):
        """Test creating client with linked user"""
        user = User(
            email="client@example.com",
            password_hash="hash",
            name="John Doe",
            role=UserRole.CLIENT
        )
        db_session.add(user)
        db_session.commit()
        
        client = Client(
            user_id=user.id,
            phone="+254700000000",
            address="123 Main St"
        )
        db_session.add(client)
        db_session.commit()
        
        assert client.id is not None
        assert client.user.name == "John Doe"


class TestBookingModel:
    """Tests for Booking model and relationships"""
    
    def test_create_booking(self, db_session):
        """Test creating booking with chef and client"""
        # Create chef
        chef_user = User(
            email="chef@example.com",
            password_hash="hash",
            name="Chef Mario",
            role=UserRole.CHEF
        )
        db_session.add(chef_user)
        db_session.commit()
        
        chef = Chef(user_id=chef_user.id, hourly_rate=50.0)
        db_session.add(chef)
        db_session.commit()
        
        # Create client
        client_user = User(
            email="client@example.com",
            password_hash="hash",
            name="John Doe",
            role=UserRole.CLIENT
        )
        db_session.add(client_user)
        db_session.commit()
        
        client = Client(user_id=client_user.id)
        db_session.add(client)
        db_session.commit()
        
        # Create booking
        booking = Booking(
            client_id=client.id,
            chef_id=chef.id,
            booking_date=date(2025, 12, 15),
            booking_time=time(18, 0),
            duration_hours=3.0,
            location="Client's home",
            hourly_rate=50.0,
            total_price=150.0,
            status=BookingStatus.PENDING
        )
        db_session.add(booking)
        db_session.commit()
        
        assert booking.id is not None
        assert booking.status == BookingStatus.PENDING
        assert booking.total_price == 150.0
    
    def test_booking_relationships(self, db_session):
        """Test booking can access chef and client"""
        # Setup (abbreviated)
        chef_user = User(email="chef@example.com", password_hash="h", name="Chef", role=UserRole.CHEF)
        db_session.add(chef_user)
        db_session.commit()
        
        chef = Chef(user_id=chef_user.id, hourly_rate=50.0)
        db_session.add(chef)
        db_session.commit()
        
        client_user = User(email="client@example.com", password_hash="h", name="Client", role=UserRole.CLIENT)
        db_session.add(client_user)
        db_session.commit()
        
        client = Client(user_id=client_user.id)
        db_session.add(client)
        db_session.commit()
        
        booking = Booking(
            client_id=client.id,
            chef_id=chef.id,
            booking_date=date(2025, 12, 15),
            booking_time=time(18, 0),
            duration_hours=3.0,
            location="Test",
            hourly_rate=50.0,
            total_price=150.0
        )
        db_session.add(booking)
        db_session.commit()
        
        # Test relationships
        assert booking.chef.user.name == "Chef"
        assert booking.client.user.name == "Client"
        assert chef.bookings[0].id == booking.id
        assert client.bookings[0].id == booking.id


# TODO: Add tests for:
# - Cascade deletes
# - to_dict() methods
# - Default values
# - Nullable constraints
