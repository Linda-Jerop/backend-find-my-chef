"""
Tests for Chef Search Feature

Corresponds to frontend: src/features/search/ChefSearch.jsx
Tests the backend endpoint for searching and filtering chefs
"""
import pytest
from fastapi import status


class TestChefSearch:
    """Tests for chef search and filtering: GET /api/chefs"""
    
    def test_get_all_chefs(self, client, sample_user_data):
        """
        Test getting list of all chefs
        Frontend: ChefSearch.jsx initial load
        """
        # Register 3 chefs
        for i in range(3):
            sample_user_data["email"] = f"chef{i}@example.com"
            sample_user_data["role"] = "chef"
            client.post("/api/auth/register", json=sample_user_data)
        
        # Get all the chefs
        response = client.get("/api/chefs")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_filter_by_cuisine(self, client, sample_user_data):
        """
        Test filtering chefs by cuisine type
        Frontend: Cuisine dropdown filter
        """
        # Register Italian chef
        sample_user_data["email"] = "italian@example.com"
        sample_user_data["role"] = "chef"
        response = client.post("/api/auth/register", json=sample_user_data)
        token = response.json()["token"]
        chef_id = response.json()["chef_profile"]["id"]
        
        # Update with Italian cuisine
        client.patch(
            f"/api/chefs/{chef_id}",
            json={"cuisines": "Italian,French"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Register Japanese chef
        sample_user_data["email"] = "japanese@example.com"
        response = client.post("/api/auth/register", json=sample_user_data)
        token2 = response.json()["token"]
        chef_id2 = response.json()["chef_profile"]["id"]
        
        client.patch(
            f"/api/chefs/{chef_id2}",
            json={"cuisines": "Japanese,Asian"},
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        # Filter by Italian
        response = client.get("/api/chefs?cuisine=Italian")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert "Italian" in data[0]["cuisines"]
    
    def test_filter_by_max_price(self, client, sample_user_data):
        """
        Test filtering by maximum hourly rate
        Frontend: Price slider/input filter
        """
        # Register expensive chef
        sample_user_data["email"] = "expensive@example.com"
        sample_user_data["role"] = "chef"
        response = client.post("/api/auth/register", json=sample_user_data)
        token = response.json()["token"]
        chef_id = response.json()["chef_profile"]["id"]
        
        client.patch(
            f"/api/chefs/{chef_id}",
            json={"hourly_rate": 100.0},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Register budget chef
        sample_user_data["email"] = "budget@example.com"
        response = client.post("/api/auth/register", json=sample_user_data)
        token2 = response.json()["token"]
        chef_id2 = response.json()["chef_profile"]["id"]
        
        client.patch(
            f"/api/chefs/{chef_id2}",
            json={"hourly_rate": 30.0},
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        # Filter by max price 50
        response = client.get("/api/chefs?max_price=50")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["hourly_rate"] <= 50
    
    def test_filter_by_location(self, client, sample_user_data):
        """
        Test filtering by chef location
        Frontend: Location dropdown filter
        """
        # Register Nairobi chef
        sample_user_data["email"] = "nairobi@example.com"
        sample_user_data["role"] = "chef"
        response = client.post("/api/auth/register", json=sample_user_data)
        token = response.json()["token"]
        chef_id = response.json()["chef_profile"]["id"]
        
        client.patch(
            f"/api/chefs/{chef_id}",
            json={"location": "Nairobi"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Register Mombasa chef
        sample_user_data["email"] = "mombasa@example.com"
        response = client.post("/api/auth/register", json=sample_user_data)
        token2 = response.json()["token"]
        chef_id2 = response.json()["chef_profile"]["id"]
        
        client.patch(
            f"/api/chefs/{chef_id2}",
            json={"location": "Mombasa"},
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        # Filter by Nairobi
        response = client.get("/api/chefs?location=Nairobi")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["location"] == "Nairobi"
    
    def test_combine_multiple_filters(self, client, sample_user_data):
        """
        Test combining multiple filters
        Frontend: User selects Italian + max 80 KSH + Nairobi
        """
        # Create matching chef
        sample_user_data["email"] = "perfect@example.com"
        sample_user_data["role"] = "chef"
        response = client.post("/api/auth/register", json=sample_user_data)
        token = response.json()["token"]
        chef_id = response.json()["chef_profile"]["id"]
        
        client.patch(
            f"/api/chefs/{chef_id}",
            json={
                "cuisines": "Italian,French",
                "hourly_rate": 60.0,
                "location": "Nairobi"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Filter with all criteria
        response = client.get("/api/chefs?cuisine=Italian&max_price=80&location=Nairobi")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
    
    def test_search_by_name(self, client, sample_user_data):
        """
        Test searching chefs by name
        Frontend: Search bar input
        """
        sample_user_data["name"] = "Gordon Ramsay"
        sample_user_data["role"] = "chef"
        client.post("/api/auth/register", json=sample_user_data)
        
        response = client.get("/api/chefs?search=Gordon")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert "Gordon" in data[0]["name"]
    
    def test_empty_results(self, client):
        """
        Test searching with no matching results
        Frontend: Shows "No chefs found" message
        """
        response = client.get("/api/chefs?cuisine=Ethiopian&max_price=5")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0


# TODO: Add tests for:
# - Pagination
# - Sorting (by rating, price, etc.)
# - Only show available chefs
