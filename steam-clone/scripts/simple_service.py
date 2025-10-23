#!/usr/bin/env python3
"""
Simple FastAPI Service for Testing
A minimal service that can run without external dependencies
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import random
from datetime import datetime
from typing import List, Dict, Any

# Create FastAPI app
app = FastAPI(
    title="Steam Clone Test Service",
    description="A simple test service for Steam Clone platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
mock_games = []
mock_users = []

def generate_mock_data():
    """Generate mock data for testing"""
    global mock_games, mock_users
    
    # Generate mock games
    for i in range(100):
        game = {
            "id": i + 1,
            "app_id": 100000 + i,
            "name": f"Test Game {i + 1}",
            "type": "game",
            "price": round(random.uniform(4.99, 79.99), 2),
            "discount": random.choice([0, 0, 0, 10, 15, 20, 25, 30]),
            "final_price": 0,  # Will be calculated
            "currency": "USD",
            "release_date": "2023-01-01",
            "developer": random.choice([
                "Valve Corporation", "CD Projekt Red", "Rockstar Games", "Ubisoft",
                "Electronic Arts", "Activision", "Blizzard Entertainment", "Bethesda"
            ]),
            "publisher": random.choice([
                "Valve Corporation", "CD Projekt", "Rockstar Games", "Ubisoft",
                "Electronic Arts", "Activision", "Blizzard Entertainment", "Bethesda"
            ]),
            "genres": random.sample([
                "Action", "Adventure", "RPG", "Strategy", "Simulation", "Sports",
                "Racing", "Fighting", "Puzzle", "Horror", "Indie", "Casual"
            ], random.randint(1, 4)),
            "tags": random.sample([
                "Singleplayer", "Multiplayer", "Co-op", "Online Co-op", "Local Co-op",
                "PvP", "MMO", "VR", "Early Access", "Free to Play", "Steam Workshop",
                "Steam Cloud", "Steam Achievements", "Steam Trading Cards",
                "Controller Support", "Full Controller Support", "Partial Controller Support",
                "Keyboard and Mouse", "Touch Controls", "Tracked Motion Controllers",
                "Valve Index", "HTC Vive", "Oculus Rift", "Windows Mixed Reality",
                "OpenVR", "SteamVR", "Room-Scale", "Seated", "Standing"
            ], random.randint(5, 15)),
            "platforms": random.sample(["Windows", "Mac", "Linux"], random.randint(1, 3)),
            "description": f"Experience the ultimate gaming adventure in Test Game {i + 1}.",
            "short_description": f"An amazing game that will captivate you from start to finish.",
            "header_image": f"https://cdn.akamai.steamstatic.com/steam/apps/{100000 + i}/header.jpg",
            "capsule_image": f"https://cdn.akamai.steamstatic.com/steam/apps/{100000 + i}/capsule_616x353.jpg",
            "background": f"https://cdn.akamai.steamstatic.com/steam/apps/{100000 + i}/page_bg_generated_v6b.jpg",
            "metacritic_score": random.randint(60, 95) if random.random() > 0.3 else None,
            "steam_score": random.randint(70, 95),
            "positive_reviews": random.randint(100, 50000),
            "negative_reviews": random.randint(10, 5000),
            "total_reviews": 0,  # Will be calculated
            "languages": random.sample([
                "English", "Spanish", "French", "German", "Italian", "Portuguese",
                "Russian", "Japanese", "Korean", "Chinese (Simplified)"
            ], random.randint(1, 8)),
            "achievements": random.randint(0, 100),
            "dlc_count": random.randint(0, 10),
            "is_free": random.choice([True, False, False, False]),
            "is_early_access": random.choice([True, False, False, False, False]),
            "is_vr_supported": random.choice([True, False, False, False, False]),
            "is_multiplayer": random.choice([True, False]),
            "is_singleplayer": random.choice([True, False]),
            "is_coop": random.choice([True, False]),
            "is_online_coop": random.choice([True, False]),
            "is_local_coop": random.choice([True, False]),
            "is_pvp": random.choice([True, False]),
            "is_mmo": random.choice([True, False]),
            "is_strategy": random.choice([True, False]),
            "is_rpg": random.choice([True, False]),
            "is_action": random.choice([True, False]),
            "is_adventure": random.choice([True, False]),
            "is_simulation": random.choice([True, False]),
            "is_sports": random.choice([True, False]),
            "is_racing": random.choice([True, False]),
            "is_fighting": random.choice([True, False]),
            "is_puzzle": random.choice([True, False]),
            "is_horror": random.choice([True, False]),
            "is_indie": random.choice([True, False]),
            "is_casual": random.choice([True, False]),
            "is_educational": False,
            "is_utilities": False,
            "is_web": False,
            "is_software": False,
            "is_video": False,
            "is_music": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Calculate derived fields
        game["final_price"] = round(game["price"] * (1 - game["discount"] / 100), 2)
        game["total_reviews"] = game["positive_reviews"] + game["negative_reviews"]
        
        mock_games.append(game)
    
    # Generate mock users
    for i in range(100):
        user = {
            "id": f"user-{i + 1}",
            "username": f"user{random.randint(1000, 9999)}",
            "email": f"user{random.randint(1000, 9999)}@example.com",
            "first_name": random.choice(["John", "Jane", "Mike", "Sarah", "David", "Lisa", "Chris", "Emma", "Alex", "Maria"]),
            "last_name": random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]),
            "display_name": f"user{random.randint(1000, 9999)}#{random.randint(1000, 9999)}",
            "avatar_url": f"https://api.dicebear.com/7.x/avataaars/svg?seed=user{i + 1}",
            "country": random.choice(["US", "CA", "GB", "DE", "FR", "IT", "ES", "AU", "JP", "KR", "BR", "MX", "RU", "CN", "IN"]),
            "language": random.choice(["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"]),
            "timezone": random.choice(["UTC-8", "UTC-5", "UTC+0", "UTC+1", "UTC+8", "UTC+9"]),
            "is_active": random.choice([True, True, True, False]),
            "is_verified": random.choice([True, True, False]),
            "is_premium": random.choice([True, False, False, False]),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat() if random.random() > 0.1 else None,
            "preferences": {
                "theme": random.choice(["dark", "light", "auto"]),
                "notifications": {
                    "email": random.choice([True, False]),
                    "push": random.choice([True, False]),
                    "in_game": True
                },
                "privacy": {
                    "profile_public": random.choice([True, False]),
                    "game_library_public": random.choice([True, False]),
                    "activity_public": random.choice([True, False])
                }
            }
        }
        
        mock_users.append(user)

# Initialize mock data
generate_mock_data()

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "steam-clone-test-service",
        "timestamp": datetime.now().isoformat(),
        "games_count": len(mock_games),
        "users_count": len(mock_users)
    }

# Root endpoint
@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Steam Clone Test Service API", 
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Games endpoints
@app.get("/games")
def get_games(skip: int = 0, limit: int = 100):
    """Get all games with pagination"""
    return {
        "games": mock_games[skip:skip + limit],
        "total": len(mock_games),
        "skip": skip,
        "limit": limit
    }

@app.get("/games/{game_id}")
def get_game(game_id: int):
    """Get a specific game by ID"""
    game = next((g for g in mock_games if g["id"] == game_id), None)
    if not game:
        return {"error": "Game not found"}
    return game

@app.get("/games/search")
def search_games(q: str = "", genre: str = "", platform: str = "", skip: int = 0, limit: int = 100):
    """Search games"""
    filtered_games = mock_games
    
    if q:
        filtered_games = [g for g in filtered_games if q.lower() in g["name"].lower()]
    
    if genre:
        filtered_games = [g for g in filtered_games if genre in g["genres"]]
    
    if platform:
        filtered_games = [g for g in filtered_games if platform in g["platforms"]]
    
    return {
        "games": filtered_games[skip:skip + limit],
        "total": len(filtered_games),
        "skip": skip,
        "limit": limit,
        "query": q,
        "genre": genre,
        "platform": platform
    }

# Users endpoints
@app.get("/users")
def get_users(skip: int = 0, limit: int = 100):
    """Get all users with pagination"""
    return {
        "users": mock_users[skip:skip + limit],
        "total": len(mock_users),
        "skip": skip,
        "limit": limit
    }

@app.get("/users/{user_id}")
def get_user(user_id: str):
    """Get a specific user by ID"""
    user = next((u for u in mock_users if u["id"] == user_id), None)
    if not user:
        return {"error": "User not found"}
    return user

@app.get("/users/me")
def get_current_user():
    """Get current user (mock)"""
    return mock_users[0] if mock_users else {"error": "No users available"}

# Reviews endpoints
@app.get("/reviews")
def get_reviews(skip: int = 0, limit: int = 100):
    """Get all reviews with pagination"""
    reviews = []
    for i in range(50):  # Generate 50 mock reviews
        review = {
            "id": f"review-{i + 1}",
            "user_id": random.choice(mock_users)["id"],
            "game_id": random.choice(mock_games)["id"],
            "rating": random.randint(1, 5),
            "title": f"Review for {random.choice(mock_games)['name']}",
            "content": random.choice([
                "Amazing game! Highly recommended!",
                "Great graphics and gameplay.",
                "Not bad, but could be better.",
                "Disappointed with this game.",
                "One of the best games I've played this year.",
                "Good game but has some bugs.",
                "Love this game! Perfect for relaxing.",
                "Waste of money. Not what I expected.",
                "Decent game with good potential.",
                "Absolutely fantastic! A masterpiece."
            ]),
            "is_positive": random.choice([True, False]),
            "is_helpful": random.choice([True, True, True, False]),
            "helpful_count": random.randint(0, 50),
            "not_helpful_count": random.randint(0, 10),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        reviews.append(review)
    
    return {
        "reviews": reviews[skip:skip + limit],
        "total": len(reviews),
        "skip": skip,
        "limit": limit
    }

# Shopping endpoints
@app.get("/cart")
def get_cart():
    """Get shopping cart (mock)"""
    cart_items = []
    for i in range(random.randint(1, 5)):
        game = random.choice(mock_games)
        cart_items.append({
            "id": f"cart-item-{i + 1}",
            "game_id": game["id"],
            "game_name": game["name"],
            "price": game["final_price"],
            "quantity": random.randint(1, 3),
            "added_at": datetime.now().isoformat()
        })
    
    return {
        "cart_id": "cart-1",
        "items": cart_items,
        "total_items": len(cart_items),
        "total_amount": sum(item["price"] * item["quantity"] for item in cart_items)
    }

@app.get("/wishlist")
def get_wishlist():
    """Get wishlist (mock)"""
    wishlist_items = []
    for i in range(random.randint(3, 10)):
        game = random.choice(mock_games)
        wishlist_items.append({
            "id": f"wishlist-item-{i + 1}",
            "game_id": game["id"],
            "game_name": game["name"],
            "price": game["final_price"],
            "added_at": datetime.now().isoformat()
        })
    
    return {
        "wishlist_id": "wishlist-1",
        "items": wishlist_items,
        "total_items": len(wishlist_items)
    }

# Statistics endpoint
@app.get("/stats")
def get_stats():
    """Get service statistics"""
    return {
        "games": {
            "total": len(mock_games),
            "free": len([g for g in mock_games if g["is_free"]]),
            "paid": len([g for g in mock_games if not g["is_free"]]),
            "early_access": len([g for g in mock_games if g["is_early_access"]]),
            "vr_supported": len([g for g in mock_games if g["is_vr_supported"]]),
            "multiplayer": len([g for g in mock_games if g["is_multiplayer"]]),
            "average_price": sum(g["final_price"] for g in mock_games if not g["is_free"]) / len([g for g in mock_games if not g["is_free"]]) if any(not g["is_free"] for g in mock_games) else 0,
            "average_rating": sum(g["steam_score"] for g in mock_games) / len(mock_games) if mock_games else 0
        },
        "users": {
            "total": len(mock_users),
            "active": len([u for u in mock_users if u["is_active"]]),
            "verified": len([u for u in mock_users if u["is_verified"]]),
            "premium": len([u for u in mock_users if u["is_premium"]]),
            "countries": len(set(u["country"] for u in mock_users)),
            "languages": len(set(u["language"] for u in mock_users))
        },
        "service": {
            "name": "steam-clone-test-service",
            "version": "1.0.0",
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Steam Clone Test Service...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("📊 Statistics: http://localhost:8000/stats")
    print("⏹️  Press Ctrl+C to stop")
    
    uvicorn.run(
        "simple_service:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )