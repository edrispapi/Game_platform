"""
Online Service API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database

router = APIRouter()


@router.post("/presence", response_model=schemas.PresenceResponse)
def update_presence(presence: schemas.PresenceUpdate, db: Session = Depends(database.get_db)):
    """Upsert presence for a user."""
    return crud.upsert_presence(db, presence)


@router.get("/presence/{user_id}", response_model=schemas.PresenceResponse)
def get_presence(user_id: str, db: Session = Depends(database.get_db)):
    """Fetch a user's presence."""
    presence = crud.get_presence(db, user_id)
    if not presence:
        raise HTTPException(status_code=404, detail="Presence not found.")
    return presence


@router.get("/presence", response_model=List[schemas.PresenceResponse])
def list_presence(user_ids: List[str] = Query(default=[]), db: Session = Depends(database.get_db)):
    """Batch fetch presence records."""
    return crud.list_presence(db, user_ids)


@router.post("/messages", response_model=schemas.ChatMessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(message: schemas.ChatMessageCreate, db: Session = Depends(database.get_db)):
    """Send a direct chat message."""
    if message.sender_id == message.recipient_id:
        raise HTTPException(status_code=400, detail="Cannot send a message to yourself.")
    return crud.create_message(db, message)


@router.get("/messages", response_model=List[schemas.ChatMessageResponse])
def get_conversation_messages(
    user_id: str,
    peer_id: str,
    limit: int = 50,
    db: Session = Depends(database.get_db),
):
    """Retrieve conversation history between two users."""
    return crud.get_conversation_messages(db, user_id=user_id, peer_id=peer_id, limit=limit)
