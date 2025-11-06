"""
Shared Pydantic models for API requests/responses
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    status: StatusEnum = StatusEnum.ACTIVE

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class GameBase(BaseModel):
    title: str
    description: str
    developer: str
    publisher: str
    price: float
    release_date: datetime
    genres: List[str] = []
    tags: List[str] = []
    system_requirements: Optional[Dict[str, Any]] = None

class GameCreate(GameBase):
    pass

class GameResponse(GameBase):
    id: int
    created_at: datetime
    updated_at: datetime
    average_rating: Optional[float] = None
    total_reviews: int = 0
    
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    game_id: int
    rating: int
    title: str
    content: str
    is_positive: bool

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    helpful_votes: int = 0
    
    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    user_id: int
    game_id: int
    amount: float
    currency: str = "USD"

class PurchaseCreate(PurchaseBase):
    payment_method: str

class PurchaseResponse(PurchaseBase):
    id: int
    status: str
    created_at: datetime
    transaction_id: Optional[str] = None
    
    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None