"""HTTP routes for the simplified catalog service."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.get("/games/{game_id}", response_model=schemas.GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = crud.get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return game


@router.post("/games", response_model=schemas.GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(payload: schemas.GameCreate, db: Session = Depends(get_db)):
    return crud.create_game(db, payload)


@router.get("/games/search", response_model=List[schemas.GameResponse])
def search_games(q: str = "", db: Session = Depends(get_db)):
    return crud.search_games(db, q)
