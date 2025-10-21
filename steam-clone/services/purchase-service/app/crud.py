"""
Purchase Service CRUD Operations
"""
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def create_purchase(db: Session, purchase: schemas.PurchaseCreate) -> models.Purchase:
    """Create a new purchase"""
    db_purchase = models.Purchase(
        user_id=purchase.user_id,
        total_amount=purchase.total_amount,
        currency=purchase.currency,
        payment_method=purchase.payment_method
    )
    db.add(db_purchase)
    db.flush()  # Get the ID
    
    # Create purchase items
    for item in purchase.items:
        db_item = models.PurchaseItem(
            purchase_id=db_purchase.id,
            game_id=item.game_id,
            game_name=item.game_name,
            price=item.price,
            quantity=item.quantity
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def get_purchase(db: Session, purchase_id: str) -> Optional[models.Purchase]:
    """Get purchase by ID"""
    return db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()

def get_user_purchases(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[models.Purchase]:
    """Get purchases for a user"""
    return db.query(models.Purchase).filter(models.Purchase.user_id == user_id).offset(skip).limit(limit).all()

def update_purchase(db: Session, purchase_id: str, purchase_update: schemas.PurchaseUpdate) -> Optional[models.Purchase]:
    """Update purchase"""
    db_purchase = get_purchase(db, purchase_id)
    if not db_purchase:
        return None
    
    for field, value in purchase_update.dict(exclude_unset=True).items():
        setattr(db_purchase, field, value)
    
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def create_refund(db: Session, refund: schemas.RefundCreate, user_id: str) -> models.Refund:
    """Create a refund request"""
    # Get the purchase to calculate refund amount
    purchase = get_purchase(db, refund.purchase_id)
    if not purchase:
        raise ValueError("Purchase not found")
    
    db_refund = models.Refund(
        purchase_id=refund.purchase_id,
        user_id=user_id,
        amount=purchase.total_amount,
        reason=refund.reason
    )
    db.add(db_refund)
    db.commit()
    db.refresh(db_refund)
    return db_refund

def get_refund(db: Session, refund_id: str) -> Optional[models.Refund]:
    """Get refund by ID"""
    return db.query(models.Refund).filter(models.Refund.id == refund_id).first()

def get_user_refunds(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[models.Refund]:
    """Get refunds for a user"""
    return db.query(models.Refund).filter(models.Refund.user_id == user_id).offset(skip).limit(limit).all()