"""Declarative base for the SQLAlchemy shim."""
from __future__ import annotations

from typing import Any, Dict, Type

from ..engine import MetaData
from ..types import Column


class DeclarativeMeta(type):
    def __new__(mcls, name, bases, namespace):
        columns: Dict[str, Any] = {}
        for base in bases:
            columns.update(getattr(base, "__columns__", {}))
        for attr, value in list(namespace.items()):
            if isinstance(value, Column):
                columns[attr] = value
        namespace["__columns__"] = columns
        cls = super().__new__(mcls, name, bases, namespace)
        metadata: MetaData = getattr(cls, "metadata", MetaData())
        metadata.register(cls)
        cls.metadata = metadata
        return cls


def declarative_base():
    shared_metadata = MetaData()

    class Base(metaclass=DeclarativeMeta):
        def __init__(self, **kwargs):
            for name, column in self.__columns__.items():
                if name in kwargs:
                    value = kwargs.pop(name)
                else:
                    value = column._default_value() if hasattr(column, "_default_value") else None
                setattr(self, name, value)
            for key, value in kwargs.items():
                setattr(self, key, value)

    Base.metadata = shared_metadata
    return Base


__all__ = ["declarative_base"]
