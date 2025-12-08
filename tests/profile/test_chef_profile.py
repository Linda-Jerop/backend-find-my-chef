"""
Tests for Chef Profile Feature

Corresponds to frontend: src/features/profile/ChefProfile.jsx
Tests the backend endpoints for viewing and editing chef profiles
"""
import pytest
from fastapi import status


class TestChefProfileView:
    """Tests for viewing chef profiles: GET /api/chefs/:id"""
    
    def test_get_chef_profile_success(self, client, sample_user_data, sample_chef_data):
        """
        Test viewing a chef profile
        Frontend: ChefProfile.jsx displays chef details
        """
        # Register as chef
        sample_user_data["role"] = "chef"
        register_response = client.post("/api/auth/register", json=sample_user_data)
        chef_id = register_response.json()["chef_profile"]["id"]
        
        # View profile
        response = client.get(f"/api/chefs/{chef_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == chef_id
        assert "bio" in data
        assert "hourly_rate" in data
        assert "cuisines" in data
    
    def test_get_nonexistent_chef(self, client):
        """
        Test viewing chef that doesn't exist
        Frontend: Should show 404 error page
        """
        response = client.get("/api/chefs/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_chef_profile_shows_all_fields(self, client, sample_user_data, sample_chef_data):
        """
        Test that profile returns all required fields
        Frontend: ChefProfile.jsx expects these fields
        """
        sample_user_data["role"] = "chef"
        register_response = client.post("/api/auth/register", json=sample_user_data)
        chef_id = register_response.json()["chef_profile"]["id"]
        
        response = client.get(f"/api/chefs/{chef_id}")
        data = response.json()
        
        # Check all fields frontend needs
        required_fields = [
            "id", "name", "bio", "cuisines", "hourly_rate",
            "location", "phone", "photo_url", "rating", "is_available"
        ]
        for field in required_fields:
            assert field in data


class TestChefProfileEdit:
    """Tests for editing chef profiles: PATCH /api/chefs/:id"""
    
    def test_update_own_profile_success(self, client, sample_user_data):
        """
        Test chef updating their own profile
        Frontend: ChefProfile.jsx edit form submission
        """
        # Register as chef
        sample_user_data["role"] = "chef"
        register_response = client.post("/api/auth/register", json=sample_user_data)
        token = register_response.json()["token"]
        chef_id = register_response.json()["chef_profile"]["id"]
        
        # Update profile
        update_data = {
            "bio": "Updated bio text",
            "hourly_rate": 75.0,
            "location": "Mombasa"
        }
        response = client.patch(
            f"/api/chefs/{chef_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["bio"] == "Updated bio text"
        assert data["hourly_rate"] == 75.0
        assert data["location"] == "Mombasa"
    
    def test_update_profile_without_auth(self, client, sample_user_data):
        """
        Test updating profile without authentication
        Frontend: Should redirect to login
        """
        update_data = {"bio": "Should fail"}
        response = client.patch("/api/chefs/1", json=update_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_other_chef_profile_forbidden(self, client, sample_user_data):
        """
        Test chef trying to edit another chef's profile
        Frontend: Edit button should not appear for non-owners
        """
        # Register first chef
        sample_user_data["role"] = "chef"
        client.post("/api/auth/register", json=sample_user_data)
        
        # Register second chef
        sample_user_data["email"] = "chef2@example.com"
        register_response = client.post("/api/auth/register", json=sample_user_data)
        token2 = register_response.json()["token"]
        
        # Try to update first chef's profile with second chef's token
        response = client.patch(
            "/api/chefs/1",
            json={"bio": "Hacking attempt"},
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_validates_hourly_rate(self, client, sample_user_data):
        """
        Test that negative or invalid hourly rates are rejected
        Frontend: Form validation should prevent this
        """
        sample_user_data["role"] = "chef"
        register_response = client.post("/api/auth/register", json=sample_user_data)
        token = register_response.json()["token"]
        chef_id = register_response.json()["chef_profile"]["id"]
        
        # Try negative rate
        response = client.patch(
            f"/api/chefs/{chef_id}",
            json={"hourly_rate": -50.0},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# TODO: Add tests for:
# - Profile photo upload
# - Updating cuisines list
# - Availability toggle
# - Rating calculation
