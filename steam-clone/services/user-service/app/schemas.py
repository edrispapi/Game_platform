"""Pydantic schemas for the simplified user service."""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int
    email_verified: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
