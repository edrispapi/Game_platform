"""
Purchase Service CRUD Operations
"""
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
import uuid
from datetime import datetime

def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    """Create a new order"""
    # Generate unique order number
    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    # Create order
    db_order = models.Order(
        user_id=order.user_id,
        order_number=order_number,
        total_amount=order.total_amount,
        currency=order.currency
    )
    db.add(db_order)
    db.flush()  # Get the order ID
    
    # Create order items
    for item in order.order_items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            game_id=item.game_id,
            game_title=item.game_title,
            price=item.price,
            quantity=item.quantity
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    """Get order by ID"""
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_order_by_number(db: Session, order_number: str) -> Optional[models.Order]:
    """Get order by order number"""
    return db.query(models.Order).filter(models.Order.order_number == order_number).first()

def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Order]:
    """Get orders for a user"""
    return db.query(models.Order).filter(models.Order.user_id == user_id).offset(skip).limit(limit).all()

def update_order_status(db: Session, order_id: int, status: models.OrderStatus) -> Optional[models.Order]:
    """Update order status"""
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = status
        if status == models.OrderStatus.COMPLETED:
            db_order.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(db_order)
    return db_order

def create_payment_transaction(db: Session, transaction: schemas.PaymentTransactionCreate) -> models.PaymentTransaction:
    """Create a payment transaction"""
    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    
    db_transaction = models.PaymentTransaction(
        order_id=transaction.order_id,
        transaction_id=transaction_id,
        payment_method=transaction.payment_method,
        amount=transaction.amount
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_payment_status(db: Session, transaction_id: str, status: models.PaymentStatus) -> Optional[models.PaymentTransaction]:
    """Update payment transaction status"""
    db_transaction = db.query(models.PaymentTransaction).filter(
        models.PaymentTransaction.transaction_id == transaction_id
    ).first()
    if db_transaction:
        db_transaction.status = status
        if status == models.PaymentStatus.PAID:
            db_transaction.processed_at = datetime.utcnow()
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def create_refund(db: Session, refund: schemas.RefundCreate) -> models.Refund:
    """Create a refund"""
    refund_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
    
    db_refund = models.Refund(
        order_id=refund.order_id,
        refund_id=refund_id,
        amount=refund.amount,
        reason=refund.reason
    )
    db.add(db_refund)
    db.commit()
    db.refresh(db_refund)
    return db_refund

def get_order_summary(db: Session, user_id: Optional[int] = None) -> dict:
    """Get order summary statistics"""
    query = db.query(models.Order)
    if user_id:
        query = query.filter(models.Order.user_id == user_id)
    
    total_orders = query.count()
    total_revenue = query.filter(models.Order.status == models.OrderStatus.COMPLETED).with_entities(
        db.func.sum(models.Order.total_amount)
    ).scalar() or 0
    
    pending_orders = query.filter(models.Order.status == models.OrderStatus.PENDING).count()
    completed_orders = query.filter(models.Order.status == models.OrderStatus.COMPLETED).count()
    cancelled_orders = query.filter(models.Order.status == models.OrderStatus.CANCELLED).count()
    
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders
    }