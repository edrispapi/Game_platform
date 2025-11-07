"""CRUD helpers for the simplified review service."""
from typing import List

from sqlalchemy.orm import Session

from . import models, schemas


def create_review(db: Session, payload: schemas.ReviewCreate) -> models.Review:
    review = models.Review(
        user_id=payload.user_id,
        game_id=payload.game_id,
        rating=payload.rating,
        title=payload.title,
        content=payload.content,
        is_positive=payload.is_positive,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_review_highlights(db: Session, limit: int = 5) -> List[models.Review]:
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 5
    reviews = [
        review
        for review in db.query(models.Review).all()
        if review.status == models.ReviewStatus.APPROVED.value and review.total_votes > 0
    ]
    reviews.sort(key=lambda review: (review.helpful_votes, review.rating), reverse=True)
    return reviews[:limit]
