"""Compatibility package exposing the microservice modules."""
from __future__ import annotations

from pathlib import Path

_real_path = Path(__file__).resolve().parent.parent / "steam-clone" / "services"
__path__ = [str(_real_path.resolve())]
