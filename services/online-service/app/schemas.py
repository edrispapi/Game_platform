"""
Online Service Pydantic Schemas
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel, Field, ConfigDict


class PresenceUpdate(BaseModel):
    user_id: str
    status: str = Field(default="online", pattern="^(online|offline|away|in-game)$")
    platform: str = Field(default="desktop", max_length=20)
    activity: Optional[str] = Field(default=None, max_length=100)
    region: Optional[str] = Field(default=None, max_length=10)
    metadata: Optional[Dict[str, str]] = None


class PresenceResponse(PresenceUpdate):
    id: int
    last_seen: datetime
    updated_at: datetime

    metadata: Optional[Dict[str, str]] = Field(default=None, alias="extra_metadata")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ChatMessageCreate(BaseModel):
    sender_id: str
    recipient_id: str
    content: str = Field(..., min_length=1, max_length=2000)


class ChatMessageResponse(BaseModel):
    id: int
    conversation_id: str
    sender_id: str
    recipient_id: str
    content: str
    is_read: bool
    sent_at: datetime
    read_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
