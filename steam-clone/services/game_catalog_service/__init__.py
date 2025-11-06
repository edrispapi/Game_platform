"""Compatibility layer exposing the game catalog service package."""
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent.parent / "game-catalog-service")]
