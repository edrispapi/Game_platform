"""Type and column descriptors for the SQLAlchemy shim."""
from __future__ import annotations

from typing import Any, Callable, Optional


class ColumnComparator:
    def __init__(self, column: "Column"):
        self.column = column

    def __eq__(self, other: Any):  # pragma: no cover - trivial
        return lambda obj: getattr(obj, self.column.name, None) == other

    def __ne__(self, other: Any):  # pragma: no cover - trivial
        return lambda obj: getattr(obj, self.column.name, None) != other


class Column:
    def __init__(self, type_: Any = None, default: Any = None, server_default: Any = None,
                 nullable: bool = True, primary_key: bool = False, index: bool = False,
                 unique: bool = False, **extra: Any):
        self.type_ = type_
        self.default = default
        self.server_default = server_default
        self.nullable = nullable
        self.primary_key = primary_key
        self.index = index
        self.unique = unique
        self.extra = extra
        self.name: Optional[str] = None

    def __set_name__(self, owner, name):
        self.name = name
        columns = getattr(owner, "__columns__", {})
        columns[name] = self
        owner.__columns__ = columns

    def __get__(self, instance, owner):
        if instance is None:
            return ColumnComparator(self)
        return instance.__dict__.get(self.name, self._default_value())

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def _default_value(self):
        if callable(self.default):
            return self.default()
        if self.default is not None:
            return self.default
        if callable(self.server_default):
            return self.server_default()
        return self.server_default


class Integer:  # pragma: no cover - metadata only
    pass


class String:  # pragma: no cover - metadata only
    def __init__(self, length: int = 0):
        self.length = length


class Float:  # pragma: no cover - metadata only
    pass


class Boolean:  # pragma: no cover - metadata only
    pass


class DateTime:  # pragma: no cover - metadata only
    def __init__(self, timezone: bool = False):
        self.timezone = timezone


class Text:  # pragma: no cover - metadata only
    pass


class Enum:  # pragma: no cover - metadata only
    def __init__(self, enum_cls):
        self.enum_cls = enum_cls


class JSONB:  # pragma: no cover - metadata only
    pass


class UUID:  # pragma: no cover - metadata only
    def __init__(self, as_uuid: bool = False):
        self.as_uuid = as_uuid


__all__ = [
    "Boolean",
    "Column",
    "DateTime",
    "Enum",
    "Float",
    "Integer",
    "JSONB",
    "String",
    "Text",
    "UUID",
]
