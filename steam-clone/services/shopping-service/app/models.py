"""
Shopping Service Database Models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from enum import Enum as PyEnum
from shared.database import Base

class CartStatus(PyEnum):
    ACTIVE = "active"
    ABANDONED = "abandoned"
    CONVERTED = "converted"
    EXPIRED = "expired"

class WishlistStatus(PyEnum):
    ACTIVE = "active"
    PURCHASED = "purchased"
    REMOVED = "removed"

class ShoppingCart(Base):
    __tablename__ = "shopping_carts"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to user service
    status = Column(String(20), default="active", nullable=False)
    
    # Cart metadata
    session_id = Column(String(255), nullable=True, index=True)  # For guest users
    currency = Column(String(3), default="USD", nullable=False)
    language = Column(String(5), default="en", nullable=False)
    
    # Pricing
    subtotal = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Additional metadata
    metadata = Column(JSONB, nullable=True)
    
    # Relationships
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_carts_user_status', 'user_id', 'status'),
        Index('idx_carts_session_status', 'session_id', 'status'),
    )

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("shopping_carts.id"), nullable=False, index=True)
    game_id = Column(Integer, nullable=False, index=True)  # Reference to game catalog service
    quantity = Column(Integer, default=1, nullable=False)
    
    # Pricing
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    
    # Item metadata
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Additional metadata
    metadata = Column(JSONB, nullable=True)
    
    # Relationships
    cart = relationship("ShoppingCart", back_populates="items")
    
    # Ensure unique game per cart
    __table_args__ = (
        Index('idx_cart_items_cart_game', 'cart_id', 'game_id', unique=True),
    )

class Wishlist(Base):
    __tablename__ = "wishlists"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to user service
    name = Column(String(100), nullable=False)  # e.g., "My Wishlist", "Games to Buy"
    description = Column(String(500), nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Additional metadata
    metadata = Column(JSONB, nullable=True)
    
    # Relationships
    items = relationship("WishlistItem", back_populates="wishlist", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_wishlists_user_default', 'user_id', 'is_default'),
        Index('idx_wishlists_user_public', 'user_id', 'is_public'),
    )

class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False, index=True)
    game_id = Column(Integer, nullable=False, index=True)  # Reference to game catalog service
    status = Column(String(20), default="active", nullable=False)
    
    # Pricing at time of addition
    price_when_added = Column(Float, nullable=True)
    currency_when_added = Column(String(3), nullable=True)
    
    # Notifications
    notify_on_sale = Column(Boolean, default=True, nullable=False)
    notify_on_release = Column(Boolean, default=True, nullable=False)
    notify_on_price_drop = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Additional metadata
    metadata = Column(JSONB, nullable=True)
    
    # Relationships
    wishlist = relationship("Wishlist", back_populates="items")
    
    # Ensure unique game per wishlist
    __table_args__ = (
        Index('idx_wishlist_items_wishlist_game', 'wishlist_id', 'game_id', unique=True),
    )

class Coupon(Base):
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    
    # Discount configuration
    discount_type = Column(String(20), nullable=False)  # percentage, fixed_amount, free_shipping
    discount_value = Column(Float, nullable=False)
    minimum_amount = Column(Float, default=0.0, nullable=False)
    maximum_discount = Column(Float, nullable=True)
    
    # Usage limits
    usage_limit = Column(Integer, nullable=True)  # Total usage limit
    usage_limit_per_user = Column(Integer, default=1, nullable=False)
    used_count = Column(Integer, default=0, nullable=False)
    
    # Validity
    is_active = Column(Boolean, default=True, nullable=False)
    valid_from = Column(DateTime(timezone=True), nullable=True)
    valid_until = Column(DateTime(timezone=True), nullable=True)
    
    # Applicable games
    applicable_games = Column(JSONB, nullable=True)  # List of game IDs
    applicable_genres = Column(JSONB, nullable=True)  # List of genre IDs
    applicable_tags = Column(JSONB, nullable=True)  # List of tag IDs
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Additional metadata
    metadata = Column(JSONB, nullable=True)

class CouponUsage(Base):
    __tablename__ = "coupon_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to user service
    cart_id = Column(Integer, ForeignKey("shopping_carts.id"), nullable=True, index=True)
    order_id = Column(Integer, nullable=True, index=True)  # Reference to purchase service
    
    # Usage details
    discount_amount = Column(Float, nullable=False)
    used_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    coupon = relationship("Coupon")
    cart = relationship("ShoppingCart")

class PriceAlert(Base):
    __tablename__ = "price_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to user service
    game_id = Column(Integer, nullable=False, index=True)  # Reference to game catalog service
    target_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Alert configuration
    is_active = Column(Boolean, default=True, nullable=False)
    notify_email = Column(Boolean, default=True, nullable=False)
    notify_push = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_checked = Column(DateTime(timezone=True), nullable=True)
    
    # Additional metadata
    metadata = Column(JSONB, nullable=True)
    
    # Ensure unique alert per user per game
    __table_args__ = (
        Index('idx_price_alerts_user_game', 'user_id', 'game_id', unique=True),
    )