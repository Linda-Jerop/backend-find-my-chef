"""
Tests for Chef Bookings Feature

Corresponds to frontend: src/features/bookings/ChefBookings.jsx
Tests viewing and managing bookings from chef perspective
"""
import pytest
from fastapi import status


class TestViewChefBookings:
    """Tests for chef viewing their booking requests: GET /api/bookings"""
    
    def test_chef_sees_incoming_requests(self, client, sample_user_data, sample_booking_data):
        """
        Test chef viewing booking requests
        Frontend: ChefBookings.jsx displays pending bookings
        """
        # Register chef
        sample_user_data["role"] = "chef"
        sample_user_data["email"] = "chef@example.com"
        chef_response = client.post("/api/auth/register", json=sample_user_data)
        chef_token = chef_response.json()["token"]
        chef_id = chef_response.json()["chef_profile"]["id"]
        
        # Register client and create booking
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
        
        # Chef views bookings
        response = client.get(
            "/api/bookings",
            headers={"Authorization": f"Bearer {chef_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert data[0]["status"] == "pending"


class TestAcceptDeclineBooking:
    """Tests for chef accepting/declining bookings: PATCH /api/bookings/:id"""
    
    def test_chef_accepts_booking(self, client, sample_user_data, sample_booking_data):
        """
        Test chef accepting a booking request
        Frontend: Chef clicks "Accept" button
        """
        # Setup chef and client, create booking
        sample_user_data["role"] = "chef"
        sample_user_data["email"] = "chef@example.com"
        chef_response = client.post("/api/auth/register", json=sample_user_data)
        chef_token = chef_response.json()["token"]
        chef_id = chef_response.json()["chef_profile"]["id"]
        
        sample_user_data["role"] = "client"
        sample_user_data["email"] = "client@example.com"
        client_response = client.post("/api/auth/register", json=sample_user_data)
        client_token = client_response.json()["token"]
        
        sample_booking_data["chef_id"] = chef_id
        booking_response = client.post(
            "/api/bookings",
            json=sample_booking_data,
            headers={"Authorization": f"Bearer {client_token}"}
        )
        booking_id = booking_response.json()["id"]
        
        # Chef accepts
        response = client.patch(
            f"/api/bookings/{booking_id}",
            json={"status": "accepted"},
            headers={"Authorization": f"Bearer {chef_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "accepted"
    
    def test_chef_declines_booking(self, client, sample_user_data, sample_booking_data):
        """
        Test chef declining a booking request
        Frontend: Chef clicks "Decline" button
        """
        # Setup (same as accept test)
        sample_user_data["role"] = "chef"
        sample_user_data["email"] = "chef@example.com"
        chef_response = client.post("/api/auth/register", json=sample_user_data)
        chef_token = chef_response.json()["token"]
        chef_id = chef_response.json()["chef_profile"]["id"]
        
        sample_user_data["role"] = "client"
        sample_user_data["email"] = "client@example.com"
        client_response = client.post("/api/auth/register", json=sample_user_data)
        client_token = client_response.json()["token"]
        
        sample_booking_data["chef_id"] = chef_id
        booking_response = client.post(
            "/api/bookings",
            json=sample_booking_data,
            headers={"Authorization": f"Bearer {client_token}"}
        )
        booking_id = booking_response.json()["id"]
        
        # Chef declines
        response = client.patch(
            f"/api/bookings/{booking_id}",
            json={"status": "declined"},
            headers={"Authorization": f"Bearer {chef_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "declined"
    
    def test_only_chef_can_accept_their_bookings(self, client, sample_user_data, sample_booking_data):
        """
        Test authorization: only the booked chef can accept/decline
        Frontend: Other chefs don't see these bookings
        """
        # Create two chefs
        sample_user_data["role"] = "chef"
        sample_user_data["email"] = "chef1@example.com"
        chef1_response = client.post("/api/auth/register", json=sample_user_data)
        chef1_id = chef1_response.json()["chef_profile"]["id"]
        
        sample_user_data["email"] = "chef2@example.com"
        chef2_response = client.post("/api/auth/register", json=sample_user_data)
        chef2_token = chef2_response.json()["token"]
        
        # Client books chef1
        sample_user_data["role"] = "client"
        sample_user_data["email"] = "client@example.com"
        client_response = client.post("/api/auth/register", json=sample_user_data)
        client_token = client_response.json()["token"]
        
        sample_booking_data["chef_id"] = chef1_id
        booking_response = client.post(
            "/api/bookings",
            json=sample_booking_data,
            headers={"Authorization": f"Bearer {client_token}"}
        )
        booking_id = booking_response.json()["id"]
        
        # Chef2 tries to accept chef1's booking
        response = client.patch(
            f"/api/bookings/{booking_id}",
            json={"status": "accepted"},
            headers={"Authorization": f"Bearer {chef2_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_client_cannot_accept_booking(self, client, sample_user_data, sample_booking_data):
        """
        Test that clients cannot change booking status
        Frontend: Accept/decline buttons only visible to chefs
        """
        # TODO: Implement this authorization check
        pytest.skip("Implement authorization logic first")


class TestChefEarnings:
    """Tests for calculating chef earnings"""
    
    def test_calculate_total_earnings(self, client, sample_user_data, sample_booking_data):
        """
        Test calculating total earnings from accepted bookings
        Frontend: ChefBookings.jsx shows "Total Earnings: KSH X"
        """
        # TODO: Implement earnings calculation endpoint
        pytest.skip("Implement earnings calculation endpoint")


# TODO: Add tests for:
# - Booking details view
# - Adding chef notes to booking
# - Marking booking as completed
# - Booking history
