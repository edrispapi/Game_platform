"""CRUD helpers for the simplified user service."""
from typing import Optional

from sqlalchemy.orm import Session

from shared.auth import get_password_hash, verify_password
from . import models, schemas


class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, payload: schemas.UserCreate) -> models.User:
        if self.get_user_by_username(payload.username):
            raise ValueError("Username already exists")
        if self.get_user_by_email(payload.email):
            raise ValueError("Email already exists")
        user = models.User(
            username=payload.username,
            email=payload.email,
            full_name=payload.full_name,
            password_hash=get_password_hash(payload.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int) -> Optional[models.User]:
        return self.db.query(models.User).filter(lambda u: u.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(lambda u: u.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(lambda u: u.email == email).first()

    def authenticate_user(self, username: str, password: str) -> Optional[models.User]:
        user = self.get_user_by_username(username)
        if user and verify_password(password, user.password_hash):
            return user
        return None


def create_user(db: Session, payload: schemas.UserCreate) -> models.User:
    return UserCRUD(db).create_user(payload)


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return UserCRUD(db).get_user(user_id)


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return UserCRUD(db).get_user_by_username(username)


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    return UserCRUD(db).authenticate_user(username, password)
