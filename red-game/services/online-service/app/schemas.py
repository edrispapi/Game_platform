"""
Online Service Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# Add your schemas here
# Example:
# class OnlineStatusBase(BaseModel):
#     pass
# 
# class OnlineStatusCreate(OnlineStatusBase):
#     pass
# 
# class OnlineStatusResponse(OnlineStatusBase):
#     id: str
#     created_at: datetime
#     
#     class Config:
#         from_attributes = True
