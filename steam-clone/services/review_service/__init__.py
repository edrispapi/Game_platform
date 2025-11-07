"""Compatibility layer exposing the review service package."""
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent.parent / "review-service")]
