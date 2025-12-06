import pytest
from fastapi import status


class TestRegister:
    def test_register_client_success(self, client, sample_user_data):
        response = client.post("/api/auth/register", json=sample_user_data)  # Frontend: Register.jsx form submission.
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["role"] == "client"
        assert "token" in data
    
    def test_register_chef_success(self, client, sample_user_data):
        sample_user_data["role"] = "chef"
        response = client.post("/api/auth/register", json=sample_user_data)  # Frontend: Register.jsx with chef role.
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["role"] == "chef"
    
    def test_register_duplicate_email(self, client, sample_user_data):
        client.post("/api/auth/register", json=sample_user_data)  # First registration.
        response = client.post("/api/auth/register", json=sample_user_data)  # Second registration with same email.
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_invalid_email(self, client, sample_user_data):
        sample_user_data["email"] = "not-an-email"
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_missing_fields(self, client):
        response = client.post("/api/auth/register", json={"email": "test@example.com"})  # Missing other required fields.
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLogin:
    def test_login_success(self, client, sample_user_data):
        client.post("/api/auth/register", json=sample_user_data)  # Register user first.
        login_data = {"email": sample_user_data["email"], "password": sample_user_data["password"]}
        response = client.post("/api/auth/login", json=login_data)  # Frontend: Login.jsx form submission.
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "token" in data
        assert data["user"]["email"] == sample_user_data["email"]
    
    def test_login_wrong_password(self, client, sample_user_data):
        client.post("/api/auth/register", json=sample_user_data)
        login_data = {"email": sample_user_data["email"], "password": "WrongPassword!"}
        response = client.post("/api/auth/login", json=login_data)  # Wrong password should fail.
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_nonexistent_user(self, client):
        response = client.post("/api/auth/login", json={"email": "nonexistent@example.com", "password": "Pass123!"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_missing_fields(self, client):
        response = client.post("/api/auth/login", json={"email": "test@example.com"})  # Missing password.
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGoogleLogin:
    def test_google_login_new_user(self, client):
        pytest.skip("TODO: Implement when Firebase integration is complete")  # Frontend: "Sign in with Google" button.
    
    def test_google_login_existing_user(self, client):
        pytest.skip("TODO: Implement when Firebase integration is complete")
