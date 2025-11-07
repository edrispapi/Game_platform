"""Session and query implementations for the SQLAlchemy shim."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Type

from ..engine import Engine


class Query:
    def __init__(self, session: "Session", model: Type, data: Iterable[Any]):
        self._session = session
        self._model = model
        self._data = list(data)

    def filter(self, predicate):
        if predicate is None:
            return self
        return Query(self._session, self._model, filter(predicate, self._data))

    def offset(self, value: int):
        return Query(self._session, self._model, self._data[value:])

    def limit(self, value: int):
        return Query(self._session, self._model, self._data[:value])

    def all(self) -> List[Any]:
        return list(self._data)

    def first(self) -> Optional[Any]:
        return self._data[0] if self._data else None

    def update(self, values: Dict[str, Any]):
        for item in self._data:
            for key, val in values.items():
                setattr(item, key, val)


class Session:
    def __init__(self, engine: Engine):
        self._engine = engine

    def add(self, obj: Any) -> None:
        storage = self._engine.storage.setdefault(type(obj), [])
        if getattr(obj, "id", None) is None:
            next_id = self._engine.identity.setdefault(type(obj), 1)
            setattr(obj, "id", next_id)
            self._engine.identity[type(obj)] = next_id + 1
        storage.append(obj)

    def commit(self) -> None:  # pragma: no cover - no-op for shim
        pass

    def refresh(self, obj: Any) -> None:  # pragma: no cover - no-op
        pass

    def close(self) -> None:  # pragma: no cover - no-op
        pass

    def query(self, model: Type) -> Query:
        storage = self._engine.storage.setdefault(model, [])
        return Query(self, model, storage)

    def delete(self, obj: Any) -> None:
        storage = self._engine.storage.setdefault(type(obj), [])
        if obj in storage:
            storage.remove(obj)


def sessionmaker(autocommit: bool = False, autoflush: bool = False, bind: Optional[Engine] = None):
    engine = bind or Engine()

    class _SessionFactory:
        def __call__(self, *args, **kwargs):
            return Session(engine)

    return _SessionFactory()


__all__ = ["Session", "sessionmaker"]
