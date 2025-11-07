"""Pydantic schemas for the simplified catalog service."""
from pydantic import BaseModel, Field
from typing import Optional


class GameBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    genre: Optional[str] = None
    platform: Optional[str] = None


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    genre: Optional[str] = None
    platform: Optional[str] = None


class GameResponse(GameBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
