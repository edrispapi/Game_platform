"""HTTP routes for the simplified review service."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.ReviewResponse)
def create_review(payload: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, payload)


@router.get("/highlights", response_model=List[schemas.ReviewResponse])
def review_highlights(limit: int = 5, db: Session = Depends(get_db)):
    highlights = crud.get_review_highlights(db, limit=limit)
    return highlights
