"""
Notification Service API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database

router = APIRouter()

# Add your routes here
# Example:
# @router.post("/", response_model=schemas.NotificationResponse, status_code=status.HTTP_201_CREATED)
# def create_notification(
#     notification: schemas.NotificationCreate,
#     db: Session = Depends(database.get_db)
# ):
#     """Create a new notification"""
#     return crud.create_notification(db=db, notification=notification)
