"""
Purchase Service Database Models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    status = Column(String(20), default="pending")  # pending, completed, cancelled, refunded
    payment_method = Column(String(50))
    payment_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")

class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    purchase_id = Column(String, ForeignKey("purchases.id"), nullable=False)
    game_id = Column(String, nullable=False)
    game_name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    purchase = relationship("Purchase", back_populates="items")

class Refund(Base):
    __tablename__ = "refunds"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    purchase_id = Column(String, ForeignKey("purchases.id"), nullable=False)
    user_id = Column(String, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    reason = Column(Text)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    processed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    purchase = relationship("Purchase")