"""
Review Service CRUD Operations
"""
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def create_review(db: Session, review: schemas.ReviewCreate) -> models.Review:
    """Create a new review"""
    db_review = models.Review(
        user_id=review.user_id,
        game_id=review.game_id,
        rating=review.rating,
        title=review.title,
        content=review.content,
        is_positive=review.is_positive
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: str) -> Optional[models.Review]:
    """Get review by ID"""
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def get_game_reviews(db: Session, game_id: str, skip: int = 0, limit: int = 100) -> List[models.Review]:
    """Get reviews for a game"""
    return db.query(models.Review).filter(models.Review.game_id == game_id).offset(skip).limit(limit).all()

def get_user_reviews(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[models.Review]:
    """Get reviews by a user"""
    return db.query(models.Review).filter(models.Review.user_id == user_id).offset(skip).limit(limit).all()

def update_review(db: Session, review_id: str, review_update: schemas.ReviewUpdate) -> Optional[models.Review]:
    """Update review"""
    db_review = get_review(db, review_id)
    if not db_review:
        return None
    
    for field, value in review_update.dict(exclude_unset=True).items():
        setattr(db_review, field, value)
    
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: str) -> bool:
    """Delete review"""
    db_review = get_review(db, review_id)
    if not db_review:
        return False
    
    db.delete(db_review)
    db.commit()
    return True

def create_review_comment(db: Session, comment: schemas.ReviewCommentCreate) -> models.ReviewComment:
    """Create a review comment"""
    db_comment = models.ReviewComment(
        review_id=comment.review_id,
        user_id=comment.user_id,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_review_comments(db: Session, review_id: str, skip: int = 0, limit: int = 100) -> List[models.ReviewComment]:
    """Get comments for a review"""
    return db.query(models.ReviewComment).filter(models.ReviewComment.review_id == review_id).offset(skip).limit(limit).all()

def vote_review(db: Session, review_id: str, user_id: str, is_helpful: bool) -> models.ReviewVote:
    """Vote on a review"""
    # Check if user already voted
    existing_vote = db.query(models.ReviewVote).filter(
        models.ReviewVote.review_id == review_id,
        models.ReviewVote.user_id == user_id
    ).first()
    
    if existing_vote:
        existing_vote.is_helpful = is_helpful
        db.commit()
        db.refresh(existing_vote)
        return existing_vote
    
    db_vote = models.ReviewVote(
        review_id=review_id,
        user_id=user_id,
        is_helpful=is_helpful
    )
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote