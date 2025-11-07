"""Simplified SQLAlchemy shim backed by in-memory storage for tests."""
from __future__ import annotations

from datetime import datetime
import itertools
from typing import Any, Callable, Dict, Iterable, List, Optional

from .orm.session import Session, sessionmaker
from .orm.declarative import declarative_base
from .types import (Boolean, Column, DateTime, Enum, Float, Integer, JSONB, String, Text, UUID)
from .functions import and_, or_, func
from .engine import create_engine, MetaData
from .pool import StaticPool

__all__ = [
    "Boolean",
    "Column",
    "DateTime",
    "Enum",
    "Float",
    "Integer",
    "JSONB",
    "MetaData",
    "StaticPool",
    "String",
    "Text",
    "UUID",
    "Session",
    "and_",
    "create_engine",
    "declarative_base",
    "func",
    "or_",
    "sessionmaker",
]


# Re-export submodules for compatibility
import sys

from . import orm as _orm_module
from . import sql as _sql_module
from . import pool as _pool_module
from . import ext as _ext_module
from .dialects import postgresql as _postgresql_module

sys.modules[__name__ + ".orm"] = _orm_module
sys.modules[__name__ + ".sql"] = _sql_module
sys.modules[__name__ + ".pool"] = _pool_module
sys.modules[__name__ + ".ext"] = _ext_module
sys.modules[__name__ + ".dialects"] = __import__("sqlalchemy.dialects")
sys.modules[__name__ + ".dialects.postgresql"] = _postgresql_module
