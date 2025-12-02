from fastapi import HTTPException, status
from uuid import UUID
from typing import Any


def validate_uuid(value: Any) -> bool:
    try:
        UUID(str(value))
        return True
    except (ValueError, TypeError):
        return False


def validate_uuid_str(value: Any) -> str:
    try:
        uuid_str = str(value).strip()
        UUID(uuid_str)
        return uuid_str
    except (ValueError, TypeError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid UUID: {value}. Expected a valid UUID string.",
        )


class UUIDStr(str):
    """
    Custom Pydantic type for UUID validation in Automeet.
    Ensures UUID strings are valid when used in Pydantic models/schemas.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any):
        from pydantic_core import core_schema
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                str, return_schema=core_schema.str_schema()
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: Any, handler: Any):
        return {
            "type": "string",
            "format": "uuid",
            "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        }

    @classmethod
    def validate(cls, value: Any) -> str:
        if value is None:
            return value
        try:
            uuid_str = str(value).strip()
            UUID(uuid_str)
            return uuid_str
        except (ValueError, TypeError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid UUID format: {value}. Expected a valid UUID string.",
            )
