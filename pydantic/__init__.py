"""Lightweight subset of Pydantic used for unit testing."""
from __future__ import annotations

import os
from typing import Any, Callable, Dict, Optional

__all__ = [
    "BaseModel",
    "BaseSettings",
    "EmailStr",
    "Field",
    "field_validator",
]


EmailStr = str


class FieldInfo:
    def __init__(self, default: Any = Ellipsis, *, default_factory: Optional[Callable[[], Any]] = None, **metadata: Any):
        self.default = default
        self.default_factory = default_factory
        self.metadata = metadata


def Field(default: Any = Ellipsis, *, default_factory: Optional[Callable[[], Any]] = None, **metadata: Any) -> FieldInfo:
    return FieldInfo(default, default_factory=default_factory, **metadata)


class ModelMeta(type):
    def __new__(mcls, name, bases, namespace):
        annotations = dict(namespace.get("__annotations__", {}))
        fields: Dict[str, FieldInfo] = {}
        validators = []

        for base in bases:
            fields.update(getattr(base, "__fields__", {}))
            validators.extend(getattr(base, "__validators__", []))

        for field_name, annotation in annotations.items():
            default = namespace.pop(field_name, Ellipsis)
            if isinstance(default, FieldInfo):
                field_info = default
            else:
                field_info = FieldInfo(default)
            field_info.annotation = annotation
            fields[field_name] = field_info

        namespace["__fields__"] = fields
        collected_validators = validators + namespace.get("__validators__", [])
        for value in namespace.values():
            target = None
            is_classmethod = False
            if callable(value) and hasattr(value, "__validator_fields__"):
                target = value
            elif isinstance(value, classmethod) and hasattr(value.__func__, "__validator_fields__"):
                target = value.__func__
                is_classmethod = True
            if target is not None:
                setattr(target, "__validator_is_classmethod__", is_classmethod)
                collected_validators.append(target)
        namespace["__validators__"] = collected_validators
        return super().__new__(mcls, name, bases, namespace)


class BaseModel(metaclass=ModelMeta):
    def __init__(self, **data: Any):
        self.__dict__["__data__"] = {}
        self.__dict__["__fields_set__"] = set()

        for name, field in self.__fields__.items():
            if name in data:
                value = data[name]
                self.__fields_set__.add(name)
            else:
                if field.default_factory is not None:
                    value = field.default_factory()
                elif field.default is not Ellipsis:
                    value = field.default
                else:
                    raise ValueError(f"Missing field: {name}")
            self.__data__[name] = value
            setattr(self, name, value)

        apply_validators(self)

    def dict(self, *, exclude_unset: bool = False) -> Dict[str, Any]:
        if exclude_unset:
            return {k: v for k, v in self.__data__.items() if k in self.__fields_set__}
        return dict(self.__data__)

    def model_dump(self, *, exclude_unset: bool = False) -> Dict[str, Any]:  # compatibility helper
        return self.dict(exclude_unset=exclude_unset)

    @classmethod
    def parse_obj(cls, data: Any):
        if isinstance(data, cls):
            return data
        if not isinstance(data, dict):
            raise TypeError("Expected dict for parsing")
        return cls(**data)


class SettingsMeta(ModelMeta):
    pass


class BaseSettings(BaseModel, metaclass=SettingsMeta):
    class Config:
        env_file = None
        env_file_encoding = "utf-8"

    def __init__(self, **data: Any):
        env_data: Dict[str, Any] = {}
        for name in self.__fields__:
            env_key = name.upper()
            if env_key in os.environ:
                env_data[name] = os.environ[env_key]
        env_data.update(data)
        super().__init__(**env_data)


def field_validator(*field_names: str, mode: str = "after"):
    def decorator(func: Callable[[Any, Any], Any]):
        if not hasattr(func, "__validator_fields__"):
            func.__validator_fields__ = []  # type: ignore[attr-defined]
        func.__validator_fields__.extend(field_names)  # type: ignore[attr-defined]
        func.__validator_mode__ = mode  # type: ignore[attr-defined]
        return func
    return decorator


def apply_validators(instance: BaseModel):
    for validator in getattr(instance.__class__, "__validators__", []):
        fields = getattr(validator, "__validator_fields__", [])
        mode = getattr(validator, "__validator_mode__", "after")
        for field in fields:
            value = instance.__data__.get(field)
            call_value = value if mode == "before" else instance.__data__.get(field)
            if getattr(validator, "__validator_is_classmethod__", False):
                new_value = validator(instance.__class__, call_value)
            else:
                new_value = validator(call_value)
            instance.__data__[field] = new_value
            setattr(instance, field, new_value)


