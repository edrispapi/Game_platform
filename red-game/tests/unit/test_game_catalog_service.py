"""
Unit tests for Game Catalog Service
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.game_catalog_service.app.main import app
from services.game_catalog_service.app import crud, schemas, models

client = TestClient(app)

def test_create_game(db_session: Session, test_game_data):
    """Test creating a new game"""
    game = crud.create_game(db_session, schemas.GameCreate(**test_game_data))
    assert game.title == test_game_data["title"]
    assert game.description == test_game_data["description"]
    assert game.price == test_game_data["price"]

def test_get_game_by_id(db_session: Session, test_game_data):
    """Test getting a game by ID"""
    # Create a game first
    game = crud.create_game(db_session, schemas.GameCreate(**test_game_data))
    
    # Get game by ID
    found_game = crud.get_game(db_session, game_id=game.id)
    assert found_game is not None
    assert found_game.title == test_game_data["title"]

def test_search_games(db_session: Session, test_game_data):
    """Test searching games"""
    # Create a game first
    game = crud.create_game(db_session, schemas.GameCreate(**test_game_data))
    
    # Search for games
    games = crud.search_games(db_session, query="Test")
    assert len(games) > 0
    assert any(g.title == test_game_data["title"] for g in games)

def test_game_catalog_api_endpoints():
    """Test game catalog API endpoints"""
    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "game-catalog-service"

    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert "Game Catalog Service API" in response.json()["message"]

def test_create_game_endpoint():
    """Test creating a game via API"""
    game_data = {
        "title": "Test Game",
        "description": "A test game for testing purposes",
        "price": 29.99,
        "genre": "Action",
        "platform": "PC"
    }
    
    response = client.post("/api/v1/catalog/games", json=game_data)
    assert response.status_code == 201
    
    game = response.json()
    assert game["title"] == game_data["title"]
    assert game["description"] == game_data["description"]
    assert game["price"] == game_data["price"]
    assert "id" in game
    assert "created_at" in game

def test_get_game_endpoint():
    """Test getting a game via API"""
    # First create a game
    game_data = {
        "title": "Test Game 2",
        "description": "Another test game",
        "price": 19.99,
        "genre": "RPG",
        "platform": "PC"
    }
    
    create_response = client.post("/api/v1/catalog/games", json=game_data)
    assert create_response.status_code == 201
    game_id = create_response.json()["id"]
    
    # Now get the game
    response = client.get(f"/api/v1/catalog/games/{game_id}")
    assert response.status_code == 200
    
    game = response.json()
    assert game["title"] == game_data["title"]
    assert game["description"] == game_data["description"]

def test_search_games_endpoint():
    """Test searching games via API"""
    # Create some test games
    games_data = [
        {
            "title": "Action Game",
            "description": "An action-packed game",
            "price": 29.99,
            "genre": "Action",
            "platform": "PC"
        },
        {
            "title": "RPG Game",
            "description": "A role-playing game",
            "price": 39.99,
            "genre": "RPG",
            "platform": "PC"
        }
    ]
    
    for game_data in games_data:
        response = client.post("/api/v1/catalog/games", json=game_data)
        assert response.status_code == 201
    
    # Search for games
    response = client.get("/api/v1/catalog/games/search?q=Action")
    assert response.status_code == 200
    
    games = response.json()
    assert len(games) > 0
    assert any(game["title"] == "Action Game" for game in games)

def test_get_nonexistent_game():
    """Test getting a game that doesn't exist"""
    response = client.get("/api/v1/catalog/games/nonexistent-id")
    assert response.status_code == 404
    assert "Game not found" in response.json()["detail"]