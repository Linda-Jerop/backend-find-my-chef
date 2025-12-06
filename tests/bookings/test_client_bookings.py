"""
Tests for Client Bookings Feature

Corresponds to frontend: src/features/bookings/ClientBookings.jsx
Tests booking creation and viewing from client perspective
"""
import pytest
from fastapi import status


class TestCreateBooking:
    """Tests for creating bookings: POST /api/bookings"""
    
    def test_create_booking_success(self, client, sample_user_data, sample_booking_data):
        """
        Test client successfully creating a booking
        Frontend: ClientBookings.jsx booking form submission
        """
        # Register chef
        sample_user_data["role"] = "chef"
        sample_user_data["email"] = "chef@example.com"
        chef_response = client.post("/api/auth/register", json=sample_user_data)
        chef_id = chef_response.json()["chef_profile"]["id"]
        
        # Update chef with hourly rate
        chef_token = chef_response.json()["token"]
        client.patch(
            f"/api/chefs/{chef_id}",
            json={"hourly_rate": 50.0},
            headers={"Authorization": f"Bearer {chef_token}"}
        )
        
        # Register client
        sample_user_data["role"] = "client"
        sample_user_data["email"] = "client@example.com"
        client_response = client.post("/api/auth/register", json=sample_user_data)
        client_token = client_response.json()["token"]
        
        # Create booking
        sample_booking_data["chef_id"] = chef_id
        response = client.post(
            "/api/bookings",
            json=sample_booking_data,
            headers={"Authorization": f"Bearer {client_token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["chef_id"] == chef_id
        assert data["status"] == "pending"
        assert data["total_price"] == 150.0  # 3 hours * 50 KSH
    
    def test_create_booking_calculates_price(self, client, sample_user_data, sample_booking_data):
        """
        Test that backend calculates price (not frontend)
        Frontend sends hours, backend multiplies by rate
        """
        # Setup chef and client (same as above)
        sample_user_data["role"] = "chef"
        sample_user_data["email"] = "chef@example.com"
        chef_response = client.post("/api/auth/register", json=sample_user_data)
        chef_id = chef_response.json()["chef_profile"]["id"]
        chef_token = chef_response.json()["token"]
        
        client.patch(
            f"/api/chefs/{chef_id}",
            json={"hourly_rate": 75.0},
            headers={"Authorization": f"Bearer {chef_token}"}
        )
        
        sample_user_data["role"] = "client"
        sample_user_data["email"] = "client@example.com"
        client_response = client.post("/api/auth/register", json=sample_user_data)
        client_token = client_response.json()["token"]
        
        # Book for 4 hours
        sample_booking_data["chef_id"] = chef_id
        sample_booking_data["duration_hours"] = 4.0
        
        response = client.post(
            "/api/bookings",
            json=sample_booking_data,
            headers={"Authorization": f"Bearer {client_token}"}
        )
        
        assert response.json()["total_price"] == 300.0  # 4 * 75
    
    def test_create_booking_requires_auth(self, client, sample_booking_data):
        """
        Test that booking creation requires login
        Frontend: Should redirect to login if not authenticated
        """
        response = client.post("/api/bookings", json=sample_booking_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_booking_validates_required_fields(self, client, sample_user_data):
        """
        Test validation of required booking fields
        Frontend: Form validation should catch this first
        """
        sample_user_data["role"] = "client"
        client_response = client.post("/api/auth/register", json=sample_user_data)
        client_token = client_response.json()["token"]
        
        # Missing required fields
        response = client.post(
            "/api/bookings",
            json={"chef_id": 1},
            headers={"Authorization": f"Bearer {client_token}"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestViewClientBookings:
    """Tests for viewing client's bookings: GET /api/bookings"""
    
    def test_get_client_bookings(self, client, sample_user_data, sample_booking_data):
        """
        Test client viewing their booking history
        Frontend: ClientBookings.jsx displays list of bookings
        """
        # Setup and create booking (abbreviated)
        sample_user_data["role"] = "chef"
        sample_user_data["email"] = "chef@example.com"
        chef_response = client.post("/api/auth/register", json=sample_user_data)
        chef_id = chef_response.json()["chef_profile"]["id"]
        
        sample_user_data["role"] = "client"
        sample_user_data["email"] = "client@example.com"
        client_response = client.post("/api/auth/register", json=sample_user_data)
        client_token = client_response.json()["token"]
        
        sample_booking_data["chef_id"] = chef_id
        client.post(
            "/api/bookings",
            json=sample_booking_data,
            headers={"Authorization": f"Bearer {client_token}"}
        )
        
        # Get bookings
        response = client.get(
            "/api/bookings",
            headers={"Authorization": f"Bearer {client_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert data[0]["status"] == "pending"
    
    def test_filter_bookings_by_status(self, client, sample_user_data, sample_booking_data):
        """
        Test filtering bookings by status
        Frontend: Status filter dropdown
        """
        # TODO: Create bookings with different statuses and test filter
        pytest.skip("Implement after basic booking creation works")


# TODO: Add tests for:
# - Booking past dates validation
# - Booking times validation
# - Chef availability check
# - Client cancelling booking
