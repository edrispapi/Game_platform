"""Response helpers for the simplified FastAPI shim."""
from __future__ import annotations

from typing import Any, Dict, Optional

from . import Response


class JSONResponse(Response):
    def __init__(self, content: Any, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        super().__init__(content, status_code=status_code, headers=headers)


__all__ = ["JSONResponse"]
