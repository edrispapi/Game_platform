"""Simplified review model."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from enum import Enum
from sqlalchemy.sql import func

from shared.database import Base


class ReviewStatus(str, Enum):
    APPROVED = "approved"
    PENDING = "pending"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    game_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(1024), nullable=False)
    is_positive = Column(Boolean, default=True)
    helpful_votes = Column(Integer, default=0)
    total_votes = Column(Integer, default=0)
    status = Column(String(32), default=ReviewStatus.PENDING.value)
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
