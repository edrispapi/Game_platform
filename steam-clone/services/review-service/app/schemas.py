"""Pydantic schemas for the simplified review service."""
from pydantic import BaseModel, Field
from typing import Optional

from .models import ReviewStatus


class ReviewCreate(BaseModel):
    user_id: int
    game_id: int
    rating: int = Field(..., ge=1, le=5)
    title: str
    content: str
    is_positive: bool = True


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    game_id: int
    rating: int
    title: str
    content: str
    is_positive: bool
    helpful_votes: int
    total_votes: int
    status: str

    class Config:
        from_attributes = True
