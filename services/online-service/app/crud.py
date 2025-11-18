"""
Online Service CRUD Operations
"""
from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from shared.kafka import publish_event
from .core.config import settings

from . import models, schemas


def _publish(event_type: str, payload: dict) -> None:
    publish_event(settings.KAFKA_ONLINE_TOPIC, {"event_type": event_type, **payload})


def upsert_presence(db: Session, presence: schemas.PresenceUpdate) -> models.UserPresence:
    db_presence = (
        db.query(models.UserPresence)
        .filter(models.UserPresence.user_id == presence.user_id)
        .one_or_none()
    )

    update_data = presence.model_dump(exclude_unset=True)
    metadata_value = update_data.pop("metadata", None)

    if db_presence:
        for field, value in update_data.items():
            setattr(db_presence, field, value)
        if metadata_value is not None:
            db_presence.extra_metadata = metadata_value
    else:
        if metadata_value is not None:
            update_data["extra_metadata"] = metadata_value
        db_presence = models.UserPresence(**update_data)
        db.add(db_presence)

    db.commit()
    db.refresh(db_presence)
    _publish("presence_updated", {"user_id": db_presence.user_id, "status": db_presence.status})
    return db_presence


def get_presence(db: Session, user_id: str) -> models.UserPresence | None:
    return (
        db.query(models.UserPresence)
        .filter(models.UserPresence.user_id == user_id)
        .one_or_none()
    )


def list_presence(db: Session, user_ids: List[str]) -> List[models.UserPresence]:
    if not user_ids:
        return []
    return (
        db.query(models.UserPresence)
        .filter(models.UserPresence.user_id.in_(user_ids))
        .all()
    )


def _conversation_id(user_a: str, user_b: str) -> str:
    return "::".join(sorted([user_a, user_b]))


def create_message(db: Session, payload: schemas.ChatMessageCreate) -> models.ChatMessage:
    conversation_id = _conversation_id(payload.sender_id, payload.recipient_id)
    message = models.ChatMessage(
        conversation_id=conversation_id,
        sender_id=payload.sender_id,
        recipient_id=payload.recipient_id,
        content=payload.content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    _publish(
        "chat_message_sent",
        {
            "conversation_id": conversation_id,
            "sender_id": payload.sender_id,
            "recipient_id": payload.recipient_id,
            "message_id": message.id,
        },
    )
    return message


def get_conversation_messages(
    db: Session,
    user_id: str,
    peer_id: str,
    limit: int = 50,
) -> List[models.ChatMessage]:
    conversation_id = _conversation_id(user_id, peer_id)
    limit = max(1, min(limit, 100))
    return (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.conversation_id == conversation_id)
        .order_by(models.ChatMessage.sent_at.desc())
        .limit(limit)
        .all()
    )
