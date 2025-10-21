"""
Shopping Service Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class CartItemBase(BaseModel):
    game_id: str
    game_name: str
    price: Decimal
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None

class CartItemResponse(CartItemBase):
    id: str
    cart_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ShoppingCartBase(BaseModel):
    user_id: str

class ShoppingCartCreate(ShoppingCartBase):
    pass

class ShoppingCartResponse(ShoppingCartBase):
    id: str
    created_at: datetime
    updated_at: datetime
    items: List[CartItemResponse] = []
    
    class Config:
        from_attributes = True

class WishlistItemBase(BaseModel):
    game_id: str
    game_name: str
    price: Decimal

class WishlistItemCreate(WishlistItemBase):
    pass

class WishlistItemResponse(WishlistItemBase):
    id: str
    wishlist_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class WishlistBase(BaseModel):
    user_id: str
    name: str = "My Wishlist"

class WishlistCreate(WishlistBase):
    pass

class WishlistResponse(WishlistBase):
    id: str
    created_at: datetime
    updated_at: datetime
    items: List[WishlistItemResponse] = []
    
    class Config:
        from_attributes = True