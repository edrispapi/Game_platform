"""Compatibility layer exposing the API gateway service package."""
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent.parent / "api-gateway")]
