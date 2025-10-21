"""
Purchase Service API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, models
from .database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """Create a new order"""
    return crud.create_order(db=db, order=order)

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order by ID"""
    order = crud.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/number/{order_number}", response_model=schemas.OrderResponse)
def get_order_by_number(order_number: str, db: Session = Depends(get_db)):
    """Get order by order number"""
    order = crud.get_order_by_number(db=db, order_number=order_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/user/{user_id}", response_model=List[schemas.OrderResponse])
def get_user_orders(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get orders for a user"""
    return crud.get_user_orders(db=db, user_id=user_id, skip=skip, limit=limit)

@router.patch("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: int, status_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    """Update order status"""
    order = crud.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if status_update.status:
        order = crud.update_order_status(db=db, order_id=order_id, status=status_update.status)
    
    return order

@router.post("/{order_id}/payment", response_model=schemas.PaymentTransactionResponse)
def create_payment_transaction(order_id: int, transaction: schemas.PaymentTransactionCreate, db: Session = Depends(get_db)):
    """Create a payment transaction for an order"""
    # Verify order exists
    order = crud.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    transaction.order_id = order_id
    return crud.create_payment_transaction(db=db, transaction=transaction)

@router.patch("/payment/{transaction_id}/status", response_model=schemas.PaymentTransactionResponse)
def update_payment_status(transaction_id: str, status_update: dict, db: Session = Depends(get_db)):
    """Update payment transaction status"""
    status = status_update.get("status")
    if not status:
        raise HTTPException(status_code=400, detail="Status is required")
    
    try:
        payment_status = models.PaymentStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    transaction = crud.update_payment_status(db=db, transaction_id=transaction_id, status=payment_status)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return transaction

@router.post("/{order_id}/refund", response_model=schemas.RefundResponse)
def create_refund(order_id: int, refund: schemas.RefundCreate, db: Session = Depends(get_db)):
    """Create a refund for an order"""
    # Verify order exists
    order = crud.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    refund.order_id = order_id
    return crud.create_refund(db=db, refund=refund)

@router.get("/stats/summary", response_model=schemas.OrderSummary)
def get_order_summary(user_id: int = None, db: Session = Depends(get_db)):
    """Get order summary statistics"""
    return crud.get_order_summary(db=db, user_id=user_id)