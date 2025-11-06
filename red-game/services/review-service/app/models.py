"""
Review Service Database Models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from enum import Enum as PyEnum
from shared.database import Base

class ReviewStatus(PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FLAGGED = "flagged"

class ReviewType(PyEnum):
    GAME = "game"
    DLC = "dlc"
    SOFTWARE = "software"

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to user service
    game_id = Column(Integer, nullable=False, index=True)  # Reference to game catalog service
    review_type = Column(String(20), default="game", nullable=False)
    
    # Review content
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    is_positive = Column(Boolean, nullable=False)
    
    # Review metadata
    status = Column(String(20), default="pending", nullable=False)
    language = Column(String(5), default="en", nullable=False)
    playtime_at_review = Column(Integer, default=0, nullable=False)  # in minutes
    is_early_access = Column(Boolean, default=False, nullable=False)
    
    # Engagement metrics
    helpful_votes = Column(Integer, default=0, nullable=False)
    unhelpful_votes = Column(Integer, default=0, nullable=False)
    total_votes = Column(Integer, default=0, nullable=False)
    
    # Moderation
    is_flagged = Column(Boolean, default=False, nullable=False)
    flag_reason = Column(String(100), nullable=True)
    moderator_notes = Column(Text, nullable=True)
    moderated_by = Column(Integer, nullable=True)  # Reference to moderator user
    moderated_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Additional metadata
    metadata = Column(JSONB, nullable=True)
    
    # Relationships
    comments = relationship("ReviewComment", back_populates="review")
    votes = relationship("ReviewVote", back_populates="review")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_reviews_user_game', 'user_id', 'game_id'),
        Index('idx_reviews_game_rating', 'game_id', 'rating'),
        Index('idx_reviews_status_created', 'status', 'created_at'),
        Index('idx_reviews_helpful_votes', 'helpful_votes'),
    )

class ReviewComment(Base):
    __tablename__ = "review_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to user service
    parent_comment_id = Column(Integer, ForeignKey("review_comments.id"), nullable=True, index=True)
    
    # Comment content
    content = Column(Text, nullable=False)
    is_edited = Column(Boolean, default=False, nullable=False)
    
    # Engagement metrics
    helpful_votes = Column(Integer, default=0, nullable=False)
    unhelpful_votes = Column(Integer, default=0, nullable=False)
    
    # Moderation
    is_flagged = Column(Boolean, default=False, nullable=False)
    flag_reason = Column(String(100), nullable=True)
    moderated_by = Column(Integer, nullable=True)
    moderated_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    review = relationship("Review", back_populates="comments")
    parent_comment = relationship("ReviewComment", remote_side=[id])
    replies = relationship("ReviewComment", back_populates="parent_comment")
    votes = relationship("CommentVote", back_populates="comment")

class ReviewVote(Base):
    __tablename__ = "review_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to user service
    is_helpful = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    review = relationship("Review", back_populates="votes")
    
    # Ensure one vote per user per review
    __table_args__ = (
        Index('idx_review_votes_user_review', 'user_id', 'review_id', unique=True),
    )

class CommentVote(Base):
    __tablename__ = "comment_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("review_comments.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to user service
    is_helpful = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    comment = relationship("ReviewComment", back_populates="votes")
    
    # Ensure one vote per user per comment
    __table_args__ = (
        Index('idx_comment_votes_user_comment', 'user_id', 'comment_id', unique=True),
    )

class ReviewReport(Base):
    __tablename__ = "review_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to user service
    report_reason = Column(String(100), nullable=False)
    report_description = Column(Text, nullable=True)
    status = Column(String(20), default="pending", nullable=False)  # pending, reviewed, resolved
    reviewed_by = Column(Integer, nullable=True)  # Reference to moderator user
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    review = relationship("Review")

class ReviewModerationLog(Base):
    __tablename__ = "review_moderation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, index=True)
    moderator_id = Column(Integer, nullable=False, index=True)  # Reference to moderator user
    action = Column(String(50), nullable=False)  # approve, reject, flag, unflag
    reason = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    review = relationship("Review")