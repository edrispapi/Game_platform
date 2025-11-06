"""
Game Catalog Service API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas, models
from .database import get_db
import math

router = APIRouter()

@router.post("/games", response_model=schemas.GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    """Create a new game"""
    game_crud = crud.GameCRUD(db)
    
    # Check if Steam App ID already exists
    if game.steam_app_id and game_crud.get_game_by_steam_app_id(game.steam_app_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game with this Steam App ID already exists"
        )
    
    # Create game
    db_game = game_crud.create_game(game)
    return db_game

@router.get("/games", response_model=schemas.GameSearchResponse)
def search_games(
    filters: schemas.GameSearchFilters = Depends(),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search games with filters and pagination"""
    game_crud = crud.GameCRUD(db)
    games, total = game_crud.search_games(filters, page, per_page)
    
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    
    return {
        "games": games,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "filters_applied": filters
    }

@router.get("/games/{game_id}", response_model=schemas.GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    """Get game by ID"""
    game_crud = crud.GameCRUD(db)
    game = game_crud.get_game_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game

@router.put("/games/{game_id}", response_model=schemas.GameResponse)
def update_game(
    game_id: int,
    game_update: schemas.GameUpdate,
    db: Session = Depends(get_db)
):
    """Update game information"""
    game_crud = crud.GameCRUD(db)
    updated_game = game_crud.update_game(game_id, game_update)
    if not updated_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return updated_game

@router.delete("/games/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    """Delete a game"""
    game_crud = crud.GameCRUD(db)
    success = game_crud.delete_game(game_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return {"message": "Game deleted successfully"}

@router.get("/games/featured", response_model=List[schemas.GameResponse])
def get_featured_games(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get featured games"""
    game_crud = crud.GameCRUD(db)
    games = game_crud.get_featured_games(limit)
    return games

@router.get("/games/new-releases", response_model=List[schemas.GameResponse])
def get_new_releases(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get new releases"""
    game_crud = crud.GameCRUD(db)
    games = game_crud.get_new_releases(limit)
    return games

@router.get("/games/on-sale", response_model=List[schemas.GameResponse])
def get_on_sale_games(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get games on sale"""
    game_crud = crud.GameCRUD(db)
    games = game_crud.get_on_sale_games(limit)
    return games

# Genre routes
@router.post("/genres", response_model=schemas.GenreResponse, status_code=status.HTTP_201_CREATED)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    """Create a new genre"""
    genre_crud = crud.GenreCRUD(db)
    
    # Check if genre already exists
    if genre_crud.get_genre_by_name(genre.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre already exists"
        )
    
    db_genre = genre_crud.create_genre(genre)
    return db_genre

@router.get("/genres", response_model=List[schemas.GenreResponse])
def get_genres(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of genres"""
    genre_crud = crud.GenreCRUD(db)
    genres = genre_crud.get_genres(skip=skip, limit=limit)
    return genres

@router.get("/genres/{genre_id}", response_model=schemas.GenreResponse)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    """Get genre by ID"""
    genre_crud = crud.GenreCRUD(db)
    genre = genre_crud.get_genre_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return genre

# Tag routes
@router.post("/tags", response_model=schemas.TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    """Create a new tag"""
    tag_crud = crud.TagCRUD(db)
    
    # Check if tag already exists
    if tag_crud.get_tag_by_name(tag.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already exists"
        )
    
    db_tag = tag_crud.create_tag(tag)
    return db_tag

@router.get("/tags", response_model=List[schemas.TagResponse])
def get_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of tags"""
    tag_crud = crud.TagCRUD(db)
    tags = tag_crud.get_tags(skip=skip, limit=limit)
    return tags

@router.get("/tags/{tag_id}", response_model=schemas.TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """Get tag by ID"""
    tag_crud = crud.TagCRUD(db)
    tag = tag_crud.get_tag_by_id(tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return tag

# Platform routes
@router.post("/platforms", response_model=schemas.PlatformResponse, status_code=status.HTTP_201_CREATED)
def create_platform(platform: schemas.PlatformCreate, db: Session = Depends(get_db)):
    """Create a new platform"""
    platform_crud = crud.PlatformCRUD(db)
    
    # Check if platform already exists
    if platform_crud.get_platform_by_name(platform.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Platform already exists"
        )
    
    db_platform = platform_crud.create_platform(platform)
    return db_platform

@router.get("/platforms", response_model=List[schemas.PlatformResponse])
def get_platforms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of platforms"""
    platform_crud = crud.PlatformCRUD(db)
    platforms = platform_crud.get_platforms(skip=skip, limit=limit)
    return platforms

@router.get("/platforms/{platform_id}", response_model=schemas.PlatformResponse)
def get_platform(platform_id: int, db: Session = Depends(get_db)):
    """Get platform by ID"""
    platform_crud = crud.PlatformCRUD(db)
    platform = platform_crud.get_platform_by_id(platform_id)
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )
    return platform