"""Compatibility layer exposing the user service package."""
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent.parent / "user-service")]
