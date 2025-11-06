"""
Recommendation Service Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# Add your schemas here
# Example:
# class RecommendationBase(BaseModel):
#     pass
# 
# class RecommendationCreate(RecommendationBase):
#     pass
# 
# class RecommendationResponse(RecommendationBase):
#     id: str
#     created_at: datetime
#     
#     class Config:
#         from_attributes = True
