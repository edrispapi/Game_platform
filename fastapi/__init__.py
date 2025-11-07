"""Lightweight FastAPI-compatible façade used for tests."""
from __future__ import annotations

import asyncio
import types
from dataclasses import dataclass
from inspect import Parameter, iscoroutine, signature
from typing import Any, Callable, Dict, Iterable, List, Optional

__all__ = [
    "APIRouter",
    "Depends",
    "FastAPI",
    "HTTPException",
    "Query",
    "Request",
    "status",
]


class QueryParam:
    def __init__(self, default: Any = None, **_: Any):
        self.default = default


def Query(default: Any = None, **_: Any) -> QueryParam:
    return QueryParam(default)


class HTTPException(Exception):
    """Exception raised by request handlers to signal HTTP errors."""

    def __init__(self, status_code: int, detail: Any = None, headers: Optional[Dict[str, str]] = None):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail
        self.headers = headers or {}


class status:
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_404_NOT_FOUND = 404
    HTTP_429_TOO_MANY_REQUESTS = 429
    HTTP_500_INTERNAL_SERVER_ERROR = 500


class Depends:
    """Declare a callable dependency."""

    def __init__(self, dependency: Callable[..., Any]):
        self.dependency = dependency


@dataclass
class _Route:
    method: str
    path: str
    endpoint: Callable[..., Any]
    status_code: Optional[int] = None

    def match(self, request_path: str) -> Optional[Dict[str, Any]]:
        request_segments = [segment for segment in request_path.strip("/").split("/") if segment]
        route_segments = [segment for segment in self.path.strip("/").split("/") if segment]

        if len(route_segments) != len(request_segments):
            return None

        params: Dict[str, Any] = {}
        for route_segment, request_segment in zip(route_segments, request_segments):
            if route_segment.startswith("{") and route_segment.endswith("}"):
                params[route_segment[1:-1]] = request_segment
            elif route_segment != request_segment:
                return None
        return params


class Request:
    """Simplified request object."""

    def __init__(self, method: str, url: str, *, headers: Optional[Dict[str, str]] = None,
                 query_params: Optional[Dict[str, Any]] = None, body: Any = None, client: Optional[str] = None, app: Any = None):
        self.method = method
        self.url = url
        self.headers = {k.lower(): v for k, v in (headers or {}).items()}
        self.query_params = query_params or {}
        self._body = body
        self.client = type("Client", (), {"host": client or "testclient"})()
        self.app = app
        self._rate_counter = 0

    async def body(self) -> Any:
        return self._body


class Response:
    def __init__(self, content: Any, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}


class FastAPI:
    def __init__(self, **_: Any):
        self.routes: List[_Route] = []
        self.middleware: List[Any] = []
        self.dependency_overrides: Dict[Callable[..., Any], Callable[..., Any]] = {}

    def add_middleware(self, middleware_class: Any, **kwargs: Any) -> None:
        self.middleware.append((middleware_class, kwargs))

    def include_router(self, router: "APIRouter", *, prefix: str = "", tags: Optional[List[str]] = None) -> None:
        prefix = prefix.rstrip("/")
        for route in router.routes:
            full_path = f"{prefix}{route.path}" if prefix else route.path
            self.routes.append(
                _Route(
                    route.method,
                    full_path,
                    route.endpoint,
                    status_code=route.status_code,
                )
            )

    def api_route(self, path: str, *, methods: Iterable[str], status_code: Optional[int] = None, **_: Any):
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            normalized_path = path if path.startswith("/") else f"/{path}"
            for method in methods:
                self.routes.append(
                    _Route(
                        method.upper(),
                        normalized_path,
                        func,
                        status_code=status_code,
                    )
                )
            return func
        return decorator

    def get(self, path: str, **kwargs: Any):
        return self.api_route(path, methods=["GET"], **kwargs)

    def post(self, path: str, **kwargs: Any):
        return self.api_route(path, methods=["POST"], **kwargs)

    def put(self, path: str, **kwargs: Any):
        return self.api_route(path, methods=["PUT"], **kwargs)

    def delete(self, path: str, **kwargs: Any):
        return self.api_route(path, methods=["DELETE"], **kwargs)


class APIRouter(FastAPI):
    def __init__(self):
        super().__init__()
        self.routes: List[_Route] = []


def _resolve_default(default: Any) -> Any:
    if isinstance(default, QueryParam):
        return default.default
    return default


def _call_dependency(dep: Depends, request: Request):
    dependency = dep.dependency
    overrides = getattr(request.app, 'dependency_overrides', {}) if request and hasattr(request, 'app') else {}
    dependency = overrides.get(dependency, dependency)
    if signature(dependency).parameters:
        value = dependency(request)
    else:
        value = dependency()
    if isinstance(value, types.GeneratorType):
        try:
            resolved = next(value)
        finally:
            try:
                next(value)
            except StopIteration:
                pass
        return resolved
    return value


async def _call_endpoint(endpoint: Callable[..., Any], request: Request, path_params: Dict[str, Any],
                         query_params: Dict[str, Any], body: Any) -> Any:
    params = signature(endpoint).parameters
    kwargs: Dict[str, Any] = {}

    for name, param in params.items():
        default = param.default
        default_value = _resolve_default(default)
        if isinstance(default, Depends):
            kwargs[name] = _call_dependency(default, request)
            continue
        if param.annotation is Request or name == "request":
            kwargs[name] = request
            continue
        if name in path_params:
            kwargs[name] = _convert_value(param, path_params[name])
            continue
        if request.method in {"POST", "PUT", "PATCH"}:
            if len(params) == 1 and body is not None:
                kwargs[name] = _convert_value(param, body)
                continue
            if isinstance(body, dict):
                if name in body:
                    kwargs[name] = _convert_value(param, body[name])
                    continue
                if hasattr(param.annotation, "parse_obj"):
                    kwargs[name] = param.annotation.parse_obj(body)  # type: ignore[attr-defined]
                    continue
        if name in query_params:
            kwargs[name] = _convert_value(param, query_params[name])
            continue
        if default_value is not Parameter.empty:
            kwargs[name] = default_value
            continue
        kwargs[name] = None

    result = endpoint(**kwargs)
    if iscoroutine(result):
        result = await result
    return result


def _convert_value(param: Parameter, value: Any) -> Any:
    annotation = param.annotation
    if annotation is Parameter.empty or value is None:
        return value
    try:
        if hasattr(annotation, "parse_obj"):
            return annotation.parse_obj(value)  # type: ignore[attr-defined]
        return annotation(value)
    except Exception:
        return value


def _find_route(app: FastAPI, method: str, path: str) -> Optional[tuple[_Route, Dict[str, Any]]]:
    matches: List[tuple[_Route, Dict[str, Any]]] = []
    for route in app.routes:
        if route.method != method:
            continue
        params = route.match(path)
        if params is not None:
            matches.append((route, params))
    if not matches:
        return None
    matches.sort(key=lambda item: item[0].path.count("{"))
    return matches[0]


def _execute(app: FastAPI, method: str, path: str, *, headers: Optional[Dict[str, str]] = None,
             query_params: Optional[Dict[str, Any]] = None, body: Any = None):
    match = _find_route(app, method, path)
    if match is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Not Found")

    route, params = match
    request = Request(method, path, headers=headers, query_params=query_params, body=body, app=app)

    try:
        result = asyncio.run(_call_endpoint(route.endpoint, request, params, query_params or {}, body))
    except HTTPException:
        raise

    if isinstance(result, Response):
        return result
    status_code = route.status_code or status.HTTP_200_OK
    return Response(result, status_code=status_code)


