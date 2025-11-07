"""Minimal synchronous test client compatible with the simplified FastAPI shim."""
from __future__ import annotations

import json
from urllib.parse import parse_qsl
from typing import Any, Dict, Optional

from . import HTTPException, Response, _execute


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    if hasattr(value, "dict") and callable(value.dict):
        return value.dict()
    if hasattr(value, "__dict__"):
        return {k: _to_jsonable(v) for k, v in value.__dict__.items() if not k.startswith("_")}
    return value


class _ClientResponse:
    def __init__(self, response: Response):
        self._response = response
        self.status_code = response.status_code
        self.headers = response.headers

    def json(self) -> Any:
        payload = _to_jsonable(self._response.content)
        if isinstance(payload, (dict, list)):
            return payload
        if isinstance(payload, str):
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                return payload
        return payload

    @property
    def text(self) -> str:
        payload = _to_jsonable(self._response.content)
        if isinstance(payload, str):
            return payload
        return json.dumps(payload)


class TestClient:
    def __init__(self, app):
        self.app = app

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def request(self, method: str, path: str, *, json: Any = None, params: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None) -> _ClientResponse:
        query_params = dict(params or {})
        if '?' in path:
            path, raw_query = path.split('?', 1)
            for key, value in parse_qsl(raw_query, keep_blank_values=True):
                query_params.setdefault(key, value)
        try:
            response = _execute(self.app, method.upper(), path, headers=headers, query_params=query_params, body=json)
        except HTTPException as exc:
            payload = {"detail": exc.detail}
            response = Response(payload, status_code=exc.status_code, headers=exc.headers)
        return _ClientResponse(response)

    def get(self, path: str, *, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        return self.request("GET", path, params=params, headers=headers)

    def post(self, path: str, *, json: Any = None, headers: Optional[Dict[str, str]] = None):
        return self.request("POST", path, json=json, headers=headers)

    def put(self, path: str, *, json: Any = None, headers: Optional[Dict[str, str]] = None):
        return self.request("PUT", path, json=json, headers=headers)

    def delete(self, path: str, *, headers: Optional[Dict[str, str]] = None):
        return self.request("DELETE", path, headers=headers)


__all__ = ["TestClient"]
