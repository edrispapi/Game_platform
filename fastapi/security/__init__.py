"""Security primitives for the simplified FastAPI shim."""
from __future__ import annotations

from typing import Optional

from .. import HTTPException, Request, status


class OAuth2PasswordBearer:
    def __init__(self, tokenUrl: str):
        self.token_url = tokenUrl

    def __call__(self, request: Request) -> str:
        authorization = request.headers.get("authorization")
        if not authorization or not authorization.lower().startswith("bearer "):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        return authorization.split(" ", 1)[1].strip()


__all__ = ["OAuth2PasswordBearer"]
