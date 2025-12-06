"""
Tests for Client Profile Feature

Corresponds to frontend: src/features/profile/ClientProfile.jsx
Tests the backend endpoints for viewing and editing client profiles
"""
import pytest
from fastapi import status


class TestClientProfileView:
    """Tests for viewing client profiles: GET /api/clients/:id"""
    
    def test_get_client_profile_success(self, client, sample_user_data):
        """
        Test viewing a client profile
        Frontend: ClientProfile.jsx displays client details
        """
        # Register as client
        register_response = client.post("/api/auth/register", json=sample_user_data)
        client_id = register_response.json()["client_profile"]["id"]
        
        # View profile
        response = client.get(f"/api/clients/{client_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == client_id
        assert data["name"] == sample_user_data["name"]
        assert data["email"] == sample_user_data["email"]
    
    def test_get_nonexistent_client(self, client):
        """
        Test viewing client that doesn't exist
        Frontend: Should show 404 error
        """
        response = client.get("/api/clients/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestClientProfileEdit:
    """Tests for editing client profiles: PATCH /api/clients/:id"""
    
    def test_update_own_profile_success(self, client, sample_user_data):
        """
        Test client updating their own profile
        Frontend: ClientProfile.jsx edit form
        """
        # Register as client
        register_response = client.post("/api/auth/register", json=sample_user_data)
        token = register_response.json()["token"]
        client_id = register_response.json()["client_profile"]["id"]
        
        # Update profile
        update_data = {
            "name": "Updated Name",
            "phone": "+254700000000",
            "address": "123 Updated St, Nairobi"
        }
        response = client.patch(
            f"/api/clients/{client_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["phone"] == "+254700000000"
    
    def test_update_profile_without_auth(self, client):
        """
        Test updating profile without authentication
        Frontend: Should redirect to login
        """
        update_data = {"name": "Should fail"}
        response = client.patch("/api/clients/1", json=update_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_other_client_profile_forbidden(self, client, sample_user_data):
        """
        Test client trying to edit another client's profile
        Frontend: Edit button hidden for non-owners
        """
        # Register first client
        client.post("/api/auth/register", json=sample_user_data)
        
        # Register second client
        sample_user_data["email"] = "client2@example.com"
        register_response = client.post("/api/auth/register", json=sample_user_data)
        token2 = register_response.json()["token"]
        
        # Try to update first client's profile with second client's token
        response = client.patch(
            "/api/clients/1",
            json={"name": "Hacking attempt"},
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_email_readonly_cannot_update(self, client, sample_user_data):
        """
        Test that email cannot be changed
        Frontend: Email field is read-only in UI
        """
        register_response = client.post("/api/auth/register", json=sample_user_data)
        token = register_response.json()["token"]
        client_id = register_response.json()["client_profile"]["id"]
        
        # Try to change email
        response = client.patch(
            f"/api/clients/{client_id}",
            json={"email": "newemail@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Email should remain unchanged
        get_response = client.get(f"/api/clients/{client_id}")
        assert get_response.json()["email"] == sample_user_data["email"]


# TODO: Add tests for:
# - Preferred cuisines update
# - Total bookings counter
# - Profile completion status
