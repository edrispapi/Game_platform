"""
Recommendation Service API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database

router = APIRouter()


@router.post(
    "/batch",
    response_model=List[schemas.RecommendationResponse],
    status_code=status.HTTP_201_CREATED,
)
def upsert_recommendations(
    batch: schemas.RecommendationBatchCreate,
    db: Session = Depends(database.get_db),
):
    """Replace a user's recommendations with a new batch."""
    if not batch.recommendations:
        raise HTTPException(status_code=400, detail="Recommendations list cannot be empty.")
    return crud.replace_user_recommendations(db=db, batch=batch)


@router.get(
    "/user/{user_id}",
    response_model=List[schemas.RecommendationResponse],
)
def get_user_recommendations(
    user_id: str,
    limit: int = 20,
    db: Session = Depends(database.get_db),
):
    """Return the active recommendations for a user."""
    limit = max(1, min(limit, 50))
    return crud.get_user_recommendations(db=db, user_id=user_id, limit=limit)


@router.post(
    "/feedback",
    response_model=schemas.RecommendationFeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(
    feedback: schemas.RecommendationFeedbackCreate,
    db: Session = Depends(database.get_db),
):
    """Record user feedback for a recommendation."""
    return crud.record_feedback(db, feedback.recommendation_id, feedback)
