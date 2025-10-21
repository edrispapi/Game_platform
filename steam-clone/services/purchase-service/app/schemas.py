"""
Purchase Service Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class PurchaseItemBase(BaseModel):
    game_id: str
    game_name: str
    price: Decimal
    quantity: int = 1

class PurchaseItemCreate(PurchaseItemBase):
    pass

class PurchaseItemResponse(PurchaseItemBase):
    id: str
    purchase_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    user_id: str
    total_amount: Decimal
    currency: str = "USD"
    payment_method: Optional[str] = None

class PurchaseCreate(PurchaseBase):
    items: List[PurchaseItemCreate]

class PurchaseUpdate(BaseModel):
    status: Optional[str] = None
    payment_id: Optional[str] = None

class PurchaseResponse(PurchaseBase):
    id: str
    status: str
    payment_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[PurchaseItemResponse] = []
    
    class Config:
        from_attributes = True

class RefundBase(BaseModel):
    purchase_id: str
    reason: Optional[str] = None

class RefundCreate(RefundBase):
    pass

class RefundResponse(RefundBase):
    id: str
    user_id: str
    amount: Decimal
    status: str
    processed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True