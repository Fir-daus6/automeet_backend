from typing import Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict
from datetime import datetime
from .validate_uuid import UUIDStr


class BaseSchema(BaseModel):
    """
    BaseSchema provides common fields for entities using an integer primary key (ID).
    Suitable for simple entities like logs, counters, or sequential records.
    """

    id: Optional[int] = Field(
        default=None, description="Unique integer identifier of the entity."
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the entity was created."
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the entity was last updated."
    )
    views: Optional[int] = Field(
        default=0, description="Number of times this entity has been accessed or viewed."
    )

    model_config = ConfigDict(from_attributes=True)


class BaseUUIDSchema(BaseModel):
    """
    BaseUUIDSchema provides common fields for entities using UUID as the primary identifier.
    Suitable for core Automeet entities like Users, Teams, TeamInvites, Meetings, etc.
    """

    uuid: Optional[UUIDStr] = Field(
        default=None, description="Unique UUID identifier of the entity."
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the entity was created."
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the entity was last updated."
    )
    views: Optional[int] = Field(
        default=0, description="Number of times this entity has been accessed or viewed."
    )
    delete_protection: Optional[bool] = Field(
        default=False, description="Indicates if the entity is protected from deletion."
    )

    model_config = ConfigDict(from_attributes=True)


class BaseSlugSchema(BaseUUIDSchema):
    """
    BaseSlugSchema extends BaseUUIDSchema by adding a slug field.
    Useful for entities that require human-readable unique identifiers for URLs.
    """

    slug: Optional[str] = Field(
        default=None,
        description="Human-readable unique identifier for the entity, commonly used in URLs.",
    )

    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchema(BaseModel):
    """
    BaseResponseSchema defines a standard API response structure.
    Can be extended for all response models in Automeet.
    """

    status: int = Field(description="HTTP status code of the response.")
    detail: str = Field(description="A descriptive message regarding the response.")

    model_config = ConfigDict(from_attributes=True)


class BaseTotalCountResponseSchema(BaseModel):
    """
    BaseTotalCountResponseSchema extends BaseResponseSchema by including total_count.
    Suitable for paginated or list responses.
    """

    status: int = Field(description="HTTP status code of the response.")
    detail: str = Field(description="A descriptive message regarding the response.")
    total_count: int = Field(description="Total number of items relevant to the response.")

    model_config = ConfigDict(from_attributes=True)
