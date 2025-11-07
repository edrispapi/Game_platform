"""In-memory engine implementation for the SQLAlchemy shim."""
from __future__ import annotations

from typing import Dict, List, Type


class Engine:
    def __init__(self):
        self.storage: Dict[Type, List] = {}
        self.identity: Dict[Type, int] = {}


def create_engine(*args, **kwargs) -> Engine:  # pragma: no cover - simple factory
    return Engine()


class MetaData:
    def __init__(self):
        self._models: List[Type] = []

    def register(self, model: Type) -> None:
        if model not in self._models:
            self._models.append(model)

    def create_all(self, bind: Engine) -> None:
        for model in self._models:
            bind.storage.setdefault(model, [])
            bind.identity.setdefault(model, 1)

    def drop_all(self, bind: Engine) -> None:
        for model in self._models:
            bind.storage[model] = []
            bind.identity[model] = 1


__all__ = ["Engine", "MetaData", "create_engine"]
