"""Utility functions for the SQLAlchemy shim."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable


def and_(*conditions: Callable[[Any], bool]) -> Callable[[Any], bool]:
    def matcher(obj: Any) -> bool:
        return all(condition(obj) for condition in conditions)
    return matcher


def or_(*conditions: Callable[[Any], bool]) -> Callable[[Any], bool]:
    def matcher(obj: Any) -> bool:
        return any(condition(obj) for condition in conditions)
    return matcher


class _FuncModule:
    @staticmethod
    def now():
        return lambda: datetime.utcnow()


func = _FuncModule()

__all__ = ["and_", "or_", "func"]
