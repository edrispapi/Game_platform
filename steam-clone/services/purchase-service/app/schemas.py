"""
Purchase Service Pydantic Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from .models import OrderStatus, PaymentStatus

class OrderItemBase(BaseModel):
    game_id: int
    game_title: str
    price: Decimal
    quantity: int = 1

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    total_amount: Decimal
    currency: str = "USD"

class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None

class OrderResponse(OrderBase):
    id: int
    order_number: str
    status: OrderStatus
    payment_status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    order_items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

class PaymentTransactionBase(BaseModel):
    order_id: int
    payment_method: str
    amount: Decimal

class PaymentTransactionCreate(PaymentTransactionBase):
    pass

class PaymentTransactionResponse(PaymentTransactionBase):
    id: int
    transaction_id: str
    status: PaymentStatus
    gateway_response: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class RefundBase(BaseModel):
    order_id: int
    amount: Decimal
    reason: Optional[str] = None

class RefundCreate(RefundBase):
    pass

class RefundResponse(RefundBase):
    id: int
    refund_id: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class OrderSummary(BaseModel):
    total_orders: int
    total_revenue: Decimal
    pending_orders: int
    completed_orders: int
    cancelled_orders: int