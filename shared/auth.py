"""Authentication helpers without external dependencies."""
from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
_PBKDF2_ITERATIONS = 120_000


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def get_password_hash(password: str) -> str:
    """Hash a plaintext password using PBKDF2."""

    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")
    salt = secrets.token_hex(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), _PBKDF2_ITERATIONS)
    return f"{salt}:{_PBKDF2_ITERATIONS}:{derived.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plaintext password matches the stored hash."""

    try:
        salt, iterations_str, stored_hash = hashed_password.split(":")
        iterations = int(iterations_str)
    except ValueError:
        return False
    candidate = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), iterations)
    return hmac.compare_digest(candidate.hex(), stored_hash)


def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed token with an expiration claim."""

    payload = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    payload["exp"] = int(expire.timestamp())
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    signature = hmac.new(settings.SECRET_KEY.encode("utf-8"), body, hashlib.sha256).digest()
    return f"{_b64encode(body)}.{_b64encode(signature)}"


def verify_token(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    """Decode and validate an incoming access token."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        body_segment, signature_segment = token.split(".")
        body = _b64decode(body_segment)
        signature = _b64decode(signature_segment)
    except (ValueError, binascii.Error):
        raise credentials_exception

    expected_signature = hmac.new(settings.SECRET_KEY.encode("utf-8"), body, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected_signature):
        raise credentials_exception

    try:
        payload = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise credentials_exception from exc

    if payload.get("exp") is None or int(payload["exp"]) < int(time.time()):
        raise credentials_exception

    if "user_id" not in payload:
        raise credentials_exception

    return payload


__all__ = [
    "create_access_token",
    "get_password_hash",
    "verify_password",
    "verify_token",
]
