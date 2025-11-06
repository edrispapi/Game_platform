"""
Unit tests for User Service
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.user_service.app.main import app
from services.user_service.app import crud, schemas, models

client = TestClient(app)

def test_create_user(db_session: Session, test_user_data):
    """Test creating a new user"""
    user = crud.create_user(db_session, schemas.UserCreate(**test_user_data))
    assert user.username == test_user_data["username"]
    assert user.email == test_user_data["email"]
    assert user.full_name == test_user_data["full_name"]

def test_get_user_by_username(db_session: Session, test_user_data):
    """Test getting a user by username"""
    # Create a user first
    user = crud.create_user(db_session, schemas.UserCreate(**test_user_data))
    
    # Get user by username
    found_user = crud.get_user_by_username(db_session, username=test_user_data["username"])
    assert found_user is not None
    assert found_user.username == test_user_data["username"]

def test_authenticate_user(db_session: Session, test_user_data):
    """Test user authentication"""
    # Create a user first
    user = crud.create_user(db_session, schemas.UserCreate(**test_user_data))
    
    # Test authentication
    authenticated_user = crud.authenticate_user(
        db_session, 
        username=test_user_data["username"], 
        password=test_user_data["password"]
    )
    assert authenticated_user is not None
    assert authenticated_user.username == test_user_data["username"]

def test_user_api_endpoints():
    """Test user API endpoints"""
    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "user-service"

    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert "User Service API" in response.json()["message"]

def test_create_user_endpoint():
    """Test creating a user via API"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    user = response.json()
    assert user["username"] == user_data["username"]
    assert user["email"] == user_data["email"]
    assert user["full_name"] == user_data["full_name"]
    assert "id" in user
    assert "created_at" in user

def test_get_user_endpoint():
    """Test getting a user via API"""
    # First create a user
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword123",
        "full_name": "Test User 2"
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]
    
    # Now get the user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    
    user = response.json()
    assert user["username"] == user_data["username"]
    assert user["email"] == user_data["email"]

def test_get_nonexistent_user():
    """Test getting a user that doesn't exist"""
    response = client.get("/api/v1/users/nonexistent-id")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]