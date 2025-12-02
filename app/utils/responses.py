from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def created_response(
    message: str = "Created",
    data: Any = None,
    headers: Optional[Dict[str, str]] = None,
    status_code: int = status.HTTP_201_CREATED,
):
    """Return a 201 Created response."""
    response_data = {"status": status_code, "detail": message}
    if data is not None:
        response_data["data"] = data
    if headers:
        return JSONResponse(content=response_data, status_code=status_code, headers=headers)
    return response_data


def success_response(
    message: str = "Success",
    data: Any = None,
    total_count: Optional[int] = None,
    headers: Optional[Dict[str, str]] = None,
    status_code: int = status.HTTP_200_OK,
):
    """Return a 200 OK response."""
    response_data = {"status": status_code, "detail": message}
    if data is not None:
        response_data["data"] = data
    if total_count is not None:
        response_data["total_count"] = total_count
    if headers:
        return JSONResponse(content=response_data, status_code=status_code, headers=headers)
    return response_data


def forbidden_response(message: str = "Forbidden", headers: Optional[Dict[str, str]] = None):
    """Raise 403 Forbidden HTTPException."""
    exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def not_found_response(message: str = "Not found", headers: Optional[Dict[str, str]] = None):
    """Raise 404 Not Found HTTPException."""
    exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def not_authorized_response(message: str = "Not authorized", headers: Optional[Dict[str, str]] = None):
    """Raise 401 Unauthorized HTTPException."""
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def bad_request_response(message: str = "Bad request", headers: Optional[Dict[str, str]] = None):
    """Raise 400 Bad Request HTTPException."""
    exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def conflict_response(message: str = "Conflict", headers: Optional[Dict[str, str]] = None):
    """Raise 409 Conflict HTTPException."""
    exception = HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def unprocessable_entity_response(message: str = "Unprocessable entity", headers: Optional[Dict[str, str]] = None):
    """Raise 422 Unprocessable Entity HTTPException."""
    exception = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def internal_server_error_response(message: str = "Internal server error", headers: Optional[Dict[str, str]] = None):
    """Raise 500 Internal Server Error HTTPException."""
    exception = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def too_many_requests_response(message: str = "Too many requests", headers: Optional[Dict[str, str]] = None):
    """Raise 429 Too Many Requests HTTPException."""
    exception = HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def method_not_allowed_response(message: str = "Method not allowed", headers: Optional[Dict[str, str]] = None):
    """Raise 405 Method Not Allowed HTTPException."""
    exception = HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def service_unavailable_response(message: str = "Service unavailable", headers: Optional[Dict[str, str]] = None):
    """Raise 503 Service Unavailable HTTPException."""
    exception = HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def not_acceptable_response(message: str, headers: Optional[Dict[str, str]] = None):
    """Raise 406 Not Acceptable HTTPException."""
    exception = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=message)
    if headers:
        exception.headers = headers
    raise exception


def custom_response(message: str, data: Any = None, status_code: int = status.HTTP_200_OK, headers: Optional[Dict[str, str]] = None):
    """Create a custom response with full control."""
    response_data = {"status": status_code, "detail": message, "data": data}
    if headers:
        return JSONResponse(content=response_data, status_code=status_code, headers=headers)
    return response_data


def custom_exception(message: str, status_code: int = status.HTTP_400_BAD_REQUEST, headers: Optional[Dict[str, str]] = None):
    """Raise a custom HTTPException."""
    exception = HTTPException(status_code=status_code, detail=message)
    if headers:
        exception.headers = headers
    raise exception
