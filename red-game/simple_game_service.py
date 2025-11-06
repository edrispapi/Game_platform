#!/usr/bin/env python3
"""
Simple Game Catalog Service
A simplified version that uses sample data without requiring a database
"""

import json
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Simple Game Catalog Service",
    description="A simplified game catalog service using sample data",
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

# Load sample data
def load_sample_data():
    """Load sample data from JSON files"""
    data = {}
    sample_data_dir = "/workspace/red-game/sample_data"
    
    for filename in ["games.json", "users.json", "reviews.json", "achievements.json"]:
        filepath = os.path.join(sample_data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data[filename.replace('.json', '')] = json.load(f)
        else:
            data[filename.replace('.json', '')] = []
    
    return data

# Load data on startup
sample_data = load_sample_data()

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Simple Game Catalog Service API", 
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "simple-game-catalog-service"}

@app.get("/api/v1/games")
def get_games(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    is_free: Optional[bool] = Query(None)
):
    """Get games with optional filtering"""
    games = sample_data.get("games", [])
    
    # Apply filters
    if search:
        games = [g for g in games if search.lower() in g.get("name", "").lower()]
    
    if genre:
        games = [g for g in games if genre.lower() in [g.lower() for g in g.get("genres", [])]]
    
    if platform:
        games = [g for g in games if platform.lower() in [p.lower() for p in g.get("platforms", [])]]
    
    if min_price is not None:
        games = [g for g in games if g.get("price", 0) >= min_price]
    
    if max_price is not None:
        games = [g for g in games if g.get("price", 0) <= max_price]
    
    if is_free is not None:
        games = [g for g in games if g.get("is_free", False) == is_free]
    
    # Apply pagination
    total = len(games)
    games = games[offset:offset + limit]
    
    return {
        "games": games,
        "total": total,
        "limit": limit,
        "offset": offset
    }

@app.get("/api/v1/games/{game_id}")
def get_game(game_id: int):
    """Get a specific game by ID"""
    games = sample_data.get("games", [])
    game = next((g for g in games if g.get("app_id") == game_id), None)
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return game

@app.get("/api/v1/games/{game_id}/reviews")
def get_game_reviews(
    game_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get reviews for a specific game"""
    reviews = sample_data.get("reviews", [])
    game_reviews = [r for r in reviews if r.get("game_id") == game_id]
    
    total = len(game_reviews)
    game_reviews = game_reviews[offset:offset + limit]
    
    return {
        "reviews": game_reviews,
        "total": total,
        "limit": limit,
        "offset": offset
    }

@app.get("/api/v1/games/{game_id}/achievements")
def get_game_achievements(game_id: int):
    """Get achievements for a specific game"""
    achievements = sample_data.get("achievements", [])
    game_achievements = [a for a in achievements if a.get("game_id") == game_id]
    
    return {
        "achievements": game_achievements,
        "total": len(game_achievements)
    }

@app.get("/api/v1/genres")
def get_genres():
    """Get all available genres"""
    games = sample_data.get("games", [])
    genres = set()
    for game in games:
        genres.update(game.get("genres", []))
    
    return {"genres": sorted(list(genres))}

@app.get("/api/v1/platforms")
def get_platforms():
    """Get all available platforms"""
    games = sample_data.get("games", [])
    platforms = set()
    for game in games:
        platforms.update(game.get("platforms", []))
    
    return {"platforms": sorted(list(platforms))}

@app.get("/api/v1/stats")
def get_stats():
    """Get general statistics"""
    games = sample_data.get("games", [])
    users = sample_data.get("users", [])
    reviews = sample_data.get("reviews", [])
    achievements = sample_data.get("achievements", [])
    
    free_games = sum(1 for g in games if g.get("is_free", False))
    paid_games = len(games) - free_games
    avg_price = sum(g.get("price", 0) for g in games if not g.get("is_free", False)) / paid_games if paid_games > 0 else 0
    
    positive_reviews = sum(1 for r in reviews if r.get("is_positive", False))
    avg_rating = sum(r.get("rating", 0) for r in reviews) / len(reviews) if reviews else 0
    
    return {
        "games": {
            "total": len(games),
            "free": free_games,
            "paid": paid_games,
            "average_price": round(avg_price, 2)
        },
        "users": {
            "total": len(users),
            "verified": sum(1 for u in users if u.get("is_verified", False)),
            "premium": sum(1 for u in users if u.get("is_premium", False))
        },
        "reviews": {
            "total": len(reviews),
            "positive": positive_reviews,
            "negative": len(reviews) - positive_reviews,
            "average_rating": round(avg_rating, 2)
        },
        "achievements": {
            "total": len(achievements),
            "rare": sum(1 for a in achievements if a.get("is_rare", False)),
            "hidden": sum(1 for a in achievements if a.get("is_hidden", False))
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Simple Game Catalog Service...")
    print("📊 Loaded sample data:")
    print(f"  - Games: {len(sample_data.get('games', []))}")
    print(f"  - Users: {len(sample_data.get('users', []))}")
    print(f"  - Reviews: {len(sample_data.get('reviews', []))}")
    print(f"  - Achievements: {len(sample_data.get('achievements', []))}")
    print("🌐 Service will be available at: http://localhost:8002")
    print("📚 API documentation at: http://localhost:8002/docs")
    
    uvicorn.run(
        "simple_game_service:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )
