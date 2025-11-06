"""
Pytest configuration and shared fixtures
"""
import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.database import Base

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    # This will be overridden by individual service tests
    pass

@pytest.fixture(scope="function")
def test_user_data():
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }

@pytest.fixture(scope="function")
def test_game_data():
    """Sample game data for testing."""
    return {
        "title": "Test Game",
        "description": "A test game for testing purposes",
        "price": 29.99,
        "genre": "Action",
        "platform": "PC"
    }

@pytest.fixture(scope="function")
def test_review_data():
    """Sample review data for testing."""
    return {
        "user_id": "test-user-id",
        "game_id": "test-game-id",
        "rating": 5,
        "title": "Great game!",
        "content": "This is a fantastic game that I highly recommend.",
        "is_positive": True
    }