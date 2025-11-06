"""
Payment Service Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# Add your schemas here
# Example:
# class PaymentBase(BaseModel):
#     pass
# 
# class PaymentCreate(PaymentBase):
#     pass
# 
# class PaymentResponse(PaymentBase):
#     id: str
#     created_at: datetime
#     
#     class Config:
#         from_attributes = True
