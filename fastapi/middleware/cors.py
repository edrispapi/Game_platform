"""No-op CORS middleware placeholder."""
from __future__ import annotations

from typing import Iterable


class CORSMiddleware:  # pragma: no cover - behaviour handled by shim client
    def __init__(self, app=None, allow_origins: Iterable[str] = (), allow_credentials: bool = False,
                 allow_methods: Iterable[str] = ("GET", "POST"), allow_headers: Iterable[str] = ("*",)):
        self.app = app
        self.allow_origins = list(allow_origins)
        self.allow_credentials = allow_credentials
        self.allow_methods = list(allow_methods)
        self.allow_headers = list(allow_headers)


__all__ = ["CORSMiddleware"]
