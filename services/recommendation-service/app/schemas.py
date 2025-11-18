"""
Recommendation Service Pydantic Schemas
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel, Field, ConfigDict


class RecommendationItem(BaseModel):
    game_id: str
    score: float = Field(..., ge=0.0)
    reason: Optional[str] = Field(default=None, max_length=500)
    context: Optional[Dict[str, str]] = None
    algorithm: str = "hybrid"


class RecommendationBatchCreate(BaseModel):
    user_id: str
    recommendations: List[RecommendationItem]
    expires_in_hours: Optional[int] = Field(default=None, ge=1)


class RecommendationResponse(BaseModel):
    id: int
    uuid: str
    user_id: str
    game_id: str
    score: float
    rank: int
    algorithm: str
    reason: Optional[str]
    context: Optional[Dict[str, str]]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecommendationFeedbackCreate(BaseModel):
    recommendation_id: Optional[int] = None
    user_id: str
    game_id: str
    action: str = Field(..., pattern="^(clicked|ignored|wishlisted|purchased)$")
    details: Optional[Dict[str, str]] = None


class RecommendationFeedbackResponse(RecommendationFeedbackCreate):
    id: int
    recommendation_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
