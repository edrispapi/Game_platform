"""Simplified models for the in-memory catalog service."""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from shared.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=False)
    price = Column(Float, nullable=False)
    genre = Column(String(64), nullable=True)
    platform = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
