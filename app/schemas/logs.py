from typing import List, Optional, Union, Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from .base_schema import BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters
from .validate_uuid import UUIDStr


class ActivityLogBaseSchema(BaseModel):
    id: Optional[str] = Field(None, description="The UUID of the activity log")
    timestamp: Optional[int] = Field(None, description="The timestamp of the log")
    timestamp_readable: Optional[str] = Field(
        None, description="Human-readable timestamp"
    )
    user_uuid: Optional[UUIDStr] = Field(None, description="UUID of the user performing the action")
    action: Optional[str] = Field(None, description="Description of the performed action")
    entity: Optional[str] = Field(
        None, description="The entity affected by the action (e.g., 'meeting', 'team', 'profile')"
    )
    entity_uuid: Optional[UUIDStr] = Field(None, description="UUID of the affected entity, if applicable")
    ip_address: Optional[str] = Field(None, description="IP address of the user")
    user_agent: Optional[str] = Field(None, description="User agent string of the user")

    @model_validator(mode="before")
    def add_human_readable_timestamp(cls, values):
        ts = values.get("timestamp")
        if ts:
            values["timestamp_readable"] = datetime.utcfromtimestamp(ts).isoformat()
        return values


class ActivityLogSchema(ActivityLogBaseSchema):
    pass


class ActivityLogResponseSchema(BaseResponseSchema):
    data: Optional[ActivityLogSchema] = None


class ActivityLogListResponseSchema(BaseResponseSchema):
    data: Optional[List[ActivityLogSchema]] = None


class ActivityLogTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[ActivityLogSchema]] = None


class ActivityLogFilters(BaseFilters):
    sort: Optional[str] = Field(
        "timestamp:desc",
        description="Sorting criteria for the result set in the format 'field:direction' (e.g., 'timestamp:desc' or 'timestamp:asc')",
        example="timestamp:desc",
    )
    user_uuid: Optional[UUIDStr] = Field(None, description="Filter by user UUID")
    action: Optional[str] = Field(None, description="Filter by action keyword")
    entity: Optional[str] = Field(None, description="Filter by entity type (e.g., 'meeting')")
    entity_uuid: Optional[UUIDStr] = Field(None, description="Filter by entity UUID")
    ip_address: Optional[str] = Field(None, description="Filter by IP address")
    start_date: Optional[datetime] = Field(None, description="Filter logs from this date")
    end_date: Optional[datetime] = Field(None, description="Filter logs up to this date")
    search: Optional[str] = Field(
        None,
        description="Search across action, entity, and user UUID fields",
    )
